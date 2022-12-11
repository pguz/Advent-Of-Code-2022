import argparse
import functools
import json
import os.path
import time

from solutions import (
    day_01,
    day_02,
    day_03,
    day_04,
    day_05,
    day_06,
    day_07,
    day_08,
    day_09,
    day_10,
    day_11,
    day_12,
    day_13,
    day_14,
    day_15,
    day_16,
    day_17,
    day_18,
    day_19,
    day_20,
    day_21,
    day_22,
    day_23,
    day_24,
    day_25,
)

day_to_solution_file_mapping = {
    "01": day_01,
    "02": day_02,
    "03": day_03,
    "04": day_04,
    "05": day_05,
    "06": day_06,
    "07": day_07,
    "08": day_08,
    "09": day_09,
    "10": day_10,
    "11": day_11,
    "12": day_12,
    "13": day_13,
    "14": day_14,
    "15": day_15,
    "16": day_16,
    "17": day_17,
    "18": day_18,
    "19": day_19,
    "20": day_20,
    "21": day_21,
    "22": day_22,
    "23": day_23,
    "24": day_24,
    "25": day_25,
}


def aoc_day_argument(day):
    day_int = int(day)
    if not (1 <= day_int and day_int <= 25):
        raise argparse.ArgumentTypeError(
            "AoC contains 25 days. Argument needs to be in <1;25> range."
        )
    day_str = f"{day_int:02d}"
    if day_str not in day_to_solution_file_mapping:
        raise argparse.ArgumentTypeError(f"AoC day {day_str} has not been solved yet.")
    return day_str


def read_results_file():
    results_file_path = "./results.json"
    if not os.path.exists(results_file_path):
        return None
    with open(results_file_path) as f:
        results = json.load(f)
    return results


def measure_aoc_task_execution(function):
    @functools.wraps(function)
    def wrap(task_name, retry, **kwargs):
        task_duration = 0
        for _ in range(retry):
            time_start_point = time.time()
            result = function(**kwargs)
            time_end_point = time.time()
            task_duration += time_end_point - time_start_point
        print(f"{task_name} took {task_duration/retry:.5f}[s]")
        return result

    return wrap


@measure_aoc_task_execution
def run_solution_function(input_file, file_parse_function, solution_function):
    with open(input_file, "r") as fd:
        parsed_input = file_parse_function(fd)
        calculated_result = solution_function(*parsed_input)
        return calculated_result


def main():
    parser = argparse.ArgumentParser(description="Advent of Code 2021")
    parser.add_argument(
        "--day",
        required=True,
        type=aoc_day_argument,
        help="Please provide AoC2021 day <1:25>",
    )
    parser.add_argument(
        "--task",
        required=True,
        choices=["01", "02"],
        help="Please provide AoC2021 task number '01' or '02'",
    )
    parser.add_argument(
        "--expected-result",
        required=False,
        type=int,
        help="Please provide expected result for a given task or provide 'results.json' file",
    )
    parser.add_argument(
        "--retry",
        required=False,
        type=int,
        help="Number of iterations for a given task. For more stable time measurement. Default: 100",
    )
    parser.add_argument(
        "--improved",
        action="store_true",
        help="Run improved solution",
    )
    args = parser.parse_args()
    day = args.day
    task_id = args.task
    expected_result = args.expected_result
    retry = args.retry or 100
    improved = args.improved
    if not expected_result:
        results = read_results_file()
        if results is not None:
            try:
                expected_result = results[day][int(task_id) - 1]
            except KeyError:
                print(
                    f"No expected results for day {day} in results.json file provided."
                )

    day_module = day_to_solution_file_mapping[day]

    solution_function = getattr(day_module, f"solution_function_{task_id}")
    if improved is True:
        if not hasattr(day_module, f"improved_solution_function_{task_id}"):
            print("Improved solution has not been found")
            return
        solution_function = getattr(day_module, f"improved_solution_function_{task_id}")

    calculated_result = run_solution_function(
        task_name=f"day_{day}_task_{task_id}",
        retry=retry,
        input_file=f"inputs/{day}.txt",
        file_parse_function=day_module.parse_file,
        solution_function=solution_function,
    )

    if expected_result is not None:
        if calculated_result != expected_result:
            print(
                f"Provided expected result {expected_result} is not equal to the calculated one {calculated_result}"
            )
    else:
        print("No expected result was provided")


if __name__ == "__main__":
    main()
