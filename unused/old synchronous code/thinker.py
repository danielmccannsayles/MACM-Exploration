from utils.gpt import generate_from_gpt, generate_from_gpt_with_schema
from utils.helpers import conditions_objectives_to_string
from macm.schemas import ConditionsAndObjectives, NewConditions
from chains.prompt_staging import (
    extract_conditions_objectives_from_problem,
    Discover_new_conditions,
    Determine_Steps,
)


# Extract from original - get conditions and objectives from original question
# New conditions from existing - get new conditions from existing conditions and objectives
# Create steps - create a step by step plan, based on the existing conditions and objectives, to solve the problem


# TODO: Is there a better way to handle multi-step objectives? Kinda like steps? Would be cool to split the work up into some discreet steps.
# ... something to think about
def extract_from_original(question):
    """
    Extract conditions and objective(s) from the original question
    Args:
        Question: The given word problem (str)
    Returns:
        (conditions, objectives): List of conditions and objective(s)?
    """
    messages = [
        {
            "role": "system",
            "content": "You are a thinker. Be creative",
        },
        {
            "role": "user",
            "content": extract_conditions_objectives_from_problem.format(
                question=question
            ),
        },
    ]
    conditions_and_objectives = generate_from_gpt_with_schema(
        messages, ConditionsAndObjectives
    )

    return conditions_and_objectives.conditions, conditions_and_objectives.objectives


# TODO: For some rason I thought this used to use code. I can't find any supporting evidence of this in the logs though, and intuitively idk why it would
def new_conditions_from_existing(conditions, objectives):
    """
    Come up with new conditions from the existing conditions and the objective(s)
    """
    conditions_str, objectives_str = conditions_objectives_to_string(
        conditions, objectives
    )
    messages = [
        {
            "role": "system",
            "content": "You are a thinker. Be creative. Don't be afraid to be wrong",
        },
        {
            "role": "user",
            "content": Discover_new_conditions.format(
                conditions=conditions_str, objectives=objectives_str
            ),
        },
    ]
    new_conditions = generate_from_gpt_with_schema(messages, NewConditions)

    # Not sure if this is neccessary but want to avoid errors
    if not new_conditions.value:
        new_conditions.value = []

    # Manually make sure that we only produce 3 conditions. This was added in main 3, reasoning being - adding less conditions at a time prevents contradictory conclusions + allows for more variability depending on problem difficulty
    return new_conditions.value[0:3]


# TODO: should I use json schema to force this into a list? Probably not needed..
def create_steps(conditions, objectives, optional_comments="") -> str:
    """
    Create steps from list of conditions and objectives
    """
    conditions_str, objectives_str = conditions_objectives_to_string(
        conditions, objectives
    )
    steps = generate_from_gpt(
        [
            {
                "role": "user",
                "content": Determine_Steps.format(
                    Known_conditions=conditions_str,
                    Objective=objectives_str,
                    optional_comments=optional_comments,
                ),
            }
        ]
    )
    return steps
