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
    from FactionRelationship import FactionRelationship
    from Relationship import Relationship
    from TYPE import TYPE
    from uuid import UUID as Uuid

class Faction:
    id: Uuid
    relations: List[FactionRelationship]
    player_relations: Relationship





    def __init__(self, id, relations, player_relations):
        self.id = id
        self.relations = relations
        self.player_relations = player_relations

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
        if 'relations' in data:
            relations = data['relations']
            # Handle nested objects based on type
            if isinstance(relations, dict) and hasattr(cls, '_relations_type'):
                relations = getattr(cls, '_relations_type').fromDict(relations)
            elif isinstance(relations, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    relations = [item_type.fromDict(item) if isinstance(item, dict) else item for item in relations]
        else:
            relations = None
        if 'player_relations' in data:
            player_relations = data['player_relations']
            # Handle nested objects based on type
            if isinstance(player_relations, dict) and hasattr(cls, '_player_relations_type'):
                player_relations = getattr(cls, '_player_relations_type').fromDict(player_relations)
            elif isinstance(player_relations, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    player_relations = [item_type.fromDict(item) if isinstance(item, dict) else item for item in player_relations]
        else:
            player_relations = None
        return cls(id, relations, player_relations)
