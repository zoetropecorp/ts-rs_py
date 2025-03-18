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

    quote! { type WithoutGenerics = #rust_ty<#(#generics_params),*>; }
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

// Placeholder functions - we'll implement these properly later
fn py_struct_def(s: &syn::ItemStruct) -> Result<DerivedPy> {
    let crate_rename: Path = parse_quote!(::ts_rs);
    let mut dependencies = Dependencies::new(crate_rename.clone());
    
    // Generate field declarations and type annotations for the struct
    let (field_annotations, constructor_params, field_assignments) = match &s.fields {
        syn::Fields::Named(fields) => {
            let mut annotations = Vec::new();
            let mut params = Vec::new();
            let mut assignments = Vec::new();
            
            for f in &fields.named {
                if let Some(field_name) = &f.ident {
                    // Get field type for type annotation
                    let field_type = match get_py_type_for_rust_type(&f.ty) {
                        Ok(py_type) => py_type,
                        Err(_) => "Any".to_string() // Default to Any for unknown types
                    };
                    
                    // Add this field's type to the dependencies
                    // For container types like Option, Vec, etc. we need to extract the inner type
                    if let syn::Type::Path(type_path) = &f.ty {
                        if let Some(last_segment) = type_path.path.segments.last() {
                            let type_name = last_segment.ident.to_string();
                            
                            match type_name.as_str() {
                                "Option" | "Vec" => {
                                    // For container types, we need to extract the inner type and add it
                                    if let syn::PathArguments::AngleBracketed(args) = &last_segment.arguments {
                                        if let Some(syn::GenericArgument::Type(inner_type)) = args.args.first() {
                                            // Add the inner type to dependencies
                                            dependencies.push(inner_type);
                                        }
                                    }
                                },
                                _ if !is_primitive_type(&type_name) => {
                                    // For non-primitive custom types, add them as dependencies
                                    dependencies.push(&f.ty);
                                },
                                _ => {} // Skip primitive types
                            }
                        }
                    } else {
                        // For any non-path types, add them to dependencies
                        dependencies.append_from(&f.ty);
                    }
                    
                    let field_name_str = field_name.to_string();
                    
                    // Add field type annotation
                    annotations.push(format!("    {}: {}", field_name_str, field_type));
                    
                    // Add constructor parameter with type annotation
                    params.push(format!("{}: {}", field_name_str, field_type));
                    
                    // Add field assignment in __init__ method
                    assignments.push(format!("        self.{} = {}", field_name_str, field_name_str));
                }
            }
            
            (
                annotations.join("\n"),
                params.join(", "),
                if assignments.is_empty() {
                    "        pass".to_string()
                } else {
                    assignments.join("\n")
                }
            )
        },
        syn::Fields::Unnamed(fields) => {
            // For tuple structs, we need to add fields to dependencies too
            for field in &fields.unnamed {
                dependencies.push(&field.ty);
            }
            
            (
                "    # Tuple struct fields (unnamed)".to_string(),
                "*args".to_string(),
                "        # Store args as is\n        self.args = args".to_string()
            )
        },
        syn::Fields::Unit => (
            "".to_string(),
            "".to_string(),
            "        pass  # Unit struct has no fields".to_string()
        ),
    };
    
    // Construct the complete Python class with relative imports
    let class_name = s.ident.to_string();
    
    // Generate proper imports using TYPE_CHECKING to prevent circular imports
    let mut imports = Vec::new();
    
    // Start with __future__ imports (these MUST be first in Python file)
    imports.push("from __future__ import annotations".to_string());
    imports.push("".to_string());
    
    // Standard library imports
    imports.push("import json".to_string());
    imports.push("import sys".to_string());
    imports.push("from pathlib import Path".to_string());
    imports.push("from enum import Enum".to_string());
    imports.push("from typing import Any, Optional, List, Dict, Union, TYPE_CHECKING".to_string());
    imports.push("".to_string());
    
    // Path handling for better imports
    imports.push("# Add current directory to Python path to facilitate imports".to_string());
    imports.push("_current_file = Path(__file__).resolve()".to_string());
    imports.push("_current_dir = _current_file.parent".to_string());
    imports.push("if str(_current_dir) not in sys.path:".to_string());
    imports.push("    sys.path.append(str(_current_dir))".to_string());
    imports.push("".to_string());
    
    // Add TYPE_CHECKING block for forward references
    imports.push("# Forward references for type checking only".to_string());
    imports.push("if TYPE_CHECKING:".to_string());
    imports.push("    pass  # Type checking imports will use annotations".to_string());
    
    // Construct header
    let import_block = imports.join("\n");
    let mut py_class = format!("{}\n\nclass {}:\n{}\n", 
        import_block,
        class_name,
        field_annotations
    );
    
    // Add constructor method
    py_class.push_str(&format!("\n    def __init__(self, {}) -> None:\n{}\n", 
        constructor_params,
        field_assignments
    ));
    
    // Add toJSON method for JSON serialization
    py_class.push_str("\n    def toJSON(self) -> str:\n");
    py_class.push_str("        def _serialize(obj):\n");
    py_class.push_str("            if hasattr(obj, '__dict__'):\n");
    py_class.push_str("                result = {}\n");
    py_class.push_str("                for key, value in obj.__dict__.items():\n");
    py_class.push_str("                    result[key] = _serialize(value)\n");
    py_class.push_str("                return result\n");
    py_class.push_str("            elif isinstance(obj, list):\n");
    py_class.push_str("                return [_serialize(item) for item in obj]\n");
    py_class.push_str("            elif isinstance(obj, dict):\n");
    py_class.push_str("                return {k: _serialize(v) for k, v in obj.items()}\n");
    py_class.push_str("            elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')):\n");
    py_class.push_str("                return json.loads(obj.toJSON())\n");
    py_class.push_str("            elif hasattr(obj, 'value') and isinstance(obj, Enum):\n");
    py_class.push_str("                return obj.name\n");
    py_class.push_str("            elif isinstance(obj, Enum):\n");
    py_class.push_str("                return obj.name\n");
    py_class.push_str("            return obj\n");
    py_class.push_str("        return json.dumps(_serialize(self), indent=2)\n\n");
    
    // Add fromJSON class method for deserialization
    py_class.push_str("    @classmethod\n");
    py_class.push_str("    def fromJSON(cls, json_str):\n");
    py_class.push_str("        \"\"\"Deserialize JSON string to a new instance\"\"\"\n");
    py_class.push_str("        data = json.loads(json_str)\n");
    py_class.push_str("        return cls.fromDict(data)\n\n");
    
    py_class.push_str("    @classmethod\n");
    py_class.push_str("    def fromDict(cls, data):\n");
    py_class.push_str("        \"\"\"Create an instance from a dictionary\"\"\"\n");
    
    // Extract field names for constructor parameters
    let field_names: Vec<_> = match &s.fields {
        syn::Fields::Named(fields) => {
            fields.named.iter()
                .filter_map(|f| f.ident.as_ref().map(|name| name.to_string()))
                .collect()
        },
        _ => Vec::new()
    };
    
    // Generate field processing code
    for field in &field_names {
        py_class.push_str(&format!("        if '{}' in data:\n", field));
        py_class.push_str(&format!("            {} = data['{}']\n", field, field));
        py_class.push_str(&format!("            # Handle nested objects based on type\n"));
        py_class.push_str(&format!("            if isinstance({}, dict) and hasattr(cls, '_{}_type'):\n", field, field));
        py_class.push_str(&format!("                {} = getattr(cls, '_{}_type').fromDict({})\n", field, field, field));
        py_class.push_str(&format!("            elif isinstance({}, list) and hasattr(cls, '_item_type'):\n", field));
        py_class.push_str("                item_type = getattr(cls, '_item_type')\n");
        py_class.push_str(&format!("                if hasattr(item_type, 'fromDict'):\n"));
        py_class.push_str(&format!("                    {} = [item_type.fromDict(item) if isinstance(item, dict) else item for item in {}]\n", field, field));
        py_class.push_str(&format!("        else:\n"));
        py_class.push_str(&format!("            {} = None\n", field));
    }
    
    // Create the instance with the processed fields
    let constructor_args = field_names.join(", ");
    py_class.push_str(&format!("        return cls({})\n", constructor_args));
    
    Ok(DerivedPy {
        crate_rename: crate_rename.clone(),
        py_name: s.ident.to_string(),
        docs: String::new(),
        inline: quote!(#py_class.to_owned()),
        inline_flattened: None,
        dependencies,
        concrete: HashMap::new(),
        bound: None,
        export: false,
        export_to: None,
    })
}

// Helper function to check if a type is a primitive type
fn is_primitive_type(type_name: &str) -> bool {
    matches!(type_name, 
        "i8" | "i16" | "i32" | "i64" | "i128" | 
        "u8" | "u16" | "u32" | "u64" | "u128" | 
        "isize" | "usize" | "f32" | "f64" | 
        "bool" | "String" | "str" | "char")
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

fn py_enum_def(e: &syn::ItemEnum) -> Result<DerivedPy> {
    let crate_rename: Path = parse_quote!(::ts_rs);
    let mut dependencies = Dependencies::new(crate_rename.clone());
    
    // Generate variant declarations for the enum
    let enum_name = e.ident.to_string();
    
    // Check if we have any variants with fields
    let has_complex_variants = e.variants.iter().any(|v| !matches!(v.fields, syn::Fields::Unit));
    
    let mut generated_code = String::new();
    
    // Generate proper imports using TYPE_CHECKING to prevent circular imports
    let mut imports = Vec::new();
    
    // Start with __future__ imports (these MUST be first in Python file)
    imports.push("from __future__ import annotations".to_string());
    imports.push("".to_string());
    
    // Standard library imports
    imports.push("import json".to_string());
    imports.push("import sys".to_string());
    imports.push("from pathlib import Path".to_string());
    imports.push("from enum import Enum, auto".to_string());
    imports.push("from typing import Any, Optional, List, Dict, Union, TYPE_CHECKING".to_string());
    imports.push("from dataclasses import dataclass".to_string());
    imports.push("".to_string());
    
    // Path handling for better imports
    imports.push("# Add current directory to Python path to facilitate imports".to_string());
    imports.push("_current_file = Path(__file__).resolve()".to_string());
    imports.push("_current_dir = _current_file.parent".to_string());
    imports.push("if str(_current_dir) not in sys.path:".to_string());
    imports.push("    sys.path.append(str(_current_dir))".to_string());
    imports.push("".to_string());
    
    // Add TYPE_CHECKING block for forward references
    imports.push("# Forward references for type checking only".to_string());
    imports.push("if TYPE_CHECKING:".to_string());
    imports.push("    pass  # Type checking imports will use annotations".to_string());
    imports.push("".to_string());
    
    // Join and add to the generated code
    let import_block = imports.join("\n");
    generated_code.push_str(&import_block);
    generated_code.push_str("\n\n");
    
    // Generate dataclasses for variants with fields
    for variant in &e.variants {
        match &variant.fields {
            syn::Fields::Named(fields) => {
                // Generate a dataclass for this variant
                let variant_class_name = format!("{}_{}", enum_name, variant.ident);
                
                // Build field definitions
                let fields_defs = fields.named.iter().map(|f| {
                    let field_name = f.ident.as_ref().unwrap().to_string();
                    let field_type = match get_py_type_for_rust_type(&f.ty) {
                        Ok(py_type) => py_type,
                        Err(_) => "Any".to_string()
                    };
                    
                    // Add field types to dependencies
                    if let syn::Type::Path(type_path) = &f.ty {
                        if let Some(last_segment) = type_path.path.segments.last() {
                            let type_name = last_segment.ident.to_string();
                            
                            match type_name.as_str() {
                                "Option" | "Vec" => {
                                    // For container types, extract the inner type
                                    if let syn::PathArguments::AngleBracketed(args) = &last_segment.arguments {
                                        if let Some(syn::GenericArgument::Type(inner_type)) = args.args.first() {
                                            dependencies.push(inner_type);
                                        }
                                    }
                                },
                                _ if !is_primitive_type(&type_name) => {
                                    // For non-primitive types, add them directly
                                    dependencies.push(&f.ty);
                                },
                                _ => {} // Skip primitive types
                            }
                        }
                    } else {
                        dependencies.append_from(&f.ty);
                    }
                    
                    format!("    {}: {}", field_name, field_type)
                }).collect::<Vec<_>>().join("\n");
                
                // Add dataclass with toJSON method
                let mut dataclass_code = format!("@dataclass\nclass {}:\n{}\n", 
                    variant_class_name, 
                    if fields_defs.is_empty() { "    pass" } else { &fields_defs }
                );
                
                // Add toJSON method
                dataclass_code.push_str("    def toJSON(self) -> str:\n");
                dataclass_code.push_str("        def _serialize(obj):\n");
                dataclass_code.push_str("            if hasattr(obj, '__dict__'):\n");
                dataclass_code.push_str("                result = {}\n");
                dataclass_code.push_str("                for key, value in obj.__dict__.items():\n");
                dataclass_code.push_str("                    result[key] = _serialize(value)\n");
                dataclass_code.push_str("                return result\n");
                dataclass_code.push_str("            elif isinstance(obj, list):\n");
                dataclass_code.push_str("                return [_serialize(item) for item in obj]\n");
                dataclass_code.push_str("            elif isinstance(obj, dict):\n");
                dataclass_code.push_str("                return {k: _serialize(v) for k, v in obj.items()}\n");
                dataclass_code.push_str("            elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')):\n");
                dataclass_code.push_str("                return json.loads(obj.toJSON())\n");
                dataclass_code.push_str("            elif hasattr(obj, 'value') and isinstance(obj, Enum):\n");
                dataclass_code.push_str("                return obj.name\n");
                dataclass_code.push_str("            elif isinstance(obj, Enum):\n");
                dataclass_code.push_str("                return obj.name\n");
                dataclass_code.push_str("            return obj\n");
                dataclass_code.push_str("        return json.dumps(_serialize(self), indent=2)\n\n");
                
                // Add fromJSON class method for deserialization
                dataclass_code.push_str("    @classmethod\n");
                dataclass_code.push_str("    def fromJSON(cls, json_str):\n");
                dataclass_code.push_str("        \"\"\"Deserialize JSON string to a new instance\"\"\"\n");
                dataclass_code.push_str("        data = json.loads(json_str)\n");
                dataclass_code.push_str("        return cls.fromDict(data)\n\n");
                
                dataclass_code.push_str("    @classmethod\n");
                dataclass_code.push_str("    def fromDict(cls, data):\n");
                dataclass_code.push_str("        \"\"\"Create an instance from a dictionary\"\"\"\n");
                
                // Extract field names from named fields
                let field_names: Vec<_> = fields.named.iter()
                    .filter_map(|f| f.ident.as_ref().map(|name| name.to_string()))
                    .collect();
                
                // Generate field processing code
                for field in &field_names {
                    dataclass_code.push_str(&format!("        if '{}' in data:\n", field));
                    dataclass_code.push_str(&format!("            {} = data['{}']\n", field, field));
                    dataclass_code.push_str(&format!("            # Handle nested objects based on type\n"));
                    dataclass_code.push_str(&format!("            if isinstance({}, dict) and hasattr(cls, '_{}_type'):\n", field, field));
                    dataclass_code.push_str(&format!("                {} = getattr(cls, '_{}_type').fromDict({})\n", field, field, field));
                    dataclass_code.push_str(&format!("            elif isinstance({}, list) and hasattr(cls, '_item_type'):\n", field));
                    dataclass_code.push_str("                item_type = getattr(cls, '_item_type')\n");
                    dataclass_code.push_str(&format!("                if hasattr(item_type, 'fromDict'):\n"));
                    dataclass_code.push_str(&format!("                    {} = [item_type.fromDict(item) if isinstance(item, dict) else item for item in {}]\n", field, field));
                    dataclass_code.push_str(&format!("        else:\n"));
                    dataclass_code.push_str(&format!("            {} = None\n", field));
                }
                
                // Create the instance with the processed fields
                let constructor_args = field_names.join(", ");
                dataclass_code.push_str(&format!("        return cls({})\n\n", constructor_args));
                
                generated_code.push_str(&dataclass_code);
            },
            syn::Fields::Unnamed(fields) if !fields.unnamed.is_empty() => {
                // Generate a dataclass for this tuple variant
                let variant_class_name = format!("{}_{}", enum_name, variant.ident);
                
                // Build field definitions
                let fields_defs = fields.unnamed.iter().enumerate().map(|(i, f)| {
                    let field_name = format!("field_{}", i);
                    let field_type = match get_py_type_for_rust_type(&f.ty) {
                        Ok(py_type) => py_type,
                        Err(_) => "Any".to_string()
                    };
                    
                    // Add field types to dependencies
                    dependencies.push(&f.ty);
                    
                    format!("    {}: {}", field_name, field_type)
                }).collect::<Vec<_>>().join("\n");
                
                // Add dataclass with toJSON method
                let mut dataclass_code = format!("@dataclass\nclass {}:\n{}\n", 
                    variant_class_name, 
                    if fields_defs.is_empty() { "    pass" } else { &fields_defs }
                );
                
                // Add toJSON method
                dataclass_code.push_str("    def toJSON(self) -> str:\n");
                dataclass_code.push_str("        def _serialize(obj):\n");
                dataclass_code.push_str("            if hasattr(obj, '__dict__'):\n");
                dataclass_code.push_str("                result = {}\n");
                dataclass_code.push_str("                for key, value in obj.__dict__.items():\n");
                dataclass_code.push_str("                    result[key] = _serialize(value)\n");
                dataclass_code.push_str("                return result\n");
                dataclass_code.push_str("            elif isinstance(obj, list):\n");
                dataclass_code.push_str("                return [_serialize(item) for item in obj]\n");
                dataclass_code.push_str("            elif isinstance(obj, dict):\n");
                dataclass_code.push_str("                return {k: _serialize(v) for k, v in obj.items()}\n");
                dataclass_code.push_str("            elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')):\n");
                dataclass_code.push_str("                return json.loads(obj.toJSON())\n");
                dataclass_code.push_str("            elif hasattr(obj, 'value') and isinstance(obj, Enum):\n");
                dataclass_code.push_str("                return obj.name\n");
                dataclass_code.push_str("            elif isinstance(obj, Enum):\n");
                dataclass_code.push_str("                return obj.name\n");
                dataclass_code.push_str("            return obj\n");
                dataclass_code.push_str("        return json.dumps(_serialize(self), indent=2)\n\n");
                
                // Add fromJSON class method for deserialization
                dataclass_code.push_str("    @classmethod\n");
                dataclass_code.push_str("    def fromJSON(cls, json_str):\n");
                dataclass_code.push_str("        \"\"\"Deserialize JSON string to a new instance\"\"\"\n");
                dataclass_code.push_str("        data = json.loads(json_str)\n");
                dataclass_code.push_str("        return cls.fromDict(data)\n\n");
                
                dataclass_code.push_str("    @classmethod\n");
                dataclass_code.push_str("    def fromDict(cls, data):\n");
                dataclass_code.push_str("        \"\"\"Create an instance from a dictionary\"\"\"\n");
                
                // For tuple variants, count the number of fields
                let field_count = fields.unnamed.len();
                
                // Generate field processing code
                dataclass_code.push_str("        # For tuple variant, create from positional data\n");
                dataclass_code.push_str("        if isinstance(data, list):\n");
                dataclass_code.push_str(&format!("            # Expect a list of {} items\n", field_count));
                dataclass_code.push_str(&format!("            return cls(*data[:{}])\n", field_count));
                dataclass_code.push_str("        else:\n");
                dataclass_code.push_str("            # Extract fields from dictionary\n");
                
                // For each field by position
                for i in 0..field_count {
                    let field_name = format!("field_{}", i);
                    dataclass_code.push_str(&format!("            {} = data.get('{}', None)\n", field_name, field_name));
                }
                
                // Create field list for constructor
                let field_args = (0..field_count)
                    .map(|i| format!("field_{}", i))
                    .collect::<Vec<_>>()
                    .join(", ");
                
                dataclass_code.push_str(&format!("            return cls({})\n\n", field_args));
                
                generated_code.push_str(&dataclass_code);
            },
            _ => {}  // Skip unit variants
        }
    }
    
    // Generate the enum class
    if has_complex_variants {
        // For complex enums, we'll use Union types to represent variants with fields
        let variants_decl = e.variants.iter().map(|v| {
            let variant_name = v.ident.to_string();
            
            match &v.fields {
                syn::Fields::Unit => {
                    format!("    {} = auto()", variant_name)
                },
                syn::Fields::Named(_) | syn::Fields::Unnamed(_) => {
                    let variant_class_name = format!("{}_{}", enum_name, variant_name);
                    format!("    {} = {}  # Complex variant with fields", variant_name, variant_class_name)
                }
            }
        }).collect::<Vec<_>>().join("\n");
        
        generated_code.push_str(&format!("class {}(Enum):\n{}\n", enum_name, variants_decl));
        
        // Add helper methods for complex enum
        generated_code.push_str(&format!("\n    @classmethod\n    def create_{}(cls, variant_name: str, **kwargs):\n", 
            variant_name_to_snake_case(&enum_name)
        ));
        generated_code.push_str("        \"\"\"Helper to create a variant instance with fields\"\"\"\n");
        generated_code.push_str("        for variant in cls:\n");
        generated_code.push_str("            if variant.name.lower() == variant_name.lower():\n");
        
        // Add code to create variant instances
        for variant in &e.variants {
            if !matches!(variant.fields, syn::Fields::Unit) {
                let variant_name = variant.ident.to_string();
                let variant_class_name = format!("{}_{}", enum_name, variant_name);
                
                generated_code.push_str(&format!(
                    "                if variant == cls.{}:\n                    return {}(**kwargs)\n",
                    variant_name, variant_class_name
                ));
            }
        }
        
        generated_code.push_str("        raise ValueError(f\"Unknown variant {variant_name}\")\n");
        
        // Add toJSON method for complex enum
        generated_code.push_str("\n    def toJSON(self) -> str:\n");
        generated_code.push_str("        if isinstance(self.value, (int, str, bool, float)):\n");
        generated_code.push_str("            return json.dumps({\"type\": self.name})\n");
        generated_code.push_str("        if hasattr(self.value, 'toJSON') and callable(getattr(self.value, 'toJSON')):\n");
        generated_code.push_str("            # For complex variants, we merge the variant type with the inner value\n");
        generated_code.push_str("            inner_data = json.loads(self.value.toJSON())\n");
        generated_code.push_str("            if isinstance(inner_data, dict):\n");
        generated_code.push_str("                inner_data[\"type\"] = self.name\n");
        generated_code.push_str("                return json.dumps(inner_data)\n");
        generated_code.push_str("        return json.dumps({\"type\": self.name})\n");
        
        // Add fromJSON class method for complex enum deserialization
        generated_code.push_str("\n    @classmethod\n");
        generated_code.push_str("    def fromJSON(cls, json_str):\n");
        generated_code.push_str("        \"\"\"Deserialize JSON string to an enum instance\"\"\"\n");
        generated_code.push_str("        data = json.loads(json_str)\n");
        generated_code.push_str("        if isinstance(data, str):\n");
        generated_code.push_str("            # Simple enum with string value\n");
        generated_code.push_str("            return cls[data]  # Get enum by name\n");
        generated_code.push_str("        elif isinstance(data, dict):\n");
        generated_code.push_str("            # Complex enum with fields\n");
        generated_code.push_str("            if \"type\" in data:\n");
        generated_code.push_str("                variant_name = data[\"type\"]\n");
        generated_code.push_str("                variant = cls[variant_name]  # Get enum variant by name\n");
        generated_code.push_str("                \n");
        generated_code.push_str("                # For complex variants with associated data\n");
        generated_code.push_str("                if hasattr(variant.value, 'fromDict') and callable(getattr(variant.value, 'fromDict')):\n");
        generated_code.push_str("                    # Create data object from the dictionary (excluding the type field)\n");
        generated_code.push_str("                    variant_data = {k: v for k, v in data.items() if k != \"type\"}\n");
        generated_code.push_str("                    return variant.value.__class__.fromDict(variant_data)\n");
        generated_code.push_str("                \n");
        generated_code.push_str("                return variant\n");
        generated_code.push_str("        # Default fallback - return first variant\n");
        generated_code.push_str("        return next(iter(cls))\n");
        
    } else {
        // Simple enum with just unit variants
        let variants_code = e.variants.iter().enumerate().map(|(i, v)| {
            format!("    {} = {}", v.ident, i + 1)
        }).collect::<Vec<_>>().join("\n");
        
        generated_code.push_str(&format!("class {}(Enum):\n{}\n", enum_name, variants_code));
        
        // Add toJSON method for simple enum
        generated_code.push_str("\n    def toJSON(self) -> str:\n");
        generated_code.push_str("        return json.dumps(self.name)\n");
        
        // Add fromJSON method for simple enum
        generated_code.push_str("\n    @classmethod\n");
        generated_code.push_str("    def fromJSON(cls, json_str):\n");
        generated_code.push_str("        \"\"\"Deserialize JSON string to an enum instance\"\"\"\n");
        generated_code.push_str("        data = json.loads(json_str)\n");
        generated_code.push_str("        if isinstance(data, str):\n");
        generated_code.push_str("            return cls[data]  # Get enum by name\n");
        generated_code.push_str("        elif isinstance(data, int):\n");
        generated_code.push_str("            # Get enum by value if it's an integer\n");
        generated_code.push_str("            for enum_item in cls:\n");
        generated_code.push_str("                if enum_item.value == data:\n");
        generated_code.push_str("                    return enum_item\n");
        generated_code.push_str("        # Default fallback - return first variant\n");
        generated_code.push_str("        return next(iter(cls))\n");
    }
    
    Ok(DerivedPy {
        crate_rename: crate_rename.clone(),
        py_name: e.ident.to_string(),
        docs: String::new(),
        inline: quote!(#generated_code.to_owned()),
        inline_flattened: None,
        dependencies,
        concrete: HashMap::new(),
        bound: None,
        export: false,
        export_to: None,
    })
}

fn variant_name_to_snake_case(name: &str) -> String {
    let mut result = String::new();
    
    for (i, c) in name.char_indices() {
        if i > 0 && c.is_uppercase() {
            result.push('_');
        }
        result.push(c.to_lowercase().next().unwrap());
    }
    
    result
}