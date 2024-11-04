from utils.helpers import conditions_objectives_to_string, list_to_numbered_string
from utils.async_gpt import agenerate_from_gpt_with_schema, agenerate_from_gpt
from new_stuff.prompts import (
    givens_from_problem,
    direct_mathematical_relationship,
    verify_relationship_prompt,
    find_method_prompt,
    verify_method_prompt,
)
from new_stuff.schemas import (
    ConditionsAndObjective,
    NewRelationships,
    MathRelationship,
    VerificationSteps,
    Method,
)


async def givens_from_question(question):
    """
    Get the givens of a question.
    """
    messages = [
        {
            "role": "user",
            "content": givens_from_problem.format(question=question),
        },
    ]
    conditions_and_objectives = await agenerate_from_gpt_with_schema(
        messages, ConditionsAndObjective
    )

    return conditions_and_objectives.conditions, conditions_and_objectives.objective


async def relationships_from_existing(conditions, objectives) -> list[MathRelationship]:
    """
    Come up with new conditions from the existing conditions and the objective(s)
    """
    conditions_str, objectives_str = conditions_objectives_to_string(
        conditions, objectives
    )
    messages = [
        {
            "role": "user",
            "content": direct_mathematical_relationship.format(
                conditions=conditions_str, objectives=objectives_str
            ),
        },
    ]
    relationships = await agenerate_from_gpt_with_schema(messages, NewRelationships)

    if not relationships.value:
        relationships.value = []

    # Make sure we only return 2 2
    return relationships.value[0:2]


async def verify_relationship(
    r: MathRelationship, conditions: list, objectives
) -> VerificationSteps:
    """
    Verify relationship
    """
    # Convert from 1 based to 0 based, handle any incorrect indices, then extract only those relevant conditions
    zero_based = [i - 1 for i in r.conditions]
    clean_indices = [i for i in zero_based if 0 <= i < len(conditions)]
    relevant_conditions = [conditions[i - 1] for i in clean_indices]
    messages = [
        {
            "role": "user",
            "content": verify_relationship_prompt.format(
                relationship=r.relationship,
                conditions=relevant_conditions,
                objectives=objectives,
                reason=r.reason,
            ),
        },
    ]
    verification = await agenerate_from_gpt_with_schema(messages, VerificationSteps)

    return verification


# TODO: complete this
async def work_backwards(
    r: MathRelationship, conditions: list, objectives
) -> VerificationSteps:
    """
    Check for sub-objectives that can lead to the end. This will be added to the list of objectives
    """


async def find_method(
    question: str, relationships: list[str], conditions: list, objectives
) -> Method:
    """
    Find a method
    """
    rs = list_to_numbered_string(relationships)
    cs, os = conditions_objectives_to_string(conditions, objectives)
    messages = [
        {
            "role": "user",
            "content": find_method_prompt.format(
                question=question,
                relationships=rs,
                conditions=cs,
                objectives=os,
            ),
        },
    ]
    method = await agenerate_from_gpt_with_schema(messages, Method)

    return method


async def verify_method(
    m: Method, question: str, relationships: list[str], conditions: list, objectives
):
    """
    Verify the method
    """
    rs = list_to_numbered_string(relationships)
    cs, os = conditions_objectives_to_string(conditions, objectives)

    messages = [
        {
            "role": "user",
            "content": verify_method_prompt.format(
                question=question,
                relationships=rs,
                conditions=cs,
                objectives=os,
                method=m.method,
                reason=m.reason,
            ),
        },
    ]
    method = await agenerate_from_gpt_with_schema(messages, Method)

    return method
