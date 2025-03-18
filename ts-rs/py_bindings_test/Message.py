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
    pass  # Type checking imports will use annotations


@dataclass
class Message_Text:
    content: str
    sender: str
    def toJSON(self) -> str:
        def _serialize(obj):
            if hasattr(obj, '__dict__'):
                result = {}
                for key, value in obj.__dict__.items():
                    result[key] = _serialize(value)
                return result
            elif isinstance(obj, list):
                return [_serialize(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: _serialize(v) for k, v in obj.items()}
            elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')):
                return json.loads(obj.toJSON())
            elif hasattr(obj, 'value') and isinstance(obj, Enum):
                return obj.name
            elif isinstance(obj, Enum):
                return obj.name
            return obj
        return json.dumps(_serialize(self), indent=2)

    @classmethod
    def fromJSON(cls, json_str):
        """Deserialize JSON string to a new instance"""
        data = json.loads(json_str)
        return cls.fromDict(data)

    @classmethod
    def fromDict(cls, data):
        """Create an instance from a dictionary"""
        if 'content' in data:
            content = data['content']
            # Handle nested objects based on type
            if isinstance(content, dict) and hasattr(cls, '_content_type'):
                content = getattr(cls, '_content_type').fromDict(content)
            elif isinstance(content, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    content = [item_type.fromDict(item) if isinstance(item, dict) else item for item in content]
        else:
            content = None
        if 'sender' in data:
            sender = data['sender']
            # Handle nested objects based on type
            if isinstance(sender, dict) and hasattr(cls, '_sender_type'):
                sender = getattr(cls, '_sender_type').fromDict(sender)
            elif isinstance(sender, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    sender = [item_type.fromDict(item) if isinstance(item, dict) else item for item in sender]
        else:
            sender = None
        return cls(content, sender)

@dataclass
class Message_Image:
    url: str
    width: int
    height: int
    def toJSON(self) -> str:
        def _serialize(obj):
            if hasattr(obj, '__dict__'):
                result = {}
                for key, value in obj.__dict__.items():
                    result[key] = _serialize(value)
                return result
            elif isinstance(obj, list):
                return [_serialize(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: _serialize(v) for k, v in obj.items()}
            elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')):
                return json.loads(obj.toJSON())
            elif hasattr(obj, 'value') and isinstance(obj, Enum):
                return obj.name
            elif isinstance(obj, Enum):
                return obj.name
            return obj
        return json.dumps(_serialize(self), indent=2)

    @classmethod
    def fromJSON(cls, json_str):
        """Deserialize JSON string to a new instance"""
        data = json.loads(json_str)
        return cls.fromDict(data)

    @classmethod
    def fromDict(cls, data):
        """Create an instance from a dictionary"""
        if 'url' in data:
            url = data['url']
            # Handle nested objects based on type
            if isinstance(url, dict) and hasattr(cls, '_url_type'):
                url = getattr(cls, '_url_type').fromDict(url)
            elif isinstance(url, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    url = [item_type.fromDict(item) if isinstance(item, dict) else item for item in url]
        else:
            url = None
        if 'width' in data:
            width = data['width']
            # Handle nested objects based on type
            if isinstance(width, dict) and hasattr(cls, '_width_type'):
                width = getattr(cls, '_width_type').fromDict(width)
            elif isinstance(width, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    width = [item_type.fromDict(item) if isinstance(item, dict) else item for item in width]
        else:
            width = None
        if 'height' in data:
            height = data['height']
            # Handle nested objects based on type
            if isinstance(height, dict) and hasattr(cls, '_height_type'):
                height = getattr(cls, '_height_type').fromDict(height)
            elif isinstance(height, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    height = [item_type.fromDict(item) if isinstance(item, dict) else item for item in height]
        else:
            height = None
        return cls(url, width, height)

@dataclass
class Message_File:
    field_0: str
    def toJSON(self) -> str:
        def _serialize(obj):
            if hasattr(obj, '__dict__'):
                result = {}
                for key, value in obj.__dict__.items():
                    result[key] = _serialize(value)
                return result
            elif isinstance(obj, list):
                return [_serialize(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: _serialize(v) for k, v in obj.items()}
            elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')):
                return json.loads(obj.toJSON())
            elif hasattr(obj, 'value') and isinstance(obj, Enum):
                return obj.name
            elif isinstance(obj, Enum):
                return obj.name
            return obj
        return json.dumps(_serialize(self), indent=2)

    @classmethod
    def fromJSON(cls, json_str):
        """Deserialize JSON string to a new instance"""
        data = json.loads(json_str)
        return cls.fromDict(data)

    @classmethod
    def fromDict(cls, data):
        """Create an instance from a dictionary"""
        # For tuple variant, create from positional data
        if isinstance(data, list):
            # Expect a list of 1 items
            return cls(*data[:1])
        else:
            # Extract fields from dictionary
            field_0 = data.get('field_0', None)
            return cls(field_0)

class Message(Enum):
    Text = Message_Text  # Complex variant with fields
    Image = Message_Image  # Complex variant with fields
    File = Message_File  # Complex variant with fields

    @classmethod
    def create_message(cls, variant_name: str, **kwargs):
        """Helper to create a variant instance with fields"""
        for variant in cls:
            if variant.name.lower() == variant_name.lower():
                if variant == cls.Text:
                    return Message_Text(**kwargs)
                if variant == cls.Image:
                    return Message_Image(**kwargs)
                if variant == cls.File:
                    return Message_File(**kwargs)
        raise ValueError(f"Unknown variant {variant_name}")

    def toJSON(self) -> str:
        if isinstance(self.value, (int, str, bool, float)):
            return json.dumps({"type": self.name})
        if hasattr(self.value, 'toJSON') and callable(getattr(self.value, 'toJSON')):
            # For complex variants, we merge the variant type with the inner value
            inner_data = json.loads(self.value.toJSON())
            if isinstance(inner_data, dict):
                inner_data["type"] = self.name
                return json.dumps(inner_data)
        return json.dumps({"type": self.name})

    @classmethod
    def fromJSON(cls, json_str):
        """Deserialize JSON string to an enum instance"""
        data = json.loads(json_str)
        if isinstance(data, str):
            # Simple enum with string value
            return cls[data]  # Get enum by name
        elif isinstance(data, dict):
            # Complex enum with fields
            if "type" in data:
                variant_name = data["type"]
                variant = cls[variant_name]  # Get enum variant by name
                
                # For complex variants with associated data
                if hasattr(variant.value, 'fromDict') and callable(getattr(variant.value, 'fromDict')):
                    # Create data object from the dictionary (excluding the type field)
                    variant_data = {k: v for k, v in data.items() if k != "type"}
                    return variant.value.__class__.fromDict(variant_data)
                
                return variant
        # Default fallback - return first variant
        return next(iter(cls))
