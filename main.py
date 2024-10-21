import os
import json
import random
from prompt.prompts import *
from macm.executor import execute_steps
from macm.judge import verify_new_condition, check_answer
from macm.thinker import (
    extract_from_original,
    new_conditions_from_existing,
    create_steps,
)
from utils.assistants import create_agents_and_thread


def log(title, *args):
    content = []
    for arg in args:
        content.append(str(arg))
    content_str = "\n".join(content)

    file_path = f"./output/messages.md"
    with open(file_path, "a") as f:
        f.write(f"======\n## {title}\n #{content_str} \n")


def main(question, max_times_mining_new):
    """
    Input question and get the final answer from muti-Agent got
    Input:
    quesion, the number of times new conditions are identified, the number of the inspectors  (Str, int, int)
    Output:
    final answer (Str)
    """

    # Create the agents
    coding_assistant, coding_thread = create_agents_and_thread()

    ### The actual coding

    # TODO: I'd like to have GPT rate how hard it thinks the problem is at different steps. And then dynamically adjust the iterations we do.
    # This seems like with some tweaking it would really improve the efficiency

    # TODO: do we want to put a loop around this? And check that the questions analyzed by the thinker are correct?

    print(f"Extracting conditions and objective(s) from problem..")
    conditions, objectives = extract_from_original(question)
    log("Extracted from problem, (conditions, objectives)", conditions, objectives)

    # New condition mining loop has a max # of tries
    for i in range(max_times_mining_new):
        print(f"Mining new conditions from existing ({i+1}/{max_times_mining_new})")
        unchecked_conditions = new_conditions_from_existing(conditions, objectives)
        log(
            f"Unchecked Conditions ({i+1}/{max_times_mining_new})",
            unchecked_conditions,
        )

        verified_conditions = []
        # Check each new condition w/ the judge - check_statment
        for i, unchecked in enumerate(unchecked_conditions):
            print(f"Verifying condition #{i+1}..")
            print(f"{unchecked}\n")

            # Verifies new condition. If it's wrong, tries to correct. Verifies that corrected condition. If wrong again, returns None
            verified = verify_new_condition(
                conditions,
                unchecked,
                coding_assistant,
                coding_thread,
            )
            if verified:
                verified_conditions.append(verified.new_condition)

        # Add the new verified conditions to the exisiting conditions!
        conditions += verified_conditions

        print("Checking if we have the answer..")
        if_got_answer = check_answer(conditions, objectives)
        print(if_got_answer)
        if if_got_answer:
            break

    # Use the thinker to create the steps the executor should take
    # TODO: Is this totally necessary? Probably decently so.. might be useful to make steps earlier, and potentially revise them.. hmm..
    print(f"thinker is thinking steps...")
    steps = create_steps(conditions, objectives)
    log("Steps", conditions, objectives, steps)

    # TODO: Consider adding a check on the steps before executing them - one judge - good/bad, if bad ask it to fix it given feedback.
    # Consider multiple loops here?

    print(f"Executor is trying to calculate the answer...")
    answer = execute_steps(
        conditions, objectives, steps, coding_assistant, coding_thread
    )
    log("Anser: ", answer)

    # TODO: consider doing a voter system here - running the executor more than once. If the first two line up we good.
    # If they don't, do two more. If there's not a clear majority still, -
    # TODO: (improve this step) - ask GPT which answer is the most accurate and return that?

    print(f"The final answer is {answer}")
    return answer


if __name__ == "__main__":
    max_times_mining_new = 1  # The upper limit of the mining times
    question = """Square ABCD has side lengths of 13 units. Point E
lies in the interior of the square such that AE = 5 units
and BE = 12 units. What is the distance from E to
side AD"""  # Input your own question

    main(question, max_times_mining_new)


# --------------------------------------
# TODO: use this function to run certain tests
def evaluate_dataset(folder_path, times, n, limit=5):  #
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    random.shuffle(all_files)  # Shuffle the order of files randomly

    for count, file_path in enumerate(all_files[:limit]):
        with open(file_path, "r") as json_file:
            try:
                data = json.load(json_file)
                problem = data.get("problem")
                if problem:
                    print(f"#{count} Problem:\n", problem)
                    solution = data.get("solution")
                    print(f"#{count} Solution\n", solution)
                    main(problem, times, n)
            except json.JSONDecodeError:
                print(f"Error reading file {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
