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

    def __init__(self, npc_id, dest):
        self.npc_id = npc_id
        self.dest = dest

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
        # Filter out method definitions and only pass actual field values
        return cls(npc_id, dest)

@dataclass
class Command_SpawnNPCs:
    npcs: List[NPC]

    def __init__(self, npcs):
        self.npcs = npcs

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
        # Filter out method definitions and only pass actual field values
        return cls(npcs)

@dataclass
class Command_DespawnNPCs:
    npcs: List[Uuid]

    def __init__(self, npcs):
        self.npcs = npcs

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
        # Filter out method definitions and only pass actual field values
        return cls(npcs)

@dataclass
class Command_SetAttitude:
    id: Uuid
    attitude: str

    def __init__(self, id, attitude):
        self.id = id
        self.attitude = attitude

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
        # Filter out method definitions and only pass actual field values
        return cls(id, attitude)

@dataclass
class Command_Print:
    data: str

    def __init__(self, data):
        self.data = data

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
        # Filter out method definitions and only pass actual field values
        return cls(data)

@dataclass
class Command_RegisterLocation:
    id: Uuid
    position: Position
    distance: float

    def __init__(self, id, position, distance):
        self.id = id
        self.position = position
        self.distance = distance

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
        # Filter out method definitions and only pass actual field values
        return cls(id, position, distance)

@dataclass
class Command_UpdateDialogue:
    field_0: DialogueNode

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
        # Filter out method definitions and only pass actual field values
        return cls(field_0)

@dataclass
class Command_CreateQuest:
    field_0: Quest

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
        # Filter out method definitions and only pass actual field values
        return cls(field_0)

@dataclass
class Command_CreateObjective:
    quest_id: Uuid
    objective: Objective

    def __init__(self, quest_id, objective):
        self.quest_id = quest_id
        self.objective = objective

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
        # Filter out method definitions and only pass actual field values
        return cls(quest_id, objective)

@dataclass
class Command_CompleteObjective:
    id: Uuid
    did_fail: bool

    def __init__(self, id, did_fail):
        self.id = id
        self.did_fail = did_fail

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
        # Filter out method definitions and only pass actual field values
        return cls(id, did_fail)

@dataclass
class Command_IncrementObjectiveCounter:
    objective_id: Uuid

    def __init__(self, objective_id):
        self.objective_id = objective_id

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
        # Filter out method definitions and only pass actual field values
        return cls(objective_id)

@dataclass
class Command_CompleteQuest:
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
class Command_DeleteQuest:
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
class Command_UnregisterLocation:
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
class Command_AttachDialogue:
    npc_id: Uuid
    dialogue: DialogueNode

    def __init__(self, npc_id, dialogue):
        self.npc_id = npc_id
        self.dialogue = dialogue

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
        # Filter out method definitions and only pass actual field values
        return cls(npc_id, dialogue)

@dataclass
class Command_CreateContact:
    field_0: Contact

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
        # Filter out method definitions and only pass actual field values
        return cls(field_0)

@dataclass
class Command_UpdateMessage:
    field_0: Message

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
        # Filter out method definitions and only pass actual field values
        return cls(field_0)

@dataclass
class Command_UpdateChoice:
    field_0: PhoneChoice

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
        # Filter out method definitions and only pass actual field values
        return cls(field_0)

@dataclass
class Command_ReplaceChoices:
    contact_id: Uuid
    messages: List[Message]
    choices: List[PhoneChoice]

    def __init__(self, contact_id, messages, choices):
        self.contact_id = contact_id
        self.messages = messages
        self.choices = choices

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
        # Filter out method definitions and only pass actual field values
        return cls(contact_id, messages, choices)

@dataclass
class Command_DeleteContact:
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
class Command_SetOTP:
    otp: Optional[str]

    def __init__(self, otp):
        self.otp = otp

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
        # Filter out method definitions and only pass actual field values
        return cls(otp)

@dataclass
class Command_UpdatePositionLogs:
    updated: List[PositionLog]
    deleted: List[Uuid]

    def __init__(self, updated, deleted):
        self.updated = updated
        self.deleted = deleted

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
        # Filter out method definitions and only pass actual field values
        return cls(updated, deleted)

@dataclass
class Command_CreateFactions:
    factions: List[Faction]

    def __init__(self, factions):
        self.factions = factions

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
        # Filter out method definitions and only pass actual field values
        return cls(factions)

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
                if variant.name == "inner_data":
                    try:
                        return Command_inner_data.fromDict(kwargs)
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
