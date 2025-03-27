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

class SkyrimNPCData:
    ref_id: int
    cell_id: int
    worldspace_id: Optional[int]





    def __init__(self, ref_id, cell_id, worldspace_id):
        self.ref_id = ref_id
        self.cell_id = cell_id
        self.worldspace_id = worldspace_id

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
        if 'ref_id' in data:
            ref_id = data['ref_id']
            # Handle nested objects based on type
            if isinstance(ref_id, dict) and hasattr(cls, '_ref_id_type'):
                ref_id = getattr(cls, '_ref_id_type').fromDict(ref_id)
            elif isinstance(ref_id, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    ref_id = [item_type.fromDict(item) if isinstance(item, dict) else item for item in ref_id]
        else:
            ref_id = None
        if 'cell_id' in data:
            cell_id = data['cell_id']
            # Handle nested objects based on type
            if isinstance(cell_id, dict) and hasattr(cls, '_cell_id_type'):
                cell_id = getattr(cls, '_cell_id_type').fromDict(cell_id)
            elif isinstance(cell_id, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    cell_id = [item_type.fromDict(item) if isinstance(item, dict) else item for item in cell_id]
        else:
            cell_id = None
        if 'worldspace_id' in data:
            worldspace_id = data['worldspace_id']
            # Handle nested objects based on type
            if isinstance(worldspace_id, dict) and hasattr(cls, '_worldspace_id_type'):
                worldspace_id = getattr(cls, '_worldspace_id_type').fromDict(worldspace_id)
            elif isinstance(worldspace_id, list) and hasattr(cls, '_item_type'):
                item_type = getattr(cls, '_item_type')
                if hasattr(item_type, 'fromDict'):
                    worldspace_id = [item_type.fromDict(item) if isinstance(item, dict) else item for item in worldspace_id]
        else:
            worldspace_id = None
        return cls(ref_id, cell_id, worldspace_id)
