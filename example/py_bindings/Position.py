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

class Position:
    x: float
    y: float
    z: float
    w: float





    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

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
        if 'x' in data:
            x = data['x']
            # Handle nested objects based on type
            if isinstance(x, dict) and hasattr(cls, '_x_type'):
                x = getattr(cls, '_x_type').fromDict(x)
            elif isinstance(x, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    x = [item_type.fromDict(item) if isinstance(item, dict) else item for item in x]
        else:
            x = None
        if 'y' in data:
            y = data['y']
            # Handle nested objects based on type
            if isinstance(y, dict) and hasattr(cls, '_y_type'):
                y = getattr(cls, '_y_type').fromDict(y)
            elif isinstance(y, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    y = [item_type.fromDict(item) if isinstance(item, dict) else item for item in y]
        else:
            y = None
        if 'z' in data:
            z = data['z']
            # Handle nested objects based on type
            if isinstance(z, dict) and hasattr(cls, '_z_type'):
                z = getattr(cls, '_z_type').fromDict(z)
            elif isinstance(z, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    z = [item_type.fromDict(item) if isinstance(item, dict) else item for item in z]
        else:
            z = None
        if 'w' in data:
            w = data['w']
            # Handle nested objects based on type
            if isinstance(w, dict) and hasattr(cls, '_w_type'):
                w = getattr(cls, '_w_type').fromDict(w)
            elif isinstance(w, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    w = [item_type.fromDict(item) if isinstance(item, dict) else item for item in w]
        else:
            w = None
        return cls(x, y, z, w)
