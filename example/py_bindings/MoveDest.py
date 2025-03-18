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
    from MoveDest import MoveDest
    from MoveDest_Entity import MoveDest_Entity
    from MoveDest_Position import MoveDest_Position
    from Path( import Path(
    from Position import Position
    from TYPE import TYPE
    from uuid import UUID as Uuid

class MoveDest_Entity:
    entity_id: Uuid



    field_0: Position



    Entity = MoveDest_Entity  # Complex variant with fields
    Position = MoveDest_Position  # Complex variant with fields




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
class MoveDest_Entity:
    entity_id: Uuid
    def toJSON(self) -> str: 
    def _serialize(obj): 
    if hasattr(obj, '__dict__'): 
    for key, value in obj.__dict__.items(): 
    elif isinstance(obj, list): 
    elif isinstance(obj, dict): 
    return {k: _serialize(v) for k, v in obj.items()}
    elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')): 
    elif hasattr(obj, 'value') and isinstance(obj, Enum): 
    elif isinstance(obj, Enum): 
    def fromJSON(cls, json_str): 
    def fromDict(cls, data): 
    if 'entity_id' in data: 
    if isinstance(entity_id, dict) and hasattr(cls, '_entity_id_type'): 
    elif isinstance(entity_id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, entity_id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'entity_id' in data, if isinstance(entity_id, dict) and hasattr(cls, '_entity_id_type'), elif isinstance(entity_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.entity_id = entity_id
        self.def toJSON(self) -> str = def toJSON(self) -> str
        self.def _serialize(obj) = def _serialize(obj)
        self.if hasattr(obj, '__dict__') = if hasattr(obj, '__dict__')
        self.for key, value in obj.__dict__.items() = for key, value in obj.__dict__.items()
        self.elif isinstance(obj, list) = elif isinstance(obj, list)
        self.elif isinstance(obj, dict) = elif isinstance(obj, dict)
        self.return {k = return {k
        self.elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')) = elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON'))
        self.elif hasattr(obj, 'value') and isinstance(obj, Enum) = elif hasattr(obj, 'value') and isinstance(obj, Enum)
        self.elif isinstance(obj, Enum) = elif isinstance(obj, Enum)
        self.def fromJSON(cls, json_str) = def fromJSON(cls, json_str)
        self.def fromDict(cls, data) = def fromDict(cls, data)
        self.if 'entity_id' in data = if 'entity_id' in data
        self.if isinstance(entity_id, dict) and hasattr(cls, '_entity_id_type') = if isinstance(entity_id, dict) and hasattr(cls, '_entity_id_type')
        self.elif isinstance(entity_id, list) and hasattr(cls, '_item_type') = elif isinstance(entity_id, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else

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
        entity_id = data.get('entity_id', None)
        if isinstance(entity_id, dict) and 'Uuid' in locals():
            entity_id = Uuid.fromDict(entity_id)
        elif isinstance(entity_id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                entity_id = Uuid[entity_id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        def toJSON(self) -> str = data.get('def toJSON(self) -> str', None)
        def _serialize(obj) = data.get('def _serialize(obj)', None)
        if hasattr(obj, '__dict__') = data.get('if hasattr(obj, '__dict__')', None)
        for key, value in obj.__dict__.items() = data.get('for key, value in obj.__dict__.items()', None)
        elif isinstance(obj, list) = data.get('elif isinstance(obj, list)', None)
        elif isinstance(obj, dict) = data.get('elif isinstance(obj, dict)', None)
        return {k = data.get('return {k', None)
        elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')) = data.get('elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON'))', None)
        elif hasattr(obj, 'value') and isinstance(obj, Enum) = data.get('elif hasattr(obj, 'value') and isinstance(obj, Enum)', None)
        elif isinstance(obj, Enum) = data.get('elif isinstance(obj, Enum)', None)
        def fromJSON(cls, json_str) = data.get('def fromJSON(cls, json_str)', None)
        def fromDict(cls, data) = data.get('def fromDict(cls, data)', None)
        if 'entity_id' in data = data.get('if 'entity_id' in data', None)
        if isinstance(entity_id, dict) and hasattr(cls, '_entity_id_type') = data.get('if isinstance(entity_id, dict) and hasattr(cls, '_entity_id_type')', None)
        elif isinstance(entity_id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(entity_id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(entity_id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'entity_id' in data, if isinstance(entity_id, dict) and hasattr(cls, '_entity_id_type'), elif isinstance(entity_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class MoveDest_Position:
    field_0: Position
    def toJSON(self) -> str: 
    def _serialize(obj): 
    if hasattr(obj, '__dict__'): 
    for key, value in obj.__dict__.items(): 
    elif isinstance(obj, list): 
    elif isinstance(obj, dict): 
    return {k: _serialize(v) for k, v in obj.items()}
    elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')): 
    elif hasattr(obj, 'value') and isinstance(obj, Enum): 
    elif isinstance(obj, Enum): 
    def fromJSON(cls, json_str): 
    def fromDict(cls, data): 
    if isinstance(data, list): 
    return cls(*data[: 1])
    else: 

    def __init__(self, field_0, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if isinstance(data, list), return cls(*data[, else):
        self.field_0 = field_0
        self.def toJSON(self) -> str = def toJSON(self) -> str
        self.def _serialize(obj) = def _serialize(obj)
        self.if hasattr(obj, '__dict__') = if hasattr(obj, '__dict__')
        self.for key, value in obj.__dict__.items() = for key, value in obj.__dict__.items()
        self.elif isinstance(obj, list) = elif isinstance(obj, list)
        self.elif isinstance(obj, dict) = elif isinstance(obj, dict)
        self.return {k = return {k
        self.elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')) = elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON'))
        self.elif hasattr(obj, 'value') and isinstance(obj, Enum) = elif hasattr(obj, 'value') and isinstance(obj, Enum)
        self.elif isinstance(obj, Enum) = elif isinstance(obj, Enum)
        self.def fromJSON(cls, json_str) = def fromJSON(cls, json_str)
        self.def fromDict(cls, data) = def fromDict(cls, data)
        self.if isinstance(data, list) = if isinstance(data, list)
        self.return cls(*data[ = return cls(*data[
        self.else = else

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
        # Import Position type at runtime
        try:
            from Position import Position
        except ImportError:
            pass  # Type not available, will use generic handling
        field_0 = data.get('field_0', None)
        if isinstance(field_0, dict) and 'Position' in locals():
            field_0 = Position.fromDict(field_0)
        elif isinstance(field_0, str) and 'Position' in locals() and hasattr(Position, '__contains__'):
            try:
                field_0 = Position[field_0]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        def toJSON(self) -> str = data.get('def toJSON(self) -> str', None)
        def _serialize(obj) = data.get('def _serialize(obj)', None)
        if hasattr(obj, '__dict__') = data.get('if hasattr(obj, '__dict__')', None)
        for key, value in obj.__dict__.items() = data.get('for key, value in obj.__dict__.items()', None)
        elif isinstance(obj, list) = data.get('elif isinstance(obj, list)', None)
        elif isinstance(obj, dict) = data.get('elif isinstance(obj, dict)', None)
        return {k = data.get('return {k', None)
        elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')) = data.get('elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON'))', None)
        elif hasattr(obj, 'value') and isinstance(obj, Enum) = data.get('elif hasattr(obj, 'value') and isinstance(obj, Enum)', None)
        elif isinstance(obj, Enum) = data.get('elif isinstance(obj, Enum)', None)
        def fromJSON(cls, json_str) = data.get('def fromJSON(cls, json_str)', None)
        def fromDict(cls, data) = data.get('def fromDict(cls, data)', None)
        if isinstance(data, list) = data.get('if isinstance(data, list)', None)
        return cls(*data[ = data.get('return cls(*data[', None)
        else = data.get('else', None)
        return cls(field_0, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if isinstance(data, list), return cls(*data[, else)

# The main MoveDest class
class MoveDest(Enum):
    Entity = MoveDest_Entity
    Position = MoveDest_Position
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
                if variant.name == "Entity":
                    try:
                        return MoveDest_Entity.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "Position":
                    try:
                        return MoveDest_Position.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "if variant.name.lower()":
                    try:
                        return MoveDest_if variant.name.lower().fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "inner_data":
                    try:
                        return MoveDest_inner_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "inner_data["type"]":
                    try:
                        return MoveDest_inner_data["type"].fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "data":
                    try:
                        return MoveDest_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_name":
                    try:
                        return MoveDest_variant_name.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant":
                    try:
                        return MoveDest_variant.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_data":
                    try:
                        return MoveDest_variant_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
        # If not found, return the first variant as a fallback
        return next(iter(cls))
