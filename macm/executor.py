from utils.gpt_assistants import generate_from_assistant
from utils.gpt_code_assistant import generate_from_code_assistant
from utils.gpt import Find_Answer_from_GPT
from prompt.prompts import *


def Execute_steps(conditions, objectives, steps, assistant, thread):
    """
    **Uses Code Interpreter**

    Ask GPT to Judge the thoughts from the thinker
    Input:
    conditions,objectives,steps (List, List, Str)
    Output:
    final answer (Str)
    """
    numbered_conditions = "\n".join(
        f"{i + 1}. {condition}" for i, condition in enumerate(conditions)
    )
    numbered_objective = "\n".join(
        f"{i + 1}. {objective}" for i, objective in enumerate(objectives)
    )

    messages = [
        {
            "role": "user",
            "content": find_target.format(
                Objective=numbered_objective,
                Conditions=numbered_conditions,
                Steps=steps,
            ),
        },
        {"role": "user", "content": box_target},
    ]

    persona = "You're an excutor. I need you to calculate the final result based on some conditions and steps. You need to provide me the answer based on the format of the examples."
    boxed_answer = generate_from_code_assistant(
        persona, messages, assistant, thread, "executor (code)"
    )
    return boxed_answer


# TODO: don't believe this is being used at all
def Find_Answer(conditions, objectives, assistant, thread):
    """
    ask GPT to Judge the thoughts from the thinker
    Input:
    conditions,objectives,steps (List, List, Str)
    Output:
    final answer (Str)
    """
    messages = []
    numbered_conditions = "\n".join(
        f"{i + 1}. {condition}" for i, condition in enumerate(conditions)
    )
    numbered_objective = "\n".join(
        f"{i + 1}. {objective}" for i, objective in enumerate(objectives)
    )
    message = {
        "role": "user",
        "content": find_target.format(
            Objective=numbered_objective, Conditions=numbered_conditions
        ),
    }
    messages.append(message)
    final_answer = Find_Answer_from_GPT(
        messages, max_tokens=512, model="gpt-4-1106-preview", temperature=0.7, n=1
    )
    return final_answer
