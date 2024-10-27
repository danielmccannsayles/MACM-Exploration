from utils.helpers import list_to_numbered_string
from utils.gpt_code_assistant import generate_from_code_assistant
from utils.gpt import generate_from_gpt_with_schema
from chains.prompt_staging import find_target
from macm.schemas import FinalAnswer


def execute_steps(conditions, objectives, steps, assistant, thread):
    """
    **Uses Code Interpreter**

    Executes the steps given to it. Makes two calls. Once to find the target, using code interpreter,
    and once to return the answer as formatted

    Input:
        conditions,objectives, steps (List, List, Str)
    Output:
        final answer (float)
    """
    conditions_str = list_to_numbered_string(conditions)
    objectives_str = list_to_numbered_string(objectives)
    content = find_target.format(
        Objective=objectives_str,
        Conditions=conditions_str,
        Steps=steps,
    )

    persona = "You're an executor. I need you to calculate the final result based on some conditions, objectives, and the provided steps. Follow ONLY the instructions and do not deviate"
    response_messages = generate_from_code_assistant(
        persona, content, assistant, thread, "executor (code)"
    )

    # Second time calling - force schema to return float. Only give access to assistant response to reduce tokens
    response_messages.append(
        {"role": "user", "content": "Please return ONLY the above answer as a float"},
    )
    final_answer = generate_from_gpt_with_schema(response_messages, FinalAnswer)
    return final_answer.value
