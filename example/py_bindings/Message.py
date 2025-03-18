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
    from TYPE import TYPE
    from uuid import UUID as Uuid

class Message:
    id: Uuid
    text: str
    did_send: bool





    def __init__(self, id, text, did_send):
        self.id = id
        self.text = text
        self.did_send = did_send

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
        if 'text' in data:
            text = data['text']
            # Handle nested objects based on type
            if isinstance(text, dict) and hasattr(cls, '_text_type'):
                text = getattr(cls, '_text_type').fromDict(text)
            elif isinstance(text, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    text = [item_type.fromDict(item) if isinstance(item, dict) else item for item in text]
        else:
            text = None
        if 'did_send' in data:
            did_send = data['did_send']
            # Handle nested objects based on type
            if isinstance(did_send, dict) and hasattr(cls, '_did_send_type'):
                did_send = getattr(cls, '_did_send_type').fromDict(did_send)
            elif isinstance(did_send, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    did_send = [item_type.fromDict(item) if isinstance(item, dict) else item for item in did_send]
        else:
            did_send = None
        return cls(id, text, did_send)
