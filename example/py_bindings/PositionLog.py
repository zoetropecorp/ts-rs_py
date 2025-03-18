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
    from Orientation import Orientation
    from Path( import Path(
    from Position import Position
    from TYPE import TYPE
    from uuid import UUID as Uuid

class PositionLog:
    id: Uuid
    group_name: str
    building: str
    room: str
    name: str
    tags_list: List[str]
    description: str
    orientation: Orientation
    position: Position
    deleted_at: Optional[str]





    def __init__(self, id, group_name, building, room, name, tags_list, description, orientation, position, deleted_at):
        self.id = id
        self.group_name = group_name
        self.building = building
        self.room = room
        self.name = name
        self.tags_list = tags_list
        self.description = description
        self.orientation = orientation
        self.position = position
        self.deleted_at = deleted_at

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
        if 'group_name' in data:
            group_name = data['group_name']
            # Handle nested objects based on type
            if isinstance(group_name, dict) and hasattr(cls, '_group_name_type'):
                group_name = getattr(cls, '_group_name_type').fromDict(group_name)
            elif isinstance(group_name, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    group_name = [item_type.fromDict(item) if isinstance(item, dict) else item for item in group_name]
        else:
            group_name = None
        if 'building' in data:
            building = data['building']
            # Handle nested objects based on type
            if isinstance(building, dict) and hasattr(cls, '_building_type'):
                building = getattr(cls, '_building_type').fromDict(building)
            elif isinstance(building, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    building = [item_type.fromDict(item) if isinstance(item, dict) else item for item in building]
        else:
            building = None
        if 'room' in data:
            room = data['room']
            # Handle nested objects based on type
            if isinstance(room, dict) and hasattr(cls, '_room_type'):
                room = getattr(cls, '_room_type').fromDict(room)
            elif isinstance(room, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    room = [item_type.fromDict(item) if isinstance(item, dict) else item for item in room]
        else:
            room = None
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
        if 'tags_list' in data:
            tags_list = data['tags_list']
            # Handle nested objects based on type
            if isinstance(tags_list, dict) and hasattr(cls, '_tags_list_type'):
                tags_list = getattr(cls, '_tags_list_type').fromDict(tags_list)
            elif isinstance(tags_list, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    tags_list = [item_type.fromDict(item) if isinstance(item, dict) else item for item in tags_list]
        else:
            tags_list = None
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
        if 'orientation' in data:
            orientation = data['orientation']
            # Handle nested objects based on type
            if isinstance(orientation, dict) and hasattr(cls, '_orientation_type'):
                orientation = getattr(cls, '_orientation_type').fromDict(orientation)
            elif isinstance(orientation, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    orientation = [item_type.fromDict(item) if isinstance(item, dict) else item for item in orientation]
        else:
            orientation = None
        if 'position' in data:
            position = data['position']
            # Handle nested objects based on type
            if isinstance(position, dict) and hasattr(cls, '_position_type'):
                position = getattr(cls, '_position_type').fromDict(position)
            elif isinstance(position, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    position = [item_type.fromDict(item) if isinstance(item, dict) else item for item in position]
        else:
            position = None
        if 'deleted_at' in data:
            deleted_at = data['deleted_at']
            # Handle nested objects based on type
            if isinstance(deleted_at, dict) and hasattr(cls, '_deleted_at_type'):
                deleted_at = getattr(cls, '_deleted_at_type').fromDict(deleted_at)
            elif isinstance(deleted_at, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    deleted_at = [item_type.fromDict(item) if isinstance(item, dict) else item for item in deleted_at]
        else:
            deleted_at = None
        return cls(id, group_name, building, room, name, tags_list, description, orientation, position, deleted_at)
