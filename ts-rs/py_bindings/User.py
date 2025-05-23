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

class User:
    id: int
    name: str
    email: str
    active: bool





    def __init__(self, id, name, email, active):
        self.id = id
        self.name = name
        self.email = email
        self.active = active

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
        if 'id' in data:
            id = data['id']
            # Handle nested objects based on type
            if isinstance(id, dict) and hasattr(cls, '_id_type'):
                id = getattr(cls, '_id_type').fromDict(id)
            elif isinstance(id, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    id = [item_type.fromDict(item) if isinstance(item, dict) else item for item in id]
        else:
            id = None
        if 'name' in data:
            name = data['name']
            # Handle nested objects based on type
            if isinstance(name, dict) and hasattr(cls, '_name_type'):
                name = getattr(cls, '_name_type').fromDict(name)
            elif isinstance(name, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    name = [item_type.fromDict(item) if isinstance(item, dict) else item for item in name]
        else:
            name = None
        if 'email' in data:
            email = data['email']
            # Handle nested objects based on type
            if isinstance(email, dict) and hasattr(cls, '_email_type'):
                email = getattr(cls, '_email_type').fromDict(email)
            elif isinstance(email, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    email = [item_type.fromDict(item) if isinstance(item, dict) else item for item in email]
        else:
            email = None
        if 'active' in data:
            active = data['active']
            # Handle nested objects based on type
            if isinstance(active, dict) and hasattr(cls, '_active_type'):
                active = getattr(cls, '_active_type').fromDict(active)
            elif isinstance(active, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    active = [item_type.fromDict(item) if isinstance(item, dict) else item for item in active]
        else:
            active = None
        return cls(id, name, email, active)
