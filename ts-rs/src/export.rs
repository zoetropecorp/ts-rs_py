use std::{
    any::TypeId,
    collections::BTreeMap,
    fmt::Write,
    path::{Component, Path, PathBuf},
};

use thiserror::Error;

use ExportError::*;

use crate::TS;

const NOTE: &str = "// This file was generated by [ts-rs](https://github.com/Aleph-Alpha/ts-rs). Do not edit this file manually.\n";

/// An error which may occur when exporting a type
#[derive(Error, Debug)]
pub enum ExportError {
    #[error("this type cannot be exported")]
    CannotBeExported(&'static str),
    #[cfg(feature = "format")]
    #[error("an error occurred while formatting the generated typescript output")]
    Formatting(String),
    #[error("an error occurred while performing IO")]
    Io(#[from] std::io::Error),
    #[error("the environment variable CARGO_MANIFEST_DIR is not set")]
    ManifestDirNotSet,
}

pub(crate) use recursive_export::export_type_with_dependencies;
mod recursive_export {
    use std::{any::TypeId, collections::HashSet};

    use super::export_type;
    use crate::{
        typelist::{TypeList, TypeVisitor},
        ExportError, TS,
    };

    struct Visit<'a> {
        seen: &'a mut HashSet<TypeId>,
        error: Option<ExportError>,
    }

    impl<'a> TypeVisitor for Visit<'a> {
        fn visit<T: TS + 'static + ?Sized>(&mut self) {
            // if an error occurred previously, or the type cannot be exported (it's a primitive),
            // we return
            if self.error.is_some() || T::EXPORT_TO.is_none() {
                return;
            }

            self.error = export_recursive::<T>(self.seen).err();
        }
    }

    /// Exports `T` to the file specified by the `#[ts(export_to = ..)]` attribute.
    /// Additionally, all dependencies of `T` will be exported as well.
    /// TODO: This might cause a race condition:
    ///       If two types `A` and `B` are `#[ts(export)]` and depend on type `C`,
    ///       then both tests for exporting `A` and `B` will try to write `C` to `C.ts`.
    ///       Since rust, by default, executes tests in paralell, this might cause `C.ts` to be corrupted.
    pub(crate) fn export_type_with_dependencies<T: TS + ?Sized + 'static>(
    ) -> Result<(), ExportError> {
        let mut seen = HashSet::new();
        export_recursive::<T>(&mut seen)
    }

    // exports T, then recursively calls itself with all of its dependencies
    fn export_recursive<T: TS + ?Sized + 'static>(
        seen: &mut HashSet<TypeId>,
    ) -> Result<(), ExportError> {
        if !seen.insert(TypeId::of::<T>()) {
            return Ok(());
        }

        export_type::<T>()?;

        let mut visitor = Visit { seen, error: None };
        T::dependency_types().for_each(&mut visitor);

        if let Some(e) = visitor.error {
            Err(e)
        } else {
            Ok(())
        }
    }
}

/// Export `T` to the file specified by the `#[ts(export_to = ..)]` attribute
pub(crate) fn export_type<T: TS + ?Sized + 'static>() -> Result<(), ExportError> {
    let path = output_path::<T>()?;
    export_type_to::<T, _>(&path)
}

/// Export `T` to the file specified by the `path` argument.
pub(crate) fn export_type_to<T: TS + ?Sized + 'static, P: AsRef<Path>>(
    path: P,
) -> Result<(), ExportError> {
    #[allow(unused_mut)]
    let mut buffer = export_type_to_string::<T>()?;

    // format output
    #[cfg(feature = "format")]
    {
        use dprint_plugin_typescript::{configuration::ConfigurationBuilder, format_text};

        let fmt_cfg = ConfigurationBuilder::new().deno().build();
        if let Some(formatted) =
            format_text(path.as_ref(), &buffer, &fmt_cfg).map_err(|e| Formatting(e.to_string()))?
        {
            buffer = formatted;
        }
    }

    if let Some(parent) = path.as_ref().parent() {
        std::fs::create_dir_all(parent)?;
    }
    std::fs::write(path.as_ref(), buffer)?;
    Ok(())
}

/// Returns the generated defintion for `T`.
pub(crate) fn export_type_to_string<T: TS + ?Sized + 'static>() -> Result<String, ExportError> {
    let mut buffer = String::with_capacity(1024);
    buffer.push_str(NOTE);
    generate_imports::<T>(&mut buffer)?;
    generate_decl::<T>(&mut buffer);
    Ok(buffer)
}

/// Compute the output path to where `T` should be exported.
fn output_path<T: TS + ?Sized>() -> Result<PathBuf, ExportError> {
    let manifest_dir = std::env::var("CARGO_MANIFEST_DIR").map_err(|_| ManifestDirNotSet)?;
    let manifest_dir = Path::new(&manifest_dir);
    let path = PathBuf::from(T::EXPORT_TO.ok_or(CannotBeExported(std::any::type_name::<T>()))?);
    Ok(manifest_dir.join(path))
}

/// Push the declaration of `T`
fn generate_decl<T: TS + ?Sized>(out: &mut String) {
    out.push_str("export ");
    out.push_str(&T::decl());
}

/// Push an import statement for all dependencies of `T`
fn generate_imports<T: TS + ?Sized + 'static>(out: &mut String) -> Result<(), ExportError> {
    let path =
        Path::new(T::EXPORT_TO.ok_or(ExportError::CannotBeExported(std::any::type_name::<T>()))?);

    let deps = T::dependencies();
    let deduplicated_deps = deps
        .iter()
        .filter(|dep| dep.type_id != TypeId::of::<T>())
        .map(|dep| (&dep.ts_name, dep))
        .collect::<BTreeMap<_, _>>();

    for (_, dep) in deduplicated_deps {
        let rel_path = import_path(path, Path::new(dep.exported_to));
        writeln!(
            out,
            "import type {{ {} }} from {:?};",
            &dep.ts_name, rel_path
        )
        .unwrap();
    }
    writeln!(out).unwrap();
    Ok(())
}

/// Returns the required import path for importing `import` from the file `from`
fn import_path(from: &Path, import: &Path) -> String {
    let rel_path =
        diff_paths(import, from.parent().unwrap()).expect("failed to calculate import path");
    let path = match rel_path.components().next() {
        Some(Component::Normal(_)) => format!("./{}", rel_path.to_string_lossy()),
        _ => rel_path.to_string_lossy().into(),
    };

    let path_without_extension = path.trim_end_matches(".ts");

    if cfg!(feature = "import-esm") {
        format!("{}.js", path_without_extension)
    } else {
        path_without_extension.to_owned()
    }
}

// Construct a relative path from a provided base directory path to the provided path.
//
// Copyright 2012-2015 The Rust Project Developers.
//
// Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
// http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
// <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
// option. This file may not be copied, modified, or distributed
// except according to those terms.
//
// Adapted from rustc's path_relative_from
// https://github.com/rust-lang/rust/blob/e1d0de82cc40b666b88d4a6d2c9dcbc81d7ed27f/src/librustc_back/rpath.rs#L116-L158
fn diff_paths<P, B>(path: P, base: B) -> Option<PathBuf>
where
    P: AsRef<Path>,
    B: AsRef<Path>,
{
    let path = path.as_ref();
    let base = base.as_ref();

    if path.is_absolute() != base.is_absolute() {
        if path.is_absolute() {
            Some(PathBuf::from(path))
        } else {
            None
        }
    } else {
        let mut ita = path.components();
        let mut itb = base.components();
        let mut comps: Vec<Component> = vec![];
        loop {
            match (ita.next(), itb.next()) {
                (None, None) => break,
                (Some(a), None) => {
                    comps.push(a);
                    comps.extend(ita.by_ref());
                    break;
                }
                (None, _) => comps.push(Component::ParentDir),
                (Some(a), Some(b)) if comps.is_empty() && a == b => (),
                (Some(a), Some(Component::CurDir)) => comps.push(a),
                (Some(_), Some(Component::ParentDir)) => return None,
                (Some(a), Some(_)) => {
                    comps.push(Component::ParentDir);
                    for _ in itb {
                        comps.push(Component::ParentDir);
                    }
                    comps.push(a);
                    comps.extend(ita.by_ref());
                    break;
                }
            }
        }
        Some(comps.iter().map(|c| c.as_os_str()).collect())
    }
}
