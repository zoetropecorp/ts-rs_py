use std::{
    any::TypeId,
    path::{Path, PathBuf},
    collections::HashSet, // Add HashSet import
};

pub use crate::export::ExportError;

/// A visitor used to iterate over all dependencies or generics of a Python type.
pub trait PyTypeVisitor: Sized {
    fn visit<T: Py + 'static + ?Sized>(&mut self);
}

// Implement TypeVisitor for anything that implements PyTypeVisitor
impl<T: PyTypeVisitor> crate::TypeVisitor for T {
    fn visit<U: crate::TS + 'static + ?Sized>(&mut self) {
        // This is just a stub implementation to satisfy the compiler
        // Real implementations will use PyTypeVisitor directly
    }
}

/// A Python type which is depended upon by other types.
/// This information is required for generating the correct import statements.
#[derive(Debug, Eq, PartialEq, Ord, PartialOrd)]
pub struct PyDependency {
    /// Type ID of the Rust type
    pub type_id: TypeId,
    /// Name of the type in Python
    pub py_name: String,
    /// Path to where the type would be exported
    pub output_path: &'static Path,
}

use std::sync::OnceLock;

impl PyDependency {
    /// Constructs a [`PyDependency`] from the given type `T`.
    /// This allows any type that implements Py to be tracked as a dependency.
    pub fn from_ty<T: Py + 'static + ?Sized>() -> Option<Self> {
        // Don't create dependencies for primitive types
        if <T as Py>::name() == "int" || 
           <T as Py>::name() == "str" || 
           <T as Py>::name() == "bool" || 
           <T as Py>::name() == "float" ||
           <T as Py>::name() == "None" {
            return None;
        }
        
        // Get the ident that will be used for both the type name and file name
        let ident = <T as Py>::ident();
        
        // Skip container types like Option, Vec, etc.
        if ident == "Optional" || ident == "List" || ident == "Dict" || ident == "Union" {
            return None;
        }
        
        // Skip Dummy type used for generics
        if ident == "Dummy" {
            return None;
        }
        
        // Debug: Print what we're about to add as a dependency
        println!("Adding dependency for type: {} with TypeId: {:?}", ident, TypeId::of::<T>());
        
        // If there's a specified output path from #[py(export)], use that, otherwise
        // default to <TypeName>.py in the export directory
        let output_path = <T as Py>::output_path().unwrap_or_else(|| {
            // Create a static path that will live for the duration of the program
            static PATHS: OnceLock<std::sync::Mutex<std::collections::HashMap<String, &'static Path>>> = 
                OnceLock::new();
                
            let paths = PATHS.get_or_init(|| {
                std::sync::Mutex::new(std::collections::HashMap::new())
            });
            
            let mut paths = paths.lock().unwrap();
            
            if let Some(path) = paths.get(&ident) {
                return *path;
            }
            
            // Create a new path and leak it so it lives for the duration of the program
            let path_string = format!("{}.py", ident);
            let leaked_string = Box::leak(path_string.into_boxed_str());
            let path = Box::leak(Box::new(Path::new(leaked_string)));
            
            paths.insert(ident.clone(), path);
            path
        });
        
        Some(PyDependency {
            type_id: TypeId::of::<T>(),
            py_name: ident,
            output_path,
        })
    }
}

/// A type which can be represented in Python.  
/// Most of the time, you'd want to derive this trait instead of implementing it manually.  
/// ts-rs comes with implementations for all primitives, most collections, tuples,
/// arrays and containers.
///
/// ### exporting
/// Python bindings can be exported within a test by adding `#[py(export)]`
/// to a type you wish to export to a file.  
/// When `cargo test` is run, all types annotated with `#[py(export)]` and all of their
/// dependencies will be written to `TS_RS_PY_EXPORT_DIR`, or `./py_bindings` by default.
///
/// For each individual type, path and filename within the output directory can be changed using
/// `#[py(export_to = "...")]`. By default, the filename will be derived from the name of the type.
///
/// Bindings can also be exported manually:
///
/// | Function              | Includes Dependencies | To                    |
/// |-----------------------|-----------------------|-----------------------|
/// | [`Py::export`]        | ❌                    | `TS_RS_PY_EXPORT_DIR` |
/// | [`Py::export_all`]    | ✔️                    | `TS_RS_PY_EXPORT_DIR` |
/// | [`Py::export_all_to`] | ✔️                    | _custom_              |
///
/// ### serde compatibility
/// By default, the feature `serde-compat` is enabled.
/// ts-rs then parses serde attributes and adjusts the generated python bindings accordingly.
/// Not all serde attributes are supported yet - if you use an unsupported attribute, you'll see a
/// warning.
pub trait Py {
    /// If this type does not have generic parameters, then `WithoutGenerics` should just be `Self`.
    /// If the type does have generic parameters, then all generic parameters must be replaced with
    /// a dummy type, e.g `ts_rs::Dummy` or `()`.
    type WithoutGenerics: Py + ?Sized;

    /// If the implementing type is `std::option::Option<T>`, then this associated type is set to `T`.
    /// All other implementations of `Py` should set this type to `Self` instead.
    type OptionInnerType: ?Sized;

    /// Documentation comment to describe this type in Python
    const DOCS: Option<&'static str> = None;

    #[doc(hidden)]
    const IS_OPTION: bool = false;

    /// Identifier of this type, excluding generic parameters.
    fn ident() -> String {
        // by default, fall back to `Py::name()`.
        let name = <Self as crate::Py>::name();

        match name.find('<') {
            Some(i) => name[..i].to_owned(),
            None => name,
        }
    }

    /// Declaration of this type, e.g. `class User: user_id: int`.
    /// This function will panic if the type has no declaration.
    fn decl() -> String;

    /// Declaration of this type using the supplied generic arguments.
    /// The resulting Python definition will not be generic. For that, see `Py::decl()`.
    /// If this type is not generic, then this function is equivalent to `Py::decl()`.
    fn decl_concrete() -> String;

    /// Name of this type in Python, including generic parameters
    fn name() -> String;

    /// Formats this types definition in Python.
    /// This function will panic if the type cannot be inlined.
    fn inline() -> String;

    /// Flatten a type declaration.  
    /// This function will panic if the type cannot be flattened.
    fn inline_flattened() -> String;

    /// Iterates over all dependency of this type.
    fn visit_dependencies(_: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
    }

    /// Iterates over all type parameters of this type.
    fn visit_generics(_: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
    }

    /// Resolves all dependencies of this type recursively.
    fn dependencies() -> Vec<PyDependency>
    where
        Self: 'static,
    {
        let mut deps: Vec<PyDependency> = vec![];
        struct Visit<'a>(&'a mut Vec<PyDependency>);
        impl PyTypeVisitor for Visit<'_> {
            fn visit<T: Py + 'static + ?Sized>(&mut self) {
                if let Some(dep) = PyDependency::from_ty::<T>() {
                    self.0.push(dep);
                }
            }
        }
        <Self as crate::Py>::visit_dependencies(&mut Visit(&mut deps));

        deps
    }

    /// Manually export this type to the filesystem.
    /// To export this type together with all of its dependencies, use [`Py::export_all`].
    ///
    /// # Automatic Exporting
    /// Types annotated with `#[py(export)]`, together with all of their dependencies, will be
    /// exported automatically whenever `cargo test` is run.  
    /// In that case, there is no need to manually call this function.
    ///
    /// # Target Directory
    /// The target directory to which the type will be exported may be changed by setting the
    /// `TS_RS_PY_EXPORT_DIR` environment variable. By default, `./py_bindings` will be used.
    ///
    /// To specify a target directory manually, use [`Py::export_all_to`], which also exports all
    /// dependencies.
    ///
    /// To alter the filename or path of the type within the target directory,
    /// use `#[py(export_to = "...")]`.
    fn export() -> Result<(), ExportError>
    where
        Self: 'static,
    {
        let path = <Self as crate::Py>::default_output_path()
            .ok_or_else(std::any::type_name::<Self>)
            .map_err(ExportError::CannotBeExported)?;

        export_to::<Self, _>(path)
    }

    /// Manually export this type to the filesystem, together with all of its dependencies.  
    /// To export only this type, without its dependencies, use [`Py::export`].
    ///
    /// # Automatic Exporting
    /// Types annotated with `#[py(export)]`, together with all of their dependencies, will be
    /// exported automatically whenever `cargo test` is run.  
    /// In that case, there is no need to manually call this function.
    ///
    /// # Target Directory
    /// The target directory to which the types will be exported may be changed by setting the
    /// `TS_RS_PY_EXPORT_DIR` environment variable. By default, `./py_bindings` will be used.
    ///
    /// To specify a target directory manually, use [`Py::export_all_to`].
    ///
    /// To alter the filenames or paths of the types within the target directory,
    /// use `#[py(export_to = "...")]`.
    fn export_all() -> Result<(), ExportError>
    where
        Self: 'static,
    {
        export_all_into::<Self>(&*default_py_out_dir())
    }

    /// Manually export this type into the given directory, together with all of its dependencies.  
    /// To export only this type, without its dependencies, use [`Py::export`].
    ///
    /// Unlike [`Py::export_all`], this function disregards `TS_RS_PY_EXPORT_DIR`, using the provided
    /// directory instead.
    ///
    /// To alter the filenames or paths of the types within the target directory,
    /// use `#[py(export_to = "...")]`.
    ///
    /// # Automatic Exporting
    /// Types annotated with `#[py(export)]`, together with all of their dependencies, will be
    /// exported automatically whenever `cargo test` is run.  
    /// In that case, there is no need to manually call this function.
    fn export_all_to(out_dir: impl AsRef<Path>) -> Result<(), ExportError>
    where
        Self: 'static,
    {
        export_all_into::<Self>(out_dir)
    }

    /// Manually generate bindings for this type, returning a [`String`].  
    ///
    /// # Automatic Exporting
    /// Types annotated with `#[py(export)]`, together with all of their dependencies, will be
    /// exported automatically whenever `cargo test` is run.  
    /// In that case, there is no need to manually call this function.
    fn export_to_string() -> Result<String, ExportError>
    where
        Self: 'static,
    {
        export_to_string::<Self>()
    }

    /// Returns the output path to where `T` should be exported.  
    /// The returned path does _not_ include the base directory from `TS_RS_PY_EXPORT_DIR`.  
    ///
    /// To get the output path containing `TS_RS_PY_EXPORT_DIR`, use [`Py::default_output_path`].
    ///
    /// When deriving `Py`, the output path can be altered using `#[py(export_to = "...")]`.  
    ///
    /// The output of this function depends on the environment variable `TS_RS_PY_EXPORT_DIR`, which is
    /// used as base directory. If it is not set, `./py_bindings` is used as default directory.
    ///
    /// If `T` cannot be exported (e.g because it's a primitive type), this function will return
    /// `None`.
    fn output_path() -> Option<&'static Path> {
        None
    }

    /// Returns the output path to where `T` should be exported.  
    ///
    /// The output of this function depends on the environment variable `TS_RS_PY_EXPORT_DIR`, which is
    /// used as base directory. If it is not set, `./py_bindings` is used as default directory.
    ///
    /// To get the output path relative to `TS_RS_PY_EXPORT_DIR` and without reading the environment
    /// variable, use [`Py::output_path`].
    ///
    /// When deriving `Py`, the output path can be altered using `#[py(export_to = "...")]`.  
    ///
    /// If `T` cannot be exported (e.g because it's a primitive type), this function will return
    /// `None`.
    fn default_output_path() -> Option<PathBuf> {
        Some(default_py_out_dir().join(<Self as crate::Py>::output_path()?))
    }
}

/// Default output directory for Python bindings
fn default_py_out_dir() -> std::borrow::Cow<'static, Path> {
    match std::env::var("TS_RS_PY_EXPORT_DIR") {
        Err(..) => std::borrow::Cow::Borrowed(Path::new("./py_bindings")),
        Ok(dir) => std::borrow::Cow::Owned(PathBuf::from(dir)),
    }
}

/// Export a Python type to a file
fn export_to<T: Py + ?Sized + 'static, P: AsRef<Path>>(path: P) -> Result<(), ExportError> {
    let path = path.as_ref().to_owned();
    
    // Create the Python code with proper imports and declarations
    let mut buffer = String::with_capacity(1024);
    let decl = T::decl_concrete();
    
    // Insert the definition on the line *before* `let mut imports = ...`
    let target_class_name = T::ident(); // Get the name of the class being exported
    
    // Create a set of imports that are actually needed based on the declaration
    let mut imports = std::collections::HashSet::new();
    
    // We'll collect typing imports separately to combine them
    let mut typing_imports = Vec::new();
    
    // Standard imports based on what's actually used
    if decl.contains("Optional[") {
        typing_imports.push("Optional");
    }
    if decl.contains("List[") {
        typing_imports.push("List");
    }
    if decl.contains("Dict[") {
        typing_imports.push("Dict");
    }
    if decl.contains("Union[") {
        typing_imports.push("Union");
    }
    if decl.contains("Any") {
        typing_imports.push("Any");
    }
    
    // Combine all typing imports into one line
    if !typing_imports.is_empty() {
        typing_imports.sort(); // Sort for consistent output
        imports.insert(format!("from typing import {}", typing_imports.join(", ")));
    }
    
    // Add enum imports if needed
    if decl.contains("class") && (decl.contains("(Enum)") || decl.contains("variant instance with fields")) {
        imports.insert("from enum import Enum, auto".to_string());
    }
    
    // Add dataclass imports if needed
    if decl.contains("@dataclass") {
        imports.insert("from dataclasses import dataclass".to_string());
    }
    
    // Add imports for other dependencies
    // Manually scan the declaration to find types that need to be imported
    // This is a workaround for the limitation in the current dependency tracking
    let mut seen_types = std::collections::HashSet::new();
    
    // External types are imported from their standard libraries
    // but we don't also need to import the Uuid and NaiveDateTime types from local modules
    if decl.contains("Uuid") {
        imports.insert("from uuid import UUID as Uuid".to_string());
        seen_types.insert("Uuid".to_string()); // Prevent double import
    }
    if decl.contains("NaiveDateTime") {
        imports.insert("from datetime import datetime as NaiveDateTime".to_string());
        seen_types.insert("NaiveDateTime".to_string()); // Prevent double import
    }
    
    // Scan the entire declaration text to find custom type references
    let standard_types = ["int", "str", "bool", "float", "None", "List", "Dict", "Optional", 
                         "Union", "Any", "Enum", "auto", "dataclass", "Type", "TypeVar", 
                         "Generic", "TYPE_CHECKING", "Self", "Path", "Path("];
    
    for line in decl.lines() {
        let line = line.trim();
        
        // Skip comments and method definitions
        if line.starts_with("#") || line.starts_with("def ") {
            continue;
        }
        
        // Process class relationships and variant references
        if line.contains("=") && line.contains("Complex") {
            // Handle variant references like "B = ComplexEnum_B"
            if let Some(pos) = line.find('=') {
                let value_part = line[pos+1..].trim();
                let type_name = value_part.split_whitespace().next().unwrap_or("");
                
                if !type_name.is_empty() && type_name.chars().next().unwrap().is_uppercase() 
                   && !type_name.contains("(") && !type_name.contains("{") && !type_name.contains("[") {
                    let type_string = type_name.to_string();
                    
                    // *** Check before inserting: Skip if type is defined in this file ***
                    if !seen_types.contains(&type_string) && !standard_types.contains(&type_name) &&
                       type_string != target_class_name && 
                       !type_string.starts_with(&format!("{}_", target_class_name)) // Skip variants like Command_Move
                    {
                        seen_types.insert(type_string.clone());
                        imports.insert(format!("from {} import {}", type_string, type_string));
                    }
                }
            }
        }
        
        // Look for type annotations in field declarations
        if let Some(colon_pos) = line.find(": ") {
            // Get type part (after colon)
            let type_part = &line[colon_pos + 2..];
            
            // Find the end of the type (stops at commas, equals, etc.)
            let end_pos = type_part.find(|c| c == ',' || c == '=' || c == ')' || c == '}')
                .unwrap_or_else(|| type_part.len());
            
            let type_name = type_part[..end_pos].trim();
            
            // Parse potential complex type expressions like List[User] or Dict[str, Role]
            let mut types_to_check = Vec::new();
            
            // Handle container types
            if type_name.contains('[') && type_name.contains(']') {
                // Extract inner types from container types like List[User] or Dict[str, Role]
                if let Some(bracket_pos) = type_name.find('[') {
                    let inner_types = &type_name[bracket_pos+1..type_name.rfind(']').unwrap_or(type_name.len()-1)];
                    
                    // Split by commas for dictionary or union types
                    for inner_part in inner_types.split(',') {
                        types_to_check.push(inner_part.trim());
                    }
                }
            }
            
            // Add the main type as well
            types_to_check.push(type_name);
            
            // Process all type names (main and nested)
            for type_str in types_to_check {
                // Extract all potential class names by finding uppercase words
                for part in type_str.split(|c: char| !c.is_alphanumeric()) {
                    if !part.is_empty() && part.chars().next().unwrap().is_uppercase() {
                        let part_string = part.to_string();
                        
                        // *** Check before inserting: Skip if type is defined in this file ***
                        if !seen_types.contains(&part_string) && !standard_types.contains(&part) &&
                           part_string != target_class_name &&
                           !part_string.starts_with(&format!("{}_", target_class_name)) // Skip variants
                        {
                            seen_types.insert(part_string.clone());
                            imports.insert(format!("from {} import {}", part_string, part_string));
                        }
                    }
                }
            }
        }
        
        // Scan for special field patterns that might contain type references
        // Handle tuple fields (field_0: Type)
        if line.contains("field_") && line.contains(':') && !line.contains("def ") {
            let field_parts: Vec<&str> = line.split(':').collect();
            if field_parts.len() >= 2 {
                let field_name = field_parts[0].trim();
                
                // Skip if field looks like a Python code fragment
                if !field_name.is_empty() && 
                   !field_name.contains("(") && !field_name.contains(")") &&
                   !field_name.contains(" if ") && !field_name.contains(" for ") && 
                   !field_name.contains(" in ") && !field_name.contains(" return ") &&
                   !field_name.contains(" elif ") && !field_name.contains(" else") &&
                   !is_python_fragment(field_name) {
                   
                    let type_part = field_parts[1].trim();
                    let type_name = type_part.split(|c: char| !c.is_alphanumeric()).next().unwrap_or("");
                    
                    if !type_name.is_empty() && type_name.chars().next().unwrap().is_uppercase() {
                        let type_string = type_name.to_string();
                        
                        // *** Check before inserting: Skip if type is defined in this file ***
                        if !seen_types.contains(&type_string) && !standard_types.contains(&type_name) &&
                           type_string != target_class_name &&
                           !type_string.starts_with(&format!("{}_", target_class_name)) // Skip variants
                        {
                            seen_types.insert(type_string.clone());
                            imports.insert(format!("from {} import {}", type_string, type_string));
                        }
                    }
                }
            }
        }
        
        // Handle named fields like "nested" that often reference other types
        for field_name in ["nested", "inner", "data", "value", "content"] {
            let field_pattern = format!("{}: ", field_name);
            // Skip if this is a function definition
            if line.contains(&field_pattern) && !line.contains("def ") {
                if let Some(pos) = line.find(&field_pattern) {
                    let type_part = &line[pos + field_pattern.len()..].trim();
                    let type_name = type_part.split(|c: char| !c.is_alphanumeric()).next().unwrap_or("");
                    
                    if !type_name.is_empty() && type_name.chars().next().unwrap().is_uppercase() {
                        let type_string = type_name.to_string();
                        
                        // *** Check before inserting: Skip if type is defined in this file ***
                        if !seen_types.contains(&type_string) && !standard_types.contains(&type_name) &&
                           type_string != target_class_name &&
                           !type_string.starts_with(&format!("{}_", target_class_name)) // Skip variants
                        {
                            seen_types.insert(type_string.clone());
                            imports.insert(format!("from {} import {}", type_string, type_string));
                        }
                    }
                }
            }
        }
    }
    
    // Also specifically search for variant class references that might be missed in regular parsing
    // This addresses complex enum variant references
    for part in decl.split_whitespace() {
        if part.contains('_') {
            let parts: Vec<&str> = part.split('_').collect();
            if parts.len() >= 2 {
                let prefix = parts[0];
                
                // If it contains an underscore and the first part starts with uppercase,
                // it's likely a variant class reference like ComplexEnum_VariantName
                if !prefix.is_empty() && prefix.chars().next().unwrap().is_uppercase() 
                   && !standard_types.contains(&prefix) && !seen_types.contains(prefix) {
                    // *** Check before inserting: Skip if prefix matches target class name ***
                    if prefix != target_class_name { 
                        seen_types.insert(prefix.to_string());
                        imports.insert(format!("from {} import {}", prefix, prefix));
                    }
                }
            }
        }
    }
    
    // Create an organized buffer that ensures __future__ imports are first
    
    // 1. Start with __future__ imports (MUST be first)
    buffer.push_str("from __future__ import annotations\n\n");
    
    // 2. Add standard library imports
    buffer.push_str("import json\n");
    buffer.push_str("import sys\n");
    buffer.push_str("from pathlib import Path\n");
    buffer.push_str("from enum import Enum, auto\n");
    buffer.push_str("from typing import Any, Optional, List, Dict, Union, TYPE_CHECKING\n");
    buffer.push_str("from dataclasses import dataclass\n");
    
    // 3. Add path handling for imports
    buffer.push_str("\n# Add current directory to Python path to facilitate imports\n");
    buffer.push_str("_current_file = Path(__file__).resolve()\n");
    buffer.push_str("_current_dir = _current_file.parent\n");
    buffer.push_str("if str(_current_dir) not in sys.path:\n");
    buffer.push_str("    sys.path.append(str(_current_dir))\n\n");
    
    // 3. Add type checking block
    buffer.push_str("# Forward references for type checking only\n");
    buffer.push_str("if TYPE_CHECKING:\n");
    
    // Add collected custom imports under TYPE_CHECKING to avoid circular imports
    let mut custom_imports = Vec::new();
    // Use the original `imports` set directly
    for import in &imports { 
        if !import.starts_with("from typing import") && 
           !import.starts_with("from enum import") && 
           !import.starts_with("from dataclasses import") &&
           !import.starts_with("from pathlib import") &&
           import != "import json" {
            // Fix malformed imports
            if import.contains("from Path(") || import.contains("import Path(") {
                continue; // Skip malformed Path imports
            }
            custom_imports.push(format!("    {}", import));
        }
    }
    
    if !custom_imports.is_empty() {
        custom_imports.sort(); // Sort for consistent output
        for import_stmt in custom_imports {
            buffer.push_str(&format!("{}\n", import_stmt));
        }
    } else {
        buffer.push_str("    pass  # Type checking imports will be used via annotations\n");
    }
    buffer.push_str("\n");
    
    // 5. Remove duplicated imports and path handling from the declaration
    let mut cleaned_lines = Vec::new();
    let mut inside_path_block = false;
    
    for line in decl.lines() {
        if inside_path_block && (line.contains("sys.path.append") || line.trim().is_empty()) {
            inside_path_block = false;
            continue;
        }
        
        if line.contains("_current_file = Path") || 
           line.contains("_current_dir = ") || 
           line.contains("if str(_current_dir) not in sys.path") {
            inside_path_block = true;
            continue;
        }
        
        // Skip boilerplate imports and code we've already added
        if line.starts_with("from __future__ import") ||
           line.starts_with("from typing import") || 
           line.starts_with("from enum import") || 
           line.starts_with("import json") ||
           line.starts_with("import sys") ||
           line.starts_with("from pathlib import") ||
           line.starts_with("from dataclasses import") ||
           line.contains("sys.path.append") ||
           line.contains("TYPE_CHECKING") ||
           (line.contains("# Add current directory to Python path") || 
            line.contains("# Forward references for type checking only") || 
            line.contains("# Helper for import path resolution") || 
            line.contains("# Import utilities and custom types") ||
            line.contains("# Prevent circular imports with TYPE_CHECKING")) {
            continue;
        }
        
        // Skip additional empty lines after removed imports
        if cleaned_lines.last().map_or(false, |last: &&str| last.trim().is_empty()) && line.trim().is_empty() {
            continue;
        }
        
        cleaned_lines.push(line);
    }
    
    let cleaned_decl = normalize_field_spacing(&cleaned_lines.join("\n"));
    
    // We do the following steps to clean up the code:
    // 1. Extract the class definition (first occurrence only)
    // 2. Remove existing toJSON and _serialize methods
    // 3. Add our specialized toJSON and _serialize methods
    
    let class_name = T::ident();
    let mut clean_buffer = String::new();
    let mut in_class = false;
    let mut class_found = false;
    let mut inside_method = false;
    let mut _indent = "    "; // Default indentation
    
    // First pass: extract class definition and non-toJSON methods
    for line in cleaned_decl.lines() {
        let trimmed = line.trim();
        
        // Detect class definitions
        if trimmed.starts_with("class ") {
            if line.contains(&class_name) {
                // For the target class
                if !class_found {
                    class_found = true;
                    in_class = true;
                    clean_buffer.push_str(line);
                    clean_buffer.push('\n');
                    
                    // Save the indentation level for this class
                    if let Some(class_pos) = line.find("class") {
                        if class_pos > 0 {
                            _indent = &line[0..class_pos];
                        }
                    }
                }
                // Skip duplicate definitions of the same class
            } else {
                // For other classes, just include them
                in_class = true;
                clean_buffer.push_str(line);
                clean_buffer.push('\n');
            }
            continue;
        }
        
        // Track when we're inside a method to avoid including toJSON or _serialize
        if in_class && trimmed.starts_with("def ") {
            // Check if this is a toJSON or _serialize method that we want to replace
            if trimmed.starts_with("def toJSON(self)") || trimmed.starts_with("def _serialize(self)") {
                inside_method = true;
                continue;
            } else if trimmed.starts_with("def fromJSON(cls") {
                // Replace fromJSON with our implementation later
                inside_method = true;
                continue;
            } else {
                inside_method = true;
                clean_buffer.push_str(line);
                clean_buffer.push('\n');
                continue;
            }
        }
        
        // End of method detection
        if inside_method && (trimmed.is_empty() || trimmed.starts_with("def ") || trimmed.starts_with("class ")) {
            inside_method = false;
        }
        
        // Include non-method lines and method lines for methods we're not replacing
        if !inside_method || !in_class {
            clean_buffer.push_str(line);
            clean_buffer.push('\n');
        }
    }
    
    // Generate a completely new Python file with all needed parts
    buffer.clear();
    
    // 1. Add the standard imports
    buffer.push_str("from __future__ import annotations\n\n");
    buffer.push_str("import json\n");
    buffer.push_str("import sys\n");
    buffer.push_str("from pathlib import Path\n");
    buffer.push_str("from enum import Enum, auto\n");
    buffer.push_str("from typing import Any, Optional, List, Dict, Union, TYPE_CHECKING\n");
    buffer.push_str("from dataclasses import dataclass\n\n");
    
    // 2. Add path handling for imports
    buffer.push_str("# Add current directory to Python path to facilitate imports\n");
    buffer.push_str("_current_file = Path(__file__).resolve()\n");
    buffer.push_str("_current_dir = _current_file.parent\n");
    buffer.push_str("if str(_current_dir) not in sys.path:\n");
    buffer.push_str("    sys.path.append(str(_current_dir))\n\n");
    
    // 3. Add type checking block
    buffer.push_str("# Forward references for type checking only\n");
    buffer.push_str("if TYPE_CHECKING:\n");
    
    // Filter out imports for the class itself or its variants defined in the same file
    let target_class_name = T::ident();
    let mut filtered_imports = imports.clone(); // Clone to allow modification
    
    imports.iter().for_each(|import_stmt| {
        // Expected format: "from Module import Class"
        let parts: Vec<&str> = import_stmt.split_whitespace().collect();
        if parts.len() >= 4 && parts[0] == "from" && parts[2] == "import" {
            let module_name = parts[1];
            let class_name = parts[3]; // Class name might be different if aliased, but usually same
            
            // Check if module name matches the target class or a variant pattern
            if module_name == target_class_name || class_name == target_class_name ||
               (module_name.starts_with(&format!("{}_", target_class_name)) && class_name.starts_with(&format!("{}_", target_class_name)))
            {
                filtered_imports.remove(import_stmt);
            }
        }
    });
    
    // Add collected custom imports under TYPE_CHECKING to avoid circular imports
    let mut custom_imports = Vec::new();
    // Use the filtered set now
    for import in &filtered_imports {
        if !import.starts_with("from typing import") && 
           !import.starts_with("from enum import") && 
           !import.starts_with("from dataclasses import") &&
           !import.starts_with("from pathlib import") &&
           import != "import json" {
            // Fix malformed imports
            if import.contains("from Path(") || import.contains("import Path(") {
                continue; // Skip malformed Path imports
            }
            custom_imports.push(format!("    {}", import));
        }
    }
    
    if !custom_imports.is_empty() {
        custom_imports.sort(); // Sort for consistent output
        for import_stmt in custom_imports {
            buffer.push_str(&format!("{}\n", import_stmt));
        }
    } else {
        buffer.push_str("    pass  # Type checking imports will be used via annotations\n");
    }
    buffer.push_str("\n");
    
    // 4. Extract the main class definition (and only that)
    let mut class_def = String::new();
    let mut fields = Vec::new();
    let mut inside_class = false;
    let mut class_indent = ""; // Remember the indentation of the class
    let target_class_name = T::ident(); // Get the name of the class we are exporting
    let mut is_target_class = false; // Track if we are currently inside the target class

    for line in clean_buffer.lines() { // clean_buffer comes from cleaned_decl
        if line.trim().starts_with("class ") {
            // Start of a class definition
            if let Some(class_pos) = line.find("class") {
                if class_pos > 0 {
                    class_indent = &line[0..class_pos];
                }
            }
            // Determine the name of the class defined on this line
            let current_class_name = line.trim().split(&[' ', '(', ':'][..]).nth(1).unwrap_or("");
            if !is_target_class && current_class_name == target_class_name {
                // Found the target class definition
                is_target_class = true; // We are now inside the target class
                inside_class = true;
                class_def.push_str(line); // Start accumulating its definition
                class_def.push_str("\n"); // Corrected: use double quotes for string literal
            } else {
                // If we encounter another class (or already passed the target), stop processing for fields
                is_target_class = false;
                inside_class = false; // Treat as outside relevant class scope for field collection
                // We still need to include other class definitions in the final output later,
                // but we don't collect their fields for the main class methods.
            }
        } else if is_target_class && !line.trim().is_empty() { // Only process lines if inside the target class
            // Skip any method definitions, we'll add our own later
            if !line.trim().starts_with("def ") && !line.trim().starts_with("@") {
                class_def.push_str(line); // Accumulate non-method lines for the target class
                class_def.push_str("\n"); // Corrected: use double quotes for string literal

                // Extract field declarations ONLY from the target class
                if line.contains(":") && !line.contains("class") && !line.trim().starts_with("#") && !line.trim().starts_with("def ") {
                    // Make sure this is a valid field declaration and not a fragment of method code
                    let parts: Vec<&str> = line.trim().split(':').collect();
                    if parts.len() >= 2 {
                        let field_name = parts[0].trim();
                        // Skip if field looks like a Python code fragment or keyword
                        if !field_name.is_empty() &&
                           !field_name.contains("(") && !field_name.contains(")") &&
                           !field_name.contains(" if ") && !field_name.contains(" for ") &&
                           !field_name.contains(" in ") && !field_name.contains(" return ") &&
                           !field_name.contains(" elif ") && !field_name.contains(" else") &&
                           !is_python_fragment(field_name) && !is_python_keyword(field_name) {
                            fields.push(field_name.to_string()); // <<< Only push fields for the target class
                        }
                    }
                }
             }
        } else if is_target_class && line.trim().is_empty() { // Keep empty lines within the target class def
            class_def.push_str("\n"); // Corrected: use double quotes for string literal
        } else if !inside_class {
            // For non-class content (outside the target class scope we just defined), handle imports etc. if needed
            // This part might need adjustment depending on overall structure, but the key is `fields` is now correct.
            // For now, assume other content is handled elsewhere or doesn't affect field collection.
        }
    }
    
    // Add the class definition (without methods)
    buffer.push_str(&class_def);
    
    // Extract the class name 
    let _class_name = T::ident();
    
    // Extract indentation from the class definition
    let _indent = class_indent; // Use the indentation we captured earlier
    
    // For enum types, we have special handling
    if class_def.contains("class") && class_def.contains("(Enum)") {
        // Add toJSON method
        buffer.push_str("\n    def toJSON(self) -> str:\n");
        buffer.push_str("        \"\"\"Serialize this object to a JSON string\"\"\"\n");
        buffer.push_str("        return json.dumps(self._serialize())\n\n");
        
        // Add _serialize method
        buffer.push_str("    def _serialize(self):\n");
        buffer.push_str("        \"\"\"Convert this object to a serializable dictionary\"\"\"\n");
        buffer.push_str("        # Enum serialization\n");
        buffer.push_str("        return self.name\n\n");
        
        // Add fromJSON method
        buffer.push_str("    @classmethod\n");
        buffer.push_str("    def fromJSON(cls, json_str):\n");
        buffer.push_str("        \"\"\"Deserialize JSON string to a new instance\"\"\"\n");
        buffer.push_str("        data = json.loads(json_str)\n");
        buffer.push_str("        return cls.fromDict(data)\n\n");
        
        // Add fromDict method
        buffer.push_str("    @classmethod\n");
        buffer.push_str("    def fromDict(cls, data):\n");
        buffer.push_str("        \"\"\"Deserialize dict to an enum instance\"\"\"\n");
        buffer.push_str("        if isinstance(data, str):\n");
        buffer.push_str("            return cls[data]  # Get enum by name\n");
        buffer.push_str("        elif isinstance(data, int):\n");
        buffer.push_str("            # Get enum by value if it's an integer\n");
        buffer.push_str("            for enum_item in cls:\n");
        buffer.push_str("                if enum_item.value == data:\n");
        buffer.push_str("                    return enum_item\n");
        buffer.push_str("        # Default fallback - return first variant\n");
        buffer.push_str("        return next(iter(cls))\n");
    } 
    // For complex enums with data
    else if cleaned_decl.contains("class") && cleaned_decl.contains("variant instance with fields") {
        // Extract the main enum class name from the declaration
        let enum_name = _class_name.clone();
        
        // First, we need to extract variant information and their data from the declaration
        // This helps us generate proper variant class definitions
        
        let mut variant_classes = Vec::new();
        let mut variant_names = Vec::new();
        let mut is_collecting_variant = false;
        let mut current_variant_data = String::new();
        let mut current_variant_name = String::new();
        let mut current_class_fields = HashSet::new(); // Track fields we've seen for the current class
        
        // Parse the declaration to find variant class definitions
        for line in cleaned_decl.lines() {
            let trimmed = line.trim();
            
            // Detect the start of a variant class declaration
            if trimmed.starts_with("class") && line.contains("_") && !is_collecting_variant {
                is_collecting_variant = true;
                current_variant_data = format!("{}\n", line);
                current_class_fields.clear(); // Clear fields when starting a new class
                
                // Extract variant name from class name
                if let Some(class_start) = trimmed.find("class ") {
                    let after_class = &trimmed[class_start + 6..];
                    if let Some(space_end) = after_class.find(|c: char| c.is_whitespace() || c == ':') {
                        let class_name = &after_class[..space_end];
                        if let Some(underscore_pos) = class_name.find('_') {
                            current_variant_name = class_name[underscore_pos+1..].to_string();
                            variant_names.push(current_variant_name.clone());
                        }
                    }
                }
                
                continue;
            }
            
            // Collect lines for the current variant class
            if is_collecting_variant {
                // If we hit another class or enum definition, we're done with this variant
                if trimmed.starts_with("class ") || trimmed.starts_with("enum ") {
                    is_collecting_variant = false;
                    variant_classes.push(current_variant_data.clone());
                    current_variant_data.clear();
                    current_class_fields.clear(); // Clear fields at the end of a class
                    
                    // Start collecting the new class immediately if it's a variant
                    if trimmed.starts_with("class") && line.contains("_") {
                        is_collecting_variant = true;
                        current_variant_data = format!("{}\n", line);
                        
                        // Extract variant name
                        if let Some(class_start) = trimmed.find("class ") {
                            let after_class = &trimmed[class_start + 6..];
                            if let Some(space_end) = after_class.find(|c: char| c.is_whitespace() || c == ':') {
                                let class_name = &after_class[..space_end];
                                if let Some(underscore_pos) = class_name.find('_') {
                                    current_variant_name = class_name[underscore_pos+1..].to_string();
                                    variant_names.push(current_variant_name.clone());
                                }
                            }
                        }
                    }
                } else {
                    // Process field declarations to avoid duplicate fields
                    if trimmed.contains(":") && !trimmed.starts_with("class") && !trimmed.starts_with("#") && !trimmed.starts_with("def ") {
                        let parts: Vec<&str> = trimmed.split(':').collect();
                        if parts.len() >= 2 {
                            let field_name = parts[0].trim();
                            
                            // Only add if we haven't seen this field for the current class
                            if !current_class_fields.contains(field_name) {
                                current_class_fields.insert(field_name.to_string());
                                // Add the line to the variant data
                                current_variant_data.push_str(&format!("{}\n", line));
                            }
                        } else {
                            // Add non-field line
                            current_variant_data.push_str(&format!("{}\n", line));
                        }
                    } else {
                        // Add non-field line
                        current_variant_data.push_str(&format!("{}\n", line));
                    }
                }
            }
            
            // Check for main enum class declaration
            if !is_collecting_variant && trimmed.starts_with("class") && trimmed.contains("(Enum)") && !line.contains("_") {
                // We've found the main enum class, but we don't start collecting yet
                // Just track when we've seen it
            }
            
            // Check for variant mappings in the main enum class (e.g., "B = ComplexEnum_B")
            if !is_collecting_variant && trimmed.contains("=") && trimmed.contains("_") {
                let parts: Vec<&str> = trimmed.split('=').collect();
                if parts.len() >= 2 {
                    let variant_name = parts[0].trim();
                    // Only add valid Python identifiers, not keywords or fragments
                    if !variant_name.is_empty() && 
                        !variant_names.contains(&variant_name.to_string()) &&
                        !is_python_keyword(variant_name) && 
                        !is_python_fragment(variant_name) &&
                        // Exclude fragments that look like code
                        !variant_name.contains(".") &&
                        !variant_name.contains("_serialize") &&
                        !variant_name.contains("toJSON") &&
                        !variant_name.contains("fromDict") &&
                        !variant_name.contains("data") &&
                        !variant_name.contains("variant") {
                        variant_names.push(variant_name.to_string());
                    }
                }
            }
        }
        
        // If we're still collecting the last variant when we reach the end
        if is_collecting_variant && !current_variant_data.is_empty() {
            variant_classes.push(current_variant_data);
        }
        
        // 1. Generate all variant dataclasses first
        // This creates the necessary helper classes for the complex enum variants
        
        // Initialize a buffer for variant classes
        let mut variant_classes_buffer = String::new();
        
        for variant_class in &variant_classes {
            // Extract field names and types from the variant class
            let mut field_names = Vec::new();
            let mut field_types = Vec::new();
            
            for line in variant_class.lines() {
                let line = line.trim();
                
                // Look for field definitions like "foo: str"
                if line.contains(":") && !line.starts_with("class") && !line.starts_with("#") && !line.starts_with("def ") {
                    let parts: Vec<&str> = line.split(':').collect();
                    if parts.len() >= 2 {
                        let field_name = parts[0].trim();
                        let field_type = parts[1].trim();
                        
                        if !field_name.is_empty() && 
                           !field_name.contains("(") && !field_name.contains(")") &&
                           !field_name.contains(" if ") && !field_name.contains(" for ") && 
                           !field_name.contains(" in ") && !field_name.contains(" return ") &&
                           !field_name.contains(" elif ") && !field_name.contains(" else") &&
                           !is_python_fragment(field_name) && !is_python_keyword(field_name) {
                            field_names.push(field_name.to_string());
                            field_types.push(field_type.to_string());
                        }
                    }
                }
            }
            
            // Extract variant class name
            let mut variant_class_name = String::new();
            if let Some(class_line) = variant_class.lines().next() {
                if class_line.contains("class ") {
                    let parts: Vec<&str> = class_line.split("class ").collect();
                    if parts.len() >= 2 {
                        if let Some(end_pos) = parts[1].find(|c: char| c.is_whitespace() || c == ':') {
                            variant_class_name = parts[1][..end_pos].trim().to_string();
                        } else {
                            variant_class_name = parts[1].trim().to_string();
                        }
                    }
                }
            }
            
            if !variant_class_name.is_empty() {
                // Generate a complete dataclass for this variant
                variant_classes_buffer.push_str(&format!("@dataclass\nclass {}:\n", variant_class_name));
                
                // Add field definitions
                for (i, (name, type_)) in field_names.iter().zip(field_types.iter()).enumerate() {
                    // Skip method definitions that were incorrectly parsed as fields
                    if name.starts_with("def ") {
                        continue;
                    }
                    variant_classes_buffer.push_str(&format!("    {}: {}\n", name, type_));
                }
                
                if field_names.is_empty() || field_names.iter().all(|name| name.starts_with("def ")) {
                    variant_classes_buffer.push_str("    pass\n");
                }
                
                // Add constructor
                let valid_field_names: Vec<_> = field_names.iter()
                    .filter(|name| {
                        !name.starts_with("def ") &&
                        !name.contains("(") && !name.contains(")") &&
                        !name.contains(" if ") && !name.contains(" for ") && 
                        !name.contains(" in ") && !name.contains(" return ") &&
                        !name.contains(" elif ") && !name.contains(" else") &&
                        !is_python_fragment(name) &&
                        !is_python_keyword(name)
                    })
                    .collect();

                if !valid_field_names.is_empty() {
                    variant_classes_buffer.push_str("\n    def __init__(self");
                    
                    // Add parameters with type hints - only include actual fields
                    for name in &valid_field_names {
                        variant_classes_buffer.push_str(&format!(", {}", name));
                    }
                    
                    variant_classes_buffer.push_str("):\n");
                    
                    // Add field assignments - only include actual fields
                    for name in &valid_field_names {
                        variant_classes_buffer.push_str(&format!("        self.{} = {}\n", name, name));
                    }
                }
                
                // Add toJSON method
                variant_classes_buffer.push_str("\n    def toJSON(self) -> str:\n");
                variant_classes_buffer.push_str("        \"\"\"Serialize this object to a JSON string\"\"\"\n");
                variant_classes_buffer.push_str("        return json.dumps(self._serialize())\n\n");
                
                // Add _serialize method
                variant_classes_buffer.push_str("    def _serialize(self):\n");
                variant_classes_buffer.push_str("        \"\"\"Convert this object to a serializable dictionary\"\"\"\n");
                variant_classes_buffer.push_str("        result = {}\n");
                variant_classes_buffer.push_str("        for key, value in self.__dict__.items():\n");
                variant_classes_buffer.push_str("            # Skip private fields\n");
                variant_classes_buffer.push_str("            if key.startswith('_'):\n");
                variant_classes_buffer.push_str("                continue\n");
                variant_classes_buffer.push_str("            # Recursively serialize any nested objects\n");
                variant_classes_buffer.push_str("            if hasattr(value, '_serialize'):\n");
                variant_classes_buffer.push_str("                result[key] = value._serialize()\n");
                variant_classes_buffer.push_str("            elif isinstance(value, list):\n");
                variant_classes_buffer.push_str("                result[key] = [item._serialize() if hasattr(item, '_serialize') else item for item in value]\n");
                variant_classes_buffer.push_str("            elif isinstance(value, dict):\n");
                variant_classes_buffer.push_str("                result[key] = {k: v._serialize() if hasattr(v, '_serialize') else v for k, v in value.items()}\n");
                variant_classes_buffer.push_str("            elif isinstance(value, Enum):\n");
                variant_classes_buffer.push_str("                result[key] = value.name\n");
                variant_classes_buffer.push_str("            else:\n");
                variant_classes_buffer.push_str("                result[key] = value\n");
                variant_classes_buffer.push_str("        return result\n\n");
                
                // Add fromDict method
                variant_classes_buffer.push_str("    @classmethod\n");
                variant_classes_buffer.push_str("    def fromDict(cls, data):\n");
                variant_classes_buffer.push_str("        \"\"\"Create an instance from a dictionary\"\"\"\n");
                
                if !field_names.is_empty() {
                    // Filter out any fields that look like code fragments
                    let valid_field_names: Vec<_> = field_names.iter()
                        .filter(|name| {
                            !name.starts_with("def ") &&
                            !name.contains("(") && !name.contains(")") &&
                            !name.contains(" if ") && !name.contains(" for ") && 
                            !name.contains(" in ") && !name.contains(" return ") &&
                            !name.contains(" elif ") && !name.contains(" else") &&
                            !is_python_fragment(name) &&
                            !is_python_keyword(name)
                        })
                        .collect();
                    
                    let valid_field_types: Vec<_> = field_names.iter()
                        .zip(field_types.iter())
                        .filter(|(name, _)| {
                            !name.starts_with("def ") &&
                            !name.contains("(") && !name.contains(")") &&
                            !name.contains(" if ") && !name.contains(" for ") && 
                            !name.contains(" in ") && !name.contains(" return ") &&
                            !name.contains(" elif ") && !name.contains(" else") &&
                            !is_python_fragment(name) &&
                            !is_python_keyword(name)
                        })
                        .map(|(_, typ)| typ)
                        .collect();
                    
                    for (i, (name, type_)) in valid_field_names.iter().zip(valid_field_types.iter()).enumerate() {
                        let stripped_type = type_.split('[').next().unwrap_or("").trim();
                        
                        // Add import for the appropriate type - needs to be delayed to execution time
                        let is_known_type = ["int", "str", "bool", "float", "list", "dict", "Any", "Union", 
                                          "Optional", "List", "Dict"].contains(&stripped_type);
                        
                        if !is_known_type && stripped_type.chars().next().map_or(false, |c| c.is_uppercase()) {
                            variant_classes_buffer.push_str(&format!("        # Import {} type at runtime\n", stripped_type));
                            variant_classes_buffer.push_str(&format!("        try:\n"));
                            variant_classes_buffer.push_str(&format!("            from {} import {}\n", stripped_type, stripped_type));
                            variant_classes_buffer.push_str(&format!("        except ImportError:\n"));
                            variant_classes_buffer.push_str(&format!("            pass  # Type not available, will use generic handling\n"));
                        }
                        
                        variant_classes_buffer.push_str(&format!("        {} = data.get('{}', None)\n", name, name));
                        
                        // Add special handling for nested types
                        if !is_known_type && stripped_type.chars().next().map_or(false, |c| c.is_uppercase()) {
                            variant_classes_buffer.push_str(&format!("        if isinstance({}, dict) and '{}' in locals():\n", name, stripped_type));
                            variant_classes_buffer.push_str(&format!("            {} = {}.fromDict({})\n", name, stripped_type, name));
                            variant_classes_buffer.push_str(&format!("        elif isinstance({}, str) and '{}' in locals() and hasattr({}, '__contains__'):\n", name, stripped_type, stripped_type));
                            variant_classes_buffer.push_str(&format!("            try:\n"));
                            variant_classes_buffer.push_str(&format!("                {} = {}[{}]\n", name, stripped_type, name));
                            variant_classes_buffer.push_str(&format!("            except (KeyError, ValueError):\n"));
                            variant_classes_buffer.push_str(&format!("                pass  # Leave as string if not a valid enum value\n"));
                        }
                    }
                    
                    // Filter out method definitions from the generated code
                    variant_classes_buffer.push_str("        # Filter out method definitions and only pass actual field values\n");
                    variant_classes_buffer.push_str("        return cls(");
                    
                    for (i, name) in valid_field_names.iter().enumerate() {
                        if i > 0 {
                            variant_classes_buffer.push_str(", ");
                        }
                        variant_classes_buffer.push_str(name);
                    }
                    
                    variant_classes_buffer.push_str(")\n\n");
                } else {
                    // For empty variants or variants with only methods
                    variant_classes_buffer.push_str("        return cls()\n\n");
                }
            }
        }
        
        // 2. Now generate the main enum class
        // Add the variant class definitions first
        buffer.push_str("# Classes for complex enum variants\n");
        buffer.push_str(&variant_classes_buffer);
        
        // Add the main enum class
        buffer.push_str(&format!("# The main {} class\n", enum_name));
        buffer.push_str(&format!("class {}(Enum):\n", enum_name));
        
        // Add variant declarations
        for variant_name in &variant_names {
            // Determine if this is a simple or complex variant
            let is_complex = variant_classes.iter().any(|vc| vc.contains(&format!("{}_{}", enum_name, variant_name)));
            
            if is_complex {
                buffer.push_str(&format!("    {} = {}_{}\n", variant_name, enum_name, variant_name));
            } else {
                buffer.push_str(&format!("    {} = auto()\n", variant_name));
            }
        }
        
        buffer.push_str("\n");
        
        // Add toJSON method
        buffer.push_str("    def toJSON(self) -> str:\n");
        buffer.push_str("        \"\"\"Serialize this object to a JSON string\"\"\"\n");
        buffer.push_str("        return json.dumps(self._serialize())\n\n");
        
        // Add _serialize method
        buffer.push_str("    def _serialize(self):\n");
        buffer.push_str("        \"\"\"Convert this object to a serializable dictionary\"\"\"\n");
        buffer.push_str("        # Complex enum serialization - the self is the Enum instance\n");
        buffer.push_str("        if isinstance(self.value, (int, str, bool, float)):\n");
        buffer.push_str("            return {\"type\": self.name}\n");
        buffer.push_str("        \n");
        buffer.push_str("        # If the value is a variant class, serialize it and add the type tag\n");
        buffer.push_str("        if hasattr(self.value, '__dict__'):\n");
        buffer.push_str("            # Start with the variant name\n");
        buffer.push_str("            result = {\"type\": self.name}\n");
        buffer.push_str("            \n");
        buffer.push_str("            # Add all fields from the variant value\n");
        buffer.push_str("            for key, value in self.value.__dict__.items():\n");
        buffer.push_str("                # Skip private fields\n");
        buffer.push_str("                if key.startswith('_'):\n");
        buffer.push_str("                    continue\n");
        buffer.push_str("                    \n");
        buffer.push_str("                # Recursively serialize any nested objects\n");
        buffer.push_str("                if hasattr(value, '_serialize'):\n");
        buffer.push_str("                    result[key] = value._serialize()\n");
        buffer.push_str("                elif isinstance(value, list):\n");
        buffer.push_str("                    result[key] = [item._serialize() if hasattr(item, '_serialize') else item for item in value]\n");
        buffer.push_str("                elif isinstance(value, dict):\n");
        buffer.push_str("                    result[key] = {k: v._serialize() if hasattr(v, '_serialize') else v for k, v in value.items()}\n");
        buffer.push_str("                elif isinstance(value, Enum):\n");
        buffer.push_str("                    result[key] = value.name\n");
        buffer.push_str("                else:\n");
        buffer.push_str("                    result[key] = value\n");
        buffer.push_str("            return result\n");
        buffer.push_str("        \n");
        buffer.push_str("        # If it's a simple enum instance, just return the name\n");
        buffer.push_str("        return {\"type\": self.name}\n\n");
        
        // Add fromJSON method
        buffer.push_str("    @classmethod\n");
        buffer.push_str("    def fromJSON(cls, json_str):\n");
        buffer.push_str("        \"\"\"Deserialize JSON string to a new instance\"\"\"\n");
        buffer.push_str("        data = json.loads(json_str)\n");
        buffer.push_str("        return cls.fromDict(data)\n\n");
        
        // Add fromDict method
        buffer.push_str("    @classmethod\n");
        buffer.push_str("    def fromDict(cls, data):\n");
        buffer.push_str("        \"\"\"Create a complex enum instance from a dictionary\"\"\"\n");
        buffer.push_str("        if isinstance(data, dict):\n");
        buffer.push_str("            # Complex enum with fields\n");
        buffer.push_str("            if \"type\" in data:\n");
        buffer.push_str("                variant_name = data[\"type\"]\n");
        buffer.push_str("                # Find the enum variant by name\n");
        buffer.push_str("                try:\n");
        buffer.push_str("                    variant = cls[variant_name]\n");
        buffer.push_str("                    \n");
        buffer.push_str("                    # If the variant value is a class, get a new instance\n");
        buffer.push_str("                    if hasattr(variant.value, 'fromDict'):\n");
        buffer.push_str("                        # Create data object from the dictionary (excluding the type field)\n");
        buffer.push_str("                        variant_data = {k: v for k, v in data.items() if k != \"type\"}\n");
        buffer.push_str("                        return variant.value.fromDict(variant_data)\n");
        buffer.push_str("                    \n");
        buffer.push_str("                    return variant\n");
        buffer.push_str("                except (KeyError, ValueError):\n");
        buffer.push_str("                    # Use the helper method if direct lookup fails\n");
        buffer.push_str("                    variant_data = {k: v for k, v in data.items() if k != \"type\"}\n");
        buffer.push_str("                    return cls.create_variant(variant_name, **variant_data)\n");
        buffer.push_str("        elif isinstance(data, str):\n");
        buffer.push_str("            # Simple enum name\n");
        buffer.push_str("            try:\n");
        buffer.push_str("                return cls[data]  # Get enum by name\n");
        buffer.push_str("            except (KeyError, ValueError):\n");
        buffer.push_str("                pass\n");
        buffer.push_str("        # Default fallback\n");
        buffer.push_str("        return next(iter(cls))\n\n");
        
        // Add the create_variant helper method
        buffer.push_str("    @classmethod\n");
        buffer.push_str("    def create_variant(cls, variant_name, **kwargs):\n");
        buffer.push_str("        \"\"\"Helper method to create a variant with associated data\"\"\"\n");
        buffer.push_str("        # Find the correct variant\n");
        buffer.push_str("        # Only process valid variant names that exist in the enum\n");
        buffer.push_str("        try:\n");
        buffer.push_str("            # First try direct lookup by name (most efficient)\n");
        buffer.push_str("            variant = cls[variant_name]\n");
        buffer.push_str("            \n");
        buffer.push_str("            # Special handling for specific variant types\n");

        // Then, for the variant handling code, filter the variants more strictly:
        for variant_name in &variant_names {
            // Skip variants that aren't valid Python identifiers or might be code fragments
            if !is_valid_python_identifier(variant_name) || 
               variant_name.contains(".") || 
               variant_name.contains("_serialize") || 
               variant_name.contains("toJSON") || 
               variant_name.contains("fromDict") || 
               variant_name.contains("variant") || 
               variant_name.contains("data") {
                continue;
            }
            
            buffer.push_str(&format!("            if variant.name == \"{}\":\n", variant_name));
            buffer.push_str(&format!("                try:\n"));
            buffer.push_str(&format!("                    return {}_{}.fromDict(kwargs)\n", enum_name, variant_name));
            buffer.push_str(&format!("                except Exception:\n"));
            buffer.push_str(&format!("                    return variant  # Fallback to simple variant\n"));
        }

        buffer.push_str("            # If we didn't find a specific handler, just return the variant\n");
        buffer.push_str("            return variant\n");
        buffer.push_str("        except (KeyError, ValueError):\n");
        buffer.push_str("            # If not found, return the first variant as a fallback\n");
        buffer.push_str("            return next(iter(cls))\n");
    }
    // For regular classes/dataclasses
    else {
        // Add __init__ method if the class has fields and no custom __init__ already detected
        // Filter out any method definitions
        let valid_fields: Vec<_> = fields.iter()
            .filter(|field| !field.starts_with("def "))
            .collect();

        if !valid_fields.is_empty() {
            let params = valid_fields.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", ");
            buffer.push_str("\n    def __init__(self, ");
            buffer.push_str(&params);
            buffer.push_str("):\n");
            
            // Add field assignments
            for field in &valid_fields {
                buffer.push_str(&format!("        self.{} = {}\n", field, field));
            }
            buffer.push_str("\n");
        }
        
        // Add toJSON method
        buffer.push_str("    def toJSON(self) -> str:\n");
        buffer.push_str("        \"\"\"Serialize this object to a JSON string\"\"\"\n");
        buffer.push_str("        return json.dumps(self._serialize())\n\n");
        
        // Add _serialize method
        buffer.push_str("    def _serialize(self):\n");
        buffer.push_str("        \"\"\"Convert this object to a serializable dictionary\"\"\"\n");
        buffer.push_str("        result = {}\n");
        buffer.push_str("        # Process all fields on this object\n");
        buffer.push_str("        for key, value in self.__dict__.items():\n");
        buffer.push_str("            # Skip private fields\n");
        buffer.push_str("            if key.startswith('_'):\n");
        buffer.push_str("                continue\n");
        buffer.push_str("            # Recursively serialize any nested objects\n");
        buffer.push_str("            if hasattr(value, '_serialize'):\n");
        buffer.push_str("                result[key] = value._serialize()\n");
        buffer.push_str("            elif isinstance(value, list):\n");
        buffer.push_str("                result[key] = [item._serialize() if hasattr(item, '_serialize') else item for item in value]\n");
        buffer.push_str("            elif isinstance(value, dict):\n");
        buffer.push_str("                result[key] = {k: v._serialize() if hasattr(v, '_serialize') else v for k, v in value.items()}\n");
        buffer.push_str("            elif hasattr(value, 'toJSON') and callable(getattr(value, 'toJSON')):\n");
        buffer.push_str("                result[key] = json.loads(value.toJSON())\n");
        buffer.push_str("            elif isinstance(value, Enum):\n");
        buffer.push_str("                result[key] = value.name\n");
        buffer.push_str("            else:\n");
        buffer.push_str("                result[key] = value\n");
        buffer.push_str("        return result\n\n");
        
        // Add fromJSON class method
        buffer.push_str("    @classmethod\n");
        buffer.push_str("    def fromJSON(cls, json_str):\n");
        buffer.push_str("        \"\"\"Deserialize JSON string to a new instance\"\"\"\n");
        buffer.push_str("        data = json.loads(json_str)\n");
        buffer.push_str("        return cls.fromDict(data)\n\n");
        
        // Add fromDict class method
        buffer.push_str("    @classmethod\n");
        buffer.push_str("    def fromDict(cls, data):\n");
        buffer.push_str("        \"\"\"Create an instance from a dictionary\"\"\"\n");
        
        // Filter out any method definitions
        let valid_fields: Vec<_> = fields.iter()
            .filter(|field| !field.starts_with("def "))
            .collect();

        if !valid_fields.is_empty() {
            // Generate parameter extraction code for fields
            for field in &valid_fields {
                buffer.push_str(&format!("        if '{}' in data:\n", field));
                buffer.push_str(&format!("            {} = data['{}']\n", field, field));
                buffer.push_str(&format!("            # Handle nested objects based on type\n"));
                buffer.push_str(&format!("            if isinstance({}, dict) and hasattr(cls, '_{}_type'):\n", field, field));
                buffer.push_str(&format!("                {} = getattr(cls, '_{}_type').fromDict({})\n", field, field, field));
                buffer.push_str(&format!("            elif isinstance({}, list) and hasattr(cls, '_item_type'):\n", field));
                buffer.push_str(&format!("                item_type = getattr(cls, '_item_type')\n"));
                buffer.push_str(&format!("                if hasattr(item_type, 'fromDict'):\n"));
                buffer.push_str(&format!("                    {} = [item_type.fromDict(item) if isinstance(item, dict) else item for item in {}]\n", field, field));
                buffer.push_str(&format!("        else:\n"));
                buffer.push_str(&format!("            {} = None\n", field));
            }
            
            // Create the instance with the processed fields
            buffer.push_str(&format!("        return cls({})\n", valid_fields.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", ")));
        } else {
            // Generic constructor for classes without fields
            buffer.push_str("        # Create instance with all attributes from the data dictionary\n");
            buffer.push_str("        instance = cls()\n");
            buffer.push_str("        for key, value in data.items():\n");
            buffer.push_str("            setattr(instance, key, value)\n");
            buffer.push_str("        return instance\n");
        }
    }
    
    // Ensure the directory exists
    if let Some(parent) = path.parent() {
        std::fs::create_dir_all(parent)?;
    }
    
    // Write the Python code to file
    let mut file = std::fs::File::create(&path)?;
    std::io::Write::write_all(&mut file, buffer.as_bytes())?;
    
    Ok(())
}


/// Export all Python types starting from a root type
fn export_all_into<T: Py + ?Sized + 'static>(
    out_dir: impl AsRef<Path>,
) -> Result<(), ExportError> {
    use std::collections::HashSet;
    
    // Track types we've already exported
    let mut seen = HashSet::new();
    export_recursive::<T>(&mut seen, out_dir)
}

/// Recursively export a type and its dependencies
fn export_recursive<T: Py + ?Sized + 'static>(
    seen: &mut std::collections::HashSet<TypeId>,
    out_dir: impl AsRef<Path>,
) -> Result<(), ExportError> {
    if !seen.insert(TypeId::of::<T>()) {
        return Ok(());
    }
    
    let out_dir = out_dir.as_ref();
    
    // First, export the current type
    let type_name = T::ident();
    let file_path = match T::output_path() {
        Some(path) => Some(out_dir.join(path)),
        None => {
            // Skip primitive types
            if T::name() == "int" || T::name() == "str" || T::name() == "bool" || T::name() == "float" {
                // Skip primitives, but continue with dependency traversal
                None
            } else {
                // Create a default path for this type
                let default_path = format!("{}.py", type_name);
                Some(out_dir.join(default_path))
            }
        }
    };
    
    if let Some(path) = file_path {
        export_to::<T, _>(path)?;
    }
    
    // Get all dependencies of this type after exporting the current type
    // This will include dependencies that were populated by the macro implementation
    let deps = <T as crate::Py>::dependencies();
    
    // Debug: Print the dependencies we found for this type
    println!("Dependencies for {}: {} dependencies found", type_name, deps.len());
    for dep in &deps {
        println!("  - Dependency: {} -> {}", dep.py_name, dep.output_path.display());
    }
    
    // Visit all dependencies and export them recursively
    struct Visit<'a> {
        seen: &'a mut std::collections::HashSet<TypeId>,
        out_dir: &'a Path,
        error: Option<ExportError>,
    }
    
    impl PyTypeVisitor for Visit<'_> {
        fn visit<U: Py + 'static + ?Sized>(&mut self) {
            // If an error occurred previously, return
            if self.error.is_some() {
                return;
            }
            
            // Always recurse into dependencies, even if they don't have #[py(export)] attribute
            // This ensures all types in the dependency chain get exported
            self.error = export_recursive::<U>(self.seen, self.out_dir).err();
        }
    }
    
    let mut visitor = Visit {
        seen,
        out_dir,
        error: None,
    };
    
    <T as crate::Py>::visit_dependencies(&mut visitor);
    
    if let Some(e) = visitor.error {
        Err(e)
    } else {
        Ok(())
    }
}

/// Generate Python code for a type as a string
fn export_to_string<T: Py + ?Sized + 'static>() -> Result<String, ExportError> {
    Ok(T::decl_concrete())
}

// Basic implementations for primitive types
macro_rules! impl_py_primitives {
    ($($($ty:ty),* => $l:literal),*) => { $($(
        impl Py for $ty {
            type WithoutGenerics = Self;
            type OptionInnerType = Self;
            fn name() -> String { $l.to_owned() }
            fn inline() -> String { <Self as $crate::Py>::name() }
            fn inline_flattened() -> String { panic!("{} cannot be flattened", <Self as $crate::Py>::name()) }
            fn decl() -> String { panic!("{} cannot be declared", <Self as $crate::Py>::name()) }
            fn decl_concrete() -> String { panic!("{} cannot be declared", <Self as $crate::Py>::name()) }
        }
    )*)* };
}

// Add implementations for Uuid and NaiveDateTime
#[cfg(feature = "chrono")]
impl Py for chrono::NaiveDateTime {
    type WithoutGenerics = Self;
    type OptionInnerType = Self;
    fn name() -> String { "NaiveDateTime".to_owned() }
    fn inline() -> String { "NaiveDateTime".to_owned() }
    fn inline_flattened() -> String { panic!("{} cannot be flattened", "NaiveDateTime".to_owned()) }
    fn decl() -> String { panic!("{} cannot be declared", "NaiveDateTime".to_owned()) }
    fn decl_concrete() -> String { panic!("{} cannot be declared", "NaiveDateTime".to_owned()) }
}

#[cfg(feature = "uuid")]
impl Py for uuid::Uuid {
    type WithoutGenerics = Self;
    type OptionInnerType = Self;
    fn name() -> String { "Uuid".to_owned() }
    fn inline() -> String { "Uuid".to_owned() }
    fn inline_flattened() -> String { "Uuid".to_owned() }
    fn decl() -> String { "import json\n\nclass Uuid:\n    def __init__(self, value: str = \"\"):\n        self.value = value\n\n    def __str__(self) -> str:\n        return self.value\n        \n    def toJSON(self) -> str:\n        return json.dumps(str(self))\n        \n    @classmethod\n    def fromJSON(cls, json_str):\n        \"\"\"Deserialize JSON string to a Uuid instance\"\"\"\n        data = json.loads(json_str)\n        return cls(data)\n        \n    @classmethod\n    def fromDict(cls, data):\n        \"\"\"Create a Uuid from a string\"\"\"\n        if isinstance(data, str):\n            return cls(data)\n        return cls(str(data))".to_owned() }
    fn decl_concrete() -> String { <Self as Py>::decl() }
}

// Implementation for HashMap
impl<K: Py, V: Py> Py for std::collections::HashMap<K, V> {
    type WithoutGenerics = std::collections::HashMap<crate::Dummy, crate::Dummy>;
    type OptionInnerType = Self;

    fn ident() -> String {
        "Dict".to_owned()
    }

    fn name() -> String {
        format!("Dict[{}, {}]", <K as crate::Py>::name(), <V as crate::Py>::name())
    }

    fn inline() -> String {
        format!("Dict[{}, {}]", <K as crate::Py>::inline(), <V as crate::Py>::inline())
    }

    fn visit_dependencies(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        <K as crate::Py>::visit_dependencies(v);
        <V as crate::Py>::visit_dependencies(v);
    }

    fn visit_generics(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        <K as crate::Py>::visit_generics(v);
        <V as crate::Py>::visit_generics(v);
        v.visit::<K>();
        v.visit::<V>();
    }

    fn decl() -> String {
        panic!("{} cannot be declared", <Self as crate::Py>::name())
    }

    fn decl_concrete() -> String {
        panic!("{} cannot be declared", <Self as crate::Py>::name())
    }

    fn inline_flattened() -> String {
        panic!("{} cannot be flattened", <Self as crate::Py>::name())
    }
}

// Implement for primitive types
impl_py_primitives! {
    u8, i8, u16, i16, u32, i32, usize, isize, f32, f64 => "int",
    u64, i64, u128, i128 => "int",
    bool => "bool",
    char, String, str => "str",
    () => "None"
}

// Implementation for Option<T>
impl<T: Py> Py for Option<T> {
    type WithoutGenerics = Self;
    type OptionInnerType = T;
    const IS_OPTION: bool = true;

    fn name() -> String {
        format!("Optional[{}]", <T as crate::Py>::name())
    }

    fn inline() -> String {
        format!("Optional[{}]", <T as crate::Py>::inline())
    }

    fn visit_dependencies(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        <T as crate::Py>::visit_dependencies(v);
    }

    fn visit_generics(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        <T as crate::Py>::visit_generics(v);
        v.visit::<T>();
    }

    fn decl() -> String {
        panic!("{} cannot be declared", <Self as crate::Py>::name())
    }

    fn decl_concrete() -> String {
        panic!("{} cannot be declared", <Self as crate::Py>::name())
    }

    fn inline_flattened() -> String {
        panic!("{} cannot be flattened", <Self as crate::Py>::name())
    }
}

// Add implementation for Dummy
impl Py for crate::Dummy {
    type WithoutGenerics = Self;
    type OptionInnerType = Self;
    
    fn name() -> String {
        "Dummy".to_owned()
    }
    
    fn decl() -> String {
        panic!("{} cannot be declared", <Self as crate::Py>::name())
    }
    
    fn decl_concrete() -> String {
        panic!("{} cannot be declared", <Self as crate::Py>::name())
    }
    
    fn inline() -> String {
        panic!("{} cannot be inlined", <Self as crate::Py>::name())
    }
    
    fn inline_flattened() -> String {
        panic!("{} cannot be flattened", <Self as crate::Py>::name())
    }
}

// Implementation for Vec<T>
impl<T: Py> Py for Vec<T> {
    type WithoutGenerics = Vec<crate::Dummy>;
    type OptionInnerType = Self;

    fn ident() -> String {
        "List".to_owned()
    }

    fn name() -> String {
        format!("List[{}]", <T as crate::Py>::name())
    }

    fn inline() -> String {
        format!("List[{}]", <T as crate::Py>::inline())
    }

    fn visit_dependencies(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        <T as crate::Py>::visit_dependencies(v);
    }

    fn visit_generics(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        <T as crate::Py>::visit_generics(v);
        v.visit::<T>();
    }

    fn decl() -> String {
        panic!("{} cannot be declared", <Self as crate::Py>::name())
    }

    fn decl_concrete() -> String {
        panic!("{} cannot be declared", <Self as crate::Py>::name())
    }

    fn inline_flattened() -> String {
        panic!("{} cannot be flattened", <Self as crate::Py>::name())
    }
}

// Add helper function to detect Python code fragments
fn is_python_fragment(s: &str) -> bool {
    // Check for common Python syntax patterns or keywords that are not valid field names
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

// Add helper function to detect Python reserved keywords
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

// Add a new function to check if a string is a valid Python identifier
fn is_valid_python_identifier(s: &str) -> bool {
    if s.is_empty() {
        return false;
    }
    
    let first_char = s.chars().next().unwrap();
    if !first_char.is_alphabetic() && first_char != '_' {
        return false;
    }
    
    // Check if all other characters are alphanumeric or underscore
    s.chars().all(|c| c.is_alphanumeric() || c == '_') && 
    // Make sure it's not a Python keyword
    !is_python_keyword(s) && 
    // Make sure it doesn't contain code fragments
    !is_python_fragment(s)
}

// Find where field declarations are processed in variant class definitions
// This is likely when building the cleaned_decl from the original declaration
// Create a helper function to clean up excessive newlines in field declarations

// Add this function to normalize field spacing
fn normalize_field_spacing(content: &str) -> String {
    let mut result = String::new();
    let mut last_was_field = false;
    let mut consecutive_newlines = 0;
    
    for line in content.lines() {
        let is_field_decl = line.trim().contains(':') && 
                           !line.trim().starts_with("class") && 
                           !line.trim().starts_with("def ") && 
                           !line.trim().starts_with('#');
        
        if line.trim().is_empty() {
            consecutive_newlines += 1;
            // Only add a newline if we don't already have too many consecutive ones
            if consecutive_newlines <= 1 || !last_was_field {
                result.push_str(line);
                result.push('\n');
            }
        } else {
            consecutive_newlines = 0;
            result.push_str(line);
            result.push('\n');
            last_was_field = is_field_decl;
        }
    }
    
    result
}

// Then use this function when processing the class definition
// Find the place where we create the class definition string
// And wrap it with the normalize_field_spacing function

// Modify this line:
// let cleaned_decl = cleaned_lines.join("\n");
// to:
