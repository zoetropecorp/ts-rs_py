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
    from CyberpunkNPCData import CyberpunkNPCData
    from NPCGameData import NPCGameData
    from NPCGameData_Cyberpunk import NPCGameData_Cyberpunk
    from NPCGameData_Skyrim import NPCGameData_Skyrim
    from SkyrimNPCData import SkyrimNPCData
    from TYPE import TYPE

class NPCGameData_Skyrim:
    field_0: SkyrimNPCData



    field_0: CyberpunkNPCData



    Skyrim = NPCGameData_Skyrim  # Complex variant with fields
    Cyberpunk = NPCGameData_Cyberpunk  # Complex variant with fields




                # For complex variants with associated data
                if hasattr(variant.value, 'fromDict') and callable(getattr(variant.value, 'fromDict')):
                    # Create data object from the dictionary (excluding the type field)
                    variant_data = {k: v for k, v in data.items() if k != "type"}
                    return variant.value.__class__.fromDict(variant_data)

                return variant
        # Default fallback - return first variant
        return next(iter(cls))
# Classes for complex enum variants
@dataclass
class NPCGameData_Skyrim:
    field_0: SkyrimNPCData

    def __init__(self, field_0):
        self.field_0 = field_0

    def toJSON(self) -> str:
        """Serialize this object to a JSON string"""
        return json.dumps(self._serialize())

    def _serialize(self):
        """Convert this object to a serializable dictionary"""
        result = {}
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
            elif isinstance(value, Enum):
                result[key] = value.name
            else:
                result[key] = value
        return result

    @classmethod
    def fromDict(cls, data):
        """Create an instance from a dictionary"""
        # Import SkyrimNPCData type at runtime
        try:
            from SkyrimNPCData import SkyrimNPCData
        except ImportError:
            pass  # Type not available, will use generic handling
        field_0 = data.get('field_0', None)
        if isinstance(field_0, dict) and 'SkyrimNPCData' in locals():
            field_0 = SkyrimNPCData.fromDict(field_0)
        elif isinstance(field_0, str) and 'SkyrimNPCData' in locals() and hasattr(SkyrimNPCData, '__contains__'):
            try:
                field_0 = SkyrimNPCData[field_0]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        # Filter out method definitions and only pass actual field values
        return cls(field_0)

@dataclass
class NPCGameData_Cyberpunk:
    field_0: CyberpunkNPCData

    def __init__(self, field_0):
        self.field_0 = field_0

    def toJSON(self) -> str:
        """Serialize this object to a JSON string"""
        return json.dumps(self._serialize())

    def _serialize(self):
        """Convert this object to a serializable dictionary"""
        result = {}
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
            elif isinstance(value, Enum):
                result[key] = value.name
            else:
                result[key] = value
        return result

    @classmethod
    def fromDict(cls, data):
        """Create an instance from a dictionary"""
        # Import CyberpunkNPCData type at runtime
        try:
            from CyberpunkNPCData import CyberpunkNPCData
        except ImportError:
            pass  # Type not available, will use generic handling
        field_0 = data.get('field_0', None)
        if isinstance(field_0, dict) and 'CyberpunkNPCData' in locals():
            field_0 = CyberpunkNPCData.fromDict(field_0)
        elif isinstance(field_0, str) and 'CyberpunkNPCData' in locals() and hasattr(CyberpunkNPCData, '__contains__'):
            try:
                field_0 = CyberpunkNPCData[field_0]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        # Filter out method definitions and only pass actual field values
        return cls(field_0)

# The main NPCGameData class
class NPCGameData(Enum):
    Skyrim = NPCGameData_Skyrim
    Cyberpunk = NPCGameData_Cyberpunk
    if variant.name.lower() = auto()
    inner_data = auto()
    inner_data["type"] = auto()
    data = auto()
    variant_name = auto()
    variant = auto()
    variant_data = auto()

    def toJSON(self) -> str:
        """Serialize this object to a JSON string"""
        return json.dumps(self._serialize())

    def _serialize(self):
        """Convert this object to a serializable dictionary"""
        # Complex enum serialization - the self is the Enum instance
        if isinstance(self.value, (int, str, bool, float)):
            return {"type": self.name}
        
        # If the value is a variant class, serialize it and add the type tag
        if hasattr(self.value, '__dict__'):
            # Start with the variant name
            result = {"type": self.name}
            
            # Add all fields from the variant value
            for key, value in self.value.__dict__.items():
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
                elif isinstance(value, Enum):
                    result[key] = value.name
                else:
                    result[key] = value
            return result
        
        # If it's a simple enum instance, just return the name
        return {"type": self.name}

    @classmethod
    def fromJSON(cls, json_str):
        """Deserialize JSON string to a new instance"""
        data = json.loads(json_str)
        return cls.fromDict(data)

    @classmethod
    def fromDict(cls, data):
        """Create a complex enum instance from a dictionary"""
        if isinstance(data, dict):
            # Complex enum with fields
            if "type" in data:
                variant_name = data["type"]
                # Find the enum variant by name
                try:
                    variant = cls[variant_name]
                    
                    # If the variant value is a class, get a new instance
                    if hasattr(variant.value, 'fromDict'):
                        # Create data object from the dictionary (excluding the type field)
                        variant_data = {k: v for k, v in data.items() if k != "type"}
                        return variant.value.fromDict(variant_data)
                    
                    return variant
                except (KeyError, ValueError):
                    # Use the helper method if direct lookup fails
                    variant_data = {k: v for k, v in data.items() if k != "type"}
                    return cls.create_variant(variant_name, **variant_data)
        elif isinstance(data, str):
            # Simple enum name
            try:
                return cls[data]  # Get enum by name
            except (KeyError, ValueError):
                pass
        # Default fallback
        return next(iter(cls))

    @classmethod
    def create_variant(cls, variant_name, **kwargs):
        """Helper method to create a variant with associated data"""
        # Find the correct variant
        for variant in cls:
            if variant.name.lower() == variant_name.lower():
                if variant.name == "Skyrim":
                    try:
                        return NPCGameData_Skyrim.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "Cyberpunk":
                    try:
                        return NPCGameData_Cyberpunk.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "inner_data":
                    try:
                        return NPCGameData_inner_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "data":
                    try:
                        return NPCGameData_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_name":
                    try:
                        return NPCGameData_variant_name.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant":
                    try:
                        return NPCGameData_variant.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_data":
                    try:
                        return NPCGameData_variant_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
        # If not found, return the first variant as a fallback
        return next(iter(cls))
