from __future__ import annotations

import json
import sys
from pathlib import Path
from enum import Enum
from typing import Any, Optional, List, Dict, Union, TYPE_CHECKING

# Add current directory to Python path to facilitate imports
_current_file = Path(__file__).resolve()
_current_dir = _current_file.parent
if str(_current_dir) not in sys.path:
    sys.path.append(str(_current_dir))

# Forward references for type checking only
if TYPE_CHECKING:
    pass  # Type checking imports will use annotations

class User:
    id: int
    name: str
    email: str
    active: bool

    def __init__(self, id: int, name: str, email: str, active: bool) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.active = active

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
