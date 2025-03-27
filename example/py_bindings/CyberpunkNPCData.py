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

class CyberpunkNPCData:
    faction: str
    record_tweak: str
    template_path: str
    appearance: str





    def __init__(self, faction, record_tweak, template_path, appearance):
        self.faction = faction
        self.record_tweak = record_tweak
        self.template_path = template_path
        self.appearance = appearance

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
        if 'record_tweak' in data:
            record_tweak = data['record_tweak']
            # Handle nested objects based on type
            if isinstance(record_tweak, dict) and hasattr(cls, '_record_tweak_type'):
                record_tweak = getattr(cls, '_record_tweak_type').fromDict(record_tweak)
            elif isinstance(record_tweak, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    record_tweak = [item_type.fromDict(item) if isinstance(item, dict) else item for item in record_tweak]
        else:
            record_tweak = None
        if 'template_path' in data:
            template_path = data['template_path']
            # Handle nested objects based on type
            if isinstance(template_path, dict) and hasattr(cls, '_template_path_type'):
                template_path = getattr(cls, '_template_path_type').fromDict(template_path)
            elif isinstance(template_path, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    template_path = [item_type.fromDict(item) if isinstance(item, dict) else item for item in template_path]
        else:
            template_path = None
        if 'appearance' in data:
            appearance = data['appearance']
            # Handle nested objects based on type
            if isinstance(appearance, dict) and hasattr(cls, '_appearance_type'):
                appearance = getattr(cls, '_appearance_type').fromDict(appearance)
            elif isinstance(appearance, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    appearance = [item_type.fromDict(item) if isinstance(item, dict) else item for item in appearance]
        else:
            appearance = None
        return cls(faction, record_tweak, template_path, appearance)
