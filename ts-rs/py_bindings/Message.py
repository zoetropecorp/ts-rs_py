from __future__ import annotations

import json
import sys
from pathlib import Path
from enum import Enum, auto
from typing import Any, Optional, List, Dict, Union, TYPE_CHECKING
from dataclasses import dataclass

# Add current directory to Python path to facilitate imports
_current_file = Path(__file__).resolve()
_current_dir = _current_file.parent
if str(_current_dir) not in sys.path:
    sys.path.append(str(_current_dir))

# Forward references for type checking only
if TYPE_CHECKING:
    from Message import Message
    from Message_File import Message_File
    from Message_Image import Message_Image
    from Message_Text import Message_Text
    from Path( import Path(
    from TYPE import TYPE

class Message_Text:
    content: str
    sender: str



    url: str
    width: int
    height: int



    field_0: str



    Text = Message_Text  # Complex variant with fields
    Image = Message_Image  # Complex variant with fields
    File = Message_File  # Complex variant with fields




                # For complex variants with associated data
                if hasattr(variant.value, 'fromDict') and callable(getattr(variant.value, 'fromDict')):
                    # Create data object from the dictionary (excluding the type field)
                    variant_data = {k: v for k, v in data.items() if k != "type"}
                    return variant.value.__class__.fromDict(variant_data)

                return variant
        # Default fallback - return first variant
        return next(iter(cls))
# Classes for complex enum variants
@dataclass
class Message_Text:
    content: str
    sender: str
    def toJSON(self) -> str: 
    def _serialize(obj): 
    if hasattr(obj, '__dict__'): 
    for key, value in obj.__dict__.items(): 
    elif isinstance(obj, list): 
    elif isinstance(obj, dict): 
    return {k: _serialize(v) for k, v in obj.items()}
    elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')): 
    elif hasattr(obj, 'value') and isinstance(obj, Enum): 
    elif isinstance(obj, Enum): 
    def fromJSON(cls, json_str): 
    def fromDict(cls, data): 
    if 'content' in data: 
    if isinstance(content, dict) and hasattr(cls, '_content_type'): 
    elif isinstance(content, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'sender' in data: 
    if isinstance(sender, dict) and hasattr(cls, '_sender_type'): 
    elif isinstance(sender, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, content, sender, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'content' in data, if isinstance(content, dict) and hasattr(cls, '_content_type'), elif isinstance(content, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'sender' in data, if isinstance(sender, dict) and hasattr(cls, '_sender_type'), elif isinstance(sender, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.content = content
        self.sender = sender
        self.def toJSON(self) -> str = def toJSON(self) -> str
        self.def _serialize(obj) = def _serialize(obj)
        self.if hasattr(obj, '__dict__') = if hasattr(obj, '__dict__')
        self.for key, value in obj.__dict__.items() = for key, value in obj.__dict__.items()
        self.elif isinstance(obj, list) = elif isinstance(obj, list)
        self.elif isinstance(obj, dict) = elif isinstance(obj, dict)
        self.return {k = return {k
        self.elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')) = elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON'))
        self.elif hasattr(obj, 'value') and isinstance(obj, Enum) = elif hasattr(obj, 'value') and isinstance(obj, Enum)
        self.elif isinstance(obj, Enum) = elif isinstance(obj, Enum)
        self.def fromJSON(cls, json_str) = def fromJSON(cls, json_str)
        self.def fromDict(cls, data) = def fromDict(cls, data)
        self.if 'content' in data = if 'content' in data
        self.if isinstance(content, dict) and hasattr(cls, '_content_type') = if isinstance(content, dict) and hasattr(cls, '_content_type')
        self.elif isinstance(content, list) and hasattr(cls, '_item_type') = elif isinstance(content, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'sender' in data = if 'sender' in data
        self.if isinstance(sender, dict) and hasattr(cls, '_sender_type') = if isinstance(sender, dict) and hasattr(cls, '_sender_type')
        self.elif isinstance(sender, list) and hasattr(cls, '_item_type') = elif isinstance(sender, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else

    def toJSON(self) -> str:
        """Serialize this object to a JSON string"""
        return json.dumps(self._serialize())

    def _serialize(self):
        """Convert this object to a serializable dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            # Skip private fields
            if key.startswith('_'):
                continue
            # Recursively serialize any nested objects
            if hasattr(value, '_serialize'):
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

    @classmethod
    def fromDict(cls, data):
        """Create an instance from a dictionary"""
        content = data.get('content', None)
        sender = data.get('sender', None)
        def toJSON(self) -> str = data.get('def toJSON(self) -> str', None)
        def _serialize(obj) = data.get('def _serialize(obj)', None)
        if hasattr(obj, '__dict__') = data.get('if hasattr(obj, '__dict__')', None)
        for key, value in obj.__dict__.items() = data.get('for key, value in obj.__dict__.items()', None)
        elif isinstance(obj, list) = data.get('elif isinstance(obj, list)', None)
        elif isinstance(obj, dict) = data.get('elif isinstance(obj, dict)', None)
        return {k = data.get('return {k', None)
        elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')) = data.get('elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON'))', None)
        elif hasattr(obj, 'value') and isinstance(obj, Enum) = data.get('elif hasattr(obj, 'value') and isinstance(obj, Enum)', None)
        elif isinstance(obj, Enum) = data.get('elif isinstance(obj, Enum)', None)
        def fromJSON(cls, json_str) = data.get('def fromJSON(cls, json_str)', None)
        def fromDict(cls, data) = data.get('def fromDict(cls, data)', None)
        if 'content' in data = data.get('if 'content' in data', None)
        if isinstance(content, dict) and hasattr(cls, '_content_type') = data.get('if isinstance(content, dict) and hasattr(cls, '_content_type')', None)
        elif isinstance(content, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(content, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'sender' in data = data.get('if 'sender' in data', None)
        if isinstance(sender, dict) and hasattr(cls, '_sender_type') = data.get('if isinstance(sender, dict) and hasattr(cls, '_sender_type')', None)
        elif isinstance(sender, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(sender, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(content, sender, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'content' in data, if isinstance(content, dict) and hasattr(cls, '_content_type'), elif isinstance(content, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'sender' in data, if isinstance(sender, dict) and hasattr(cls, '_sender_type'), elif isinstance(sender, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Message_Image:
    url: str
    width: int
    height: int
    def toJSON(self) -> str: 
    def _serialize(obj): 
    if hasattr(obj, '__dict__'): 
    for key, value in obj.__dict__.items(): 
    elif isinstance(obj, list): 
    elif isinstance(obj, dict): 
    return {k: _serialize(v) for k, v in obj.items()}
    elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')): 
    elif hasattr(obj, 'value') and isinstance(obj, Enum): 
    elif isinstance(obj, Enum): 
    def fromJSON(cls, json_str): 
    def fromDict(cls, data): 
    if 'url' in data: 
    if isinstance(url, dict) and hasattr(cls, '_url_type'): 
    elif isinstance(url, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'width' in data: 
    if isinstance(width, dict) and hasattr(cls, '_width_type'): 
    elif isinstance(width, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'height' in data: 
    if isinstance(height, dict) and hasattr(cls, '_height_type'): 
    elif isinstance(height, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, url, width, height, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'url' in data, if isinstance(url, dict) and hasattr(cls, '_url_type'), elif isinstance(url, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'width' in data, if isinstance(width, dict) and hasattr(cls, '_width_type'), elif isinstance(width, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'height' in data, if isinstance(height, dict) and hasattr(cls, '_height_type'), elif isinstance(height, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.url = url
        self.width = width
        self.height = height
        self.def toJSON(self) -> str = def toJSON(self) -> str
        self.def _serialize(obj) = def _serialize(obj)
        self.if hasattr(obj, '__dict__') = if hasattr(obj, '__dict__')
        self.for key, value in obj.__dict__.items() = for key, value in obj.__dict__.items()
        self.elif isinstance(obj, list) = elif isinstance(obj, list)
        self.elif isinstance(obj, dict) = elif isinstance(obj, dict)
        self.return {k = return {k
        self.elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')) = elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON'))
        self.elif hasattr(obj, 'value') and isinstance(obj, Enum) = elif hasattr(obj, 'value') and isinstance(obj, Enum)
        self.elif isinstance(obj, Enum) = elif isinstance(obj, Enum)
        self.def fromJSON(cls, json_str) = def fromJSON(cls, json_str)
        self.def fromDict(cls, data) = def fromDict(cls, data)
        self.if 'url' in data = if 'url' in data
        self.if isinstance(url, dict) and hasattr(cls, '_url_type') = if isinstance(url, dict) and hasattr(cls, '_url_type')
        self.elif isinstance(url, list) and hasattr(cls, '_item_type') = elif isinstance(url, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'width' in data = if 'width' in data
        self.if isinstance(width, dict) and hasattr(cls, '_width_type') = if isinstance(width, dict) and hasattr(cls, '_width_type')
        self.elif isinstance(width, list) and hasattr(cls, '_item_type') = elif isinstance(width, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'height' in data = if 'height' in data
        self.if isinstance(height, dict) and hasattr(cls, '_height_type') = if isinstance(height, dict) and hasattr(cls, '_height_type')
        self.elif isinstance(height, list) and hasattr(cls, '_item_type') = elif isinstance(height, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else

    def toJSON(self) -> str:
        """Serialize this object to a JSON string"""
        return json.dumps(self._serialize())

    def _serialize(self):
        """Convert this object to a serializable dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            # Skip private fields
            if key.startswith('_'):
                continue
            # Recursively serialize any nested objects
            if hasattr(value, '_serialize'):
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

    @classmethod
    def fromDict(cls, data):
        """Create an instance from a dictionary"""
        url = data.get('url', None)
        width = data.get('width', None)
        height = data.get('height', None)
        def toJSON(self) -> str = data.get('def toJSON(self) -> str', None)
        def _serialize(obj) = data.get('def _serialize(obj)', None)
        if hasattr(obj, '__dict__') = data.get('if hasattr(obj, '__dict__')', None)
        for key, value in obj.__dict__.items() = data.get('for key, value in obj.__dict__.items()', None)
        elif isinstance(obj, list) = data.get('elif isinstance(obj, list)', None)
        elif isinstance(obj, dict) = data.get('elif isinstance(obj, dict)', None)
        return {k = data.get('return {k', None)
        elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')) = data.get('elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON'))', None)
        elif hasattr(obj, 'value') and isinstance(obj, Enum) = data.get('elif hasattr(obj, 'value') and isinstance(obj, Enum)', None)
        elif isinstance(obj, Enum) = data.get('elif isinstance(obj, Enum)', None)
        def fromJSON(cls, json_str) = data.get('def fromJSON(cls, json_str)', None)
        def fromDict(cls, data) = data.get('def fromDict(cls, data)', None)
        if 'url' in data = data.get('if 'url' in data', None)
        if isinstance(url, dict) and hasattr(cls, '_url_type') = data.get('if isinstance(url, dict) and hasattr(cls, '_url_type')', None)
        elif isinstance(url, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(url, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'width' in data = data.get('if 'width' in data', None)
        if isinstance(width, dict) and hasattr(cls, '_width_type') = data.get('if isinstance(width, dict) and hasattr(cls, '_width_type')', None)
        elif isinstance(width, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(width, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'height' in data = data.get('if 'height' in data', None)
        if isinstance(height, dict) and hasattr(cls, '_height_type') = data.get('if isinstance(height, dict) and hasattr(cls, '_height_type')', None)
        elif isinstance(height, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(height, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(url, width, height, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'url' in data, if isinstance(url, dict) and hasattr(cls, '_url_type'), elif isinstance(url, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'width' in data, if isinstance(width, dict) and hasattr(cls, '_width_type'), elif isinstance(width, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'height' in data, if isinstance(height, dict) and hasattr(cls, '_height_type'), elif isinstance(height, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Message_File:
    field_0: str
    def toJSON(self) -> str: 
    def _serialize(obj): 
    if hasattr(obj, '__dict__'): 
    for key, value in obj.__dict__.items(): 
    elif isinstance(obj, list): 
    elif isinstance(obj, dict): 
    return {k: _serialize(v) for k, v in obj.items()}
    elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')): 
    elif hasattr(obj, 'value') and isinstance(obj, Enum): 
    elif isinstance(obj, Enum): 
    def fromJSON(cls, json_str): 
    def fromDict(cls, data): 
    if isinstance(data, list): 
    return cls(*data[: 1])
    else: 

    def __init__(self, field_0, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if isinstance(data, list), return cls(*data[, else):
        self.field_0 = field_0
        self.def toJSON(self) -> str = def toJSON(self) -> str
        self.def _serialize(obj) = def _serialize(obj)
        self.if hasattr(obj, '__dict__') = if hasattr(obj, '__dict__')
        self.for key, value in obj.__dict__.items() = for key, value in obj.__dict__.items()
        self.elif isinstance(obj, list) = elif isinstance(obj, list)
        self.elif isinstance(obj, dict) = elif isinstance(obj, dict)
        self.return {k = return {k
        self.elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')) = elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON'))
        self.elif hasattr(obj, 'value') and isinstance(obj, Enum) = elif hasattr(obj, 'value') and isinstance(obj, Enum)
        self.elif isinstance(obj, Enum) = elif isinstance(obj, Enum)
        self.def fromJSON(cls, json_str) = def fromJSON(cls, json_str)
        self.def fromDict(cls, data) = def fromDict(cls, data)
        self.if isinstance(data, list) = if isinstance(data, list)
        self.return cls(*data[ = return cls(*data[
        self.else = else

    def toJSON(self) -> str:
        """Serialize this object to a JSON string"""
        return json.dumps(self._serialize())

    def _serialize(self):
        """Convert this object to a serializable dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            # Skip private fields
            if key.startswith('_'):
                continue
            # Recursively serialize any nested objects
            if hasattr(value, '_serialize'):
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

    @classmethod
    def fromDict(cls, data):
        """Create an instance from a dictionary"""
        field_0 = data.get('field_0', None)
        def toJSON(self) -> str = data.get('def toJSON(self) -> str', None)
        def _serialize(obj) = data.get('def _serialize(obj)', None)
        if hasattr(obj, '__dict__') = data.get('if hasattr(obj, '__dict__')', None)
        for key, value in obj.__dict__.items() = data.get('for key, value in obj.__dict__.items()', None)
        elif isinstance(obj, list) = data.get('elif isinstance(obj, list)', None)
        elif isinstance(obj, dict) = data.get('elif isinstance(obj, dict)', None)
        return {k = data.get('return {k', None)
        elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')) = data.get('elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON'))', None)
        elif hasattr(obj, 'value') and isinstance(obj, Enum) = data.get('elif hasattr(obj, 'value') and isinstance(obj, Enum)', None)
        elif isinstance(obj, Enum) = data.get('elif isinstance(obj, Enum)', None)
        def fromJSON(cls, json_str) = data.get('def fromJSON(cls, json_str)', None)
        def fromDict(cls, data) = data.get('def fromDict(cls, data)', None)
        if isinstance(data, list) = data.get('if isinstance(data, list)', None)
        return cls(*data[ = data.get('return cls(*data[', None)
        else = data.get('else', None)
        return cls(field_0, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if isinstance(data, list), return cls(*data[, else)

# The main Message class
class Message(Enum):
    Text = Message_Text
    Image = Message_Image
    File = Message_File
    if variant.name.lower() = auto()
    inner_data = auto()
    inner_data["type"] = auto()
    data = auto()
    variant_name = auto()
    variant = auto()
    variant_data = auto()

    def toJSON(self) -> str:
        """Serialize this object to a JSON string"""
        return json.dumps(self._serialize())

    def _serialize(self):
        """Convert this object to a serializable dictionary"""
        # Complex enum serialization - the self is the Enum instance
        if isinstance(self.value, (int, str, bool, float)):
            return {"type": self.name}
        
        # If the value is a variant class, serialize it and add the type tag
        if hasattr(self.value, '__dict__'):
            # Start with the variant name
            result = {"type": self.name}
            
            # Add all fields from the variant value
            for key, value in self.value.__dict__.items():
                # Skip private fields
                if key.startswith('_'):
                    continue
                    
                # Recursively serialize any nested objects
                if hasattr(value, '_serialize'):
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
        
        # If it's a simple enum instance, just return the name
        return {"type": self.name}

    @classmethod
    def fromJSON(cls, json_str):
        """Deserialize JSON string to a new instance"""
        data = json.loads(json_str)
        return cls.fromDict(data)

    @classmethod
    def fromDict(cls, data):
        """Create a complex enum instance from a dictionary"""
        if isinstance(data, dict):
            # Complex enum with fields
            if "type" in data:
                variant_name = data["type"]
                # Find the enum variant by name
                try:
                    variant = cls[variant_name]
                    
                    # If the variant value is a class, get a new instance
                    if hasattr(variant.value, 'fromDict'):
                        # Create data object from the dictionary (excluding the type field)
                        variant_data = {k: v for k, v in data.items() if k != "type"}
                        return variant.value.fromDict(variant_data)
                    
                    return variant
                except (KeyError, ValueError):
                    # Use the helper method if direct lookup fails
                    variant_data = {k: v for k, v in data.items() if k != "type"}
                    return cls.create_variant(variant_name, **variant_data)
        elif isinstance(data, str):
            # Simple enum name
            try:
                return cls[data]  # Get enum by name
            except (KeyError, ValueError):
                pass
        # Default fallback
        return next(iter(cls))

    @classmethod
    def create_variant(cls, variant_name, **kwargs):
        """Helper method to create a variant with associated data"""
        # Find the correct variant
        for variant in cls:
            if variant.name.lower() == variant_name.lower():
                if variant.name == "Text":
                    try:
                        return Message_Text.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "Image":
                    try:
                        return Message_Image.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "File":
                    try:
                        return Message_File.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "if variant.name.lower()":
                    try:
                        return Message_if variant.name.lower().fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "inner_data":
                    try:
                        return Message_inner_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "inner_data["type"]":
                    try:
                        return Message_inner_data["type"].fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "data":
                    try:
                        return Message_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_name":
                    try:
                        return Message_variant_name.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant":
                    try:
                        return Message_variant.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_data":
                    try:
                        return Message_variant_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
        # If not found, return the first variant as a fallback
        return next(iter(cls))
