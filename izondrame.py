import random
import time
import os.path

"""
Parameters for Fine-tuning
"""
results_print_delay = 500 # in ms
read_file = "data.txt"
write_file = "randomized_results.txt"

"""
Functions for Obtaining Input
"""

def obtain_input():
    """
    :return: list of strings representing user inputs
    """

    print_inputs_message()

    idx = 1
    collection_inputs = {} # list of strings

    is_reading_from_file = False
    f = None
    if os.path.isfile(read_file):
        is_reading_from_file = True
        f = open(read_file, 'r')

    while True:

        current = ""
        if is_reading_from_file:
            current = f.readline().split("\n")[0] # needed to remove newline/enter character from line-end
            print(current)
            if current == "":
                is_reading_from_file = False
                f.close()
                continue
        else:
            current = input()

        # '/end' indicates the end of any input, regardless from file or live input
        if current.lower() == "/end":
            break
        if current in collection_inputs:
            print("Already entered {}, please try another entry.".format(current))
            continue

        collection_inputs[current] = 0
        print_individual_input_response_message(idx, current)
        idx = idx + 1

    return list(collection_inputs.keys())

"""
Functions to Process Data
"""

def execute(user_inputs):
    """
    Processes the user_inputs using the functions included, returnsing a list of results.
    :param user_inputs: Raw user inputs in a list of strings.
    :return: Result of processing the information, after a specific sequence of actions.
    """

    results_list = randomize(user_inputs)
    return results_list

def randomize(user_inputs):
    """
    Obtains a randomized list of strings, based off a score measure.
    :param user_inputs: List of strings representing user input before randomizing.
    :return: List of randomized user input strings.
    """
    num_user_inputs = len(user_inputs)
    scores = calculate_scores(num_user_inputs)
    results_list = align_results(scores, user_inputs)
    return results_list

def calculate_scores(num_user_inputs):
    """
    Produces a list of randomized scores to measure ranking of entries.
    :param num_user_inputs: Number of scores to produce.
    :return: List of scores.
    """
    scores = [] # confirmed scores
    visited_scores = {} # past scores, used for fast checks especially with large no. of entries

    for i in range(num_user_inputs):

        is_unique_random_sum = False
        while not is_unique_random_sum:
            random_augend = random.randint(1, 37)
            random_addend = random.randint(1, num_user_inputs)
            random_sum = random_augend + random_addend
            # low probability of re-rolling due to same random_sum as another
            if random_sum not in scores:
                visited_scores[random_sum] = 0
                is_unique_random_sum = True

        # at this point, current random_sum is confirmed to be unique
        scores.append(random_sum)

    return scores

def align_results(scores, user_inputs):

    hasSameLength = (len(scores) == len(user_inputs))
    if not hasSameLength:
        return ["Scores and User Inputs do not align in terms of number of entries. Please check with dev."]

    # needed to tag results with their scores
    scores_to_input_dict = {}
    for i in range(len(scores)):
        score = scores[i]
        input = user_inputs[i]
        scores_to_input_dict[score] = input

    # organize results using scores
    ordered_scores = sorted(scores)
    ordered_results = []
    for score in ordered_scores:
        ordered_results.append(scores_to_input_dict[score])

    return ordered_results

"""
Functions to handle results
"""

def handle_results(results_list):

    print_results(results_list)
    write_results(results_list)

def print_results(results_list):

    print_results_message()

    num_results = len(results_list)

    for i in range(num_results):
        wait()
        idx = i + 1
        result_value = results_list[i]
        print_individual_result_message(idx, result_value)

def write_results(results_list):

    num_results = len(results_list)

    f = open(write_file, "w")
    f.write("Here are the latest results:")

    for i in range(num_results):
        f.write("")
        idx = i + 1
        result_value = results_list[i]
        write_individual_string = "\n{}: {}".format(idx, result_value)
        f.write(write_individual_string)

    f.close()

"""
Printing messages
"""

def print_start_message():
    print("Hello! Welcome to izondrame, a randomizer for your general needs. \n"
        + "-> Other than your live input, I can also read from 'data.txt'. \n"
        + "-> Simply place it in the same folder as this program. ^^")

def print_inputs_message():
    print("--> To begin, we will read in data from the file, and then your live inputs until you end.\n"
        + "--> To end, just key in '/end' and hit enter, or include it in the 'data.txt' file.")

def print_individual_input_response_message(idx, user_input):
    print("{}: {}".format(idx, user_input))

def print_results_message():
    print("Hmmm... After applying my randomize algorithm, here's the results in 'ascending' order:")

def print_individual_result_message(idx, result_value):
    print("{}: {}".format(idx, result_value))

"""
Utility Functions
"""

def wait():
    time.sleep(results_print_delay / 1000)

"""
Main Function
"""

def run():
    """
    Highest level function, calls 3 helper functions to obtain and process user inputs, and print results.
    """
    print_start_message()
    user_inputs = obtain_input()
    results_list = execute(user_inputs)
    handle_results(results_list)

if __name__ == '__main__':
    run()