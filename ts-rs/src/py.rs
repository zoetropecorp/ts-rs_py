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

    /// Declaration of this type, e.g. `User` or `List[User]`.
    /// This should typically return the same as `name()`.
    fn decl() -> String;

    /// Declaration of this type using concrete types for generics.
    /// This should typically return the same as `name()`.
    fn decl_concrete() -> String;
    
    /// The full Python definition for this type (e.g., the class or enum block).
    fn definition() -> String;

    /// Name of this type in Python, including generic parameters
    fn name() -> String;

    /// Formats this type's name for use inline (e.g., as a type hint).
    /// Should typically return the same as `name()`.
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
    fn output_path() -> Option<&'static Path> {
        None
    }

    /// Returns the full default output path including the base directory.
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
    // let decl = T::decl_concrete(); // OLD: This now returns just the name
    let definition = T::definition(); // NEW: Use the full definition
    
    // Insert the definition on the line *before* `let mut imports = ...`
    let target_class_name = T::ident(); // Get the name of the class being exported
    
    // Create a set of imports that are actually needed based on the declaration
    let mut imports = std::collections::HashSet::new();
    
    // We'll collect typing imports separately to combine them
    let mut typing_imports = Vec::new();
    
    // Standard imports based on what's actually used in the definition
    if definition.contains("Optional[") {
        typing_imports.push("Optional");
    }
    if definition.contains("List[") {
        typing_imports.push("List");
    }
    if definition.contains("Dict[") {
        typing_imports.push("Dict");
    }
    if definition.contains("Union[") {
        typing_imports.push("Union");
    }
    if definition.contains("Any") {
        typing_imports.push("Any");
    }
    if definition.contains("TypeVar") { // Added TypeVar check
        typing_imports.push("TypeVar");
    }
    if definition.contains("Type") { // Added Type check
        typing_imports.push("Type");
    }
    if definition.contains("cast") { // Added cast check
        typing_imports.push("cast");
    }
    
    // Combine all typing imports into one line
    if !typing_imports.is_empty() {
        typing_imports.sort(); // Sort for consistent output
        imports.insert(format!("from typing import {}", typing_imports.join(", ")));
    }
    
    // Add enum imports if needed
    if definition.contains("class") && (definition.contains("(Enum)") || definition.contains("variant instance with fields")) {
        imports.insert("from enum import Enum, auto".to_string());
    }
    
    // Add dataclass imports if needed
    if definition.contains("@dataclass") {
        imports.insert("from dataclasses import *".to_string());
    }

    
    // Add imports for other dependencies
    // Manually scan the definition to find types that need to be imported
    let mut seen_types = std::collections::HashSet::new();
    
    // External types
    if definition.contains("Uuid") {
        imports.insert("from uuid import UUID as Uuid".to_string());
        seen_types.insert("Uuid".to_string()); 
    }
    if definition.contains("NaiveDateTime") {
        imports.insert("from datetime import datetime as NaiveDateTime".to_string());
        seen_types.insert("NaiveDateTime".to_string());
    }
    
    imports.insert("import sys".to_string());
    imports.insert("from pathlib import Path".to_string());
    
    // Scan the entire definition text to find custom type references
    let standard_types = ["int", "str", "bool", "float", "None", "List", "Dict", "Optional", 
                         "Union", "Any", "Enum", "auto", "dataclass", "Type", "TypeVar", "TypedDict",
                         "Generic", "TYPE_CHECKING", "Self", "Path", "Path(", "cast"]; // Added cast
    
    for line in definition.lines() { // Use definition here
        let line = line.trim();
        
        // Skip comments and method definitions (for import scanning)
        if line.starts_with("#") || line.starts_with("def ") || line.starts_with("@classmethod") { // Skip methods too
            continue;
        }
        
        // Process class inheritance (class Child(Parent):)
        if line.starts_with("class ") {
             if let Some(open_paren) = line.find('(') {
                 if let Some(close_paren) = line.find(')') {
                     let parent_part = &line[open_paren + 1..close_paren];
                     for parent in parent_part.split(',') {
                         let parent_name = parent.trim();
                         if !parent_name.is_empty() && parent_name.chars().next().unwrap().is_uppercase() {
                             let parent_string = parent_name.to_string();
                             if !seen_types.contains(&parent_string) && !standard_types.contains(&parent_name) &&
                                parent_string != target_class_name
                             {
                                 seen_types.insert(parent_string.clone());
                                 imports.insert(format!("from {} import {}", parent_string, parent_string));
                             }
                         }
                     }
                 }
             }
        }

            // Handle variant references like "B = ComplexEnum_B"
        if line.contains("=") && (line.contains("_") || line.contains("Complex")) { 
            if let Some(pos) = line.find('=') {
                let value_part = line[pos+1..].trim();
                let type_name = value_part.split_whitespace().next().unwrap_or("");
                
                if !type_name.is_empty() && type_name.chars().next().unwrap().is_uppercase() 
                   && !type_name.contains('(') && !type_name.contains('{') && !type_name.contains('[') {
                    let type_string = type_name.to_string();
                    if !seen_types.contains(&type_string) && !standard_types.contains(&type_name) &&
                       type_string != target_class_name && 
                       !type_string.starts_with(&format!("{}_", target_class_name))
                    {
                        seen_types.insert(type_string.clone());
                        imports.insert(format!("from {} import {}", type_string, type_string));
                    }
                }
            }
        }
        
        // Look for type annotations in field declarations ( field: Type )
        if let Some(colon_pos) = line.find(": ") {
            let field_name_part = &line[..colon_pos].trim();
            // Ensure it's a field line, not something else
            if field_name_part.is_empty() || field_name_part.contains(' ') || field_name_part.contains('(') {
                 continue;
            }

            let type_part = &line[colon_pos + 2..];
            let end_pos = type_part.find(|c| c == '=' || c == '#').unwrap_or_else(|| type_part.len());
            let type_annotation = type_part[..end_pos].trim();
            
            // Extract all potential class names from the annotation (handles List[User], Dict[str, Role], Optional[...], etc.)
            for part in type_annotation.split(|c: char| !c.is_alphanumeric() && c != '_') { // Include underscore
                    if !part.is_empty() && part.chars().next().unwrap().is_uppercase() {
                        let part_string = part.to_string();
                        if !seen_types.contains(&part_string) && !standard_types.contains(&part) &&
                           part_string != target_class_name &&
                        !part_string.starts_with(&format!("{}_", target_class_name))
                        {
                            seen_types.insert(part_string.clone());
                            imports.insert(format!("from {} import {}", part_string, part_string));
                        }
                    }
                }
            }
        }
        
    // Scan again for variant classes like EnumName_VariantName
    for word in definition.split(|c: char| !c.is_alphanumeric() && c != '_') { // Use definition
        if word.contains('_') {
            let parts: Vec<&str> = word.splitn(2, '_').collect();
            if parts.len() == 2 {
                let prefix = parts[0];
                if !prefix.is_empty() && prefix.chars().next().unwrap().is_uppercase() &&
                   !standard_types.contains(&prefix) && !seen_types.contains(prefix) &&
                   prefix == target_class_name // Check if prefix matches the main class being exported
                {
                    // This looks like a variant class (e.g., MyEnum_VariantA) defined *within* the current definition.
                    // We don't need to import the Enum itself if we are defining its variant.
                }
                // Check if prefix is *another* enum/class that needs importing
                else if !prefix.is_empty() && prefix.chars().next().unwrap().is_uppercase() &&
                   !standard_types.contains(&prefix) && !seen_types.contains(prefix) &&
                   prefix != target_class_name
                {
                        seen_types.insert(prefix.to_string());
                        imports.insert(format!("from {} import {}", prefix, prefix));
                }
            }
        }
    }
    
    // --- Assemble the final file content --- 
    buffer.clear(); // Start fresh
    
    // 1. __future__ imports
    buffer.push_str("from __future__ import annotations\n\n");
    
    // 2. Standard library imports (ensure necessary ones are present)
    if definition.contains("json.") { buffer.push_str("import json\n"); }
    buffer.push_str("import sys\n");
    if definition.contains("Path(") { buffer.push_str("from pathlib import Path\n"); }
    if definition.contains("(Enum)") || definition.contains("auto()") { buffer.push_str("from enum import Enum, auto\n"); }
    if definition.contains("@dataclass") { buffer.push_str("from dataclasses import *\n"); }
    
    // Add combined typing import if needed
    if !typing_imports.is_empty() {
        typing_imports.sort();
        buffer.push_str(&format!("from typing import {}\n", typing_imports.join(", ")));
    }
    buffer.push_str("from typing import TYPE_CHECKING\n"); // Always add TYPE_CHECKING
    buffer.push_str("\n");
    
    // 3. Path handling logic (optional, could be removed if imports handle it)
    // Check if definition itself includes path logic, if not, add it.
    if !definition.contains("_current_file = Path(__file__)") { 
    buffer.push_str("# Add current directory to Python path to facilitate imports\n");
    buffer.push_str("_current_file = Path(__file__).resolve()\n");
    buffer.push_str("_current_dir = _current_file.parent\n");
    buffer.push_str("if str(_current_dir) not in sys.path:\n");
    buffer.push_str("    sys.path.append(str(_current_dir))\n\n");
    }
    
    // 4. TYPE_CHECKING block for custom imports
    buffer.push_str("# Forward references for type checking only\n");
    buffer.push_str("if TYPE_CHECKING:\n");
    let mut custom_imports = Vec::new();
    for import in &imports {
        // Filter out stdlib/typing imports already handled
        if !(import.starts_with("from typing import") ||
             import.starts_with("from enum import") ||
             import.starts_with("from dataclasses import") ||
             import.starts_with("from pathlib import") ||
             import.starts_with("from uuid import") || // Handled externally
             import.starts_with("from datetime import") || // Handled externally
             import == "import json" ||
             import == "import sys")
        {
             // Basic check for malformed imports from Path objects
             if !import.contains("Path(") {
                 custom_imports.push(format!("    {}", import));
             }
        }
    }
    
    if !custom_imports.is_empty() {
        custom_imports.sort();
        buffer.push_str(&custom_imports.join("\n"));
    buffer.push_str("\n");
            } else {
        buffer.push_str("    pass\n");
    }
        buffer.push_str("\n");
        
    // 5. Add the actual definition code 
    // We trust the definition from T::definition() is mostly complete.
    // Remove any duplicate boilerplate imports that might be in the definition string.
    let mut final_definition_lines = Vec::new();
    for line in definition.lines() { // Use definition
        let trimmed_line = line.trim();
        // Remove redundant imports/setup already added to the buffer
        if !(trimmed_line.starts_with("from __future__ import") ||
             trimmed_line.starts_with("from typing import") || 
             trimmed_line.starts_with("from enum import") || 
             trimmed_line.starts_with("import json") ||
             trimmed_line.starts_with("import sys") ||
             trimmed_line.starts_with("from pathlib import") ||
             trimmed_line.starts_with("from dataclasses import") ||
             trimmed_line.contains("_current_file = Path") || // Basic check for path setup
             trimmed_line.starts_with("if TYPE_CHECKING:") ||
             trimmed_line.starts_with("# Forward references") ||
             trimmed_line.starts_with("# Add current directory"))
        {
            final_definition_lines.push(line);
        }
    }
    // Add a newline before the definition if the buffer doesn't end with one
    if !buffer.ends_with("\n\n") {
         if !buffer.ends_with("\n") { buffer.push('\n'); }
         buffer.push('\n');
    }
    buffer.push_str(&final_definition_lines.join("\n"));
    
    // Ensure the directory exists
    if let Some(dir) = path.parent() {
        std::fs::create_dir_all(dir)?;
    }

    // Write the final buffer to the file
    std::fs::write(&path, buffer)?;
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
    seen: &mut std::collections::HashSet<TypeId>, // Use `seen` again
    out_dir: impl AsRef<Path>,                // Use `impl AsRef<Path>` again
) -> Result<(), ExportError> {
    let type_id = TypeId::of::<T>();

    // *** ADD CHECK FOR STANDARD TYPES HERE ***
    let type_ident = T::ident();
    // Add explicit type annotation for the HashSet
    let standard_types: std::collections::HashSet<&str> = [
        "Any", "Optional", "List", "Dict", "Union", // Typing module
        "int", "float", "bool", "str", "bytes", "None", // Python built-ins
        "Path", // From pathlib
        "Uuid", "NaiveDateTime", // Handled primitives
        "Dummy", // Internal dummy type
    ].iter().cloned().collect();

    if standard_types.contains(type_ident.as_str()) {
        // Don't try to export built-in or standard types
        return Ok(());
    }
    // *** END CHECK ***

    // Use `seen` here
    if !seen.insert(type_id) {
        // Already visited or currently visiting (cycle detected)
        return Ok(());
    }
    
    let out_dir = out_dir.as_ref(); // Ensure we have a &Path inside the function
    
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

// ------------- Primitives ------------- 
// Generic implementation for primitives
macro_rules! impl_py_primitive { 
    ($($ty:ty => $py:expr),* $(,)?) => {
        $(impl Py for $ty {
            type WithoutGenerics = Self;
            type OptionInnerType = Self;
            fn name() -> String { $py.to_owned() }
            fn inline() -> String { $py.to_owned() }
            fn inline_flattened() -> String { panic!("Primitive type {} cannot be flattened", Self::name()) }
            fn decl() -> String { panic!("Primitive type {} cannot be declared", Self::name()) }
            fn decl_concrete() -> String { panic!("Primitive type {} cannot be declared", Self::name()) }
            fn definition() -> String { panic!("Primitive type {} cannot provide a definition", Self::name()) }
        })*
    };
}

impl_py_primitive! {
    u8 => "int", i8 => "int", u16 => "int", i16 => "int", u32 => "int", i32 => "int", 
    usize => "int", isize => "int", 
    f32 => "float", f64 => "float", // Use float for f32/f64
    u64 => "int", i64 => "int", u128 => "int", i128 => "int",
    bool => "bool",
    char => "str", String => "str", str => "str",
}

// ------------- Dummy Type ------------- 
// Used as placeholder for generics
impl Py for crate::Dummy {
    type WithoutGenerics = Self;
    type OptionInnerType = Self;
    fn name() -> String { "Dummy".to_owned() }
    fn inline() -> String { "Dummy".to_owned() } 
    fn inline_flattened() -> String { panic!("Dummy type cannot be flattened") }
    fn decl() -> String { panic!("Dummy type cannot be declared") }
    fn decl_concrete() -> String { panic!("Dummy type cannot be declared") }
    fn definition() -> String { panic!("Dummy type cannot provide a definition") }
}

// ------------- chrono ------------- 
#[cfg(feature = "chrono-impl")]
mod chrono_impl {
    use chrono::{NaiveDate, NaiveDateTime, NaiveTime, DateTime, Utc};
    use crate::py::Py;
    use crate::py::PyTypeVisitor;
    
    // Macro to implement Py for chrono types that map directly
    macro_rules! impl_py_chrono { 
        ($ty:ty, $py_name:expr) => {
            impl Py for $ty {
                type WithoutGenerics = Self;
                type OptionInnerType = Self;
                fn name() -> String { $py_name.to_owned() }
                fn inline() -> String { $py_name.to_owned() }
                fn inline_flattened() -> String { panic!("{} cannot be flattened", $py_name) }
                fn decl() -> String { panic!("{} cannot be declared", $py_name) }
                fn decl_concrete() -> String { panic!("{} cannot be declared", $py_name) }
                fn definition() -> String { panic!("{} cannot provide a definition, use Python's {} directly", $py_name, $py_name) }
            }
        };
    }

    impl_py_chrono!(NaiveDateTime, "datetime");
    impl_py_chrono!(NaiveDate, "date");
    impl_py_chrono!(NaiveTime, "time");
    impl_py_chrono!(DateTime<Utc>, "datetime"); // Map to Python datetime
}

// ------------- uuid ------------- 
#[cfg(feature = "uuid-impl")]
mod uuid_impl {
    use uuid::Uuid;
    use crate::py::Py;
    
    impl Py for Uuid {
    type WithoutGenerics = Self;
    type OptionInnerType = Self;
    fn name() -> String { "Uuid".to_owned() }
    fn inline() -> String { "Uuid".to_owned() }
    fn inline_flattened() -> String { "Uuid".to_owned() }
        fn decl() -> String { 
            // Return the custom Python class definition for UUID
            r#"
import json
from uuid import UUID as _Uuid

# Wrapper to provide consistent JSON methods
class Uuid:
    def __init__(self, value: str | _Uuid = ""):
        if isinstance(value, _Uuid):
            self._uuid = value
        else:
            self._uuid = _Uuid(value)

    def __str__(self) -> str:
        return str(self._uuid)
        
    def toJSON(self) -> str:
        return json.dumps(str(self))
        
    @classmethod
    def fromJSON(cls, json_str):
        # Assumes json_str contains just the UUID string
        data = json.loads(json_str)
        return cls(data)
        
    @classmethod
    def fromDict(cls, data):
        # Handles string or existing Uuid object
        if isinstance(data, str):
            return cls(data)
        elif isinstance(data, _Uuid):
             return cls(data)
        elif isinstance(data, cls): # Handle case where it's already our Uuid type
             return data
        return cls(str(data)) # Fallback

    # Allow access to the underlying uuid object if needed
    @property
    def raw_uuid(self) -> _Uuid:
        return self._uuid
            "#.trim().to_owned() 
        }
    fn decl_concrete() -> String { <Self as Py>::decl() }
        fn definition() -> String { <Self as Py>::decl() }
    }
}

// ------------- Containers ------------- 

impl<K, V> Py for std::collections::HashMap<K, V>
where
    K: Py + 'static,
    V: Py + 'static,
{
    type WithoutGenerics = std::collections::HashMap<crate::Dummy, crate::Dummy>;
    type OptionInnerType = Self;

    fn ident() -> String {
        "Dict".to_owned()
    }
    fn name() -> String {
        format!("Dict[{}, {}]", K::name(), V::name())
    }
    fn inline() -> String {
        format!("Dict[{}, {}]", K::inline(), V::inline())
    }
    fn visit_dependencies(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        v.visit::<K>();
        v.visit::<V>();
    }
    fn visit_generics(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        K::visit_generics(v);
        V::visit_generics(v);
    }
    fn decl() -> String {
        format!("Dict[{}, {}]", K::decl(), V::decl())
    }
    fn decl_concrete() -> String {
        format!("Dict[{}, {}]", K::decl_concrete(), V::decl_concrete())
    }
    fn inline_flattened() -> String {
        panic!("HashMap cannot be flattened")
    }
    fn definition() -> String { panic!("HashMap cannot provide a definition, use Dict[...] directly") }
}

// Similar implementation for BTreeMap
impl<K, V> Py for std::collections::BTreeMap<K, V> 
where 
    K: Py + Ord + 'static, 
    V: Py + 'static 
{
    type WithoutGenerics = std::collections::BTreeMap<crate::Dummy, crate::Dummy>;
    type OptionInnerType = Self;

    fn ident() -> String { "Dict".to_owned() }
    fn name() -> String { format!("Dict[{}, {}]", K::name(), V::name()) }
    fn inline() -> String { format!("Dict[{}, {}]", K::inline(), V::inline()) }
    fn visit_dependencies(v: &mut impl PyTypeVisitor) where Self: 'static {
        v.visit::<K>();
        v.visit::<V>();
    }
    fn visit_generics(v: &mut impl PyTypeVisitor) where Self: 'static {
        K::visit_generics(v);
        V::visit_generics(v);
    }
    fn decl() -> String { format!("Dict[{}, {}]", K::decl(), V::decl()) }
    fn decl_concrete() -> String { format!("Dict[{}, {}]", K::decl_concrete(), V::decl_concrete()) }
    fn inline_flattened() -> String { panic!("BTreeMap cannot be flattened") }
    fn definition() -> String { panic!("BTreeMap cannot provide a definition, use Dict[...] directly") }
}

// Option<T>
impl<T: Py> Py for Option<T> {
    type WithoutGenerics = Self;
    type OptionInnerType = T;
    const IS_OPTION: bool = true;

    fn name() -> String {
        format!("Optional[{}]", T::name())
    }
    fn inline() -> String {
        format!("Optional[{}]", T::inline())
    }
    fn visit_dependencies(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        v.visit::<T>();
    }
    fn visit_generics(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        T::visit_generics(v);
    }
    fn decl() -> String {
        format!("Optional[{}]", T::decl())
    }
    fn decl_concrete() -> String {
        format!("Optional[{}]", T::decl_concrete())
    }
    fn inline_flattened() -> String {
        T::inline_flattened()
    }
    fn definition() -> String { panic!("Option cannot provide a definition, use Optional[...] directly") }
}

// () - None
impl Py for () {
    type WithoutGenerics = Self;
    type OptionInnerType = Self;
    
    fn name() -> String {
        "None".to_owned()
    }
    fn decl() -> String {
        "None".to_owned()
    }
    fn decl_concrete() -> String {
        "None".to_owned()
    }
    fn inline() -> String {
        "None".to_owned()
    }
    fn inline_flattened() -> String {
        panic!("() cannot be flattened")
    }
    fn definition() -> String { panic!("() cannot provide a definition, use None directly") }
}

// Vec<T>
impl<T: Py> Py for Vec<T> {
    type WithoutGenerics = Vec<crate::Dummy>;
    type OptionInnerType = Self;

    fn ident() -> String {
        "List".to_owned()
    }
    fn name() -> String {
        format!("List[{}]", T::name())
    }
    fn inline() -> String {
        format!("List[{}]", T::inline())
    }
    fn visit_dependencies(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        v.visit::<T>();
    }
    fn visit_generics(v: &mut impl PyTypeVisitor)
    where
        Self: 'static,
    {
        T::visit_generics(v);
    }
    fn decl() -> String {
        format!("List[{}]", T::decl())
    }
    fn decl_concrete() -> String {
        format!("List[{}]", T::decl_concrete())
    }
    fn inline_flattened() -> String {
        panic!("Vec cannot be flattened")
    }
    fn definition() -> String { panic!("Vec cannot provide a definition, use List[...] directly") }
}

// Generic impl for Tuples up to size 16
macro_rules! impl_py_tuple {
    ( $($ty:ident),* ) => {
        impl<$($ty: Py + 'static),*> Py for ($($ty,)*) {
            type WithoutGenerics = Self; // Assuming generics handled within components
            type OptionInnerType = Self;

            fn name() -> String {
                format!("Tuple[{}]", [$($ty::name()),*].join(", "))
            }
            fn inline() -> String {
                 format!("Tuple[{}]", [$($ty::inline()),*].join(", "))
            }
            fn decl() -> String {
                format!("Tuple[{}]", [$($ty::decl()),*].join(", "))
            }
            fn decl_concrete() -> String {
                format!("Tuple[{}]", [$($ty::decl_concrete()),*].join(", "))
            }
            fn visit_dependencies(v: &mut impl PyTypeVisitor) where Self: 'static {
                $(v.visit::<$ty>();)*
            }
            fn visit_generics(v: &mut impl PyTypeVisitor) where Self: 'static {
                 $($ty::visit_generics(v);)*
            }
            fn inline_flattened() -> String {
                panic!("Tuples cannot be flattened")
            }
            fn definition() -> String { panic!("Tuple cannot provide a definition, use Tuple[...] directly") }
        }
    };
}

// Implement for tuples of size 1 to 16
impl_py_tuple!(T1);
impl_py_tuple!(T1, T2);
// ... up to T16 ...
impl_py_tuple!(T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16);


// Generic impl for Arrays up to size 32
impl<T: Py + 'static, const N: usize> Py for [T; N] {
    type WithoutGenerics = [crate::Dummy; N]; 
    type OptionInnerType = Self;

    fn name() -> String {
        // Represent fixed-size arrays as Tuple[T, T, ..., T]
        let type_names = std::iter::repeat(T::name()).take(N).collect::<Vec<_>>();
        format!("Tuple[{}]", type_names.join(", "))
    }
    fn inline() -> String {
        let type_inlines = std::iter::repeat(T::inline()).take(N).collect::<Vec<_>>();
        format!("Tuple[{}]", type_inlines.join(", "))
    }
    fn decl() -> String {
        let type_decls = std::iter::repeat(T::decl()).take(N).collect::<Vec<_>>();
        format!("Tuple[{}]", type_decls.join(", "))
    }
    fn decl_concrete() -> String {
        let type_decls_concrete = std::iter::repeat(T::decl_concrete()).take(N).collect::<Vec<_>>();
        format!("Tuple[{}]", type_decls_concrete.join(", "))
    }
    fn visit_dependencies(v: &mut impl PyTypeVisitor) where Self: 'static {
        v.visit::<T>();
    }
    fn visit_generics(v: &mut impl PyTypeVisitor) where Self: 'static {
         T::visit_generics(v);
    }
    fn inline_flattened() -> String {
        panic!("Arrays cannot be flattened")
    }
     fn definition() -> String { panic!("Array cannot provide a definition, use Tuple[...] directly") }
}
