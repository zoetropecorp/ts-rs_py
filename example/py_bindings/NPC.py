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
    from DialogueNode import DialogueNode
    from NPCGameData import NPCGameData
    from Orientation import Orientation
    from Position import Position
    from TYPE import TYPE
    from uuid import UUID as Uuid

class NPC:
    id: Uuid
    faction: Optional[Uuid]
    game_data: NPCGameData
    dialogue: Optional[DialogueNode]
    spawn_position: Optional[Position]
    spawn_orientation: Optional[Orientation]





    def __init__(self, id, faction, game_data, dialogue, spawn_position, spawn_orientation):
        self.id = id
        self.faction = faction
        self.game_data = game_data
        self.dialogue = dialogue
        self.spawn_position = spawn_position
        self.spawn_orientation = spawn_orientation

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
        if 'faction' in data:
            faction = data['faction']
            # Handle nested objects based on type
            if isinstance(faction, dict) and hasattr(cls, '_faction_type'):
                faction = getattr(cls, '_faction_type').fromDict(faction)
            elif isinstance(faction, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    faction = [item_type.fromDict(item) if isinstance(item, dict) else item for item in faction]
        else:
            faction = None
        if 'game_data' in data:
            game_data = data['game_data']
            # Handle nested objects based on type
            if isinstance(game_data, dict) and hasattr(cls, '_game_data_type'):
                game_data = getattr(cls, '_game_data_type').fromDict(game_data)
            elif isinstance(game_data, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    game_data = [item_type.fromDict(item) if isinstance(item, dict) else item for item in game_data]
        else:
            game_data = None
        if 'dialogue' in data:
            dialogue = data['dialogue']
            # Handle nested objects based on type
            if isinstance(dialogue, dict) and hasattr(cls, '_dialogue_type'):
                dialogue = getattr(cls, '_dialogue_type').fromDict(dialogue)
            elif isinstance(dialogue, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    dialogue = [item_type.fromDict(item) if isinstance(item, dict) else item for item in dialogue]
        else:
            dialogue = None
        if 'spawn_position' in data:
            spawn_position = data['spawn_position']
            # Handle nested objects based on type
            if isinstance(spawn_position, dict) and hasattr(cls, '_spawn_position_type'):
                spawn_position = getattr(cls, '_spawn_position_type').fromDict(spawn_position)
            elif isinstance(spawn_position, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    spawn_position = [item_type.fromDict(item) if isinstance(item, dict) else item for item in spawn_position]
        else:
            spawn_position = None
        if 'spawn_orientation' in data:
            spawn_orientation = data['spawn_orientation']
            # Handle nested objects based on type
            if isinstance(spawn_orientation, dict) and hasattr(cls, '_spawn_orientation_type'):
                spawn_orientation = getattr(cls, '_spawn_orientation_type').fromDict(spawn_orientation)
            elif isinstance(spawn_orientation, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    spawn_orientation = [item_type.fromDict(item) if isinstance(item, dict) else item for item in spawn_orientation]
        else:
            spawn_orientation = None
        return cls(id, faction, game_data, dialogue, spawn_position, spawn_orientation)
