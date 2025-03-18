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
    from Gender import Gender
    from Path( import Path(
    from Role import Role
    from TYPE import TYPE
    from User import User
    from uuid import UUID as Uuid

class User:
    user_id: int
    first_name: str
    last_name: str
    role: Role
    family: List[User]
    gender: Gender
    token: Uuid





    def __init__(self, user_id, first_name, last_name, role, family, gender, token):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.family = family
        self.gender = gender
        self.token = token

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
        if 'user_id' in data:
            user_id = data['user_id']
            # Handle nested objects based on type
            if isinstance(user_id, dict) and hasattr(cls, '_user_id_type'):
                user_id = getattr(cls, '_user_id_type').fromDict(user_id)
            elif isinstance(user_id, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    user_id = [item_type.fromDict(item) if isinstance(item, dict) else item for item in user_id]
        else:
            user_id = None
        if 'first_name' in data:
            first_name = data['first_name']
            # Handle nested objects based on type
            if isinstance(first_name, dict) and hasattr(cls, '_first_name_type'):
                first_name = getattr(cls, '_first_name_type').fromDict(first_name)
            elif isinstance(first_name, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    first_name = [item_type.fromDict(item) if isinstance(item, dict) else item for item in first_name]
        else:
            first_name = None
        if 'last_name' in data:
            last_name = data['last_name']
            # Handle nested objects based on type
            if isinstance(last_name, dict) and hasattr(cls, '_last_name_type'):
                last_name = getattr(cls, '_last_name_type').fromDict(last_name)
            elif isinstance(last_name, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    last_name = [item_type.fromDict(item) if isinstance(item, dict) else item for item in last_name]
        else:
            last_name = None
        if 'role' in data:
            role = data['role']
            # Handle nested objects based on type
            if isinstance(role, dict) and hasattr(cls, '_role_type'):
                role = getattr(cls, '_role_type').fromDict(role)
            elif isinstance(role, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    role = [item_type.fromDict(item) if isinstance(item, dict) else item for item in role]
        else:
            role = None
        if 'family' in data:
            family = data['family']
            # Handle nested objects based on type
            if isinstance(family, dict) and hasattr(cls, '_family_type'):
                family = getattr(cls, '_family_type').fromDict(family)
            elif isinstance(family, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    family = [item_type.fromDict(item) if isinstance(item, dict) else item for item in family]
        else:
            family = None
        if 'gender' in data:
            gender = data['gender']
            # Handle nested objects based on type
            if isinstance(gender, dict) and hasattr(cls, '_gender_type'):
                gender = getattr(cls, '_gender_type').fromDict(gender)
            elif isinstance(gender, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    gender = [item_type.fromDict(item) if isinstance(item, dict) else item for item in gender]
        else:
            gender = None
        if 'token' in data:
            token = data['token']
            # Handle nested objects based on type
            if isinstance(token, dict) and hasattr(cls, '_token_type'):
                token = getattr(cls, '_token_type').fromDict(token)
            elif isinstance(token, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    token = [item_type.fromDict(item) if isinstance(item, dict) else item for item in token]
        else:
            token = None
        return cls(user_id, first_name, last_name, role, family, gender, token)
