#![allow(clippy::disallowed_names)]

use serde::Serialize;
use ts_rs::{Py, TS};

#[derive(TS, Py, Serialize)]
#[ts(export)]
#[py(export)]
pub struct User {
    pub id: i32,
    pub name: String,
    pub email: String,
    pub active: bool,
}

#[derive(TS, Py, Serialize)]
#[ts(export)]
#[py(export)]
pub enum Status {
    Active,
    Inactive,
    Pending,
}

#[derive(TS, Py, Serialize)]
#[ts(export)]
#[py(export)]
pub enum Message {
    Text { content: String, sender: String },
    Image { url: String, width: u32, height: u32 },
    File(String),  // filename
}

#[test]
fn test_py_generation() {
    // Test that we can generate Python code from the struct
    let user_code = <User as ts_rs::Py>::decl_concrete();
    println!("Generated Python code for User:");
    println!("{}", user_code);
    
    // Test that we can generate Python code from the simple enum
    let status_code = <Status as ts_rs::Py>::decl_concrete();
    println!("Generated Python code for Status:");
    println!("{}", status_code);
    
    // Test that we can generate Python code from the complex enum
    let message_code = <Message as ts_rs::Py>::decl_concrete();
    println!("Generated Python code for Message (complex enum):");
    println!("{}", message_code);
    
    // Make sure the generated code has the expected structure for struct
    assert!(user_code.contains("class User(TypedDict):"));
    assert!(user_code.contains("id: int"));
    assert!(user_code.contains("name: str"));
    assert!(user_code.contains("email: str"));
    assert!(user_code.contains("active: bool"));
    // assert!(user_code.contains("def __init__(self, id: int, name: str, email: str, active: bool)"));
    // assert!(user_code.contains("self.id = id"));
    // assert!(user_code.contains("self.name = name"));
    // assert!(user_code.contains("self.email = email"));
    // assert!(user_code.contains("self.active = active"));
    
    // Make sure the generated code has the expected structure for enum
    assert!(status_code.contains("from enum import Enum"));
    assert!(status_code.contains("class Status(Enum):"));
    // Assert each variant is present
    assert!(status_code.contains("Active = 1"), "No Active variant found: {}", status_code);
    assert!(status_code.contains("Inactive = 2"), "No Inactive variant found: {}", status_code);
    assert!(status_code.contains("Pending = 3"), "No Pending variant found: {}", status_code);
    
    // Add assertions for complex enum
    assert!(message_code.contains("from dataclasses import dataclass"));
    assert!(message_code.contains("@dataclass"));
    assert!(message_code.contains("class Message_Text:"));
    assert!(message_code.contains("content: str"));
    assert!(message_code.contains("sender: str"));
    assert!(message_code.contains("class Message_Image:"));
    assert!(message_code.contains("url: str"));
    assert!(message_code.contains("width: int"));
    assert!(message_code.contains("height: int"));
    assert!(message_code.contains("class Message_File:"));
    assert!(message_code.contains("field_0: str"));
    assert!(message_code.contains("class Message(Enum):"));
    assert!(message_code.contains("def create_message(cls, variant_name: str, **kwargs):"));
    
    // Test exporting files - export each type separately
    let user_result = <User as ts_rs::Py>::export_to_string().unwrap();
    let status_result = <Status as ts_rs::Py>::export_to_string().unwrap();
    let message_result = <Message as ts_rs::Py>::export_to_string().unwrap();
    
    // Create the output directory
    let out_dir = "./py_bindings_test";
    std::fs::create_dir_all(out_dir).unwrap();
    
    // Write files manually
    std::fs::write(format!("{}/User.py", out_dir), user_result).unwrap();
    std::fs::write(format!("{}/Status.py", out_dir), status_result).unwrap();
    std::fs::write(format!("{}/Message.py", out_dir), message_result).unwrap();
    
    // Verify files were created with correct content
    let user_file = std::fs::read_to_string("./py_bindings_test/User.py").unwrap();
    let status_file = std::fs::read_to_string("./py_bindings_test/Status.py").unwrap();
    let message_file = std::fs::read_to_string("./py_bindings_test/Message.py").unwrap();
    
    assert!(user_file.contains("class User(TypedDict):"));
    assert!(status_file.contains("class Status(Enum)"));
    assert!(message_file.contains("class Message(Enum)"));
    assert!(message_file.contains("@dataclass"));
}