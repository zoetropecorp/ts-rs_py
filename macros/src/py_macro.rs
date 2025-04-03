use std::collections::{HashMap, HashSet};

use proc_macro2::{Ident, TokenStream};
use quote::{format_ident, quote};
use syn::{
    parse_quote, spanned::Spanned, ConstParam, GenericParam, Generics, Item, LifetimeParam, Path,
    Result, Type, TypeParam, WhereClause, WherePredicate,
};

use crate::{deps::Dependencies, utils::format_generics};

struct DerivedPy {
    crate_rename: Path,
    py_name: String,
    docs: String,
    inline: TokenStream,
    py_definition: TokenStream,
    inline_flattened: Option<TokenStream>,
    dependencies: Dependencies,
    concrete: HashMap<Ident, Type>,
    bound: Option<Vec<WherePredicate>>,

    export: bool,
    export_to: Option<String>,
}

impl DerivedPy {
    fn into_impl(mut self, rust_ty: Ident, generics: Generics) -> TokenStream {
        let export = self
            .export
            .then(|| self.generate_export_test(&rust_ty, &generics));

        let output_path_fn = if self.export {
            let path = match self.export_to.as_deref() {
                Some(dirname) if dirname.ends_with('/') => {
                    format!("{}{}.py", dirname, self.py_name)
                }
                Some(filename) => filename.to_owned(),
                None => format!("{}.py", self.py_name),
            };

            quote! {
                fn output_path() -> Option<&'static std::path::Path> {
                    use std::sync::OnceLock;
                    static PATH: OnceLock<&'static std::path::Path> = OnceLock::new();
                    Some(*PATH.get_or_init(|| {
                        Box::leak(Box::new(std::path::Path::new(#path)))
                    }))
                }
            }
        } else {
            quote! {
                fn output_path() -> Option<&'static std::path::Path> {
                    None
                }
            }
        };

        let docs = match &*self.docs {
            "" => None,
            docs => Some(quote!(const DOCS: Option<&'static str> = Some(#docs);)),
        };

        let crate_rename = self.crate_rename.clone();

        let ident = self.py_name.clone();
        let impl_start = generate_impl_block_header(
            &crate_rename,
            &rust_ty,
            &generics,
            self.bound.as_deref(),
            &self.dependencies,
        );
        let assoc_type = generate_assoc_type(&rust_ty, &crate_rename, &generics, &self.concrete);
        let name = self.generate_name_fn(&generics);
        let inline = self.generate_inline_fn();
        let decl = self.generate_decl_fn(&rust_ty, &generics);
        let definition = self.generate_definition_fn();
        let dependencies = &self.dependencies;
        let generics_fn = self.generate_generics_fn(&generics);

        quote! {
            #impl_start {
                #assoc_type
                type OptionInnerType = Self;

                fn ident() -> String {
                    #ident.to_owned()
                }

                #docs
                #name
                #decl
                #inline
                #definition
                #generics_fn
                #output_path_fn

                fn visit_dependencies(v: &mut impl #crate_rename::py::PyTypeVisitor)
                where
                    Self: 'static,
                {
                    #dependencies
                }
            }

            #export
        }
    }

    /// Returns an expression which evaluates to the Python name of the type, including generic
    /// parameters.
    fn name_with_generics(&self, generics: &Generics) -> TokenStream {
        let name = &self.py_name;
        let crate_rename = &self.crate_rename;
        let mut generics_py_names = generics
            .type_params()
            .filter(|ty| !self.concrete.contains_key(&ty.ident))
            .map(|ty| &ty.ident)
            .map(|generic| quote!(<#generic as #crate_rename::Py>::name()))
            .peekable();

        if generics_py_names.peek().is_some() {
            quote! {
                format!("{}[{}]", #name, vec![#(#generics_py_names),*].join(", "))
            }
        } else {
            quote!(#name.to_owned())
        }
    }

    /// Generate a dummy unit struct for every generic type parameter of this type.
    fn generate_generic_types(&self, generics: &Generics) -> TokenStream {
        let crate_rename = &self.crate_rename;
        let generics = generics
            .type_params()
            .filter(|ty| !self.concrete.contains_key(&ty.ident))
            .map(|ty| ty.ident.clone());
        let name = quote![<Self as #crate_rename::Py>::name()];
        quote! {
            #(
                #[derive(Copy, Clone, Debug, Hash, Eq, PartialEq, Ord, PartialOrd)]
                struct #generics;
                impl std::fmt::Display for #generics {
                    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                        write!(f, "{:?}", self)
                    }
                }
                impl #crate_rename::Py for #generics {
                    type WithoutGenerics = #generics;
                    type OptionInnerType = Self;
                    fn name() -> String { stringify!(#generics).to_owned() }
                    fn inline() -> String { panic!("{} cannot be inlined", #name) }
                    fn inline_flattened() -> String { stringify!(#generics).to_owned() }
                    fn decl() -> String { panic!("{} cannot be declared", #name) }
                    fn decl_concrete() -> String { panic!("{} cannot be declared", #name) }
                }
            )*
        }
    }

    fn generate_export_test(&self, rust_ty: &Ident, generics: &Generics) -> TokenStream {
        let test_fn = format_ident!(
            "export_py_bindings_{}",
            rust_ty.to_string().to_lowercase().replace("r#", "")
        );
        let crate_rename = &self.crate_rename;
        let generic_params = generics
            .type_params()
            .map(|ty| match self.concrete.get(&ty.ident) {
                None => quote! { #crate_rename::Dummy },
                Some(ty) => quote! { #ty },
            });
        let ty = quote!(<#rust_ty<#(#generic_params),*> as #crate_rename::Py>);

        quote! {
            #[cfg(test)]
            #[test]
            fn #test_fn() {
                match #ty::export_all() {
                    Ok(_) => println!("Successfully exported Python bindings for {}", stringify!(#rust_ty)),
                    Err(e) => panic!("Failed to export Python bindings for {}: {:?}", stringify!(#rust_ty), e),
                }
            }
        }
    }

    fn generate_generics_fn(&self, generics: &Generics) -> TokenStream {
        let crate_rename = &self.crate_rename;
        let generics = generics
            .type_params()
            .filter(|ty| !self.concrete.contains_key(&ty.ident))
            .map(|TypeParam { ident, .. }| {
                quote![
                    v.visit::<#ident>();
                    <#ident as #crate_rename::Py>::visit_generics(v);
                ]
            });
        quote! {
            fn visit_generics(v: &mut impl #crate_rename::py::PyTypeVisitor)
            where
                Self: 'static,
            {
                #(#generics)*
            }
        }
    }

    fn generate_name_fn(&self, generics: &Generics) -> TokenStream {
        let name = self.name_with_generics(generics);
        quote! {
            fn name() -> String {
                #name
            }
        }
    }

    fn generate_inline_fn(&self) -> TokenStream {
        let inline = &self.inline;
        let crate_rename = &self.crate_rename;

        let inline_flattened = self.inline_flattened.as_ref().map_or_else(
            || {
                quote! {
                    fn inline_flattened() -> String {
                        panic!("{} cannot be flattened", <Self as #crate_rename::Py>::name())
                    }
                }
            },
            |inline_flattened| {
                quote! {
                    fn inline_flattened() -> String {
                        #inline_flattened
                    }
                }
            },
        );
        let inline = quote! {
            fn inline() -> String {
                #inline
            }
        };
        quote! {
            #inline
            #inline_flattened
        }
    }

    fn generate_definition_fn(&self) -> TokenStream {
        let definition = &self.py_definition;
        quote! {
            fn definition() -> String {
                #definition
            }
        }
    }

    /// Generates the `decl()` and `decl_concrete()` methods.
    fn generate_decl_fn(&mut self, rust_ty: &Ident, generics: &Generics) -> TokenStream {
        let _name = &self.py_name;
        let crate_rename = &self.crate_rename;
        let generic_types = self.generate_generic_types(generics);
        let _py_generics = format_generics(
            &mut self.dependencies,
            crate_rename,
            generics,
            &self.concrete,
        );

        use GenericParam as G;
        let generic_idents = generics.params.iter().filter_map(|p| match p {
            G::Lifetime(_) => None,
            G::Type(TypeParam { ident, .. }) => match self.concrete.get(ident) {
                None => Some(quote!(#ident)),
                Some(concrete) => Some(quote!(#concrete)),
            },
            G::Const(ConstParam { ident, .. }) => Some(quote!(#ident)),
        });
        quote! {
            fn decl_concrete() -> String {
                <Self as #crate_rename::Py>::inline()
            }
            fn decl() -> String {
                #generic_types
                <#rust_ty<#(#generic_idents,)*> as #crate_rename::Py>::inline()
            }
        }
    }
}

fn generate_assoc_type(
    rust_ty: &Ident,
    crate_rename: &Path,
    generics: &Generics,
    concrete: &HashMap<Ident, Type>,
) -> TokenStream {
    use GenericParam as G;

    let generics_params = generics.params.iter().map(|x| match x {
        G::Type(ty) => match concrete.get(&ty.ident) {
            None => quote! { #crate_rename::Dummy },
            Some(ty) => quote! { #ty },
        },
        G::Const(ConstParam { ident, .. }) => quote! { #ident },
        G::Lifetime(LifetimeParam { lifetime, .. }) => quote! { #lifetime },
    });

    // Collect the generic parameters into a token stream
    let generics_params_ts = quote! { #(#generics_params),* };

    quote! { type WithoutGenerics = #rust_ty<#generics_params_ts>; }
}

fn generate_impl_block_header(
    crate_rename: &Path,
    ty: &Ident,
    generics: &Generics,
    bounds: Option<&[WherePredicate]>,
    dependencies: &Dependencies,
) -> TokenStream {
    use GenericParam as G;

    let params = generics.params.iter().map(|param| match param {
        G::Type(TypeParam {
            ident,
            colon_token,
            bounds,
            ..
        }) => quote!(#ident #colon_token #bounds),
        G::Lifetime(LifetimeParam {
            lifetime,
            colon_token,
            bounds,
            ..
        }) => quote!(#lifetime #colon_token #bounds),
        G::Const(ConstParam {
            const_token,
            ident,
            colon_token,
            ty,
            ..
        }) => quote!(#const_token #ident #colon_token #ty),
    });
    let type_args = generics.params.iter().map(|param| match param {
        G::Type(TypeParam { ident, .. }) | G::Const(ConstParam { ident, .. }) => quote!(#ident),
        G::Lifetime(LifetimeParam { lifetime, .. }) => quote!(#lifetime),
    });

    let where_bound = match bounds {
        Some(bounds) => quote! { where #(#bounds),* },
        None => {
            let bounds = generate_where_clause(crate_rename, generics, dependencies);
            quote! { #bounds }
        }
    };

    quote!(impl <#(#params),*> #crate_rename::Py for #ty <#(#type_args),*> #where_bound)
}

fn generate_where_clause(
    crate_rename: &Path,
    generics: &Generics,
    dependencies: &Dependencies,
) -> WhereClause {
    let used_types = {
        let is_type_param = |id: &Ident| generics.type_params().any(|p| &p.ident == id);

        let mut used_types = HashSet::new();
        for ty in dependencies.used_types() {
            crate::used_type_params(&mut used_types, ty, is_type_param);
        }
        used_types.into_iter()
    };

    let existing = generics.where_clause.iter().flat_map(|w| &w.predicates);
    parse_quote! {
        where #(#existing,)* #(#used_types: #crate_rename::Py),*
    }
}

pub fn py_entry(input: proc_macro::TokenStream) -> Result<TokenStream> {
    let input = syn::parse::<Item>(input)?;
    
    let (mut py, ident, generics) = match &input {
        Item::Struct(s) => (py_struct_def(&s)?, s.ident.clone(), s.generics.clone()),
        Item::Enum(e) => (py_enum_def(&e)?, e.ident.clone(), e.generics.clone()),
        _ => syn_err!(input.span(); "unsupported item"),
    };
    
    // Process py attributes
    match &input {
        Item::Struct(s) => {
            for attr in &s.attrs {
                if attr.path().is_ident("py") {
                    process_py_attribute(attr, &mut py)?;
                }
            }
        },
        Item::Enum(e) => {
            for attr in &e.attrs {
                if attr.path().is_ident("py") {
                    process_py_attribute(attr, &mut py)?;
                }
            }
        },
        _ => {}
    }

    Ok(py.into_impl(ident, generics))
}

fn process_py_attribute(attr: &syn::Attribute, py: &mut DerivedPy) -> Result<()> {
    use syn::{Meta, MetaNameValue};
    
    match &attr.meta {
        Meta::Path(path) if path.is_ident("export") => {
            py.export = true;
        },
        Meta::NameValue(MetaNameValue { path, value, .. }) => {
            if path.is_ident("export_to") {
                if let syn::Expr::Lit(syn::ExprLit { lit: syn::Lit::Str(s), .. }) = value {
                    py.export = true; // Implicitly enable export if export_to is set
                    py.export_to = Some(s.value());
                } else {
                    syn_err!(value.span(); "expected string literal");
                }
            }
        },
        _ => {
            // Handle other attributes or nested attributes
            if let Ok(list) = attr.meta.require_list() {
                for nested in list.parse_args_with(syn::punctuated::Punctuated::<Meta, syn::Token![,]>::parse_terminated)? {
                    match nested {
                        Meta::Path(path) if path.is_ident("export") => {
                            py.export = true;
                        },
                        Meta::NameValue(MetaNameValue { path, value, .. }) => {
                            if path.is_ident("export_to") {
                                if let syn::Expr::Lit(syn::ExprLit { lit: syn::Lit::Str(s), .. }) = value {
                                    py.export = true; // Implicitly enable export if export_to is set
                                    py.export_to = Some(s.value());
                                } else {
                                    syn_err!(value.span(); "expected string literal");
                                }
                            }
                        },
                        _ => {}
                    }
                }
            }
        }
    }
    
    Ok(())
}

// ====================================
// Helper functions for py_struct_def
// ====================================

// Helper to extract the inner type from Option<T>, Vec<T>, etc.
fn get_inner_type(type_path: &syn::TypePath) -> Option<&syn::Type> {
    type_path.path.segments.last()
        .and_then(|segment| match &segment.arguments {
            syn::PathArguments::AngleBracketed(args) => args.args.first(),
            _ => None,
        })
        .and_then(|generic_arg| match generic_arg {
            syn::GenericArgument::Type(ty) => Some(ty),
            _ => None,
        })
}

// Helper to extract key and value types from HashMap<K, V> or BTreeMap<K, V>
fn get_map_key_value_types(type_path: &syn::TypePath) -> Option<(Option<&syn::Type>, Option<&syn::Type>)> {
    type_path.path.segments.last()
        .and_then(|segment| match &segment.arguments {
            syn::PathArguments::AngleBracketed(args) if args.args.len() >= 2 => {
                let key_type = match args.args.first() {
                    Some(syn::GenericArgument::Type(ty)) => Some(ty),
                    _ => None,
                };
                let value_type = match args.args.get(1) {
                    Some(syn::GenericArgument::Type(ty)) => Some(ty),
                    _ => None,
                };
                Some((key_type, value_type))
            },
            _ => None, // Not enough arguments or not angle bracketed
        })
}

// Helper to get the base Python type name (e.g., "MyClass" from "Optional[MyClass]")
fn get_base_python_type_name(rust_type: &syn::Type) -> String {
    match rust_type {
        syn::Type::Path(type_path) => {
            if let Some(segment) = type_path.path.segments.last() {
                let base_name = segment.ident.to_string();
                // Handle Option<T>, Vec<T> etc. by recursing on the inner type if necessary
                 match base_name.as_str() {
                     "Option" | "Vec" => {
                         if let Some(inner) = get_inner_type(type_path) {
                             return get_base_python_type_name(inner); // Recursive call
                         }
                     },
                     "HashMap" | "BTreeMap" => {
                         // For maps, we typically care about the value type for fromDict
                         if let Some((_, Some(value_type))) = get_map_key_value_types(type_path) {
                             return get_base_python_type_name(value_type); // Recursive call on value type
                         }
                     },
                     _ => {} // Fall through for other types
                 }
                 base_name // Return the base name if not Option/Vec/Map or inner type unknown
            } else {
                "Any".to_string() // Empty path segment
            }
        },
        _ => "Any".to_string(), // Not a path type
    }
}

// Helper to check if a Python type name is a primitive
fn is_python_primitive(py_type_name: &str) -> bool {
     matches!(py_type_name, "int" | "float" | "bool" | "str" | "Any" | "None") // Consider None primitive here
}

// Helper function to check if a type is a primitive type (Rust)
fn is_primitive_type(type_name: &str) -> bool {
    matches!(type_name,
        "i8" | "i16" | "i32" | "i64" | "i128" |
        "u8" | "u16" | "u32" | "u64" | "u128" |
        "isize" | "usize" | "f32" | "f64" |
        "bool" | "String" | "str" | "char")
}

// Helper to generate the Python *expression* for serializing a field's value
fn generate_serialize_expr(inner_type: &syn::Type, value_var: &str) -> String {
     match inner_type {
        syn::Type::Path(type_path) => {
            let last_segment = type_path.path.segments.last().unwrap(); // Assume valid path
                         let type_name = last_segment.ident.to_string();

                         match type_name.as_str() {
                "Vec" => {
                     // List serialization: serialize each item if possible
                     format!(r#"[item._serialize() if hasattr(item, '_serialize') else item for item in {value}]"#,
                         value = value_var)
                },
                "HashMap" | "BTreeMap" => {
                    // Dict serialization: serialize values if possible
                    format!(r#"{{k: v._serialize() if hasattr(v, '_serialize') else v for k, v in {value}.items()}}"#,
                        value = value_var)
                },
                _ if is_primitive_type(&type_name) || type_name == "String" => {
                    // Primitive types: assign directly
                    value_var.to_string()
                },
                _ => {
                    // Assumed custom struct/enum or external type
                    format!(r#"(
                        {value}.name if isinstance({value}, Enum) 
                        else {value}._serialize() if hasattr({value}, '_serialize') 
                        else {value}
                    )"#,
                    value = value_var)
                }
            }
        },
        _ => value_var.to_string(), // Fallback for non-path types
    }
}

// Helper to generate Python serialization code for a single field
fn generate_serialize_logic(field_name: &str, rust_type: &syn::Type) -> String {
    let serialize_expr = match rust_type {
        // Option<T> -> Check inner type T
        syn::Type::Path(type_path) if type_path.path.segments.last().map_or(false, |seg| seg.ident == "Option") => {
            if let Some(inner_type) = get_inner_type(type_path) {
                generate_serialize_expr(inner_type, "value")
            } else {
                 "value".to_string()// Option<Any> or unknown
            }
        },
        _ => generate_serialize_expr(rust_type, "value") // Non-option type
    };

    format!(r#"
        key = "{key}" 
        value = self.get(key)
        if value is not None:
            result[key] = {expr}"#, 
        key = field_name, 
        expr = serialize_expr)
}

// Helper to generate the Python *expression* for deserializing a value
fn generate_deserialize_expr(inner_type: &syn::Type, value_var: &str) -> String {
    match inner_type {
        syn::Type::Path(type_path) => {
            let py_type_name = get_base_python_type_name(inner_type); // Get potential class name like "MyStruct"

            match type_path.path.segments.last().unwrap().ident.to_string().as_str() { // Match on outer type like "Vec"
                "Vec" => {
                    if let Some(item_type) = get_inner_type(type_path) { // Get type inside Vec<...>
                        let item_py_class = get_base_python_type_name(item_type);
                         if !is_python_primitive(&item_py_class) {
                             // List of complex types
                             format!(r#"[{cls}.fromDict(item) if isinstance(item, dict) else item for item in {value}]"#,
                                 cls=item_py_class, value=value_var)
                         } else {
                             // List of primitive types
                             value_var.to_string()
                         }
                    } else {
                         // Vec<Any> or unknown
                         value_var.to_string()
                    }
                },
                "HashMap" | "BTreeMap" => {
                    let (_key_type, value_type) = get_map_key_value_types(type_path).unwrap_or((None, None));
                    if let Some(val_type) = value_type {
                         let value_py_class = get_base_python_type_name(val_type);
                         if !is_python_primitive(&value_py_class) {
                             // Dictionary with complex values
                            format!(r#"{{k: {cls}.fromDict(v) if isinstance(v, dict) else v for k, v in {value}.items()}}"#,
                                cls=value_py_class, value=value_var)
                         } else {
                             // Dictionary with primitive values
                             value_var.to_string()
                         }
                    } else {
                        // HashMap<_, Any> or unknown
                        value_var.to_string()
                    }
                },
                _ if is_primitive_type(&py_type_name) || py_type_name == "String" => {
                     value_var.to_string()
                },
                 _ => { // Assumed custom struct/enum
                     format!(r#"(
                        {cls}.fromDict({value}) if isinstance({value}, dict) 
                        else {cls}[{value}] if isinstance({value}, str) and hasattr({cls}, '__members__') # Enum from name
                        else {value} # Fallback
                     )"#,
                         cls=py_type_name, value=value_var)
                 }
            }
        }
         _ => value_var.to_string(), // Fallback for non-path types
    }
}

// Helper to generate Python deserialization code for a single field
fn generate_deserialize_logic(field_name: &str, rust_type: &syn::Type) -> String {
    let base_logic = format!(r#"
        key = "{key}" 
        value = data.get(key)
        if value is not None:"#, 
        key = field_name
    );

    let assignment = match rust_type {
         syn::Type::Path(type_path) if type_path.path.segments.last().map_or(false, |seg| seg.ident == "Option") => {
             if let Some(inner_type) = get_inner_type(type_path) {
                 let inner_expr = generate_deserialize_expr(inner_type, "value");
                 format!(r#"            new_dict[key] = {expr}
        else:
            new_dict[key] = None"#, expr = inner_expr)
             } else {
                 // Option<Any>
                 format!(r#"            new_dict[key] = value
        else:
            new_dict[key] = None"#)
             }
         }
        _ => { // Not an Option
             let expr = generate_deserialize_expr(rust_type, "value");
             format!(r#"            new_dict[key] = {expr}"#, expr = expr)
        }
    };

    format!("{}\n{}", base_logic, assignment)
}

// ====================================
// End Helper functions
// ====================================

fn py_struct_def(s: &syn::ItemStruct) -> Result<DerivedPy> {
    let crate_rename: Path = parse_quote!(::ts_rs);
    let mut dependencies = Dependencies::new(crate_rename.clone());

    // Imports needed for the generated Python code
    let mut imports = Vec::new();
    
    imports.push("from __future__ import annotations".to_string());
    imports.push("".to_string());
    imports.push("import json".to_string());
    imports.push("import inspect".to_string());  // Add inspect import
    imports.push("from enum import Enum, auto".to_string());
    imports.push("from typing import Any, Optional, List, Dict, Union, TypedDict, TYPE_CHECKING".to_string());
    imports.push("from dataclasses import *".to_string());
    imports.push("from uuid import UUID as Uuid".to_string());
    imports.push("".to_string());

    let mut field_annotations_vec = Vec::new();
    let mut serialize_parts = Vec::new();
    let mut from_dict_parts = Vec::new();
    // let mut field_info = Vec::new(); // Removed as info is passed directly now

    match &s.fields {
        syn::Fields::Named(fields) => {
            for f in &fields.named {
                if let Some(field_name) = f.ident.as_ref() {
                    let field_name_str = field_name.to_string();
                    if is_python_keyword(&field_name_str) || is_python_fragment(&field_name_str) {
                        continue;
                    }

                    let rust_type = f.ty.clone();
                    let py_type_str = get_py_type_for_rust_type(&rust_type).unwrap_or_else(|_| "Any".to_string());
                    // field_info.push((field_name_str.clone(), rust_type.clone(), py_type_str.clone()));

                    field_annotations_vec.push(format!("    {}: {}", field_name_str, py_type_str));
                    dependencies.append_from(&rust_type);

                    // --- _serialize logic ---
                    let serialize_logic = generate_serialize_logic(&field_name_str, &rust_type);
                    serialize_parts.push(serialize_logic);

                    // --- fromDict logic ---
                    let deserialize_logic = generate_deserialize_logic(&field_name_str, &rust_type);
                    from_dict_parts.push(deserialize_logic);
                }
            }
        },
        syn::Fields::Unnamed(_) => {
             field_annotations_vec.push("    # TypedDict does not support unnamed fields directly".to_string());
        },
        syn::Fields::Unit => {
             field_annotations_vec.push("    pass".to_string());
        },
    };

    let field_annotations = if field_annotations_vec.is_empty() {
        "    pass".to_string()
    } else {
        field_annotations_vec.join("\n")
    };

    let serialize_impl = if serialize_parts.is_empty() {
        "        return {}".to_string()
    } else {
        format!("        result = {{}}\n{}\n        return result", serialize_parts.join("")) // Join without extra newline
    };

    let from_dict_impl = if from_dict_parts.is_empty() {
         // Use cls directly in cast, no TypeVar T needed
         format!("        return cast({}, {{}}) # Return empty dict for unit structs", s.ident.to_string()) 
    } else {
        // Construct the final dict using cast for type safety
        let construction = format!("        return cast({}, new_dict)", s.ident.to_string());
        format!("        new_dict: Dict[str, Any] = {{}}\n{}\n\n{}", 
            from_dict_parts.join(""), // Join without extra newline
            construction)
    };


    let class_name = s.ident.to_string();
    let import_block = imports.join("\n");

    // Construct the entire class string using raw strings for the main template
    let py_class_code = format!(r#"
{imports}

class {class_name}(TypedDict):
{field_annotations}

    # Note: Methods below adapted for TypedDict behavior.

    def toJSON(self) -> str:
        """Serialize this TypedDict to a JSON string."""
        return json.dumps(self._serialize())

    def _serialize(self) -> dict:
        """Convert this TypedDict to a serializable dictionary."""
{serialize_impl}

    @classmethod
    def fromJSON(cls, json_str: str) -> '{class_name}': # Use string forward reference
        """Deserialize JSON string to a dictionary matching the TypedDict structure."""
        data = json.loads(json_str)
        return cls.fromDict(data)

    @classmethod
    def fromDict(cls, data: dict) -> '{class_name}': # Use string forward reference
        """Create an instance of this TypedDict from a dictionary.
           Recursively converts nested dictionaries if necessary.
        """
{from_dict_impl}
"#,
        imports = import_block,
        class_name = class_name,
        field_annotations = field_annotations,
        serialize_impl = serialize_impl,
        from_dict_impl = from_dict_impl
    );

    // Dependencies are already added during field iteration

    let py_name_owned = class_name.clone(); // Use the Rust ident name for py_name
    let inline_name = quote!(#py_name_owned.to_owned()); // Simple name for inline
    let definition_code = quote!(#py_class_code.to_owned()); // Full code for definition

    Ok(DerivedPy {
        crate_rename: crate_rename.clone(),
        py_name: class_name, // The Python name (usually matches Rust ident)
        docs: String::new(),
        inline: inline_name, // CORRECT: Store simple name
        py_definition: definition_code, // CORRECT: Store full definition
        inline_flattened: None, // TODO: Revisit if TypedDict can be flattened meaningfully
        dependencies,
        concrete: HashMap::new(),
        bound: None,
        export: false,
        export_to: None,
    })
}

// Helper function to convert Rust type to Python type for type annotations
fn get_py_type_for_rust_type(ty: &syn::Type) -> Result<String> {
    match ty {
        syn::Type::Path(type_path) => {
            let last_segment = type_path.path.segments.last()
                .ok_or_else(|| syn::Error::new_spanned(type_path, "Empty type path"))?;
            
            let type_name = last_segment.ident.to_string();
            
            // Match common Rust types to Python types
            let py_type = match type_name.as_str() {
                "i8" | "i16" | "i32" | "i64" | "i128" | 
                "u8" | "u16" | "u32" | "u64" | "u128" | 
                "isize" | "usize" => "int".to_string(),
                "f32" | "f64" => "float".to_string(),
                "bool" => "bool".to_string(),
                "String" | "str" | "char" => "str".to_string(),
                "Option" => match &last_segment.arguments {
                    syn::PathArguments::AngleBracketed(args) => match args.args.first() {
                        Some(syn::GenericArgument::Type(inner_type)) => {
                            let inner_py_type = get_py_type_for_rust_type(inner_type)?;
                            "Optional[".to_string() + &inner_py_type + "]"
                        },
                        _ => "Optional[Any]".to_string()
                    },
                    _ => "Optional[Any]".to_string()
                },
                "Vec" => match &last_segment.arguments {
                    syn::PathArguments::AngleBracketed(args) => match args.args.first() {
                        Some(syn::GenericArgument::Type(inner_type)) => {
                            let inner_py_type = get_py_type_for_rust_type(inner_type)?;
                            "List[".to_string() + &inner_py_type + "]"
                        },
                        _ => "List[Any]".to_string()
                    },
                    _ => "List[Any]".to_string()
                },
                "HashMap" | "BTreeMap" => match &last_segment.arguments {
                    syn::PathArguments::AngleBracketed(args) if args.args.len() >= 2 => {
                        match (args.args.first(), args.args.get(1)) {
                            (Some(syn::GenericArgument::Type(key_type)), 
                             Some(syn::GenericArgument::Type(value_type))) => {
                                let key_py_type = get_py_type_for_rust_type(key_type)?;
                                let value_py_type = get_py_type_for_rust_type(value_type)?;
                                "Dict[".to_string() + &key_py_type + ", " + &value_py_type + "]"
                            },
                            _ => "Dict[Any, Any]".to_string()
                        }
                    },
                    _ => "Dict[Any, Any]".to_string()
                },
                // Map custom types directly
                _ => type_name.to_string()
            };
            
            Ok(py_type)
        },
        _ => Ok("Any".to_string())
    }
}

// =============================================
// Helper functions specifically for py_enum_def
// =============================================

// Helper function to generate the toJSON method for dataclasses
fn generate_dataclass_to_json_method() -> String {
    "\n    def toJSON(self) -> str:\n        \"\"\"Serialize this dataclass instance to a JSON string.\"\"\"\n        return json.dumps(self._serialize())\n\n".to_string()
}

// Helper function to generate the body of the fromDict method for named field variants
fn generate_dataclass_from_dict_body(fields: &syn::FieldsNamed) -> String {
    let mut body = "        kwargs = {}\n".to_string();
    for f in &fields.named {
        if let Some(field_name) = f.ident.as_ref() {
            let field_name_str = field_name.to_string();
            if is_python_keyword(&field_name_str) || is_python_fragment(&field_name_str) { continue; }

            let deserialize_expr = generate_deserialize_expr(&f.ty, "value");
            body.push_str(&format!(r#"
        key = "{key}" 
        value = data.get(key)
        if value is not None:
            kwargs[key] = {expr}
        # else: field will be None or default if Optional/has default"#,
                key = field_name_str,
                expr = deserialize_expr
            ));
        }
    }
    body.push_str("\n        return cls(**kwargs)");
    body
}

// Helper function to generate the body of the fromDict method for unnamed (tuple) field variants
fn generate_dataclass_from_dict_body_unnamed(fields: &syn::FieldsUnnamed) -> String {
    // For tuple variants, fromDict primarily expects the fields to be named field_0, field_1, ... in the dict
    // but could fall back to a list if that's how it's represented.
    let mut body = "        # Try extracting named fields first (field_0, field_1, ...)\n        kwargs = {}\n".to_string();
    let field_count = fields.unnamed.len();
    for (i, f) in fields.unnamed.iter().enumerate() {
        let field_name_str = format!("field_{}", i);
        let deserialize_expr = generate_deserialize_expr(&f.ty, "value");
         body.push_str(&format!(r#"
        key = "{key}" 
        value = data.get(key)
        if value is not None:
            kwargs[key] = {expr}
        # else: rely on dataclass defaults/errors"#,
            key = field_name_str,
            expr = deserialize_expr
        ));
    }
    body.push_str(&format!("\n        # Check if we got all fields, otherwise try list unpacking\n        if len(kwargs) == {}:\n            return cls(**kwargs)", field_count));
    // Fallback for list data (less common for fromDict)
    body.push_str(&format!(r#"
        elif isinstance(data, list) and len(data) == {field_count}: 
            # TODO: Add recursive deserialization for list items if needed
            return cls(*data) # Simple unpacking for now
        else:
            raise TypeError(f"Cannot create tuple variant {{cls.__name__}} from dict/list: {{data}}")"#,
            field_count = field_count // Pass field_count as named argument
        ));
    body
}

// =============================================
// End Enum helper functions
// =============================================

fn py_enum_def(e: &syn::ItemEnum) -> Result<DerivedPy> {
    let crate_rename: Path = parse_quote!(::ts_rs);
    let mut dependencies = Dependencies::new(crate_rename.clone());
    
    // Loop through variants to collect dependencies from fields
    for v in &e.variants {
        match &v.fields {
            syn::Fields::Named(fields) => {
                for f in &fields.named {
                    let ty = &f.ty;
                    if let syn::Type::Path(type_path) = ty {
                        if let Some(last_segment) = type_path.path.segments.last() {
                            let type_name = last_segment.ident.to_string();
                            match type_name.as_str() {
                                "Option" | "Vec" | "Dict" => {
                                    if let syn::PathArguments::AngleBracketed(args) = &last_segment.arguments {
                                        for arg in &args.args {
                                            if let syn::GenericArgument::Type(inner_type) = arg {
                                                dependencies.push(inner_type);
                                            }
                                        }
                                    }
                                },
                                _ if !is_primitive_type(&type_name) => {
                                    dependencies.push(ty);
                                },
                                _ => {}
                            }
                        }
                    } else {
                        dependencies.append_from(ty);
                    }
                }
            }
            syn::Fields::Unnamed(fields) => {
                for f in &fields.unnamed {
                    let ty = &f.ty;
                    if let syn::Type::Path(type_path) = ty {
                        if let Some(last_segment) = type_path.path.segments.last() {
                            let type_name = last_segment.ident.to_string();
                            match type_name.as_str() {
                                "Option" | "Vec" | "Dict" => {
                                    if let syn::PathArguments::AngleBracketed(args) = &last_segment.arguments {
                                        for arg in &args.args {
                                            if let syn::GenericArgument::Type(inner_type) = arg {
                                                dependencies.push(inner_type);
                                            }
                                        }
                                    }
                                },
                                _ if !is_primitive_type(&type_name) => {
                                    dependencies.push(ty);
                                },
                                _ => {}
                            }
                        }
                    } else {
                        dependencies.append_from(ty);
                    }
                }
            }
            syn::Fields::Unit => {}
        }
    }
    
    // Generate variant declarations for the enum
    let enum_name = e.ident.to_string();
    
    // Check if we have any variants with fields
    let has_complex_variants = e.variants.iter().any(|v| !matches!(v.fields, syn::Fields::Unit));
    
    let mut generated_code = String::new();
    
    // Generate proper imports using TYPE_CHECKING to prevent circular imports
    let mut imports = Vec::new();
    
    imports.push("from __future__ import annotations".to_string());
    imports.push("".to_string());
    imports.push("import json".to_string());
    imports.push("import inspect".to_string());  // Add inspect import
    imports.push("from enum import Enum, auto".to_string());
    imports.push("from typing import Any, Optional, List, Dict, Union, TypedDict, TYPE_CHECKING".to_string());
    imports.push("from dataclasses import *".to_string());
    imports.push("from uuid import UUID as Uuid".to_string());
    imports.push("".to_string());
    
    imports.push("# Forward references for type checking only".to_string());
    imports.push("if TYPE_CHECKING:".to_string());
    imports.push("".to_string());
    
    // Join and add to the generated code
    let import_block = imports.iter().map(|s| s.as_str()).collect::<Vec<_>>().join("\n");
    generated_code.push_str(&import_block);
    generated_code.push_str("\n\n");
    
    // Generate dataclasses for variants with fields
    for variant in &e.variants {
        // Get variant name
        let variant_name = variant.ident.to_string();
        
        // Skip if the variant name is a Python keyword or code fragment
        if is_python_keyword(&variant_name) || is_python_fragment(&variant_name) {
            continue;
        }
        
        match &variant.fields {
            syn::Fields::Named(fields) => {
                let variant_class_name = format!("{}_{}", enum_name, variant_name);
                let fields_defs = fields.named.iter()
                    .filter_map(|f| {
                        let field_name = f.ident.as_ref()?.to_string();
                        // Skip Python keywords and fragments
                        if is_python_keyword(&field_name) || is_python_fragment(&field_name) {
                            return None;
                        }
                        
                        let field_type = match get_py_type_for_rust_type(&f.ty) {
                            Ok(py_type) => py_type,
                            Err(_) => "Any".to_string()
                        };
                        
                        Some(format!("    {}: {}", field_name, field_type))
                    })
                    .collect::<Vec<String>>()
                    .join("\n"); // Single newline between fields
                
                // Use @dataclass for variants with fields
                let mut dataclass_code = format!("@dataclass\nclass {}(\n    # Dataclass for the '{}' variant\n):
{}
",
                    variant_class_name, 
                    variant_name,
                    if fields_defs.is_empty() { "    pass" } else { &fields_defs }
                );
                
                // Add toJSON method (uses _serialize helper)
                dataclass_code.push_str(&generate_dataclass_to_json_method());
                
                // Add _serialize helper method - modified to include variant type
                dataclass_code.push_str(r#"
    def _serialize(self) -> dict:
        """Convert this dataclass instance to a serializable dictionary with 'type' field."""
        # Add the variant type based on the class name
        variant_type = self.__class__.__name__.split('_', 1)[1] if '_' in self.__class__.__name__ else self.__class__.__name__
        result = {"type": variant_type}
        for f in fields(self):
            key = f.name
            value = getattr(self, key)
            if value is not None:
                if is_dataclass(value):
                    result[key] = value._serialize()
                elif isinstance(value, list):
                    result[key] = [item._serialize() if hasattr(item, '_serialize') else item for item in value]
                elif isinstance(value, dict):
                    result[key] = {k: v._serialize() if hasattr(v, '_serialize') else v for k, v in value.items()}
                elif isinstance(value, Enum):
                    result[key] = value.name
                else:
                    result[key] = value
        return result

"#);

                // Add fromJSON class method (Simplified signature)
                dataclass_code.push_str(&format!(
                    "    @classmethod\n    def fromJSON(cls, json_str: str) -> '{}':\n        \"\"\"Deserialize JSON string to a new instance\"\"\"\n        data = json.loads(json_str)\n        return cls.fromDict(data)\n\n",
                    variant_class_name
                ));

                // Add fromDict class method (Simplified signature)
                let from_dict_body = generate_dataclass_from_dict_body(fields);
                dataclass_code.push_str(&format!(
                    "    @classmethod\n    def fromDict(cls, data: dict) -> '{}':\n        \"\"\"Create an instance from a dictionary, handling nested types\"\"\"\n{}
",
                    variant_class_name,
                    from_dict_body
                ));
                
                generated_code.push_str(&dataclass_code);
            },
            syn::Fields::Unnamed(fields) if !fields.unnamed.is_empty() => {
                let variant_class_name = format!("{}_{}", enum_name, variant.ident);
                // Generate field defs for tuple variants (field_0: Type, ...)
                let fields_defs = fields.unnamed.iter().enumerate().map(|(i, f)| {
                    let field_name = format!("field_{}", i);
                    let field_type = match get_py_type_for_rust_type(&f.ty) {
                        Ok(py_type) => py_type,
                        Err(_) => "Any".to_string()
                    };
                    
                    // Ensure dependency is added for tuple fields
                    dependencies.push(&f.ty);
                    
                    format!("    {}: {}", field_name, field_type)
                }).collect::<Vec<String>>().join("\n");
                
                // Use @dataclass for tuple variants
                 let mut dataclass_code = format!("@dataclass\nclass {}(\n    # Dataclass for the '{}' tuple variant\n):
{}
",
                    variant_class_name, 
                    variant.ident,
                    if fields_defs.is_empty() { "    pass" } else { &fields_defs }
                );
                
                // Add toJSON method (uses _serialize helper)
                dataclass_code.push_str(&generate_dataclass_to_json_method());
                
                // Add _serialize helper method - modified to include variant type
                dataclass_code.push_str(r#"
    def _serialize(self) -> dict:
        """Convert this dataclass instance to a serializable dictionary with 'type' field."""
        # Add the variant type based on the class name
        variant_type = self.__class__.__name__.split('_', 1)[1] if '_' in self.__class__.__name__ else self.__class__.__name__
        result = {"type": variant_type}
        for f in fields(self):
            key = f.name
            value = getattr(self, key)
            if value is not None:
                if is_dataclass(value):
                    result[key] = value._serialize()
                elif isinstance(value, list):
                    result[key] = [item._serialize() if hasattr(item, '_serialize') else item for item in value]
                elif isinstance(value, dict):
                    result[key] = {k: v._serialize() if hasattr(v, '_serialize') else v for k, v in value.items()}
                elif isinstance(value, Enum):
                    result[key] = value.name
                else:
                    result[key] = value
        return result

"#);

                // Add fromJSON class method (Simplified signature, using raw string)
                 dataclass_code.push_str(&format!(r#"
    @classmethod
    def fromJSON(cls, json_str: str) -> '{variant_class_name}':
        """Deserialize JSON string to a new instance"""
        data = json.loads(json_str)
        # Expects a list for tuple variants in JSON
        if isinstance(data, list):
             return cls(*data) # Unpack list directly
        elif isinstance(data, dict): # Allow dict for named tuple fields if needed
              return cls.fromDict(data)
        else:
              raise TypeError(f"Expected list or dict for tuple variant, got {{type(data).__name__}}")

"#, // Use double braces {{}} for Python f-string within raw string
                    variant_class_name = variant_class_name
                ));
                
                // Add fromDict class method (Simplified signature)
                let from_dict_body = generate_dataclass_from_dict_body_unnamed(fields);
                dataclass_code.push_str(&format!( // This format! already uses r#"..."# 
                    "    @classmethod\n    def fromDict(cls, data: dict) -> '{}':\n        \"\"\"Create an instance from a dictionary, handling named fields or list fallback\"\"\"\n{}
",
                    variant_class_name,
                    from_dict_body
                ));
                
                generated_code.push_str(&dataclass_code);
            },
            _ => {} // Skip unit variants
        }
    }
    
    // Don't need to modify the serialization logic in a replace operation anymore
    // since we're implementing it directly above in the class definitions
    
    // Generate the enum class
    if has_complex_variants {
        // For complex enums, we'll use a regular class with direct assignments instead of Enum
        let variants_decl = e.variants.iter()
            .filter(|v| {
                // Filter out variants with invalid Python names
                let variant_name = v.ident.to_string();
                !is_python_keyword(&variant_name) && !is_python_fragment(&variant_name) && !variant_name.contains("TypedDict")
            })
            .map(|v| {
                let variant_name = v.ident.to_string();
                
                match &v.fields {
                    syn::Fields::Unit => {
                        format!("    {} = \"{}\"  # Simple variant (string constant)", variant_name, variant_name)
                    },
                    syn::Fields::Named(_) | syn::Fields::Unnamed(_) => {
                        let variant_class_name = format!("{}_{}", enum_name, variant_name);
                        format!("    {} = {}  # Complex variant (class reference)", variant_name, variant_class_name)
                    }
                }
            }).collect::<Vec<_>>().join("\n");
        
        // Create a regular class instead of an Enum
        generated_code.push_str(&format!("class {}:\n    \"\"\"Namespace for {} variants. Access variant classes directly as attributes.\"\"\"\n{}\n", 
            enum_name, enum_name, variants_decl));
        
        // Add fromJSON static method for deserialization
        generated_code.push_str("\n    @classmethod\n");
        generated_code.push_str("    def fromJSON(cls, json_str):\n");
        generated_code.push_str("        \"\"\"Deserialize JSON string to the appropriate variant type\"\"\"\n");
        generated_code.push_str("        data = json.loads(json_str)\n");
        generated_code.push_str("        if isinstance(data, str):\n");
        generated_code.push_str("            # Simple string variant\n");
        generated_code.push_str("            if hasattr(cls, data):\n");
        generated_code.push_str("                return getattr(cls, data)\n");
        generated_code.push_str("            return data  # Unknown string variant\n");
        generated_code.push_str("        elif isinstance(data, dict):\n");
        generated_code.push_str("            # Complex variant with fields\n");
        generated_code.push_str("            if \"type\" in data:\n");
        generated_code.push_str("                variant_name = data[\"type\"]\n");
        generated_code.push_str("                if hasattr(cls, variant_name):\n");
        generated_code.push_str("                    variant_class = getattr(cls, variant_name)\n");
        generated_code.push_str("                    # Check if it's a class with fromDict method\n");
        generated_code.push_str("                    if inspect.isclass(variant_class) and hasattr(variant_class, 'fromDict'):\n");
        generated_code.push_str("                        # Strip the type field before passing to fromDict\n");
        generated_code.push_str("                        variant_data = {k: v for k, v in data.items() if k != \"type\"}\n");
        generated_code.push_str("                        return variant_class.fromDict(variant_data)\n");
        generated_code.push_str("                    return variant_class  # Return the string constant\n");
        generated_code.push_str("        # Default fallback - return None for unknown type\n");
        generated_code.push_str("        return None\n");
        
        // Add helper factory method (renamed from create_*)
        generated_code.push_str("\n    @classmethod\n    def create(cls, variant_name: str, **kwargs):\n");
        generated_code.push_str("        \"\"\"Factory method to create a variant instance with fields\"\"\"\n");
        generated_code.push_str("        if hasattr(cls, variant_name):\n");
        generated_code.push_str("            variant_class = getattr(cls, variant_name)\n");
        generated_code.push_str("            if inspect.isclass(variant_class):  # Only call complex variants (classes)\n");
        generated_code.push_str("                return variant_class(**kwargs)\n");
        generated_code.push_str("            return variant_class  # Return the string constant\n");
        generated_code.push_str("        raise ValueError(f\"Unknown variant {variant_name}\")\n");
        
    } else {
        // Simple enum with just unit variants - use string constants in a namespace
        let variants_code = e.variants.iter()
            .filter(|v| {
                let variant_name = v.ident.to_string();
                // Make sure the variant name is a valid Python identifier
                !is_python_keyword(&variant_name) && !is_python_fragment(&variant_name) && !variant_name.contains("TypedDict")
            })
            .map(|v| {
                format!("    {} = \"{}\"", v.ident, v.ident)
            }).collect::<Vec<_>>().join("\n");
        
        generated_code.push_str(&format!("class {}:\n    \"\"\"Namespace for {} variants (simple string constants)\"\"\"\n{}\n", 
            enum_name, enum_name, variants_code));
        
        // Add fromJSON method for simple namespace
        generated_code.push_str("\n    @classmethod\n");
        generated_code.push_str("    def fromJSON(cls, json_str):\n");
        generated_code.push_str("        \"\"\"Deserialize JSON string to a variant constant\"\"\"\n");
        generated_code.push_str("        data = json.loads(json_str)\n");
        generated_code.push_str("        if isinstance(data, str):\n");
        generated_code.push_str("            # Return the string constant if it exists\n");
        generated_code.push_str("            if hasattr(cls, data):\n");
        generated_code.push_str("                return getattr(cls, data)\n");
        generated_code.push_str("            return data  # Unknown string value\n");
        generated_code.push_str("        elif isinstance(data, dict) and \"type\" in data:\n");
        generated_code.push_str("            variant_name = data[\"type\"]\n");
        generated_code.push_str("            if hasattr(cls, variant_name):\n");
        generated_code.push_str("                return getattr(cls, variant_name)\n");
        generated_code.push_str("        # Default fallback - return None for unknown type\n");
        generated_code.push_str("        return None\n");
    }
    
    // Also modify the dataclass serialization logic to include the variant type
    // Find and replace in the _serialize methods
    generated_code = generated_code.replace(
        "    def _serialize(self) -> dict:",
        "    def _serialize(self) -> dict:\n        \"\"\"Convert this dataclass instance to a serializable dictionary with 'type' field.\"\"\"\n        # Add the variant type based on the class name\n        variant_type = self.__class__.__name__.split('_', 1)[1] if '_' in self.__class__.__name__ else self.__class__.__name__\n        result = {\"type\": variant_type}"
    );
    
    let py_name_owned = enum_name.clone();
    let inline_name = quote!(#py_name_owned.to_owned());
    let definition_code = quote!(#generated_code.to_owned());
    
    Ok(DerivedPy {
        crate_rename: crate_rename.clone(),
        py_name: enum_name,
        docs: String::new(),
        inline: inline_name,
        py_definition: definition_code,
        inline_flattened: None,
        dependencies,
        concrete: HashMap::new(),
        bound: None,
        export: false,
        export_to: None,
    })
}

// Helper function to detect Python code fragments
fn is_python_fragment(s: &str) -> bool {
    // Check for common Python syntax patterns that are not valid field names
    let code_fragments = [
        " if ", "if ", " in ", "in ", " for ", "for ", " return ", "return ",
        " elif ", "elif ", " else", "else ", " import ", "import ", " from ", "from ",
        "(", ")", "[", "]", "{", "}", ":", ";", "->", "&", "==", "!=", ">=", "<=",
        " def ", "def ", " class ", "class ", " try ", "try ", " except ", "except ",
        " finally ", "finally ", " with ", "with ", " as ", "as ", " while ", "while ",
        " assert ", "assert ", " pass ", "pass ", " lambda ", "lambda ", " or ", "or ",
        " and ", "and ", " not ", "not ", " is ", "is ", " global ", "global ", " del ", "del ",
        " yield ", "yield "
    ];
    
    for fragment in code_fragments {
        if s.contains(fragment) {
            return true;
        }
    }
    
    false
}

// Check if a string is a Python keyword
fn is_python_keyword(s: &str) -> bool {
    let keywords = [
        "False", "None", "True", "and", "as", "assert", "async", "await", 
        "break", "class", "continue", "def", "del", "elif", "else", "except", 
        "finally", "for", "from", "global", "if", "import", "in", "is", 
        "lambda", "nonlocal", "not", "or", "pass", "raise", "return", 
        "try", "while", "with", "yield"
    ];
    
    keywords.contains(&s)
}