/// Normalize field spacing to avoid excessive newlines between field declarations
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

/// Export a Python type to a file 