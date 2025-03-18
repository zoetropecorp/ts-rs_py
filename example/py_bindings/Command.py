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
    from Command import Command
    from Command_AttachDialogue import Command_AttachDialogue
    from Command_CompleteObjective import Command_CompleteObjective
    from Command_CompleteQuest import Command_CompleteQuest
    from Command_CreateContact import Command_CreateContact
    from Command_CreateFactions import Command_CreateFactions
    from Command_CreateObjective import Command_CreateObjective
    from Command_CreateQuest import Command_CreateQuest
    from Command_DeleteContact import Command_DeleteContact
    from Command_DeleteQuest import Command_DeleteQuest
    from Command_DespawnNPCs import Command_DespawnNPCs
    from Command_IncrementObjectiveCounter import Command_IncrementObjectiveCounter
    from Command_Move import Command_Move
    from Command_Print import Command_Print
    from Command_RegisterLocation import Command_RegisterLocation
    from Command_ReplaceChoices import Command_ReplaceChoices
    from Command_SetAttitude import Command_SetAttitude
    from Command_SetOTP import Command_SetOTP
    from Command_SpawnNPCs import Command_SpawnNPCs
    from Command_UnregisterLocation import Command_UnregisterLocation
    from Command_UpdateChoice import Command_UpdateChoice
    from Command_UpdateDialogue import Command_UpdateDialogue
    from Command_UpdateMessage import Command_UpdateMessage
    from Command_UpdatePositionLogs import Command_UpdatePositionLogs
    from Contact import Contact
    from DialogueNode import DialogueNode
    from Faction import Faction
    from Message import Message
    from MoveDest import MoveDest
    from NPC import NPC
    from Objective import Objective
    from Path( import Path(
    from PhoneChoice import PhoneChoice
    from Position import Position
    from PositionLog import PositionLog
    from Quest import Quest
    from TYPE import TYPE
    from uuid import UUID as Uuid

class Command_Move:
    npc_id: Uuid
    dest: Optional[MoveDest]



    npcs: List[NPC]



    npcs: List[Uuid]



    id: Uuid
    attitude: str



    data: str



    id: Uuid
    position: Position
    distance: float



    field_0: DialogueNode



    field_0: Quest



    quest_id: Uuid
    objective: Objective



    id: Uuid
    did_fail: bool



    objective_id: Uuid



    id: Uuid



    id: Uuid



    id: Uuid



    npc_id: Uuid
    dialogue: DialogueNode



    field_0: Contact



    field_0: Message



    field_0: PhoneChoice



    contact_id: Uuid
    messages: List[Message]
    choices: List[PhoneChoice]



    id: Uuid



    otp: Optional[str]



    updated: List[PositionLog]
    deleted: List[Uuid]



    factions: List[Faction]



    Move = Command_Move  # Complex variant with fields
    SpawnNPCs = Command_SpawnNPCs  # Complex variant with fields
    DespawnNPCs = Command_DespawnNPCs  # Complex variant with fields
    SetAttitude = Command_SetAttitude  # Complex variant with fields
    Print = Command_Print  # Complex variant with fields
    ClearNPCs = auto()
    RegisterLocation = Command_RegisterLocation  # Complex variant with fields
    UpdateDialogue = Command_UpdateDialogue  # Complex variant with fields
    CreateQuest = Command_CreateQuest  # Complex variant with fields
    CreateObjective = Command_CreateObjective  # Complex variant with fields
    CompleteObjective = Command_CompleteObjective  # Complex variant with fields
    IncrementObjectiveCounter = Command_IncrementObjectiveCounter  # Complex variant with fields
    CompleteQuest = Command_CompleteQuest  # Complex variant with fields
    DeleteQuest = Command_DeleteQuest  # Complex variant with fields
    UnregisterLocation = Command_UnregisterLocation  # Complex variant with fields
    AttachDialogue = Command_AttachDialogue  # Complex variant with fields
    CreateContact = Command_CreateContact  # Complex variant with fields
    UpdateMessage = Command_UpdateMessage  # Complex variant with fields
    UpdateChoice = Command_UpdateChoice  # Complex variant with fields
    ReplaceChoices = Command_ReplaceChoices  # Complex variant with fields
    DeleteContact = Command_DeleteContact  # Complex variant with fields
    SetOTP = Command_SetOTP  # Complex variant with fields
    UpdatePositionLogs = Command_UpdatePositionLogs  # Complex variant with fields
    CreateFactions = Command_CreateFactions  # Complex variant with fields




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
class Command_Move:
    npc_id: Uuid
    dest: Optional[MoveDest]
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
    if 'npc_id' in data: 
    if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type'): 
    elif isinstance(npc_id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'dest' in data: 
    if isinstance(dest, dict) and hasattr(cls, '_dest_type'): 
    elif isinstance(dest, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, npc_id, dest, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'npc_id' in data, if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type'), elif isinstance(npc_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'dest' in data, if isinstance(dest, dict) and hasattr(cls, '_dest_type'), elif isinstance(dest, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.npc_id = npc_id
        self.dest = dest
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
        self.if 'npc_id' in data = if 'npc_id' in data
        self.if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type') = if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type')
        self.elif isinstance(npc_id, list) and hasattr(cls, '_item_type') = elif isinstance(npc_id, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'dest' in data = if 'dest' in data
        self.if isinstance(dest, dict) and hasattr(cls, '_dest_type') = if isinstance(dest, dict) and hasattr(cls, '_dest_type')
        self.elif isinstance(dest, list) and hasattr(cls, '_item_type') = elif isinstance(dest, list) and hasattr(cls, '_item_type')
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
        npc_id = data.get('npc_id', None)
        if isinstance(npc_id, dict) and 'Uuid' in locals():
            npc_id = Uuid.fromDict(npc_id)
        elif isinstance(npc_id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                npc_id = Uuid[npc_id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        dest = data.get('dest', None)
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
        if 'npc_id' in data = data.get('if 'npc_id' in data', None)
        if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type') = data.get('if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type')', None)
        elif isinstance(npc_id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(npc_id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'dest' in data = data.get('if 'dest' in data', None)
        if isinstance(dest, dict) and hasattr(cls, '_dest_type') = data.get('if isinstance(dest, dict) and hasattr(cls, '_dest_type')', None)
        elif isinstance(dest, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(dest, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(npc_id, dest, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'npc_id' in data, if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type'), elif isinstance(npc_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'dest' in data, if isinstance(dest, dict) and hasattr(cls, '_dest_type'), elif isinstance(dest, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_SpawnNPCs:
    npcs: List[NPC]
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
    if 'npcs' in data: 
    if isinstance(npcs, dict) and hasattr(cls, '_npcs_type'): 
    elif isinstance(npcs, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, npcs, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'npcs' in data, if isinstance(npcs, dict) and hasattr(cls, '_npcs_type'), elif isinstance(npcs, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.npcs = npcs
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
        self.if 'npcs' in data = if 'npcs' in data
        self.if isinstance(npcs, dict) and hasattr(cls, '_npcs_type') = if isinstance(npcs, dict) and hasattr(cls, '_npcs_type')
        self.elif isinstance(npcs, list) and hasattr(cls, '_item_type') = elif isinstance(npcs, list) and hasattr(cls, '_item_type')
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
        npcs = data.get('npcs', None)
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
        if 'npcs' in data = data.get('if 'npcs' in data', None)
        if isinstance(npcs, dict) and hasattr(cls, '_npcs_type') = data.get('if isinstance(npcs, dict) and hasattr(cls, '_npcs_type')', None)
        elif isinstance(npcs, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(npcs, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(npcs, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'npcs' in data, if isinstance(npcs, dict) and hasattr(cls, '_npcs_type'), elif isinstance(npcs, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_DespawnNPCs:
    npcs: List[Uuid]
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
    if 'npcs' in data: 
    if isinstance(npcs, dict) and hasattr(cls, '_npcs_type'): 
    elif isinstance(npcs, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, npcs, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'npcs' in data, if isinstance(npcs, dict) and hasattr(cls, '_npcs_type'), elif isinstance(npcs, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.npcs = npcs
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
        self.if 'npcs' in data = if 'npcs' in data
        self.if isinstance(npcs, dict) and hasattr(cls, '_npcs_type') = if isinstance(npcs, dict) and hasattr(cls, '_npcs_type')
        self.elif isinstance(npcs, list) and hasattr(cls, '_item_type') = elif isinstance(npcs, list) and hasattr(cls, '_item_type')
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
        npcs = data.get('npcs', None)
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
        if 'npcs' in data = data.get('if 'npcs' in data', None)
        if isinstance(npcs, dict) and hasattr(cls, '_npcs_type') = data.get('if isinstance(npcs, dict) and hasattr(cls, '_npcs_type')', None)
        elif isinstance(npcs, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(npcs, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(npcs, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'npcs' in data, if isinstance(npcs, dict) and hasattr(cls, '_npcs_type'), elif isinstance(npcs, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_SetAttitude:
    id: Uuid
    attitude: str
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
    if 'id' in data: 
    if isinstance(id, dict) and hasattr(cls, '_id_type'): 
    elif isinstance(id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'attitude' in data: 
    if isinstance(attitude, dict) and hasattr(cls, '_attitude_type'): 
    elif isinstance(attitude, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, id, attitude, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'attitude' in data, if isinstance(attitude, dict) and hasattr(cls, '_attitude_type'), elif isinstance(attitude, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.id = id
        self.attitude = attitude
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
        self.if 'id' in data = if 'id' in data
        self.if isinstance(id, dict) and hasattr(cls, '_id_type') = if isinstance(id, dict) and hasattr(cls, '_id_type')
        self.elif isinstance(id, list) and hasattr(cls, '_item_type') = elif isinstance(id, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'attitude' in data = if 'attitude' in data
        self.if isinstance(attitude, dict) and hasattr(cls, '_attitude_type') = if isinstance(attitude, dict) and hasattr(cls, '_attitude_type')
        self.elif isinstance(attitude, list) and hasattr(cls, '_item_type') = elif isinstance(attitude, list) and hasattr(cls, '_item_type')
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
        id = data.get('id', None)
        if isinstance(id, dict) and 'Uuid' in locals():
            id = Uuid.fromDict(id)
        elif isinstance(id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                id = Uuid[id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        attitude = data.get('attitude', None)
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
        if 'id' in data = data.get('if 'id' in data', None)
        if isinstance(id, dict) and hasattr(cls, '_id_type') = data.get('if isinstance(id, dict) and hasattr(cls, '_id_type')', None)
        elif isinstance(id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'attitude' in data = data.get('if 'attitude' in data', None)
        if isinstance(attitude, dict) and hasattr(cls, '_attitude_type') = data.get('if isinstance(attitude, dict) and hasattr(cls, '_attitude_type')', None)
        elif isinstance(attitude, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(attitude, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(id, attitude, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'attitude' in data, if isinstance(attitude, dict) and hasattr(cls, '_attitude_type'), elif isinstance(attitude, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_Print:
    data: str
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
    if 'data' in data: 
    if isinstance(data, dict) and hasattr(cls, '_data_type'): 
    elif isinstance(data, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, data, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'data' in data, if isinstance(data, dict) and hasattr(cls, '_data_type'), elif isinstance(data, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.data = data
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
        self.if 'data' in data = if 'data' in data
        self.if isinstance(data, dict) and hasattr(cls, '_data_type') = if isinstance(data, dict) and hasattr(cls, '_data_type')
        self.elif isinstance(data, list) and hasattr(cls, '_item_type') = elif isinstance(data, list) and hasattr(cls, '_item_type')
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
        data = data.get('data', None)
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
        if 'data' in data = data.get('if 'data' in data', None)
        if isinstance(data, dict) and hasattr(cls, '_data_type') = data.get('if isinstance(data, dict) and hasattr(cls, '_data_type')', None)
        elif isinstance(data, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(data, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(data, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'data' in data, if isinstance(data, dict) and hasattr(cls, '_data_type'), elif isinstance(data, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_RegisterLocation:
    id: Uuid
    position: Position
    distance: float
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
    if 'id' in data: 
    if isinstance(id, dict) and hasattr(cls, '_id_type'): 
    elif isinstance(id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'position' in data: 
    if isinstance(position, dict) and hasattr(cls, '_position_type'): 
    elif isinstance(position, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'distance' in data: 
    if isinstance(distance, dict) and hasattr(cls, '_distance_type'): 
    elif isinstance(distance, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, id, position, distance, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'position' in data, if isinstance(position, dict) and hasattr(cls, '_position_type'), elif isinstance(position, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'distance' in data, if isinstance(distance, dict) and hasattr(cls, '_distance_type'), elif isinstance(distance, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.id = id
        self.position = position
        self.distance = distance
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
        self.if 'id' in data = if 'id' in data
        self.if isinstance(id, dict) and hasattr(cls, '_id_type') = if isinstance(id, dict) and hasattr(cls, '_id_type')
        self.elif isinstance(id, list) and hasattr(cls, '_item_type') = elif isinstance(id, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'position' in data = if 'position' in data
        self.if isinstance(position, dict) and hasattr(cls, '_position_type') = if isinstance(position, dict) and hasattr(cls, '_position_type')
        self.elif isinstance(position, list) and hasattr(cls, '_item_type') = elif isinstance(position, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'distance' in data = if 'distance' in data
        self.if isinstance(distance, dict) and hasattr(cls, '_distance_type') = if isinstance(distance, dict) and hasattr(cls, '_distance_type')
        self.elif isinstance(distance, list) and hasattr(cls, '_item_type') = elif isinstance(distance, list) and hasattr(cls, '_item_type')
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
        id = data.get('id', None)
        if isinstance(id, dict) and 'Uuid' in locals():
            id = Uuid.fromDict(id)
        elif isinstance(id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                id = Uuid[id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        # Import Position type at runtime
        try:
            from Position import Position
        except ImportError:
            pass  # Type not available, will use generic handling
        position = data.get('position', None)
        if isinstance(position, dict) and 'Position' in locals():
            position = Position.fromDict(position)
        elif isinstance(position, str) and 'Position' in locals() and hasattr(Position, '__contains__'):
            try:
                position = Position[position]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        distance = data.get('distance', None)
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
        if 'id' in data = data.get('if 'id' in data', None)
        if isinstance(id, dict) and hasattr(cls, '_id_type') = data.get('if isinstance(id, dict) and hasattr(cls, '_id_type')', None)
        elif isinstance(id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'position' in data = data.get('if 'position' in data', None)
        if isinstance(position, dict) and hasattr(cls, '_position_type') = data.get('if isinstance(position, dict) and hasattr(cls, '_position_type')', None)
        elif isinstance(position, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(position, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'distance' in data = data.get('if 'distance' in data', None)
        if isinstance(distance, dict) and hasattr(cls, '_distance_type') = data.get('if isinstance(distance, dict) and hasattr(cls, '_distance_type')', None)
        elif isinstance(distance, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(distance, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(id, position, distance, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'position' in data, if isinstance(position, dict) and hasattr(cls, '_position_type'), elif isinstance(position, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'distance' in data, if isinstance(distance, dict) and hasattr(cls, '_distance_type'), elif isinstance(distance, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_UpdateDialogue:
    field_0: DialogueNode
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
        # Import DialogueNode type at runtime
        try:
            from DialogueNode import DialogueNode
        except ImportError:
            pass  # Type not available, will use generic handling
        field_0 = data.get('field_0', None)
        if isinstance(field_0, dict) and 'DialogueNode' in locals():
            field_0 = DialogueNode.fromDict(field_0)
        elif isinstance(field_0, str) and 'DialogueNode' in locals() and hasattr(DialogueNode, '__contains__'):
            try:
                field_0 = DialogueNode[field_0]
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
class Command_CreateQuest:
    field_0: Quest
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
        # Import Quest type at runtime
        try:
            from Quest import Quest
        except ImportError:
            pass  # Type not available, will use generic handling
        field_0 = data.get('field_0', None)
        if isinstance(field_0, dict) and 'Quest' in locals():
            field_0 = Quest.fromDict(field_0)
        elif isinstance(field_0, str) and 'Quest' in locals() and hasattr(Quest, '__contains__'):
            try:
                field_0 = Quest[field_0]
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
class Command_CreateObjective:
    quest_id: Uuid
    objective: Objective
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
    if 'quest_id' in data: 
    if isinstance(quest_id, dict) and hasattr(cls, '_quest_id_type'): 
    elif isinstance(quest_id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'objective' in data: 
    if isinstance(objective, dict) and hasattr(cls, '_objective_type'): 
    elif isinstance(objective, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, quest_id, objective, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'quest_id' in data, if isinstance(quest_id, dict) and hasattr(cls, '_quest_id_type'), elif isinstance(quest_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'objective' in data, if isinstance(objective, dict) and hasattr(cls, '_objective_type'), elif isinstance(objective, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.quest_id = quest_id
        self.objective = objective
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
        self.if 'quest_id' in data = if 'quest_id' in data
        self.if isinstance(quest_id, dict) and hasattr(cls, '_quest_id_type') = if isinstance(quest_id, dict) and hasattr(cls, '_quest_id_type')
        self.elif isinstance(quest_id, list) and hasattr(cls, '_item_type') = elif isinstance(quest_id, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'objective' in data = if 'objective' in data
        self.if isinstance(objective, dict) and hasattr(cls, '_objective_type') = if isinstance(objective, dict) and hasattr(cls, '_objective_type')
        self.elif isinstance(objective, list) and hasattr(cls, '_item_type') = elif isinstance(objective, list) and hasattr(cls, '_item_type')
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
        quest_id = data.get('quest_id', None)
        if isinstance(quest_id, dict) and 'Uuid' in locals():
            quest_id = Uuid.fromDict(quest_id)
        elif isinstance(quest_id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                quest_id = Uuid[quest_id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        # Import Objective type at runtime
        try:
            from Objective import Objective
        except ImportError:
            pass  # Type not available, will use generic handling
        objective = data.get('objective', None)
        if isinstance(objective, dict) and 'Objective' in locals():
            objective = Objective.fromDict(objective)
        elif isinstance(objective, str) and 'Objective' in locals() and hasattr(Objective, '__contains__'):
            try:
                objective = Objective[objective]
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
        if 'quest_id' in data = data.get('if 'quest_id' in data', None)
        if isinstance(quest_id, dict) and hasattr(cls, '_quest_id_type') = data.get('if isinstance(quest_id, dict) and hasattr(cls, '_quest_id_type')', None)
        elif isinstance(quest_id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(quest_id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'objective' in data = data.get('if 'objective' in data', None)
        if isinstance(objective, dict) and hasattr(cls, '_objective_type') = data.get('if isinstance(objective, dict) and hasattr(cls, '_objective_type')', None)
        elif isinstance(objective, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(objective, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(quest_id, objective, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'quest_id' in data, if isinstance(quest_id, dict) and hasattr(cls, '_quest_id_type'), elif isinstance(quest_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'objective' in data, if isinstance(objective, dict) and hasattr(cls, '_objective_type'), elif isinstance(objective, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_CompleteObjective:
    id: Uuid
    did_fail: bool
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
    if 'id' in data: 
    if isinstance(id, dict) and hasattr(cls, '_id_type'): 
    elif isinstance(id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'did_fail' in data: 
    if isinstance(did_fail, dict) and hasattr(cls, '_did_fail_type'): 
    elif isinstance(did_fail, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, id, did_fail, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'did_fail' in data, if isinstance(did_fail, dict) and hasattr(cls, '_did_fail_type'), elif isinstance(did_fail, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.id = id
        self.did_fail = did_fail
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
        self.if 'id' in data = if 'id' in data
        self.if isinstance(id, dict) and hasattr(cls, '_id_type') = if isinstance(id, dict) and hasattr(cls, '_id_type')
        self.elif isinstance(id, list) and hasattr(cls, '_item_type') = elif isinstance(id, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'did_fail' in data = if 'did_fail' in data
        self.if isinstance(did_fail, dict) and hasattr(cls, '_did_fail_type') = if isinstance(did_fail, dict) and hasattr(cls, '_did_fail_type')
        self.elif isinstance(did_fail, list) and hasattr(cls, '_item_type') = elif isinstance(did_fail, list) and hasattr(cls, '_item_type')
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
        id = data.get('id', None)
        if isinstance(id, dict) and 'Uuid' in locals():
            id = Uuid.fromDict(id)
        elif isinstance(id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                id = Uuid[id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        did_fail = data.get('did_fail', None)
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
        if 'id' in data = data.get('if 'id' in data', None)
        if isinstance(id, dict) and hasattr(cls, '_id_type') = data.get('if isinstance(id, dict) and hasattr(cls, '_id_type')', None)
        elif isinstance(id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'did_fail' in data = data.get('if 'did_fail' in data', None)
        if isinstance(did_fail, dict) and hasattr(cls, '_did_fail_type') = data.get('if isinstance(did_fail, dict) and hasattr(cls, '_did_fail_type')', None)
        elif isinstance(did_fail, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(did_fail, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(id, did_fail, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'did_fail' in data, if isinstance(did_fail, dict) and hasattr(cls, '_did_fail_type'), elif isinstance(did_fail, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_IncrementObjectiveCounter:
    objective_id: Uuid
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
    if 'objective_id' in data: 
    if isinstance(objective_id, dict) and hasattr(cls, '_objective_id_type'): 
    elif isinstance(objective_id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, objective_id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'objective_id' in data, if isinstance(objective_id, dict) and hasattr(cls, '_objective_id_type'), elif isinstance(objective_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.objective_id = objective_id
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
        self.if 'objective_id' in data = if 'objective_id' in data
        self.if isinstance(objective_id, dict) and hasattr(cls, '_objective_id_type') = if isinstance(objective_id, dict) and hasattr(cls, '_objective_id_type')
        self.elif isinstance(objective_id, list) and hasattr(cls, '_item_type') = elif isinstance(objective_id, list) and hasattr(cls, '_item_type')
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
        objective_id = data.get('objective_id', None)
        if isinstance(objective_id, dict) and 'Uuid' in locals():
            objective_id = Uuid.fromDict(objective_id)
        elif isinstance(objective_id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                objective_id = Uuid[objective_id]
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
        if 'objective_id' in data = data.get('if 'objective_id' in data', None)
        if isinstance(objective_id, dict) and hasattr(cls, '_objective_id_type') = data.get('if isinstance(objective_id, dict) and hasattr(cls, '_objective_id_type')', None)
        elif isinstance(objective_id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(objective_id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(objective_id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'objective_id' in data, if isinstance(objective_id, dict) and hasattr(cls, '_objective_id_type'), elif isinstance(objective_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_CompleteQuest:
    id: Uuid
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
    if 'id' in data: 
    if isinstance(id, dict) and hasattr(cls, '_id_type'): 
    elif isinstance(id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.id = id
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
        self.if 'id' in data = if 'id' in data
        self.if isinstance(id, dict) and hasattr(cls, '_id_type') = if isinstance(id, dict) and hasattr(cls, '_id_type')
        self.elif isinstance(id, list) and hasattr(cls, '_item_type') = elif isinstance(id, list) and hasattr(cls, '_item_type')
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
        id = data.get('id', None)
        if isinstance(id, dict) and 'Uuid' in locals():
            id = Uuid.fromDict(id)
        elif isinstance(id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                id = Uuid[id]
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
        if 'id' in data = data.get('if 'id' in data', None)
        if isinstance(id, dict) and hasattr(cls, '_id_type') = data.get('if isinstance(id, dict) and hasattr(cls, '_id_type')', None)
        elif isinstance(id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_DeleteQuest:
    id: Uuid
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
    if 'id' in data: 
    if isinstance(id, dict) and hasattr(cls, '_id_type'): 
    elif isinstance(id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.id = id
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
        self.if 'id' in data = if 'id' in data
        self.if isinstance(id, dict) and hasattr(cls, '_id_type') = if isinstance(id, dict) and hasattr(cls, '_id_type')
        self.elif isinstance(id, list) and hasattr(cls, '_item_type') = elif isinstance(id, list) and hasattr(cls, '_item_type')
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
        id = data.get('id', None)
        if isinstance(id, dict) and 'Uuid' in locals():
            id = Uuid.fromDict(id)
        elif isinstance(id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                id = Uuid[id]
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
        if 'id' in data = data.get('if 'id' in data', None)
        if isinstance(id, dict) and hasattr(cls, '_id_type') = data.get('if isinstance(id, dict) and hasattr(cls, '_id_type')', None)
        elif isinstance(id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_UnregisterLocation:
    id: Uuid
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
    if 'id' in data: 
    if isinstance(id, dict) and hasattr(cls, '_id_type'): 
    elif isinstance(id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.id = id
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
        self.if 'id' in data = if 'id' in data
        self.if isinstance(id, dict) and hasattr(cls, '_id_type') = if isinstance(id, dict) and hasattr(cls, '_id_type')
        self.elif isinstance(id, list) and hasattr(cls, '_item_type') = elif isinstance(id, list) and hasattr(cls, '_item_type')
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
        id = data.get('id', None)
        if isinstance(id, dict) and 'Uuid' in locals():
            id = Uuid.fromDict(id)
        elif isinstance(id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                id = Uuid[id]
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
        if 'id' in data = data.get('if 'id' in data', None)
        if isinstance(id, dict) and hasattr(cls, '_id_type') = data.get('if isinstance(id, dict) and hasattr(cls, '_id_type')', None)
        elif isinstance(id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_AttachDialogue:
    npc_id: Uuid
    dialogue: DialogueNode
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
    if 'npc_id' in data: 
    if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type'): 
    elif isinstance(npc_id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'dialogue' in data: 
    if isinstance(dialogue, dict) and hasattr(cls, '_dialogue_type'): 
    elif isinstance(dialogue, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, npc_id, dialogue, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'npc_id' in data, if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type'), elif isinstance(npc_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'dialogue' in data, if isinstance(dialogue, dict) and hasattr(cls, '_dialogue_type'), elif isinstance(dialogue, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.npc_id = npc_id
        self.dialogue = dialogue
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
        self.if 'npc_id' in data = if 'npc_id' in data
        self.if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type') = if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type')
        self.elif isinstance(npc_id, list) and hasattr(cls, '_item_type') = elif isinstance(npc_id, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'dialogue' in data = if 'dialogue' in data
        self.if isinstance(dialogue, dict) and hasattr(cls, '_dialogue_type') = if isinstance(dialogue, dict) and hasattr(cls, '_dialogue_type')
        self.elif isinstance(dialogue, list) and hasattr(cls, '_item_type') = elif isinstance(dialogue, list) and hasattr(cls, '_item_type')
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
        npc_id = data.get('npc_id', None)
        if isinstance(npc_id, dict) and 'Uuid' in locals():
            npc_id = Uuid.fromDict(npc_id)
        elif isinstance(npc_id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                npc_id = Uuid[npc_id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        # Import DialogueNode type at runtime
        try:
            from DialogueNode import DialogueNode
        except ImportError:
            pass  # Type not available, will use generic handling
        dialogue = data.get('dialogue', None)
        if isinstance(dialogue, dict) and 'DialogueNode' in locals():
            dialogue = DialogueNode.fromDict(dialogue)
        elif isinstance(dialogue, str) and 'DialogueNode' in locals() and hasattr(DialogueNode, '__contains__'):
            try:
                dialogue = DialogueNode[dialogue]
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
        if 'npc_id' in data = data.get('if 'npc_id' in data', None)
        if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type') = data.get('if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type')', None)
        elif isinstance(npc_id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(npc_id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'dialogue' in data = data.get('if 'dialogue' in data', None)
        if isinstance(dialogue, dict) and hasattr(cls, '_dialogue_type') = data.get('if isinstance(dialogue, dict) and hasattr(cls, '_dialogue_type')', None)
        elif isinstance(dialogue, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(dialogue, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(npc_id, dialogue, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'npc_id' in data, if isinstance(npc_id, dict) and hasattr(cls, '_npc_id_type'), elif isinstance(npc_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'dialogue' in data, if isinstance(dialogue, dict) and hasattr(cls, '_dialogue_type'), elif isinstance(dialogue, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_CreateContact:
    field_0: Contact
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
        # Import Contact type at runtime
        try:
            from Contact import Contact
        except ImportError:
            pass  # Type not available, will use generic handling
        field_0 = data.get('field_0', None)
        if isinstance(field_0, dict) and 'Contact' in locals():
            field_0 = Contact.fromDict(field_0)
        elif isinstance(field_0, str) and 'Contact' in locals() and hasattr(Contact, '__contains__'):
            try:
                field_0 = Contact[field_0]
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
class Command_UpdateMessage:
    field_0: Message
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
        # Import Message type at runtime
        try:
            from Message import Message
        except ImportError:
            pass  # Type not available, will use generic handling
        field_0 = data.get('field_0', None)
        if isinstance(field_0, dict) and 'Message' in locals():
            field_0 = Message.fromDict(field_0)
        elif isinstance(field_0, str) and 'Message' in locals() and hasattr(Message, '__contains__'):
            try:
                field_0 = Message[field_0]
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
class Command_UpdateChoice:
    field_0: PhoneChoice
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
        # Import PhoneChoice type at runtime
        try:
            from PhoneChoice import PhoneChoice
        except ImportError:
            pass  # Type not available, will use generic handling
        field_0 = data.get('field_0', None)
        if isinstance(field_0, dict) and 'PhoneChoice' in locals():
            field_0 = PhoneChoice.fromDict(field_0)
        elif isinstance(field_0, str) and 'PhoneChoice' in locals() and hasattr(PhoneChoice, '__contains__'):
            try:
                field_0 = PhoneChoice[field_0]
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
class Command_ReplaceChoices:
    contact_id: Uuid
    messages: List[Message]
    choices: List[PhoneChoice]
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
    if 'contact_id' in data: 
    if isinstance(contact_id, dict) and hasattr(cls, '_contact_id_type'): 
    elif isinstance(contact_id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'messages' in data: 
    if isinstance(messages, dict) and hasattr(cls, '_messages_type'): 
    elif isinstance(messages, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'choices' in data: 
    if isinstance(choices, dict) and hasattr(cls, '_choices_type'): 
    elif isinstance(choices, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, contact_id, messages, choices, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'contact_id' in data, if isinstance(contact_id, dict) and hasattr(cls, '_contact_id_type'), elif isinstance(contact_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'messages' in data, if isinstance(messages, dict) and hasattr(cls, '_messages_type'), elif isinstance(messages, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'choices' in data, if isinstance(choices, dict) and hasattr(cls, '_choices_type'), elif isinstance(choices, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.contact_id = contact_id
        self.messages = messages
        self.choices = choices
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
        self.if 'contact_id' in data = if 'contact_id' in data
        self.if isinstance(contact_id, dict) and hasattr(cls, '_contact_id_type') = if isinstance(contact_id, dict) and hasattr(cls, '_contact_id_type')
        self.elif isinstance(contact_id, list) and hasattr(cls, '_item_type') = elif isinstance(contact_id, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'messages' in data = if 'messages' in data
        self.if isinstance(messages, dict) and hasattr(cls, '_messages_type') = if isinstance(messages, dict) and hasattr(cls, '_messages_type')
        self.elif isinstance(messages, list) and hasattr(cls, '_item_type') = elif isinstance(messages, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'choices' in data = if 'choices' in data
        self.if isinstance(choices, dict) and hasattr(cls, '_choices_type') = if isinstance(choices, dict) and hasattr(cls, '_choices_type')
        self.elif isinstance(choices, list) and hasattr(cls, '_item_type') = elif isinstance(choices, list) and hasattr(cls, '_item_type')
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
        contact_id = data.get('contact_id', None)
        if isinstance(contact_id, dict) and 'Uuid' in locals():
            contact_id = Uuid.fromDict(contact_id)
        elif isinstance(contact_id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                contact_id = Uuid[contact_id]
            except (KeyError, ValueError):
                pass  # Leave as string if not a valid enum value
        messages = data.get('messages', None)
        choices = data.get('choices', None)
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
        if 'contact_id' in data = data.get('if 'contact_id' in data', None)
        if isinstance(contact_id, dict) and hasattr(cls, '_contact_id_type') = data.get('if isinstance(contact_id, dict) and hasattr(cls, '_contact_id_type')', None)
        elif isinstance(contact_id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(contact_id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'messages' in data = data.get('if 'messages' in data', None)
        if isinstance(messages, dict) and hasattr(cls, '_messages_type') = data.get('if isinstance(messages, dict) and hasattr(cls, '_messages_type')', None)
        elif isinstance(messages, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(messages, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'choices' in data = data.get('if 'choices' in data', None)
        if isinstance(choices, dict) and hasattr(cls, '_choices_type') = data.get('if isinstance(choices, dict) and hasattr(cls, '_choices_type')', None)
        elif isinstance(choices, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(choices, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(contact_id, messages, choices, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'contact_id' in data, if isinstance(contact_id, dict) and hasattr(cls, '_contact_id_type'), elif isinstance(contact_id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'messages' in data, if isinstance(messages, dict) and hasattr(cls, '_messages_type'), elif isinstance(messages, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'choices' in data, if isinstance(choices, dict) and hasattr(cls, '_choices_type'), elif isinstance(choices, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_DeleteContact:
    id: Uuid
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
    if 'id' in data: 
    if isinstance(id, dict) and hasattr(cls, '_id_type'): 
    elif isinstance(id, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.id = id
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
        self.if 'id' in data = if 'id' in data
        self.if isinstance(id, dict) and hasattr(cls, '_id_type') = if isinstance(id, dict) and hasattr(cls, '_id_type')
        self.elif isinstance(id, list) and hasattr(cls, '_item_type') = elif isinstance(id, list) and hasattr(cls, '_item_type')
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
        id = data.get('id', None)
        if isinstance(id, dict) and 'Uuid' in locals():
            id = Uuid.fromDict(id)
        elif isinstance(id, str) and 'Uuid' in locals() and hasattr(Uuid, '__contains__'):
            try:
                id = Uuid[id]
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
        if 'id' in data = data.get('if 'id' in data', None)
        if isinstance(id, dict) and hasattr(cls, '_id_type') = data.get('if isinstance(id, dict) and hasattr(cls, '_id_type')', None)
        elif isinstance(id, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(id, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(id, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'id' in data, if isinstance(id, dict) and hasattr(cls, '_id_type'), elif isinstance(id, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_SetOTP:
    otp: Optional[str]
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
    if 'otp' in data: 
    if isinstance(otp, dict) and hasattr(cls, '_otp_type'): 
    elif isinstance(otp, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, otp, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'otp' in data, if isinstance(otp, dict) and hasattr(cls, '_otp_type'), elif isinstance(otp, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.otp = otp
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
        self.if 'otp' in data = if 'otp' in data
        self.if isinstance(otp, dict) and hasattr(cls, '_otp_type') = if isinstance(otp, dict) and hasattr(cls, '_otp_type')
        self.elif isinstance(otp, list) and hasattr(cls, '_item_type') = elif isinstance(otp, list) and hasattr(cls, '_item_type')
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
        otp = data.get('otp', None)
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
        if 'otp' in data = data.get('if 'otp' in data', None)
        if isinstance(otp, dict) and hasattr(cls, '_otp_type') = data.get('if isinstance(otp, dict) and hasattr(cls, '_otp_type')', None)
        elif isinstance(otp, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(otp, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(otp, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'otp' in data, if isinstance(otp, dict) and hasattr(cls, '_otp_type'), elif isinstance(otp, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_UpdatePositionLogs:
    updated: List[PositionLog]
    deleted: List[Uuid]
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
    if 'updated' in data: 
    if isinstance(updated, dict) and hasattr(cls, '_updated_type'): 
    elif isinstance(updated, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 
    if 'deleted' in data: 
    if isinstance(deleted, dict) and hasattr(cls, '_deleted_type'): 
    elif isinstance(deleted, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, updated, deleted, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'updated' in data, if isinstance(updated, dict) and hasattr(cls, '_updated_type'), elif isinstance(updated, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'deleted' in data, if isinstance(deleted, dict) and hasattr(cls, '_deleted_type'), elif isinstance(deleted, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.updated = updated
        self.deleted = deleted
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
        self.if 'updated' in data = if 'updated' in data
        self.if isinstance(updated, dict) and hasattr(cls, '_updated_type') = if isinstance(updated, dict) and hasattr(cls, '_updated_type')
        self.elif isinstance(updated, list) and hasattr(cls, '_item_type') = elif isinstance(updated, list) and hasattr(cls, '_item_type')
        self.if hasattr(item_type, 'fromDict') = if hasattr(item_type, 'fromDict')
        self.else = else
        self.if 'deleted' in data = if 'deleted' in data
        self.if isinstance(deleted, dict) and hasattr(cls, '_deleted_type') = if isinstance(deleted, dict) and hasattr(cls, '_deleted_type')
        self.elif isinstance(deleted, list) and hasattr(cls, '_item_type') = elif isinstance(deleted, list) and hasattr(cls, '_item_type')
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
        updated = data.get('updated', None)
        deleted = data.get('deleted', None)
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
        if 'updated' in data = data.get('if 'updated' in data', None)
        if isinstance(updated, dict) and hasattr(cls, '_updated_type') = data.get('if isinstance(updated, dict) and hasattr(cls, '_updated_type')', None)
        elif isinstance(updated, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(updated, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        if 'deleted' in data = data.get('if 'deleted' in data', None)
        if isinstance(deleted, dict) and hasattr(cls, '_deleted_type') = data.get('if isinstance(deleted, dict) and hasattr(cls, '_deleted_type')', None)
        elif isinstance(deleted, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(deleted, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(updated, deleted, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'updated' in data, if isinstance(updated, dict) and hasattr(cls, '_updated_type'), elif isinstance(updated, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else, if 'deleted' in data, if isinstance(deleted, dict) and hasattr(cls, '_deleted_type'), elif isinstance(deleted, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

@dataclass
class Command_CreateFactions:
    factions: List[Faction]
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
    if 'factions' in data: 
    if isinstance(factions, dict) and hasattr(cls, '_factions_type'): 
    elif isinstance(factions, list) and hasattr(cls, '_item_type'): 
    if hasattr(item_type, 'fromDict'): 
    else: 

    def __init__(self, factions, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'factions' in data, if isinstance(factions, dict) and hasattr(cls, '_factions_type'), elif isinstance(factions, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else):
        self.factions = factions
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
        self.if 'factions' in data = if 'factions' in data
        self.if isinstance(factions, dict) and hasattr(cls, '_factions_type') = if isinstance(factions, dict) and hasattr(cls, '_factions_type')
        self.elif isinstance(factions, list) and hasattr(cls, '_item_type') = elif isinstance(factions, list) and hasattr(cls, '_item_type')
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
        factions = data.get('factions', None)
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
        if 'factions' in data = data.get('if 'factions' in data', None)
        if isinstance(factions, dict) and hasattr(cls, '_factions_type') = data.get('if isinstance(factions, dict) and hasattr(cls, '_factions_type')', None)
        elif isinstance(factions, list) and hasattr(cls, '_item_type') = data.get('elif isinstance(factions, list) and hasattr(cls, '_item_type')', None)
        if hasattr(item_type, 'fromDict') = data.get('if hasattr(item_type, 'fromDict')', None)
        else = data.get('else', None)
        return cls(factions, def toJSON(self) -> str, def _serialize(obj), if hasattr(obj, '__dict__'), for key, value in obj.__dict__.items(), elif isinstance(obj, list), elif isinstance(obj, dict), return {k, elif hasattr(obj, 'toJSON') and callable(getattr(obj, 'toJSON')), elif hasattr(obj, 'value') and isinstance(obj, Enum), elif isinstance(obj, Enum), def fromJSON(cls, json_str), def fromDict(cls, data), if 'factions' in data, if isinstance(factions, dict) and hasattr(cls, '_factions_type'), elif isinstance(factions, list) and hasattr(cls, '_item_type'), if hasattr(item_type, 'fromDict'), else)

# The main Command class
class Command(Enum):
    Move = Command_Move
    SpawnNPCs = Command_SpawnNPCs
    DespawnNPCs = Command_DespawnNPCs
    SetAttitude = Command_SetAttitude
    Print = Command_Print
    RegisterLocation = Command_RegisterLocation
    UpdateDialogue = Command_UpdateDialogue
    CreateQuest = Command_CreateQuest
    CreateObjective = Command_CreateObjective
    CompleteObjective = Command_CompleteObjective
    IncrementObjectiveCounter = Command_IncrementObjectiveCounter
    CompleteQuest = Command_CompleteQuest
    DeleteQuest = Command_DeleteQuest
    UnregisterLocation = Command_UnregisterLocation
    AttachDialogue = Command_AttachDialogue
    CreateContact = Command_CreateContact
    UpdateMessage = Command_UpdateMessage
    UpdateChoice = Command_UpdateChoice
    ReplaceChoices = Command_ReplaceChoices
    DeleteContact = Command_DeleteContact
    SetOTP = Command_SetOTP
    UpdatePositionLogs = Command_UpdatePositionLogs
    CreateFactions = Command_CreateFactions
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
                if variant.name == "Move":
                    try:
                        return Command_Move.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "SpawnNPCs":
                    try:
                        return Command_SpawnNPCs.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "DespawnNPCs":
                    try:
                        return Command_DespawnNPCs.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "SetAttitude":
                    try:
                        return Command_SetAttitude.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "Print":
                    try:
                        return Command_Print.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "RegisterLocation":
                    try:
                        return Command_RegisterLocation.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "UpdateDialogue":
                    try:
                        return Command_UpdateDialogue.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "CreateQuest":
                    try:
                        return Command_CreateQuest.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "CreateObjective":
                    try:
                        return Command_CreateObjective.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "CompleteObjective":
                    try:
                        return Command_CompleteObjective.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "IncrementObjectiveCounter":
                    try:
                        return Command_IncrementObjectiveCounter.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "CompleteQuest":
                    try:
                        return Command_CompleteQuest.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "DeleteQuest":
                    try:
                        return Command_DeleteQuest.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "UnregisterLocation":
                    try:
                        return Command_UnregisterLocation.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "AttachDialogue":
                    try:
                        return Command_AttachDialogue.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "CreateContact":
                    try:
                        return Command_CreateContact.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "UpdateMessage":
                    try:
                        return Command_UpdateMessage.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "UpdateChoice":
                    try:
                        return Command_UpdateChoice.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "ReplaceChoices":
                    try:
                        return Command_ReplaceChoices.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "DeleteContact":
                    try:
                        return Command_DeleteContact.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "SetOTP":
                    try:
                        return Command_SetOTP.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "UpdatePositionLogs":
                    try:
                        return Command_UpdatePositionLogs.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "CreateFactions":
                    try:
                        return Command_CreateFactions.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "if variant.name.lower()":
                    try:
                        return Command_if variant.name.lower().fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "inner_data":
                    try:
                        return Command_inner_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "inner_data["type"]":
                    try:
                        return Command_inner_data["type"].fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "data":
                    try:
                        return Command_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_name":
                    try:
                        return Command_variant_name.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant":
                    try:
                        return Command_variant.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
                if variant.name == "variant_data":
                    try:
                        return Command_variant_data.fromDict(kwargs)
                    except Exception:
                        return variant  # Fallback to simple variant
        # If not found, return the first variant as a fallback
        return next(iter(cls))
