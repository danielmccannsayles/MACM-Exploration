from utils.gpt_code_assistant import generate_from_code_assistant
from utils.gpt import generate_from_gpt_with_schema, generate_from_gpt
from macm.helpers import list_to_numbered_string, conditions_objectives_to_string
from macm.schemas import NewCondition, CorrectOrCorrectedCondition, TrueOrFalse
from prompt.prompts import *
from typing import Optional


# TODO: extract some code from this bloated function
# TODO: onnly pass in the conditions that are supposed to support the conclusion - this may reduce accuracy, but it tests whether this pattern actually works
# much better than current, where we give it all the conditions.
# TODO: We can have the judge return "True" or if it's incorrect we can correct it.
def verify_new_condition(
    known_conditions: list, new_condition: NewCondition, assistant, thread
) -> Optional[NewCondition]:
    """
    **Uses code interpreter**

    ask GPT to Judge the thoughts from the thinker
    Input:
    Known_condtions, Condition from the thinker (List, Str)
    Output:
        New Condition or false
    """
    known_conditions_str = list_to_numbered_string(known_conditions)
    indices = " and ".join(str(x) for x in new_condition.based_on_known_conditions)

    new_condition_str = f"Based on Known Condition(s) {indices}, we can derive: {new_condition.new_condition}, because: {new_condition.reason}"

    content = Judge_T_F.format(
        known_conditions=known_conditions_str,
        new_condition=new_condition_str,
    )

    persona = "You're a judge. I need you to make judgments on some statements. "
    response_messages = generate_from_code_assistant(
        persona, content, assistant, thread, "judge (code)"
    )

    # Response messages is all the GPT responses. I don't think it includes the code stuff. Maybe would be worth including?
    # TODO: do I need to give more context? I could also add in the original messages object. Let's see if it gets confused like this
    response_messages.append(
        {
            "role": "user",
            "content": """Using ONLY the messages above -> 
            Set the 'correct' response property to true if the condition under review was verified and false if not.
            Set the corrected_condition property to the suggested new condition if the above messages suggest a new condition. Else set it to None""",
        }
    )

    correct_or_corrected_condition = generate_from_gpt_with_schema(
        response_messages, CorrectOrCorrectedCondition
    )

    # If the new condition was verified correctly, then we return it and end here!
    if correct_or_corrected_condition.correct:
        return new_condition

    # If they returned a corrected condition let's verify it by using the assistant and then asking gpt once more
    if correct_or_corrected_condition.corrected_condition:
        corrected_condition = correct_or_corrected_condition.corrected_condition
        indices = " and ".join(
            str(x) for x in corrected_condition.based_on_known_conditions
        )
        corrected_condition_str = f"Based on Known Condition(s) {indices}, we can derive: {corrected_condition.new_condition}, because: {corrected_condition.reason}"
        content = Judge_T_F.format(
            known_conditions=known_conditions_str,
            new_condition=corrected_condition_str,
        )

        persona = "You're a judge. I need you to make judgments on some statements. "
        response_messages = generate_from_code_assistant(
            persona, content, assistant, thread, "judge (code)"
        )
        response_messages.append(
            {"role": "user", "content": "Return only true or false"}
        )
        verify = generate_from_gpt(response_messages)

        # If this still isn't correct, give up on this condition completely
        if "False" in verify or "false" in verify:
            return None
        else:
            return corrected_condition

    return None


def check_answer(conditions, objectives):
    """
    Ask GPT to Judge if we already got the answer
    Input:
    Known_condtions, objectives (List, List)
    Output:
    False / True ,answer (Str)
    """

    conditions_str, objectives_str = conditions_objectives_to_string(
        conditions, objectives
    )
    messages = [
        {
            "role": "user",
            "content": Judge_if_got_Answer.format(
                conditions=conditions_str, objectives=objectives_str
            ),
        },
    ]

    response = generate_from_gpt(messages)

    messages = [
        {"role": "assistant", "content": response},
        {
            "role": "user",
            "content": "Summarize the above analysis as just True or False",
        },
    ]

    do_we_have_answer = generate_from_gpt_with_schema(messages, TrueOrFalse)
    return do_we_have_answer.value
