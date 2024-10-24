from macm.executor import execute_steps
from macm.judge import verify_new_condition, check_answer
from macm.thinker import (
    extract_from_original,
    new_conditions_from_existing,
    create_steps,
)
from utils.custom_logger import CustomLogger
from utils.to_string_helpers import (
    conditions_objectives_to_string,
    list_to_numbered_string,
)


def main(question, max_times_mining_new, coding_assistant, coding_thread):
    """
    This is ~ the papers original solution. With a few tweaks
    """

    ### The actual coding

    # TODO: I'd like to have GPT rate how hard it thinks the problem is at different steps. And then dynamically adjust the iterations we do.
    # This seems like with some tweaking it would really improve the efficiency

    # TODO: do we want to put a loop around this? And check that the questions analyzed by the thinker are correct?

    print(f"Extracting conditions and objective(s) from problem..")
    conditions, objectives = extract_from_original(question)
    c_str, o_str = conditions_objectives_to_string(conditions, objectives)
    CustomLogger.default_log(
        "Extracted from problem, (conditions, objectives)", c_str, o_str
    )

    # New condition mining loop has a max # of tries
    for i in range(max_times_mining_new):
        print(f"Mining new conditions from existing ({i+1}/{max_times_mining_new})")
        unchecked_conditions = new_conditions_from_existing(conditions, objectives)
        CustomLogger.default_log(
            f"Unchecked Conditions ({i+1}/{max_times_mining_new})",
            list_to_numbered_string(unchecked_conditions),
        )

        verified_conditions = []
        # Check each new condition w/ the judge - check_statment
        for i, unchecked in enumerate(unchecked_conditions):
            print(f"Verifying condition #{i+1}..")
            print(f"{unchecked}\n")

            # Verifies new condition. If it's wrong, tries to correct. Verifies that corrected condition. If wrong again, returns None
            verified = verify_new_condition(
                objectives,
                conditions,
                unchecked,
                coding_assistant,
                coding_thread,
            )
            if verified:
                verified_conditions.append(verified.new_condition)

        # Add the new verified conditions to the exisiting conditions!
        conditions += verified_conditions
        CustomLogger.default_log(
            "Valid conditions:", list_to_numbered_string(conditions)
        )

        print("Checking if we have the answer..")
        if_got_answer = check_answer(conditions, objectives)
        print(if_got_answer)
        if if_got_answer:
            break

    # Use the thinker to create the steps the executor should take
    # TODO: Is this totally necessary? Probably decently so.. might be useful to make steps earlier, and potentially revise them.. hmm..
    print(f"thinker is thinking steps...")
    steps = create_steps(conditions, objectives)
    CustomLogger.default_log("Steps", conditions, objectives, steps)

    # TODO: Consider adding a check on the steps before executing them - one judge - good/bad, if bad ask it to fix it given feedback.
    # Consider multiple loops here?

    print(f"Executor is trying to calculate the answer...")
    answer = execute_steps(
        conditions, objectives, steps, coding_assistant, coding_thread
    )
    CustomLogger.default_log("Anser: ", answer)

    # TODO: consider doing a voter system here - running the executor more than once. If the first two line up we good.
    # If they don't, do two more. If there's not a clear majority still, -
    # TODO: (improve this step) - ask GPT which answer is the most accurate and return that?

    print(f"The final answer is {answer}")
    return answer
