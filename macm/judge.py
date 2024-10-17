from utils.gpt_assistants import generate_from_assistant
from utils.gpt_code_assistant import generate_from_code_assistant
from prompt.prompts import *


def Judge_condition(question, condition, assistant, thread):
    """
    ask GPT to Judge the thoughts from the thinker
    Input:
    Known_condtions, Condition from the thinker (List, Str)
    Output:
    True/False (Str)
    """
    messages = []
    message = {
        "role": "user",
        "content": Judge_condtion.format(
            question=question, Initial_conditions=condition
        ),
    }
    messages.append(message)
    T_or_F = generate_from_assistant(messages, assistant, thread, "judge")
    return T_or_F


def Judge_statement(Known_condtions, condition_from_thinker, assistant, thread):
    """
    **Uses code interpreter**

    ask GPT to Judge the thoughts from the thinker
    Input:
    Known_condtions, Condition from the thinker (List, Str)
    Output:
    True/False (Str)
    """
    numbered_conditions = "\n".join(
        f"{i + 1}. {condition}" for i, condition in enumerate(Known_condtions)
    )
    messages = [
        {
            "role": "user",
            "content": Judge_T_F.format(
                Known_condtions=numbered_conditions,
                condition_from_thinker=condition_from_thinker,
            ),
        },
        {"role": "user", "content": T_or_F_prompt},
    ]
    persona = "You're a judge. I need you to make judgments on some statements. "

    T_or_F = generate_from_code_assistant(
        persona, messages, assistant, thread, "judge (code)"
    )
    return T_or_F


def Judge_answer(Known_condtions, objectives, assistant, thread):
    """
    Ask GPT to Judge if we already got the answer
    Input:
    Known_condtions, objectives (List, List)
    Output:
    False / True ,answer (Str)
    """
    messages = []
    numbered_conditions = "\n".join(
        f"{i + 1}. {condition}" for i, condition in enumerate(Known_condtions)
    )
    numbered_Objective = "\n".join(
        f"{i + 1}. {objective}" for i, objective in enumerate(objectives)
    )
    message = {
        "role": "user",
        "content": Judge_if_got_Answer.format(
            Known_condtions=numbered_conditions, Objective=numbered_Objective
        ),
    }
    messages.append(message)
    message = {"role": "user", "content": If_got_Answer_T_F}
    messages.append(message)
    T_or_F = generate_from_assistant(messages, assistant, thread, "judge")
    return T_or_F
