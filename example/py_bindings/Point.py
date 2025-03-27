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
    from TYPE import TYPE

class Point:
    time: int
    value: int





    def __init__(self, time, value):
        self.time = time
        self.value = value

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
        if 'time' in data:
            time = data['time']
            # Handle nested objects based on type
            if isinstance(time, dict) and hasattr(cls, '_time_type'):
                time = getattr(cls, '_time_type').fromDict(time)
            elif isinstance(time, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    time = [item_type.fromDict(item) if isinstance(item, dict) else item for item in time]
        else:
            time = None
        if 'value' in data:
            value = data['value']
            # Handle nested objects based on type
            if isinstance(value, dict) and hasattr(cls, '_value_type'):
                value = getattr(cls, '_value_type').fromDict(value)
            elif isinstance(value, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    value = [item_type.fromDict(item) if isinstance(item, dict) else item for item in value]
        else:
            value = None
        return cls(time, value)
