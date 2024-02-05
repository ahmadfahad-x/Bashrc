import argparse
import json
import logging
import os
import re
from typing import Dict, List, Optional
from collections import Counter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_duplicate_functions(file_path: str) -> Dict[str, List[str]]:
    function_list = []
    duplicate_functions = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_function = None

    for line in lines:
        match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\)\s*{', line)
        if match:
            current_function = match.group(1)
            function_list.append(current_function)
    duplicate_functions = [x for x, count in Counter(function_list).items()
                            if count > 1]
    print(f"these are duplicates {duplicate_functions}")
    return function_list

def save_to_json(data: Dict, file_path: str):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def delete_duplicate_functions(bashrc_path: str, duplicates: Dict[str, List[str]]):
    with open(bashrc_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    current_function = None

    for line in lines:
        match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\)\s*{', line)
        if match:
            current_function = match.group(1)
        elif line.startswith("}"):
            current_function = None
        elif current_function and current_function not in duplicates:
            new_lines.append(line)

    with open(bashrc_path, 'w') as file:
        file.writelines(new_lines)

def main():
    parser = argparse.ArgumentParser(description="Find duplicate functions in a bashrc file")
    parser.add_argument("bashrc_path", type=str, help="Path to the bashrc file")
    parser.add_argument("--output_json", type=str, default="duplicate_functions.json", help="Path to output JSON file")
    parser.add_argument("--delete", action="store_true", help="Delete duplicate functions from the bashrc file")
    args = parser.parse_args()

    duplicate_functions = find_duplicate_functions(args.bashrc_path)

    if duplicate_functions:
        logger.info("Duplicate functions found:")
        for function, code_list in duplicate_functions.items():
            logger.info(f"Function: {function}")
            for code in code_list:
                logger.info(f"  {code}")
            logger.info("-" * 20)

        save_to_json(duplicate_functions, args.output_json)

        if args.delete:
            logger.info("Deleting duplicate functions.")
            delete_duplicate_functions(args.bashrc_path, duplicate_functions)
            logger.info("Duplicate functions deleted.")
    else:
        logger.info("No duplicate functions found.")

if __name__ == "__main__":
    main()
