from pydantic import BaseModel
from typing import Optional


class RemoveConditions(BaseModel):
    indices: list[int]


class AcceptOrRejectSteps(BaseModel):
    acccept: bool
    reason: str


class FinalAnswer(BaseModel):
    value: float


class ConditionsAndObjectives(BaseModel):
    conditions: list[str]
    objectives: list[str]


class NewCondition(BaseModel):
    based_on_known_conditions: list[int]
    new_condition: str
    reason: str


# Used in judge to get either confirmation
class CorrectOrCorrectedCondition(BaseModel):
    correct: bool
    corrected_condition: Optional[NewCondition]


class NewConditions(BaseModel):
    value: list[NewCondition]


class TrueOrFalse(BaseModel):
    value: bool
