from pydantic import BaseModel, Json
from typing import Any, List
from datetime import datetime


class TaskModel(BaseModel):
    id: int
    group_id: int
    added: datetime
    name: str
    kpt_status: Json[Any]
    kad_status: Json[Any]


class TaskGroupModel(BaseModel):
    id: int
    name: str
    added: datetime
    statistics: Json[Any]


class ResponseGroupsModel(BaseModel):
    groups: List[TaskGroupModel]


class ResponseTasksModel(BaseModel):
    tasks: List[TaskModel]
