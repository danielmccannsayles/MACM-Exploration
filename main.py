import os
import json
import random
from utils.custom_logger import CustomLogger
from utils.create_assistant import create_agents_and_thread


if __name__ == "__main__":
    CustomLogger.update_path("messages")  # default
    max_times_mining_new = 1  # The upper limit of the mining times
    question = """Square ABCD has side lengths of 13 units. Point E
lies in the interior of the square such that AE = 5 units
and BE = 12 units. What is the distance from E to
side AD"""  # Input your own question

    # create agents
    coding_assistant, coding_thread = create_agents_and_thread()
    main(question, max_times_mining_new, coding_assistant, coding_thread)


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
