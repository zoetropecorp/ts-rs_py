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
    from Trigger import Trigger
    from Trigger_DialogueOptionChosen import Trigger_DialogueOptionChosen
    from Trigger_InProximity import Trigger_InProximity
    from Trigger_NPCKilled import Trigger_NPCKilled
    from Trigger_PhoneReplyChosen import Trigger_PhoneReplyChosen
    from uuid import UUID as Uuid

class Trigger_NPCKilled:
    id: Uuid



    id: Uuid



    id: Uuid



    id: Uuid



    NPCKilled = Trigger_NPCKilled  # Complex variant with fields
    DialogueOptionChosen = Trigger_DialogueOptionChosen  # Complex variant with fields
    InProximity = Trigger_InProximity  # Complex variant with fields
    PhoneReplyChosen = Trigger_PhoneReplyChosen  # Complex variant with fields




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
class Trigger_NPCKilled:
    id: Uuid

    def __init__(self, id):
        self.id = id

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
        # Import Uuid type at runtime
        try:
            from Uuid import Uuid
        except ImportError:
            pass  # Type not available, will use generic handling
        id = data.get('id', None)
        if isinstance(id, dict) and 'Uuid' in locals():
            id = Uuid.fromDict(id)
        elif isinstance(id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                id = Uuid[id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        # Filter out method definitions and only pass actual field values
        return cls(id)

@dataclass
class Trigger_DialogueOptionChosen:
    id: Uuid

    def __init__(self, id):
        self.id = id

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
        # Import Uuid type at runtime
        try:
            from Uuid import Uuid
        except ImportError:
            pass  # Type not available, will use generic handling
        id = data.get('id', None)
        if isinstance(id, dict) and 'Uuid' in locals():
            id = Uuid.fromDict(id)
        elif isinstance(id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                id = Uuid[id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        # Filter out method definitions and only pass actual field values
        return cls(id)

@dataclass
class Trigger_InProximity:
    id: Uuid

    def __init__(self, id):
        self.id = id

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
        # Import Uuid type at runtime
        try:
            from Uuid import Uuid
        except ImportError:
            pass  # Type not available, will use generic handling
        id = data.get('id', None)
        if isinstance(id, dict) and 'Uuid' in locals():
            id = Uuid.fromDict(id)
        elif isinstance(id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                id = Uuid[id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        # Filter out method definitions and only pass actual field values
        return cls(id)

@dataclass
class Trigger_PhoneReplyChosen:
    id: Uuid

    def __init__(self, id):
        self.id = id

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
        # Import Uuid type at runtime
        try:
            from Uuid import Uuid
        except ImportError:
            pass  # Type not available, will use generic handling
        id = data.get('id', None)
        if isinstance(id, dict) and 'Uuid' in locals():
            id = Uuid.fromDict(id)
        elif isinstance(id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                id = Uuid[id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        # Filter out method definitions and only pass actual field values
        return cls(id)

# The main Trigger class
class Trigger(Enum):
    NPCKilled = Trigger_NPCKilled
    DialogueOptionChosen = Trigger_DialogueOptionChosen
    InProximity = Trigger_InProximity
    PhoneReplyChosen = Trigger_PhoneReplyChosen
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
                if variant.name == "NPCKilled":
                    try:
                        return Trigger_NPCKilled.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "DialogueOptionChosen":
                    try:
                        return Trigger_DialogueOptionChosen.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "InProximity":
                    try:
                        return Trigger_InProximity.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "PhoneReplyChosen":
                    try:
                        return Trigger_PhoneReplyChosen.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "inner_data":
                    try:
                        return Trigger_inner_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "data":
                    try:
                        return Trigger_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_name":
                    try:
                        return Trigger_variant_name.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant":
                    try:
                        return Trigger_variant.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_data":
                    try:
                        return Trigger_variant_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
        # If not found, return the first variant as a fallback
        return next(iter(cls))
