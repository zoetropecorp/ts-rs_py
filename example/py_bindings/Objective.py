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
    from Path( import Path(
    from Position import Position
    from TYPE import TYPE
    from uuid import UUID as Uuid

class Objective:
    id: Uuid
    description: str
    optional: bool
    total_count: Optional[int]
    location: Position





    def __init__(self, id, description, optional, total_count, location):
        self.id = id
        self.description = description
        self.optional = optional
        self.total_count = total_count
        self.location = location

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
        if 'description' in data:
            description = data['description']
            # Handle nested objects based on type
            if isinstance(description, dict) and hasattr(cls, '_description_type'):
                description = getattr(cls, '_description_type').fromDict(description)
            elif isinstance(description, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    description = [item_type.fromDict(item) if isinstance(item, dict) else item for item in description]
        else:
            description = None
        if 'optional' in data:
            optional = data['optional']
            # Handle nested objects based on type
            if isinstance(optional, dict) and hasattr(cls, '_optional_type'):
                optional = getattr(cls, '_optional_type').fromDict(optional)
            elif isinstance(optional, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    optional = [item_type.fromDict(item) if isinstance(item, dict) else item for item in optional]
        else:
            optional = None
        if 'total_count' in data:
            total_count = data['total_count']
            # Handle nested objects based on type
            if isinstance(total_count, dict) and hasattr(cls, '_total_count_type'):
                total_count = getattr(cls, '_total_count_type').fromDict(total_count)
            elif isinstance(total_count, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    total_count = [item_type.fromDict(item) if isinstance(item, dict) else item for item in total_count]
        else:
            total_count = None
        if 'location' in data:
            location = data['location']
            # Handle nested objects based on type
            if isinstance(location, dict) and hasattr(cls, '_location_type'):
                location = getattr(cls, '_location_type').fromDict(location)
            elif isinstance(location, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    location = [item_type.fromDict(item) if isinstance(item, dict) else item for item in location]
        else:
            location = None
        return cls(id, description, optional, total_count, location)
