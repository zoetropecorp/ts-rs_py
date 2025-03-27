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
    from InlineComplexEnum import InlineComplexEnum
    from TYPE import TYPE

class ComplexStruct2:
    string_tree: Optional[str]
    thing: InlineComplexEnum





    def __init__(self, string_tree, thing):
        self.string_tree = string_tree
        self.thing = thing

    def toJSON(self) -> str:
        """Serialize this object to a JSON string"""
        return json.dumps(self._serialize())

    def _serialize(self):
        """Convert this object to a serializable dictionary"""
        result = {}
        # Process all fields on this object
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
            elif hasattr(value, 'toJSON') and callable(getattr(value, 'toJSON')):
                result[key] = json.loads(value.toJSON())
            elif isinstance(value, Enum):
                result[key] = value.name
            else:
                result[key] = value
        return result

    @classmethod
    def fromJSON(cls, json_str):
        """Deserialize JSON string to a new instance"""
        data = json.loads(json_str)
        return cls.fromDict(data)

    @classmethod
    def fromDict(cls, data):
        """Create an instance from a dictionary"""
        if 'string_tree' in data:
            string_tree = data['string_tree']
            # Handle nested objects based on type
            if isinstance(string_tree, dict) and hasattr(cls, '_string_tree_type'):
                string_tree = getattr(cls, '_string_tree_type').fromDict(string_tree)
            elif isinstance(string_tree, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    string_tree = [item_type.fromDict(item) if isinstance(item, dict) else item for item in string_tree]
        else:
            string_tree = None
        if 'thing' in data:
            thing = data['thing']
            # Handle nested objects based on type
            if isinstance(thing, dict) and hasattr(cls, '_thing_type'):
                thing = getattr(cls, '_thing_type').fromDict(thing)
            elif isinstance(thing, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    thing = [item_type.fromDict(item) if isinstance(item, dict) else item for item in thing]
        else:
            thing = None
        return cls(string_tree, thing)
