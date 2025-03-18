#![allow(dead_code, clippy::disallowed_names)]

use std::{collections::BTreeSet, rc::Rc, collections::HashMap};

use chrono::NaiveDateTime;
use serde::{Deserialize, Serialize};
use ts_rs::{Py, TS};
use uuid::Uuid;



#[derive(Serialize, TS, Py)]
#[ts(rename_all = "lowercase")]
#[ts(export, export_to = "UserRole.ts")]
#[py(export)]
enum Role {
    User,
    #[ts(rename = "administrator")]
    Admin,
}

#[derive(Serialize, TS, Py)]
// when 'serde-compat' is enabled, ts-rs tries to use supported serde attributes.
#[serde(rename_all = "UPPERCASE")]
#[ts(export)]
#[py(export)]
enum Gender {
    Male,
    Female,
    Other,
}

#[derive(Serialize, TS, Py)]
#[ts(export)]
#[py(export)]
struct User {
    user_id: i32,
    first_name: String,
    last_name: String,
    role: Role,
    family: Vec<User>,
    #[ts(inline)]
    gender: Gender,
    #[ts(type = "string")]
    token: Uuid,
    // NaiveDateTime is not supported, comment it out for now
    // #[ts(type = "string")]
    // created_at: NaiveDateTime,
}

#[derive(Serialize, TS, Py)]
#[serde(tag = "type", rename_all = "snake_case")]
#[ts(export)]
#[py(export)]
enum Vehicle {
    Bicycle { color: String },
    Car { brand: String, color: String },
}

#[derive(Serialize, TS, Py)]
#[ts(export)]
#[py(export)]
struct Point {
    time: u64,
    value: u64,
}

#[derive(Serialize, TS, Py)]
#[serde(default)]
#[ts(export)]
#[py(export)]
struct Series {
    points: Vec<Point>,
}

#[derive(Serialize, TS, Py)]
#[serde(tag = "kind", content = "d")]
#[ts(export)]
#[py(export)]
enum SimpleEnum {
    A,
    B,
}

#[derive(Serialize, TS, Py)]
#[serde(tag = "kind", content = "data")]
#[ts(export)]
#[py(export)]
enum ComplexEnum {
    A,
    B { foo: String, bar: f64 },
    W(SimpleEnum),
    F { nested: SimpleEnum },
    V(Series),
    U(User),
}

#[derive(Serialize, TS, Py)]
#[serde(tag = "kind")]
#[ts(export)]
#[py(export)]
enum InlineComplexEnum {
    A,
    B { foo: String, bar: f64 },
    W(SimpleEnum),
    F { nested: SimpleEnum },
    V(Series),
    U(User),
}

#[derive(Serialize, TS, Py)]
#[serde(rename_all = "camelCase")]
#[ts(export)]
#[py(export)]
struct ComplexStruct {
    #[serde(default)]
    pub string_tree: Option<String>,
}

#[derive(Serialize, TS, Py)]
#[ts(export)]
#[py(export)]
struct ComplexStruct2 {
    #[serde(default)]
    pub string_tree: Option<String>,
    pub thing: InlineComplexEnum,
}

#[derive(Deserialize, Serialize, Clone, Copy, Debug, TS, Py)]
pub struct Position {
    pub x: f32,
    pub y: f32,
    pub z: f32,
    pub w: f32,
}

#[derive(Deserialize, Serialize, Clone, Copy, Debug, TS, Py)]
pub struct Orientation {
    pub i: f32,
    pub k: f32,
    pub r: f32,
    pub j: f32,
}

#[derive(Deserialize, Serialize, Clone, Copy, Debug, TS, Py)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum MoveDest {
    Entity { entity_id: Uuid },
    Position(Position),
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct Speak {
    pub npc_id: Uuid,
    pub dialog_text: String,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct DialogueNode {
    pub id: Uuid,
    pub player_dialogue: Option<String>,
    pub npc_dialogue: String,
    pub options: Vec<DialogueNode>,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct SkyrimNPCData {
    pub ref_id: u32,
    pub cell_id: u32,
    pub worldspace_id: Option<u32>,
}

#[derive(Deserialize, Serialize, Clone, Copy, Debug, TS, Py)]
pub enum Relationship {
    Ally,
    Friend,
    Neutral,
    Hostile,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct FactionRelationship {
    pub id: Uuid,
    pub relationship: Relationship,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct Faction {
    pub id: Uuid,
    pub relations: Vec<FactionRelationship>,
    pub player_relations: Relationship,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct CyberpunkNPCData {
    pub faction: String, // todo: make enum
    pub record_tweak: String,
    pub template_path: String,
    pub appearance: String,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub enum NPCGameData {
    Skyrim(SkyrimNPCData),
    Cyberpunk(CyberpunkNPCData),
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct NPC {
    pub id: Uuid,
    pub faction: Option<Uuid>,
    pub game_data: NPCGameData,
    pub dialogue: Option<DialogueNode>,
    pub spawn_position: Option<Position>,
    pub spawn_orientation: Option<Orientation>,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct Objective {
    pub id: Uuid,
    pub description: String,
    pub optional: bool,
    pub total_count: Option<i32>,
    pub location: Position,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct Quest {
    pub id: Uuid,
    pub title: String,
    pub preview: String,
    pub description: String,
    // pub completed: bool,
    pub objectives: Vec<Objective>,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct Message {
    pub id: Uuid,
    pub text: String,
    pub did_send: bool,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct PhoneChoice {
    pub id: Uuid,
    pub text: String,
    pub responses: Vec<Message>,
    pub next_choices: Vec<PhoneChoice>,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct Contact {
    pub id: Uuid,
    pub name: String,
    pub preview: String,
    pub messages: Vec<Message>,
    pub choices: Vec<PhoneChoice>,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct PositionLog {
    pub id: Uuid,
    pub group_name: String,
    pub building: String,
    pub room: String,
    pub name: String,
    // pub tags: HashMap<String, String>,
    pub tags_list: Vec<String>,
    pub description: String,
    pub orientation: Orientation,
    pub position: Position,

    // this is a JSON timestamp, ts types don't support SystemTime.
    pub deleted_at: Option<String>,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
#[serde(tag = "command", rename_all = "snake_case")]
#[ts(export)]
#[py(export)]
enum Command {
    Move {
        npc_id: Uuid,
        dest: Option<MoveDest>,
    },
    #[serde(rename = "spawn_npcs")]
    SpawnNPCs {
        npcs: Vec<NPC>,
    },
    #[serde(rename = "despawn_npcs")]
    DespawnNPCs {
        npcs: Vec<Uuid>,
    },
    SetAttitude {
        id: Uuid,
        attitude: String,
    },
    Print {
        data: String,
    },
    #[serde(rename = "clear_npcs")]
    ClearNPCs,
    RegisterLocation {
        id: Uuid,
        position: Position,
        distance: f32,
    },
    UpdateDialogue(DialogueNode),
    CreateQuest(Quest),
    CreateObjective {
        quest_id: Uuid,
        objective: Objective,
    },
    CompleteObjective {
        id: Uuid,
        did_fail: bool,
    },
    IncrementObjectiveCounter {
        objective_id: Uuid,
    },
    CompleteQuest {
        id: Uuid,
    },
    DeleteQuest {
        id: Uuid,
    },
    UnregisterLocation {
        id: Uuid,
    },
    AttachDialogue {
        npc_id: Uuid,
        dialogue: DialogueNode,
    },
    CreateContact(Contact),
    UpdateMessage(Message),
    UpdateChoice(PhoneChoice),
    ReplaceChoices {
        contact_id: Uuid,
        messages: Vec<Message>,
        choices: Vec<PhoneChoice>,
    },
    DeleteContact {
        id: Uuid,
    },
    // internal
    #[serde(rename = "set_otp")]
    SetOTP {
        otp: Option<String>,
    },
    UpdatePositionLogs {
        updated: Vec<PositionLog>,
        deleted: Vec<Uuid>,
    },
    /// Create factions.  Note relationships can refer to factions later in the same list.
    CreateFactions {
        factions: Vec<Faction>,
    },
}

#[derive(Deserialize, Serialize, Clone, PartialEq, Debug, TS, Py)]
#[serde(tag = "type", rename_all = "snake_case")]
#[ts(export)]
#[py(export)]
pub enum Trigger {
    #[serde(rename = "npc_killed")]
    NPCKilled {
        id: Uuid,
    },
    DialogueOptionChosen {
        id: Uuid,
    },
    InProximity {
        id: Uuid,
    },
    PhoneReplyChosen {
        id: Uuid,
    },
}

fn get_true() -> bool {
    true
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct DependencyState {
    #[serde(flatten)]
    pub trigger: Trigger,
    #[serde(skip)]
    pub is_complete: bool,
}

// impl<'de> Deserialize<'de> for DependencyState {
//     fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
//     where
//         D: serde::Deserializer<'de>,
//     {
//         match D::deserialize() {
//             Ok(trigger) => Ok<DependencyState{trigger, is_complete: false}>,
//             Err(err) => Err(err)
//         }
//     }
// }

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
#[serde(tag = "type", content = "data", rename_all = "snake_case")]
pub enum Dependency {
    Trigger(DependencyState),
    Any(Vec<Dependency>),
    All(Vec<Dependency>),
    None(Vec<Dependency>),
    NComplete { n: i32, deps: Vec<Dependency> },
}

#[derive(Debug, Deserialize, Serialize, Clone, TS, Py)]
pub struct TriggerHandler {
    pub id: Uuid,
    pub dependency: Dependency,
    pub commands: Vec<Command>,
    pub children: Vec<TriggerHandler>,
    pub group: Option<Uuid>,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct TriggerEvent {
    #[serde(flatten)]
    pub trigger: Trigger,
    #[serde(default = "get_true")]
    pub is_active: bool,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
pub struct TestStruct {
    foo: String,
}

#[derive(Deserialize, Serialize, Clone, Debug, TS, Py)]
#[ts(export)]
#[py(export)]
pub struct TestStruct2 {
    foo: String,
    bar: TestStruct,
}

