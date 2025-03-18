# ts-rs

<h1 align="center" style="padding-top: 0; margin-top: 0;">
<img width="150px" src="https://raw.githubusercontent.com/Aleph-Alpha/ts-rs/main/logo.png" alt="logo">
<br/>
ts-rs
</h1>
<p align="center">
Generate TypeScript and Python type declarations from Rust types
</p>

<div align="center">
<!-- Github Actions -->
<img src="https://img.shields.io/github/actions/workflow/status/Aleph-Alpha/ts-rs/test.yml?branch=main" alt="actions status" />
<a href="https://crates.io/crates/ts-rs">
<img src="https://img.shields.io/crates/v/ts-rs.svg?style=flat-square"
alt="Crates.io version" />
</a>
<a href="https://docs.rs/ts-rs">
<img src="https://img.shields.io/badge/docs-latest-blue.svg?style=flat-square"
alt="docs.rs docs" />
</a>
<a href="https://crates.io/crates/ts-rs">
<img src="https://img.shields.io/crates/d/ts-rs.svg?style=flat-square"
alt="Download" />
</a>
</div>

### Why?
When building applications in Rust that interact with TypeScript or Python frontends, data structures have to be shared between backend and frontend.
Using this library, you can easily generate TypeScript and Python bindings to your Rust structs & enums so that you can keep your
types in one place.

ts-rs might also come in handy when working with WebAssembly or Python integrations.

### How?
ts-rs exposes two main traits:
1. `TS`: Using the `TS` derive macro, you can generate TypeScript bindings for your Rust types.
2. `Py`: Using the `Py` derive macro, you can generate Python bindings for your Rust types.

You can use these traits to obtain the TypeScript or Python bindings for your types.
We recommend doing this in your tests.
[See the example](https://github.com/Aleph-Alpha/ts-rs/blob/main/example/src/lib.rs) and [the docs](https://docs.rs/ts-rs/latest/ts_rs/).

### Get started
```toml
[dependencies]
ts-rs = "10.1"
```

```rust
use ts_rs::{TS, Py};

// Generate TypeScript binding
#[derive(TS)]
#[ts(export)]
struct User {
    user_id: i32,
    first_name: String,
    last_name: String,
}

// Or generate both TypeScript and Python bindings
#[derive(TS, Py)]
#[ts(export)]
#[py(export)]
struct Profile {
    profile_id: i32,
    username: String,
    active: bool,
}
```

When running `cargo test`:
1. The TypeScript bindings will be exported to `bindings/User.ts` and `bindings/Profile.ts` with content like:

```ts
export type User = { user_id: number, first_name: string, last_name: string, };
```

2. The Python bindings will be exported to `py_bindings/` directory with files like:

```python
# Profile.py
from typing import Any, Optional, List, Dict, Union

class Profile:
    profile_id: int
    username: str
    active: bool

    def __init__(self, profile_id: int, username: str, active: bool) -> None:
        self.profile_id = profile_id
        self.username = username
        self.active = active

# Status.py
from enum import Enum, auto
from typing import Any, Optional, List, Dict, Union
from dataclasses import dataclass

class Status(Enum):
    Active = 1
    Inactive = 2
    Pending = 3

# Message.py - Complex enum with fields
from enum import Enum, auto
from typing import Any, Optional, List, Dict, Union
from dataclasses import dataclass

@dataclass
class Message_Text:
    content: str
    sender: str

@dataclass
class Message_Image:
    url: str
    width: int
    height: int

@dataclass
class Message_File:
    field_0: str

class Message(Enum):
    Text = Message_Text
    Image = Message_Image
    File = Message_File

    @classmethod
    def create_message(cls, variant_name: str, **kwargs):
        """Helper to create a variant instance with fields"""
        # Implementation details...
```

### Features
- Generate type declarations from Rust structs for both TypeScript and Python
- Generate union declarations from Rust enums
- Inline types
- Flatten structs/types
- Generate necessary imports when exporting to multiple files
- Serde compatibility
- Generic types
- Support for ESM imports (TypeScript)
- Python class and Enum support

### cargo features
| **Feature**        | **Description**                                                                                                                                                                                           |
|:-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| serde-compat       | **Enabled by default** <br/>See the *"serde compatibility"* section below for more information.                                                                                                           |
| format             | Enables formatting of the generated TypeScript bindings. <br/>Currently, this unfortunately adds quite a few dependencies.                                                                                |
| no-serde-warnings  | By default, warnings are printed during build if unsupported serde attributes are encountered. <br/>Enabling this feature silences these warnings.                                                        |
| import-esm         | When enabled,`import` statements in the generated file will have the `.js` extension in the end of the path to conform to the ES Modules spec. <br/> Example: `import { MyStruct } from "./my_struct.js"` |
| serde-json-impl    | Implement `TS` for types from *serde_json*                                                                                                                                                                |
| chrono-impl        | Implement `TS` for types from *chrono*                                                                                                                                                                    |
| bigdecimal-impl    | Implement `TS` for types from *bigdecimal*                                                                                                                                                                |
| url-impl           | Implement `TS` for types from *url*                                                                                                                                                                       |
| uuid-impl          | Implement `TS` for types from *uuid*                                                                                                                                                                      |
| bson-uuid-impl     | Implement `TS` for *bson::oid::ObjectId* and *bson::uuid*                                                                                                                                                 |
| bytes-impl         | Implement `TS` for types from *bytes*                                                                                                                                                                     |
| indexmap-impl      | Implement `TS` for types from *indexmap*                                                                                                                                                                  |
| ordered-float-impl | Implement `TS` for types from *ordered_float*                                                                                                                                                             |
| heapless-impl      | Implement `TS` for types from *heapless*                                                                                                                                                                  |
| semver-impl        | Implement `TS` for types from *semver*                                                                                                                                                                    |
| smol_str-impl      | Implement `TS` for types from *smol_str*                                                                                                                                                                    |
| tokio-impl         | Implement `TS` for types from *tokio*                                                                                                                                                                    |

<br/>

If there's a type you're dealing with which doesn't implement `TS`, use either
`#[ts(as = "..")]` or `#[ts(type = "..")]`, or open a PR.

### `serde` compatability
With the `serde-compat` feature (enabled by default), serde attributes can be parsed for enums and structs.
Supported serde attributes:
- `rename`
- `rename-all`
- `rename-all-fields`
- `tag`
- `content`
- `untagged`
- `skip`
- `flatten`
- `default`

Note: `skip_serializing` and `skip_deserializing` are ignored. If you wish to exclude a field
from the generated type, but cannot use `#[serde(skip)]`, use `#[ts(skip)]` instead.

When ts-rs encounters an unsupported serde attribute, a warning is emitted, unless the feature `no-serde-warnings` is enabled.

### Contributing
Contributions are always welcome!
Feel free to open an issue, discuss using GitHub discussions or open a PR.
[See CONTRIBUTING.md](https://github.com/Aleph-Alpha/ts-rs/blob/main/CONTRIBUTING.md)

### MSRV
The Minimum Supported Rust Version for this crate is 1.78.0

License: MIT
