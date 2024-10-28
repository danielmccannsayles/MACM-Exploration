from macm.executor import execute_steps
from macm.judge import (
    verify_new_condition,
    check_answer,
    verify_steps,
    double_check_conditions,
)
from macm.thinker import (
    extract_from_original,
    new_conditions_from_existing,
    create_steps,
)
from utils.helpers import (
    conditions_objectives_to_string,
    list_to_numbered_string,
)
from utils.async_logger import AsyncLogger
from utils.custom_logger import CustomLogger


async def main4(
    question, max_times_mining_new, coding_assistant, coding_thread, log_path
):
    """
    Main 4 - asynchronous!!
    """

    AsyncLogger.add_message(log_path, "## Begin")
    CustomLogger.print(f"Starting {log_path}")

    conditions, objectives = await extract_from_original(question)
    c_str, o_str = conditions_objectives_to_string(conditions, objectives)
    AsyncLogger.add_message(
        log_path, "Extracted from problem, (conditions, objectives)", c_str, o_str
    )

    # New condition mining loop has a max # of tries
    for i in range(max_times_mining_new):
        unchecked_conditions = await new_conditions_from_existing(
            conditions, objectives
        )
        AsyncLogger.add_message(
            log_path,
            f"## Mined new conditions from existing ({i+1}/{max_times_mining_new}):"
            f"Unchecked Conditions ({i+1}/{max_times_mining_new})",
            list_to_numbered_string(unchecked_conditions),
        )

        verified_conditions = []
        # Check each new condition w/ the judge - check_statment
        for i, unchecked in enumerate(unchecked_conditions):
            AsyncLogger.add_message(log_path, f"Verifying condition #{i+1}")

            # Verifies new condition. If it's wrong, tries to correct. Verifies that corrected condition. If wrong again, returns None
            verified = await verify_new_condition(
                objectives,
                conditions,
                unchecked,
                coding_assistant,
                coding_thread,
            )
            if verified:
                verified_conditions.append(verified.new_condition)
                AsyncLogger.add_message(log_path, "Verified", verified.new_condition)
            else:
                AsyncLogger.add_message(
                    log_path,
                    "Invalid",
                )

        # Add the new verified conditions to the exisiting conditions!
        conditions += verified_conditions
        AsyncLogger.add_message(
            log_path, "All Conditions: ", list_to_numbered_string(conditions)
        )

        if_got_answer = await check_answer(conditions, objectives)
        AsyncLogger.add_message(log_path, f"Do we have answer?: {if_got_answer}")

        if if_got_answer:
            break

    CustomLogger.print(f"finished mining conditions ({log_path})")

    # TODO: Not sure how to make this work yet.
    # We should have a list of conditions that are ready. Let's check and see if any contradict
    # This will return the conditions if they are good, and remove any that contradict
    # conditions = double_check_conditions(conditions)

    steps = await create_steps(conditions, objectives)

    # Check if steps are accurate - 2 retries.
    for _ in range(2):
        accept_or_reject = await verify_steps(steps, objectives)
        AsyncLogger.add_message(
            log_path,
            "### Step",
            steps,
        )
        if accept_or_reject.acccept:
            AsyncLogger.add_message(
                log_path,
                "Approved",
            )
            break
        # Pass in the reason for failure
        steps = await create_steps(
            conditions,
            objectives,
            f"The last step generation process failed becase:\n {accept_or_reject.reason}",
        )

    AsyncLogger.add_message(
        log_path,
        "## Final",
        "Conditions:",
        list_to_numbered_string(conditions),
        "Objectives:",
        list_to_numbered_string(objectives),
        "Steps:",
        steps,
    )
    answer = await execute_steps(
        conditions, objectives, steps, coding_assistant, coding_thread
    )
    AsyncLogger.add_message(log_path, "Generated Answer: ", answer)

    # Flush out one message
    await AsyncLogger.flush_one(log_path)

    CustomLogger.print(
        f"Finished {log_path} in ({CustomLogger.elapsed_time()}): the final answer is {answer}"
    )
    return answer
