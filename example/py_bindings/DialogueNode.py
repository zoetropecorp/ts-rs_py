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
    from Path( import Path(
    from TYPE import TYPE
    from uuid import UUID as Uuid

class DialogueNode:
    id: Uuid
    player_dialogue: Optional[str]
    npc_dialogue: str
    options: List[DialogueNode]





    def __init__(self, id, player_dialogue, npc_dialogue, options):
        self.id = id
        self.player_dialogue = player_dialogue
        self.npc_dialogue = npc_dialogue
        self.options = options

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
        if 'player_dialogue' in data:
            player_dialogue = data['player_dialogue']
            # Handle nested objects based on type
            if isinstance(player_dialogue, dict) and hasattr(cls, '_player_dialogue_type'):
                player_dialogue = getattr(cls, '_player_dialogue_type').fromDict(player_dialogue)
            elif isinstance(player_dialogue, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    player_dialogue = [item_type.fromDict(item) if isinstance(item, dict) else item for item in player_dialogue]
        else:
            player_dialogue = None
        if 'npc_dialogue' in data:
            npc_dialogue = data['npc_dialogue']
            # Handle nested objects based on type
            if isinstance(npc_dialogue, dict) and hasattr(cls, '_npc_dialogue_type'):
                npc_dialogue = getattr(cls, '_npc_dialogue_type').fromDict(npc_dialogue)
            elif isinstance(npc_dialogue, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    npc_dialogue = [item_type.fromDict(item) if isinstance(item, dict) else item for item in npc_dialogue]
        else:
            npc_dialogue = None
        if 'options' in data:
            options = data['options']
            # Handle nested objects based on type
            if isinstance(options, dict) and hasattr(cls, '_options_type'):
                options = getattr(cls, '_options_type').fromDict(options)
            elif isinstance(options, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    options = [item_type.fromDict(item) if isinstance(item, dict) else item for item in options]
        else:
            options = None
        return cls(id, player_dialogue, npc_dialogue, options)
