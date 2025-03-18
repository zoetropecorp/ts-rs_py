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
    from ComplexEnum import ComplexEnum
    from ComplexEnum_B import ComplexEnum_B
    from ComplexEnum_F import ComplexEnum_F
    from ComplexEnum_U import ComplexEnum_U
    from ComplexEnum_V import ComplexEnum_V
    from ComplexEnum_W import ComplexEnum_W
    from Path( import Path(
    from Series import Series
    from SimpleEnum import SimpleEnum
    from TYPE import TYPE
    from User import User

class ComplexEnum_B:
    foo: str
    bar: float



    field_0: SimpleEnum



    nested: SimpleEnum



    field_0: Series



    field_0: User



    A = auto()
    B = ComplexEnum_B  # Complex variant with fields
    W = ComplexEnum_W  # Complex variant with fields
    F = ComplexEnum_F  # Complex variant with fields
    V = ComplexEnum_V  # Complex variant with fields
    U = ComplexEnum_U  # Complex variant with fields




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
class ComplexEnum_B:
    foo: str
    bar: float
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
    if 'foo' in data: 
    if isinstance(foo, dict) and hasattr(cls, '_foo_type'): 
    elif isinstance(foo, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'bar' in data: 
    if isinstance(bar, dict) and hasattr(cls, '_bar_type'): 
    elif isinstance(bar, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, foo, bar, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'foo' in data, if isinstance(foo, dict) and hasattr(cls, '_foo_type'), elif isinstance(foo, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'bar' in data, if isinstance(bar, dict) and hasattr(cls, '_bar_type'), elif isinstance(bar, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.foo = foo
        self.bar = bar
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
        self.if 'foo' in data = if 'foo' in data
        self.if isinstance(foo, dict) and hasattr(cls, '_foo_type') = if isinstance(foo, dict) and hasattr(cls, '_foo_type')
        self.elif isinstance(foo, list) and hasattr(cls, '_item_type') = elif isinstance(foo, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'bar' in data = if 'bar' in data
        self.if isinstance(bar, dict) and hasattr(cls, '_bar_type') = if isinstance(bar, dict) and hasattr(cls, '_bar_type')
        self.elif isinstance(bar, list) and hasattr(cls, '_item_type') = elif isinstance(bar, list) and hasattr(cls, '_item_type')
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
        foo = data.get('foo', None)
        bar = data.get('bar', None)
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
        if 'foo' in data = data.get('if 'foo' in data', None)
        if isinstance(foo, dict) and hasattr(cls, '_foo_type') = data.get('if isinstance(foo, dict) and hasattr(cls, '_foo_type')', None)
        elif isinstance(foo, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(foo, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'bar' in data = data.get('if 'bar' in data', None)
        if isinstance(bar, dict) and hasattr(cls, '_bar_type') = data.get('if isinstance(bar, dict) and hasattr(cls, '_bar_type')', None)
        elif isinstance(bar, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(bar, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(foo, bar, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'foo' in data, if isinstance(foo, dict) and hasattr(cls, '_foo_type'), elif isinstance(foo, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'bar' in data, if isinstance(bar, dict) and hasattr(cls, '_bar_type'), elif isinstance(bar, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class ComplexEnum_W:
    field_0: SimpleEnum
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
        # Import SimpleEnum type at runtime
        try:
            from SimpleEnum import SimpleEnum
        except ImportError:
            pass  # Type not available, will use generic handling
        field_0 = data.get('field_0', None)
        if isinstance(field_0, dict) and 'SimpleEnum' in locals():
            field_0 = SimpleEnum.fromDict(field_0)
        elif isinstance(field_0, str) and 'SimpleEnum' in locals() and hasattr(SimpleEnum, '__contains__'):
            try:
                field_0 = SimpleEnum[field_0]
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

@dataclass
class ComplexEnum_F:
    nested: SimpleEnum
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
    if 'nested' in data: 
    if isinstance(nested, dict) and hasattr(cls, '_nested_type'): 
    elif isinstance(nested, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, nested, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'nested' in data, if isinstance(nested, dict) and hasattr(cls, '_nested_type'), elif isinstance(nested, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.nested = nested
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
        self.if 'nested' in data = if 'nested' in data
        self.if isinstance(nested, dict) and hasattr(cls, '_nested_type') = if isinstance(nested, dict) and hasattr(cls, '_nested_type')
        self.elif isinstance(nested, list) and hasattr(cls, '_item_type') = elif isinstance(nested, list) and hasattr(cls, '_item_type')
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
        # Import SimpleEnum type at runtime
        try:
            from SimpleEnum import SimpleEnum
        except ImportError:
            pass  # Type not available, will use generic handling
        nested = data.get('nested', None)
        if isinstance(nested, dict) and 'SimpleEnum' in locals():
            nested = SimpleEnum.fromDict(nested)
        elif isinstance(nested, str) and 'SimpleEnum' in locals() and hasattr(SimpleEnum, '__contains__'):
            try:
                nested = SimpleEnum[nested]
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
        if 'nested' in data = data.get('if 'nested' in data', None)
        if isinstance(nested, dict) and hasattr(cls, '_nested_type') = data.get('if isinstance(nested, dict) and hasattr(cls, '_nested_type')', None)
        elif isinstance(nested, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(nested, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(nested, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'nested' in data, if isinstance(nested, dict) and hasattr(cls, '_nested_type'), elif isinstance(nested, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class ComplexEnum_V:
    field_0: Series
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
        # Import Series type at runtime
        try:
            from Series import Series
        except ImportError:
            pass  # Type not available, will use generic handling
        field_0 = data.get('field_0', None)
        if isinstance(field_0, dict) and 'Series' in locals():
            field_0 = Series.fromDict(field_0)
        elif isinstance(field_0, str) and 'Series' in locals() and hasattr(Series, '__contains__'):
            try:
                field_0 = Series[field_0]
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

@dataclass
class ComplexEnum_U:
    field_0: User
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
        # Import User type at runtime
        try:
            from User import User
        except ImportError:
            pass  # Type not available, will use generic handling
        field_0 = data.get('field_0', None)
        if isinstance(field_0, dict) and 'User' in locals():
            field_0 = User.fromDict(field_0)
        elif isinstance(field_0, str) and 'User' in locals() and hasattr(User, '__contains__'):
            try:
                field_0 = User[field_0]
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

# The main ComplexEnum class
class ComplexEnum(Enum):
    B = ComplexEnum_B
    W = ComplexEnum_W
    F = ComplexEnum_F
    V = ComplexEnum_V
    U = ComplexEnum_U
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
                if variant.name == "B":
                    try:
                        return ComplexEnum_B.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "W":
                    try:
                        return ComplexEnum_W.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "F":
                    try:
                        return ComplexEnum_F.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "V":
                    try:
                        return ComplexEnum_V.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "U":
                    try:
                        return ComplexEnum_U.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "if variant.name.lower()":
                    try:
                        return ComplexEnum_if variant.name.lower().fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "inner_data":
                    try:
                        return ComplexEnum_inner_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "inner_data["type"]":
                    try:
                        return ComplexEnum_inner_data["type"].fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "data":
                    try:
                        return ComplexEnum_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_name":
                    try:
                        return ComplexEnum_variant_name.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant":
                    try:
                        return ComplexEnum_variant.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_data":
                    try:
                        return ComplexEnum_variant_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
        # If not found, return the first variant as a fallback
        return next(iter(cls))
