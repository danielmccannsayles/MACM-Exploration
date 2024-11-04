from pydantic import BaseModel
from typing import Optional


class ConditionsAndObjective(BaseModel):
    conditions: list[str]
    objective: str


# Mathematical relationship
class MathRelationship(BaseModel):
    conditions: list[int]
    relationship: str
    reason: str


class NewRelationships(BaseModel):
    value: list[MathRelationship]


class VerificationSteps(BaseModel):
    relevant: bool
    proven: bool
    accept: bool


class Method(BaseModel):
    method: str
    reason: str


class SubObjective(BaseModel):
    goal: str
    reason: str
