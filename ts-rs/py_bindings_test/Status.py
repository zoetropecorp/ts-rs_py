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
    pass  # Type checking imports will use annotations


class Status(Enum):
    Active = 1
    Inactive = 2
    Pending = 3

    def toJSON(self) -> str:
        return json.dumps(self.name)

    @classmethod
    def fromJSON(cls, json_str):
        """Deserialize JSON string to an enum instance"""
        data = json.loads(json_str)
        if isinstance(data, str):
            return cls[data]  # Get enum by name
        elif isinstance(data, int):
            # Get enum by value if it's an integer
            for enum_item in cls:
                if enum_item.value == data:
                    return enum_item
        # Default fallback - return first variant
        return next(iter(cls))
