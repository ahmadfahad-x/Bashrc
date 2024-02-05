import argparse
import fileinput
import logging

logging.basicConfig(level=logging.INFO)

def find_duplicate_aliases(file_path):
    alias_dict = {}

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("alias"):
                parts = line.split('=')
                alias_name = parts[0].split()[1].strip()
                alias_command = parts[1].strip()
                if alias_name in alias_dict:
                    alias_dict[alias_name].append(alias_command)
                else:
                    alias_dict[alias_name] = [alias_command]

    duplicate_aliases = {alias: commands for alias, commands in alias_dict.items() if len(commands) > 1}

    return duplicate_aliases

def remove_duplicate_aliases(file_path):
    duplicates = find_duplicate_aliases(file_path)
    modified = False

    for alias, commands in duplicates.items():
        if len(commands) > 1:
            for command in commands[1:]:
                with fileinput.FileInput(file_path, inplace=True) as file:
                    for line in file:
                        if f"alias {alias}=" in line and command in line:
                            modified = True
                            break
                        else:
                            print(line, end='')

    return modified

def main():
    parser = argparse.ArgumentParser(description="Find and optionally delete duplicate aliases in a bashrc file.")
    parser.add_argument("bashrc_path", help="Path to the bashrc file to analyze")
    parser.add_argument("--delete", action="store_true", help="Delete duplicate aliases from the bashrc file")

    args = parser.parse_args()

    try:
        if args.delete:
            modified = remove_duplicate_aliases(args.bashrc_path)

            if modified:
                logging.info("Duplicate aliases removed.")
            else:
                logging.info("No duplicate aliases found.")

        else:
            duplicates = find_duplicate_aliases(args.bashrc_path)

            if duplicates:
                logging.info("Duplicate aliases found:")
                for alias, commands in duplicates.items():
                    logging.info(f"{alias}: {', '.join(commands)}")
            else:
                logging.info("No duplicate aliases found.")

    except FileNotFoundError:
        logging.error(f"Error: File not found at {args.bashrc_path}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
