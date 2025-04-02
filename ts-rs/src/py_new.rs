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

// For Python code generation and formatting
use crate::py_generator;

/// Export a Python type to a file
fn export_to<T: Py + ?Sized + 'static, P: AsRef<Path>>(path: P) -> Result<(), ExportError> {
    use crate::py_generator::{PyFileGenerator, format_python_code};
    let path = path.as_ref().to_owned();
    
    // Get the type declaration
    let type_name = T::ident();
    let decl = T::decl_concrete();
    
    // Create a PyFileGenerator to handle the generation process
    let mut generator = PyFileGenerator::new(&type_name);
    
    // Parse the declaration to extract classes, fields, and dependencies
    generator.parse_declaration(&decl);
    
    // Generate the Python code
    let buffer = generator.generate();
    
    // Format the code and save it to file
    let formatted_code = format_python_code(&buffer);
    
    // Ensure the directory exists
    if let Some(parent) = path.parent() {
        std::fs::create_dir_all(parent)?;
    }
    
    // Write the formatted code to file
    let mut file = std::fs::File::create(&path)?;
    std::io::Write::write_all(&mut file, formatted_code.as_bytes())?;
    
    Ok(())
}

/// Represents a Python class with its fields and methods
struct PyClass {
    name: String,
    fields: Vec<(String, String)>, // (name, type)
    parent_class: Option<String>,
    is_enum: bool,
    is_dataclass: bool,
}

impl PyClass {
    fn new(name: String) -> Self {
        PyClass {
            name,
            fields: Vec::new(),
            parent_class: None,
            is_enum: false,
            is_dataclass: false,
        }
    }
    
    fn with_parent(mut self, parent: &str) -> Self {
        self.parent_class = Some(parent.to_string());
        if parent == "Enum" {
            self.is_enum = true;
        }
        self
    }
    
    fn set_dataclass(&mut self, is_dataclass: bool) {
        self.is_dataclass = is_dataclass;
    }
    
    fn add_field(&mut self, name: &str, type_str: &str) -> bool {
        // Filter invalid field names
        if is_python_keyword(name) || is_python_fragment(name) || 
           name.contains(".") || name.contains("(") || name.contains(")") {
            return false;
        }
        
        // Don't add duplicate fields
        if self.fields.iter().any(|(field_name, _)| field_name == name) {
            return false;
        }
        
        self.fields.push((name.to_string(), type_str.to_string()));
        true
    }
    
    /// Generate the Python code for this class
    fn generate_class(&self) -> String {
        let mut buffer = String::new();
        
        // Add dataclass decorator if needed
        if self.is_dataclass {
            buffer.push_str("@dataclass\n");
        }
        
        // Add class definition with parent class if any
        if let Some(parent) = &self.parent_class {
            buffer.push_str(&format!("class {}({}):\n", self.name, parent));
        } else {
            buffer.push_str(&format!("class {}:\n", self.name));
        }
        
        // Add fields with type annotations
        if self.fields.is_empty() {
            buffer.push_str("    pass\n");
        } else {
            for (name, type_str) in &self.fields {
                buffer.push_str(&format!("    {}: {}\n", name, type_str));
            }
        }
        
        // Add extra newline after class definition
        buffer.push('\n');
        
        buffer
    }
    
    /// Generate a complete dataclass with constructor and serialization methods
    fn generate_dataclass(&self) -> String {
        let mut buffer = String::new();
        
        // Add dataclass decorator
        buffer.push_str("@dataclass\n");
        
        // Add class definition
        buffer.push_str(&format!("class {}:\n", self.name));
        
        // Add fields with type annotations
        for (name, type_str) in &self.fields {
            buffer.push_str(&format!("    {}: {}\n", name, type_str));
        }
        
        // Add constructor
        buffer.push_str("\n    def __init__(self");
        for (name, _) in &self.fields {
            buffer.push_str(&format!(", {}", name));
        }
        buffer.push_str("):\n");
        
        for (name, _) in &self.fields {
            buffer.push_str(&format!("        self.{} = {}\n", name, name));
        }
        
        // Add toJSON method
        buffer.push_str("\n    def toJSON(self) -> str:\n");
        buffer.push_str("        \"\"\"Serialize this object to a JSON string\"\"\"\n");
        buffer.push_str("        return json.dumps(self._serialize())\n\n");
        
        // Add _serialize method
        buffer.push_str("    def _serialize(self):\n");
        buffer.push_str("        \"\"\"Convert this object to a serializable dictionary\"\"\"\n");
        buffer.push_str("        result = {}\n");
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
        buffer.push_str("            elif isinstance(value, Enum):\n");
        buffer.push_str("                result[key] = value.name\n");
        buffer.push_str("            else:\n");
        buffer.push_str("                result[key] = value\n");
        buffer.push_str("        return result\n\n");
        
        // Add fromDict method
        buffer.push_str("    @classmethod\n");
        buffer.push_str("    def fromDict(cls, data):\n");
        buffer.push_str("        \"\"\"Create an instance from a dictionary\"\"\"\n");
        
        // Extract field values from the dictionary
        for (name, type_str) in &self.fields {
            // Extract the base type from a complex type like List[Type]
            let base_type = if type_str.contains('[') {
                let end = type_str.find('[').unwrap_or(type_str.len());
                &type_str[..end]
            } else {
                type_str
            };
            
            // Special handling for custom types that might need conversion
            if ["Uuid", "Optional", "List", "Dict", "int", "str", "bool", "float"].contains(&base_type) {
                buffer.push_str(&format!("        {} = data.get('{}', None)\n", name, name));
            } else {
                // This might be a custom type that needs special handling
                buffer.push_str(&format!("        # Import {} type at runtime\n", base_type));
                buffer.push_str("        try:\n");
                buffer.push_str(&format!("            from {} import {}\n", base_type, base_type));
                buffer.push_str("        except ImportError:\n");
                buffer.push_str("            pass  # Type not available, will use generic handling\n");
                
                buffer.push_str(&format!("        {} = data.get('{}', None)\n", name, name));
                buffer.push_str(&format!("        if isinstance({}, dict) and '{}' in locals():\n", name, base_type));
                buffer.push_str(&format!("            {} = {}.fromDict({})\n", name, base_type, name));
                buffer.push_str(&format!("        elif isinstance({}, str) and '{}' in locals() and hasattr({}, '__contains__'):\n", name, base_type, base_type));
                buffer.push_str("            try:\n");
                buffer.push_str(&format!("                {} = {}[{}]\n", name, base_type, name));
                buffer.push_str("            except (KeyError, ValueError):\n");
                buffer.push_str("                pass  # Leave as string if not a valid enum value\n");
            }
        }
        
        // Create and return the instance
        buffer.push_str("        # Filter out method definitions and only pass actual field values\n");
        buffer.push_str("        return cls(");
        for (i, (name, _)) in self.fields.iter().enumerate() {
            if i > 0 {
                buffer.push_str(", ");
            }
            buffer.push_str(name);
        }
        buffer.push_str(")\n\n");
        
        buffer
    }
    
    /// Generate an enum class with variants and serialization methods
    fn generate_enum(&self, variant_classes: &[&PyClass]) -> String {
        let mut buffer = String::new();
        
        // Add class definition
        buffer.push_str(&format!("class {}(Enum):\n", self.name));
        
        // Find corresponding variant classes for complex variants
        let mut variants_with_classes = Vec::new();
        
        // Add enum variants
        for (name, type_str) in &self.fields {
            if type_str.is_empty() {
                // Simple variant with auto() value
                buffer.push_str(&format!("    {} = auto()\n", name));
            } else {
                // Complex variant with a class
                let variant_class_name = match type_str.split_whitespace().next() {
                    Some(name) => name,
                    None => continue
                };
                
                buffer.push_str(&format!("    {} = {}\n", name, variant_class_name));
                variants_with_classes.push((name.clone(), variant_class_name.to_string()));
            }
        }
        
        // Add toJSON method
        buffer.push_str("\n    def toJSON(self) -> str:\n");
        buffer.push_str("        \"\"\"Serialize this object to a JSON string\"\"\"\n");
        buffer.push_str("        return json.dumps(self._serialize())\n\n");
        
        // Add _serialize method
        buffer.push_str("    def _serialize(self):\n");
        buffer.push_str("        \"\"\"Convert this object to a serializable dictionary\"\"\"\n");
        
        // For complex enums, distinguish between simple and complex variants
        if !variants_with_classes.is_empty() {
            buffer.push_str("        # Complex enum serialization - the self is the Enum instance\n");
            buffer.push_str("        if isinstance(self.value, (int, str, bool, float)):\n");
            buffer.push_str("            return {\"type\": self.name}\n\n");
            buffer.push_str("        # If the value is a variant class, serialize it and add the type tag\n");
            buffer.push_str("        if hasattr(self.value, '__dict__'):\n");
            buffer.push_str("            # Start with the variant name\n");
            buffer.push_str("            result = {\"type\": self.name}\n\n");
            buffer.push_str("            # Add all fields from the variant value\n");
            buffer.push_str("            for key, value in self.value.__dict__.items():\n");
            buffer.push_str("                # Skip private fields\n");
            buffer.push_str("                if key.startswith('_'):\n");
            buffer.push_str("                    continue\n\n");
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
            buffer.push_str("            return result\n\n");
            buffer.push_str("        # If it's a simple enum instance, just return the name\n");
            buffer.push_str("        return {\"type\": self.name}\n\n");
        } else {
            // Simple enum serialization
            buffer.push_str("        return self.name\n\n");
        }
        
        // Add fromJSON method
        buffer.push_str("    @classmethod\n");
        buffer.push_str("    def fromJSON(cls, json_str):\n");
        buffer.push_str("        \"\"\"Deserialize JSON string to a new instance\"\"\"\n");
        buffer.push_str("        data = json.loads(json_str)\n");
        buffer.push_str("        return cls.fromDict(data)\n\n");
        
        // Add fromDict method for complex enums
        buffer.push_str("    @classmethod\n");
        buffer.push_str("    def fromDict(cls, data):\n");
        buffer.push_str("        \"\"\"Create an enum instance from a dictionary\"\"\"\n");
        
        if !variants_with_classes.is_empty() {
            // Complex enum deserialization
            buffer.push_str("        if isinstance(data, dict):\n");
            buffer.push_str("            # Complex enum with fields\n");
            buffer.push_str("            if \"type\" in data:\n");
            buffer.push_str("                variant_name = data[\"type\"]\n");
            buffer.push_str("                # Find the enum variant by name\n");
            buffer.push_str("                try:\n");
            buffer.push_str("                    variant = cls[variant_name]\n");
            buffer.push_str("                    \n");
            buffer.push_str("                    # If the variant value is a class, get a new instance\n");
            buffer.push_str("                    if hasattr(variant.value, 'fromDict') and callable(getattr(variant.value, 'fromDict')):\n");
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
            
            // Add create_variant helper method for complex enums
            buffer.push_str("    @classmethod\n");
            buffer.push_str("    def create_variant(cls, variant_name, **kwargs):\n");
            buffer.push_str("        \"\"\"Helper method to create a variant with associated data\"\"\"\n");
            buffer.push_str("        # Find the correct variant\n");
            buffer.push_str("        try:\n");
            buffer.push_str("            # First try direct lookup by name (most efficient)\n");
            buffer.push_str("            variant = cls[variant_name]\n");
            buffer.push_str("            \n");
            buffer.push_str("            # Special handling for specific variant types\n");
            
            // Add handler for each complex variant
            for (variant_name, class_name) in &variants_with_classes {
                buffer.push_str(&format!("            if variant.name == \"{}\":\n", variant_name));
                buffer.push_str(&format!("                try:\n"));
                buffer.push_str(&format!("                    return {}.fromDict(kwargs)\n", class_name));
                buffer.push_str(&format!("                except Exception:\n"));
                buffer.push_str(&format!("                    return variant  # Fallback to simple variant\n"));
            }
            
            buffer.push_str("            # If we didn't find a specific handler, just return the variant\n");
            buffer.push_str("            return variant\n");
            buffer.push_str("        except (KeyError, ValueError):\n");
            buffer.push_str("            # If not found, return the first variant as a fallback\n");
            buffer.push_str("            return next(iter(cls))\n");
        } else {
            // Simple enum deserialization
            buffer.push_str("        if isinstance(data, str):\n");
            buffer.push_str("            try:\n");
            buffer.push_str("                return cls[data]  # Get enum by name\n");
            buffer.push_str("            except (KeyError, ValueError):\n");
            buffer.push_str("                pass\n");
            buffer.push_str("        elif isinstance(data, int):\n");
            buffer.push_str("            # Get enum by value if it's an integer\n");
            buffer.push_str("            for enum_item in cls:\n");
            buffer.push_str("                if enum_item.value == data:\n");
            buffer.push_str("                    return enum_item\n");
            buffer.push_str("        # Default fallback - return first variant\n");
            buffer.push_str("        return next(iter(cls))\n");
        }
        
        buffer
    }
}

/// Structure to generate a complete Python file
struct PyFileGenerator {
    type_name: String,
    classes: Vec<PyClass>,
    imports: HashSet<String>,
    enum_variants: Vec<String>,
    type_checking_imports: Vec<String>,
}

impl PyFileGenerator {
    fn new(type_name: &str) -> Self {
        PyFileGenerator {
            type_name: type_name.to_string(),
            classes: Vec::new(),
            imports: HashSet::new(),
            enum_variants: Vec::new(),
            type_checking_imports: Vec::new(),
        }
    }
    
    /// Parse the declaration to extract classes, fields, and dependencies
    fn parse_declaration(&mut self, decl: &str) {
        // Split the declaration into lines
        let lines: Vec<&str> = decl.lines().collect();
        
        // Track the current class being processed
        let mut current_class: Option<PyClass> = None;
        
        // First pass: collect classes
        for line in &lines {
            let trimmed = line.trim();
            
            // Skip empty lines and comments
            if trimmed.is_empty() || trimmed.starts_with('#') {
                continue;
            }
            
            // Check for imports
            if trimmed.starts_with("from ") || trimmed.starts_with("import ") {
                // Process imports separately
                self.add_import(trimmed);
                continue;
            }
            
            // Check for dataclass decorator
            if trimmed == "@dataclass" {
                if let Some(class) = &mut current_class {
                    class.set_dataclass(true);
                }
                continue;
            }
            
            // Check for class definition
            if trimmed.starts_with("class ") {
                // If we're already processing a class, save it before starting a new one
                if let Some(finished_class) = current_class.take() {
                    self.classes.push(finished_class);
                }
                
                // Extract class name and parent
                if let Some(class_name) = extract_class_name(trimmed) {
                    let mut new_class = PyClass::new(class_name.clone());
                    
                    // Check for parent class (Enum, etc.)
                    if trimmed.contains('(') && trimmed.contains(')') {
                        let start = trimmed.find('(').unwrap() + 1;
                        let end = trimmed.find(')').unwrap_or(trimmed.len());
                        let parent = trimmed[start..end].trim();
                        
                        if !parent.is_empty() {
                            new_class = new_class.with_parent(parent);
                            
                            // Add required import for parent class
                            if parent == "Enum" {
                                self.imports.insert("from enum import Enum, auto".to_string());
                            }
                        }
                    }
                    
                    // Set the current class being processed
                    current_class = Some(new_class);
                }
                continue;
            }
            
            // Check for field declaration in a class
            if let Some(class) = &mut current_class {
                // Handle enum variant declarations
                if class.is_enum && trimmed.contains('=') {
                    // Parse enum variants (e.g., "VariantName = auto()")
                    let parts: Vec<&str> = trimmed.split('=').collect();
                    if parts.len() >= 2 {
                        let variant_name = parts[0].trim();
                        let variant_value = parts[1].trim();
                        
                        // Skip invalid variants
                        if is_python_keyword(variant_name) || is_python_fragment(variant_name) {
                            continue;
                        }
                        
                        // Store the enum variant with its type if it's a complex variant
                        class.add_field(variant_name, variant_value);
                        
                        // Keep track of valid enum variants
                        self.enum_variants.push(variant_name.to_string());
                    }
                    continue;
                }
                
                // Parse regular field declarations
                if trimmed.contains(':') && !trimmed.starts_with("def ") && !trimmed.contains("@") {
                    let parts: Vec<&str> = trimmed.split(':').collect();
                    if parts.len() >= 2 {
                        let field_name = parts[0].trim();
                        let field_type = parts[1].trim();
                        
                        // Skip invalid field names
                        if is_python_keyword(field_name) || is_python_fragment(field_name) {
                            continue;
                        }
                        
                        // Add the field to the current class
                        if class.add_field(field_name, field_type) {
                            // Process field type for imports
                            self.process_type_for_imports(field_type);
                        }
                    }
                }
            }
        }
        
        // Add the last class if any
        if let Some(class) = current_class {
            self.classes.push(class);
        }
        
        // Process variant classes for complex enums
        self.process_variant_classes();
    }
    
    /// Process special variant classes for complex enums
    fn process_variant_classes(&mut self) {
        // Find the main enum class
        let main_enum = self.classes.iter().find(|c| c.is_enum && c.name == self.type_name);
        
        if let Some(enum_class) = main_enum {
            // Make all variant classes into dataclasses
            for class in &mut self.classes {
                // Check if this is a variant class for the main enum
                if !class.is_enum && class.name.starts_with(&format!("{}_", self.type_name)) {
                    class.set_dataclass(true);
                    
                    // Add dataclass import
                    self.imports.insert("from dataclasses import dataclass".to_string());
                    
                    // Add to type checking imports
                    let class_name = class.name.clone();
                    self.type_checking_imports.push(format!("from {} import {}", class_name, class_name));
                }
            }
            
            // Also add the enum class itself to type checking imports
            self.type_checking_imports.push(format!("from {} import {}", self.type_name, self.type_name));
        }
    }
    
    /// Add an import statement to the imports set
    fn add_import(&mut self, import_stmt: &str) {
        // Skip certain imports we'll add ourselves
        if import_stmt.contains("__future__") || 
           import_stmt.contains("dataclasses import dataclass") ||
           import_stmt.contains("typing import") ||
           import_stmt.contains("enum import") ||
           import_stmt.contains("json") ||
           import_stmt.contains("sys") ||
           import_stmt.contains("Path") {
            return;
        }
        
        self.imports.insert(import_stmt.to_string());
    }
    
    /// Process a type string to identify and add necessary imports
    fn process_type_for_imports(&mut self, type_str: &str) {
        // Check for common container types
        if type_str.contains("Optional[") {
            self.imports.insert("from typing import Optional".to_string());
        }
        if type_str.contains("List[") {
            self.imports.insert("from typing import List".to_string());
        }
        if type_str.contains("Dict[") {
            self.imports.insert("from typing import Dict".to_string());
        }
        if type_str.contains("Union[") {
            self.imports.insert("from typing import Union".to_string());
        }
        if type_str.contains("Any") {
            self.imports.insert("from typing import Any".to_string());
        }
        
        // Extract potential custom types
        let mut inside_bracket = false;
        let mut current_word = String::new();
        
        for c in type_str.chars() {
            if c == '[' {
                inside_bracket = true;
                if !current_word.is_empty() {
                    // Check if this is a custom type that needs an import
                    self.add_potential_type_import(&current_word);
                    current_word.clear();
                }
            } else if c == ']' {
                inside_bracket = false;
                if !current_word.is_empty() {
                    // Check potential type inside brackets
                    self.add_potential_type_import(&current_word);
                    current_word.clear();
                }
            } else if c == ',' || c.is_whitespace() {
                if !current_word.is_empty() {
                    // Check potential type
                    self.add_potential_type_import(&current_word);
                    current_word.clear();
                }
            } else {
                current_word.push(c);
            }
        }
        
        // Check last word
        if !current_word.is_empty() {
            self.add_potential_type_import(&current_word);
        }
    }
    
    /// Add a potential custom type import
    fn add_potential_type_import(&mut self, type_name: &str) {
        // Skip basic types
        if ["int", "str", "bool", "float", "None", "List", "Dict", "Optional", 
            "Union", "Any", "Enum", "auto", "dataclass"].contains(&type_name) {
            return;
        }
        
        // If the type starts with uppercase, it might be a custom type
        if !type_name.is_empty() && type_name.chars().next().unwrap().is_uppercase() {
            // Special handling for certain types
            if type_name == "Uuid" {
                self.imports.insert("from uuid import UUID as Uuid".to_string());
            } else {
                // Add to the type checking imports
                self.type_checking_imports.push(format!("from {} import {}", type_name, type_name));
            }
        }
    }
    
    /// Generate the complete Python file
    fn generate(&self) -> String {
        let mut buffer = String::new();
        
        // 1. Add __future__ imports (MUST be first)
        buffer.push_str("from __future__ import annotations\n\n");
        
        // 2. Add standard imports
        buffer.push_str("import json\n");
        buffer.push_str("import sys\n");
        buffer.push_str("from pathlib import Path\n");
        buffer.push_str("from enum import Enum, auto\n");
        buffer.push_str("from typing import Any, Optional, List, Dict, Union, TYPE_CHECKING\n");
        buffer.push_str("from dataclasses import dataclass\n\n");
        
        // 3. Add path handling for imports
        buffer.push_str("# Add current directory to Python path to facilitate imports\n");
        buffer.push_str("_current_file = Path(__file__).resolve()\n");
        buffer.push_str("_current_dir = _current_file.parent\n");
        buffer.push_str("if str(_current_dir) not in sys.path:\n");
        buffer.push_str("    sys.path.append(str(_current_dir))\n\n");
        
        // 4. Add type checking imports
        buffer.push_str("# Forward references for type checking only\n");
        buffer.push_str("if TYPE_CHECKING:\n");
        
        if !self.type_checking_imports.is_empty() {
            // Sort imports for consistency
            let mut sorted_imports = self.type_checking_imports.clone();
            sorted_imports.sort();
            
            for import_stmt in sorted_imports {
                buffer.push_str(&format!("    {}\n", import_stmt));
            }
        } else {
            buffer.push_str("    pass  # No forward references needed\n");
        }
        buffer.push_str("\n");
        
        // 5. Find and generate variant classes first (for complex enums)
        let main_enum_class = self.classes.iter().find(|c| c.is_enum && c.name == self.type_name);
        
        if let Some(main_class) = main_enum_class {
            // Generate variant classes first
            let variant_classes: Vec<&PyClass> = self.classes.iter()
                .filter(|c| !c.is_enum && c.name.starts_with(&format!("{}_", self.type_name)))
                .collect();
            
            if !variant_classes.is_empty() {
                buffer.push_str("# Classes for complex enum variants\n");
                
                for variant_class in &variant_classes {
                    buffer.push_str(&variant_class.generate_dataclass());
                }
                
                // Main enum class with complex variants
                buffer.push_str(&format!("# The main {} class\n", self.type_name));
                buffer.push_str(&main_class.generate_enum(&variant_classes));
            } else {
                // Simple enum class
                buffer.push_str(&main_class.generate_enum(&[]));
            }
        } else {
            // Not an enum, process regular dataclasses
            for class in &self.classes {
                if class.is_dataclass {
                    buffer.push_str(&class.generate_dataclass());
                } else {
                    buffer.push_str(&class.generate_class());
                }
            }
        }
        
        buffer
    }
}

/// Format Python code using available formatters
fn format_python_code(code: &str) -> String {
    // Try to use formatters in order of preference
    use std::process::{Command, Stdio};
    use std::io::Write;

    // First, clean up the code to remove common issues
    let cleaned_code = clean_python_code(code);

    // Check if black is installed (preferred)
    let has_black = Command::new("sh")
        .arg("-c")
        .arg("which black")
        .output()
        .map(|output| output.status.success())
        .unwrap_or(false);
    
    // Try using black formatter first
    if has_black {
        let mut child = match Command::new("black")
            .arg("-")  // Read from stdin
            .arg("--quiet")
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .spawn() {
                Ok(child) => child,
                Err(e) => {
                    println!("Warning: Failed to run black formatter: {}", e);
                    return cleaned_code;
                }
            };
        
        // Write code to stdin
        if let Some(mut stdin) = child.stdin.take() {
            if let Err(e) = stdin.write_all(cleaned_code.as_bytes()) {
                println!("Warning: Failed to write to black formatter: {}", e);
                return cleaned_code;
            }
        }
        
        // Get the formatted output
        match child.wait_with_output() {
            Ok(output) if output.status.success() => {
                match String::from_utf8(output.stdout) {
                    Ok(formatted) => return formatted,
                    Err(_) => {
                        println!("Warning: Failed to decode black formatter output");
                        return cleaned_code;
                    }
                }
            },
            _ => {
                println!("Warning: Black formatter failed, using cleaned code instead");
                return cleaned_code;
            }
        }
    }
    
    // Check if yapf is available
    let has_yapf = Command::new("sh")
        .arg("-c")
        .arg("which yapf")
        .output()
        .map(|output| output.status.success())
        .unwrap_or(false);
    
    // Try yapf as a fallback
    if has_yapf {
        let mut child = match Command::new("yapf")
            .arg("--style=pep8")
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .spawn() {
                Ok(child) => child,
                Err(e) => {
                    println!("Warning: Failed to run yapf formatter: {}", e);
                    return cleaned_code;
                }
            };
        
        // Write code to stdin
        if let Some(mut stdin) = child.stdin.take() {
            if let Err(e) = stdin.write_all(cleaned_code.as_bytes()) {
                println!("Warning: Failed to write to yapf formatter: {}", e);
                return cleaned_code;
            }
        }
        
        // Get the formatted output
        match child.wait_with_output() {
            Ok(output) if output.status.success() => {
                match String::from_utf8(output.stdout) {
                    Ok(formatted) => return formatted,
                    Err(_) => {
                        println!("Warning: Failed to decode yapf formatter output");
                        return cleaned_code;
                    }
                }
            },
            _ => {
                println!("Warning: yapf formatter failed, using cleaned code instead");
                return cleaned_code;
            }
        }
    }
    
    // As a last resort, try autopep8
    let has_autopep8 = Command::new("sh")
        .arg("-c")
        .arg("which autopep8")
        .output()
        .map(|output| output.status.success())
        .unwrap_or(false);
    
    if has_autopep8 {
        let mut child = match Command::new("autopep8")
            .arg("--max-line-length=100")
            .arg("-")  // Read from stdin
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .spawn() {
                Ok(child) => child,
                Err(e) => {
                    println!("Warning: Failed to run autopep8 formatter: {}", e);
                    return cleaned_code;
                }
            };
        
        // Write code to stdin
        if let Some(mut stdin) = child.stdin.take() {
            if let Err(e) = stdin.write_all(cleaned_code.as_bytes()) {
                println!("Warning: Failed to write to autopep8 formatter: {}", e);
                return cleaned_code;
            }
        }
        
        // Get the formatted output
        match child.wait_with_output() {
            Ok(output) if output.status.success() => {
                match String::from_utf8(output.stdout) {
                    Ok(formatted) => return formatted,
                    Err(_) => {
                        println!("Warning: Failed to decode autopep8 formatter output");
                        return cleaned_code;
                    }
                }
            },
            _ => {
                println!("Warning: autopep8 formatter failed, using cleaned code instead");
                return cleaned_code;
            }
        }
    }
    
    // If all formatters fail or aren't available, return the cleaned code
    cleaned_code
}

/// Clean up Python code before formatting
fn clean_python_code(code: &str) -> String {
    // Split into lines for processing
    let lines: Vec<&str> = code.lines().collect();
    
    let mut result = String::new();
    let mut last_was_empty = false;
    let mut in_class_body = false;
    let mut last_line_type: Option<&str> = None;
    
    for line in lines {
        let trimmed = line.trim();
        
        // Skip completely empty lines if the previous line was also empty
        if trimmed.is_empty() {
            if !last_was_empty {
                result.push_str(line);
                result.push('\n');
            }
            last_was_empty = true;
            continue;
        }
        
        last_was_empty = false;
        
        // Track when we're inside a class definition
        if trimmed.starts_with("class ") {
            in_class_body = true;
            
            // Add an extra empty line before class definitions
            // but only if we're not at the start of the file
            if last_line_type.is_some() && last_line_type != Some("empty") && !result.is_empty() {
                result.push('\n');
            }
            
            result.push_str(line);
            result.push('\n');
            last_line_type = Some("class");
            continue;
        }
        
        // Handle method declarations
        if trimmed.starts_with("def ") {
            // Add an empty line before method definitions
            if last_line_type != Some("empty") && last_line_type != Some("class") {
                result.push('\n');
            }
            
            result.push_str(line);
            result.push('\n');
            last_line_type = Some("method");
            continue;
        }
        
        // Handle decorators
        if trimmed.starts_with('@') {
            // Add an empty line before decorators
            if last_line_type != Some("empty") && last_line_type != Some("class") {
                result.push('\n');
            }
            
            result.push_str(line);
            result.push('\n');
            last_line_type = Some("decorator");
            continue;
        }
        
        // Check for the end of a class (when indentation returns to zero)
        if in_class_body && !line.starts_with(" ") && !line.starts_with("\t") && !trimmed.is_empty() {
            in_class_body = false;
            
            // Add an empty line after class definitions
            if last_line_type != Some("empty") {
                result.push('\n');
            }
        }
        
        // Add all other lines normally
        result.push_str(line);
        result.push('\n');
        
        // Track the type of this line
        if trimmed.is_empty() {
            last_line_type = Some("empty");
        } else {
            last_line_type = Some("content");
        }
    }
    
    // Clean up excessive newlines between field declarations
    let mut final_result = String::new();
    let mut last_was_field = false;
    let mut field_line_count = 0;
    
    for line in result.lines() {
        let trimmed = line.trim();
        
        // Check if this line is a field declaration (contains a colon but not a method definition)
        let is_field = trimmed.contains(':') && 
                      !trimmed.starts_with("class ") && 
                      !trimmed.starts_with("def ") && 
                      !trimmed.starts_with('@') && 
                      !trimmed.is_empty();
        
        // If this is an empty line after fields, limit how many we add
        if trimmed.is_empty() && last_was_field {
            field_line_count += 1;
            
            // Only allow one empty line between field groups
            if field_line_count <= 1 {
                final_result.push_str(line);
                final_result.push('\n');
            }
        } else {
            field_line_count = 0;
            final_result.push_str(line);
            final_result.push('\n');
        }
        
        last_was_field = is_field;
    }
    
    final_result
}

/// Extract class name from a class definition line
fn extract_class_name(line: &str) -> Option<String> {
    // Expected format: "class ClassName:" or "class ClassName(ParentClass):"
    let class_prefix = "class ";
    if let Some(after_class) = line.trim().strip_prefix(class_prefix) {
        // Find where the class name ends (at whitespace, colon, or open paren)
        let end_pos = after_class.find(|c: char| c.is_whitespace() || c == ':' || c == '(')
            .unwrap_or_else(|| after_class.len());
        
        let class_name = &after_class[..end_pos];
        if !class_name.is_empty() {
            return Some(class_name.to_string());
        }
    }
    None
}

/// Check if a string is a Python keyword
pub fn is_python_keyword(s: &str) -> bool {
    let keywords = [
        "False", "None", "True", "and", "as", "assert", "async", "await", 
        "break", "class", "continue", "def", "del", "elif", "else", "except", 
        "finally", "for", "from", "global", "if", "import", "in", "is", 
        "lambda", "nonlocal", "not", "or", "pass", "raise", "return", 
        "try", "while", "with", "yield"
    ];
    
    keywords.contains(&s)
}

/// Check if a string contains Python code fragments
pub fn is_python_fragment(s: &str) -> bool {
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

// Add a new function to fully replace the parse_declaration approach
// This will completely rewrite how we process class definitions
fn process_complex_enum_declaration(enum_name: &str, cleaned_decl: &str) -> (Vec<String>, Vec<String>) {
    let mut variant_classes = Vec::new();
    let mut variant_names = Vec::new();
    let mut current_class = String::new();
    let mut in_class = false;
    let mut in_method = false;
    let mut class_name = String::new();
    let mut indent_level = 0;
    
    // Process line by line with clear state tracking
    for line in cleaned_decl.lines() {
        let trimmed = line.trim();
        
        // Track indentation for method detection
        let leading_spaces = line.len() - line.trim_start().len();
        
        // Detect start of a class definition
        if trimmed.starts_with("class ") {
            // If we were already processing a class, save it
            if in_class {
                variant_classes.push(current_class);
                current_class = String::new();
            }
            
            // Start new class
            in_class = true;
            in_method = false;
            current_class = format!("{}\n", line);
            
            // Extract class name
            if let Some(name_start) = trimmed.find("class ") {
                let after_class = &trimmed[name_start + 6..];
                if let Some(end_pos) = after_class.find(|c: char| c.is_whitespace() || c == ':' || c == '(') {
                    class_name = after_class[..end_pos].to_string();
                    
                    // Only extract variant name if it's a variant class
                    if class_name.contains('_') && class_name.starts_with(enum_name) {
                        let variant_part = class_name.strip_prefix(&format!("{}_", enum_name)).unwrap_or("");
                        if !variant_part.is_empty() && 
                           !is_python_keyword(variant_part) && 
                           !is_python_fragment(variant_part) &&
                           !variant_names.contains(&variant_part.to_string()) {
                            variant_names.push(variant_part.to_string());
                        }
                    }
                }
            }
            
            // Save base indentation level
            indent_level = leading_spaces;
            continue;
        }
        
        // If we're in a class but not in a method, detect method start
        if in_class && !in_method && trimmed.starts_with("def ") {
            in_method = true;
            current_class.push_str(&format!("{}\n", line));
            continue;
        }
        
        // Handle method end detection
        if in_class && in_method {
            // Method ends if we get a line with same or less indentation as class
            if leading_spaces <= indent_level && trimmed.is_empty() {
                in_method = false;
            }
            
            // Always add the line while in a method
            current_class.push_str(&format!("{}\n", line));
            continue;
        }
        
        // Process field declarations (only if in a class but not in a method)
        if in_class && !in_method {
            // Only add the line if it's a valid field or empty line
            if trimmed.is_empty() {
                current_class.push_str(&format!("{}\n", line));
            } else if trimmed.contains(':') && !trimmed.starts_with("class") && !trimmed.contains("def ") {
                // Check if this is a field declaration, not a method body fragment
                let parts: Vec<&str> = trimmed.split(':').collect();
                if parts.len() >= 2 {
                    let field_name = parts[0].trim();
                    
                    // Skip Python code fragments that look like field declarations
                    if is_python_fragment(field_name) || is_python_keyword(field_name) ||
                       field_name.contains(".") || field_name.contains("(") || field_name.contains(")") {
                        continue;
                    }
                    
                    // Add valid field declaration
                    current_class.push_str(&format!("{}\n", line));
                }
            }
        }
        
        // Process main enum class to find variant declarations
        if !in_class && !in_method && trimmed.contains('=') && !trimmed.contains("def ") {
            // Look for variant declarations like "VariantName = auto()" or "VariantName = VariantClass"
            let parts: Vec<&str> = trimmed.split('=').collect();
            if parts.len() >= 2 {
                let variant_name = parts[0].trim();
                
                // Only add valid variant names
                if !variant_name.is_empty() && 
                   !is_python_keyword(variant_name) && 
                   !is_python_fragment(variant_name) &&
                   !variant_names.contains(&variant_name.to_string()) &&
                   // Additional checks for method fragments
                   !variant_name.contains(".") && 
                   !variant_name.contains("(") && 
                   !variant_name.contains(")") && 
                   !variant_name.contains("if ") &&
                   !variant_name.contains("for ") &&
                   !variant_name.contains("while ") {
                    variant_names.push(variant_name.to_string());
                }
            }
        }
    }
    
    // Add the last class if we were processing one
    if in_class {
        variant_classes.push(current_class);
    }
    
    (variant_classes, variant_names)
}
