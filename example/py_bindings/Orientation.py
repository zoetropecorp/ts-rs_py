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

class Orientation:
    i: float
    k: float
    r: float
    j: float





    def __init__(self, i, k, r, j):
        self.i = i
        self.k = k
        self.r = r
        self.j = j

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
        if 'i' in data:
            i = data['i']
            # Handle nested objects based on type
            if isinstance(i, dict) and hasattr(cls, '_i_type'):
                i = getattr(cls, '_i_type').fromDict(i)
            elif isinstance(i, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    i = [item_type.fromDict(item) if isinstance(item, dict) else item for item in i]
        else:
            i = None
        if 'k' in data:
            k = data['k']
            # Handle nested objects based on type
            if isinstance(k, dict) and hasattr(cls, '_k_type'):
                k = getattr(cls, '_k_type').fromDict(k)
            elif isinstance(k, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    k = [item_type.fromDict(item) if isinstance(item, dict) else item for item in k]
        else:
            k = None
        if 'r' in data:
            r = data['r']
            # Handle nested objects based on type
            if isinstance(r, dict) and hasattr(cls, '_r_type'):
                r = getattr(cls, '_r_type').fromDict(r)
            elif isinstance(r, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    r = [item_type.fromDict(item) if isinstance(item, dict) else item for item in r]
        else:
            r = None
        if 'j' in data:
            j = data['j']
            # Handle nested objects based on type
            if isinstance(j, dict) and hasattr(cls, '_j_type'):
                j = getattr(cls, '_j_type').fromDict(j)
            elif isinstance(j, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    j = [item_type.fromDict(item) if isinstance(item, dict) else item for item in j]
        else:
            j = None
        return cls(i, k, r, j)
