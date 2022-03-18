import json
import re
import constants

def clean_corpus_file(dirty_corpus_file_path: str, clean_corpus_file_path: str) -> int:
    try:
        dirty_corpus_file = open(dirty_corpus_file_path, "r")

        # Skip first line
        next(dirty_corpus_file)
    except OSError as error:
        print(error)
        print("Couldn't open dirty corpus file, is the file path correct?")
        exit(1)

    try:
        clean_corpus_file = open(clean_corpus_file_path, "w")
    except OSError as error:
        print(error)
        print("Couldn't open dirty corpus file, is the file path correct?")
        exit(1)

    iteration = 0
    errors_count = 0
    for line in dirty_corpus_file:
        iteration += 1
        if constants.DEBUG and iteration % 1000 == 0:
            print(f"Iteration: {iteration}, errors: {errors_count}")

        # Parse id
        line_index = 0
        while line[line_index] != ",":
            line_index += 1
        id = line[0:line_index]

        # Parse conclusion
        line_index += 1
        conclusion_start_index = line_index
        mark = ","
        if line[line_index] == '"':
            mark = '"'
            line_index += 1
        while line[line_index] != mark:
            line_index += 1
        conclusion = line[conclusion_start_index:line_index].strip("\"")

        # Skip beginning of the string for easier identification
        line_split = line[line_index + 1:].lstrip(",")

        # Clean JSON from whole line split
        line_split = _clean_json(line_split)

        # Parse premises
        premises_json = re.findall(r"\[{\"text\".*?}\]", line_split)[0]
        try:
            json.loads(premises_json)
        except Exception as error:
            errors_count += 1
            continue

        # Parse context
        context_json = re.findall(r",{.*?},\[", line_split)[0][:-1].strip(",")
        try:
            json.loads(context_json)
        except Exception as error:
            errors_count += 1
            continue

        # Parse sentences
        sentences_json = re.findall(r"\[{\"sent_id\".*?}\]", line_split)[0]
        try:
            json.loads(sentences_json)
        except Exception as error:
            errors_count += 1
            continue

    return errors_count

def _clean_json(json_string: str) -> str:
    # Remove all double quotes
    cleaned_json_string = json_string.replace("\"", "")
    # Remove escaped space
    cleaned_json_string = cleaned_json_string.replace("\\xa0", " ")
    # Remove escape characters
    cleaned_json_string = cleaned_json_string.replace("\\", "")
    # Remove source markings
    cleaned_json_string = re.sub(r"\[[0-9]{1,2}\]", "", cleaned_json_string)
    cleaned_json_string = re.sub(r"\[[A-Za-z]{1,4}\]", "", cleaned_json_string)

    # Clean all tags
    for tag in constants.TAGS:
        # Tag beginning and ending
        cleaned_json_string = re.sub(f"[\"']+{tag}[\"']+:", f'"{tag}":', cleaned_json_string)
        # Data beginning
        cleaned_json_string = re.sub(f"(\"{tag}\":\s+)" + r"([^{\[])", r'\1"\2', cleaned_json_string)

    # Clean tag endings
    cleaned_json_string = re.sub(r"[^\]],\s+\"", r'", "', cleaned_json_string)
    cleaned_json_string = re.sub(r"[^\]]}", r'"}', cleaned_json_string)

    # Remove all single quotes
    cleaned_json_string = cleaned_json_string.replace("'", "")

    return cleaned_json_string

if __name__ == '__main__':
    errors = clean_corpus_file(constants.DIRTY_CORPUS_FILE_LOCATION, constants.CLEAN_CORPUS_FILE_LOCATION)
    print(f"Amount of errors during processing: {errors}")