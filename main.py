# -----------------------------------------------------------
# Script to validate JSON files using JSON-schema.
# Files to validate must be stored in folder "event".
# Schemas for validating must be stored in folder "schema".
# Validation report will be stored in "validation_files.log" file.
# -----------------------------------------------------------


import json
import os

from datetime import datetime
from jsonschema import Draft7Validator


def get_file_paths(files_list=None, condition='data'):
    """Collecting file paths."""
    if files_list is None:
        files_list = []
    if condition == 'data':
        path = '.\\event'
    else:
        path = '.\\schema'
    for root, dirs, names in os.walk(path):
        for name in names:
            files_list.append(os.path.join(root, name))
    return files_list


def validate_file(files, results, schema):
    """Validation JSON file using JSON-schema."""
    with open(files, 'r') as read_data:
        json_data = json.load(read_data)
        additional_mark = ''
        if json_data:
            results.append('JSON schema: ' + json_data['event'] + '\n' * 2)
            if json_data['event'] in schema.keys():
                errors = sorted(Draft7Validator(schema[json_data['event']]).iter_errors(json_data['data']),
                                key=lambda e: e.path)
                for error in errors:
                    if 'is a required property' in str(error.message):
                        additional_mark = ' and missed, please check data file to fix that'
                    if 'is not of type' in str(error.message):
                        additional_mark = '. Need to check data file to fix it or modify validation schema'
                    results.append('Error info: ' + error.message + additional_mark + '\n')
                if errors:
                    results.append('\nValidation: FAIL\nTotal errors: ' + str(len(errors)) + '\n' + '-' * 20 + '\n')
                else:
                    results.append('Validation: PASS' + '\n' + '-' * 20 + '\n')
            else:
                results.append(f"Error info: There is no \"{json_data['event']}\" validation scheme to use.\n"
                               "Please, validate file in part of validation scheme needed or add new validation "
                               "scheme to the \"schema\" folder.\nValidation: FAIL" + '\n' + '-' * 20 + '\n')
        else:
            results.append('Validation: FAIL\nData file is empty.' + '\n' + '-' * 20 + '\n')


if __name__ == '__main__':

    with open('validation_files.log', 'w') as result_file:
        result_file.write('Data validation test' + '\n')
        result_file.write(datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + '\n' * 3)

        schema = {}
        for files in get_file_paths(condition='schema'):
            with open(files, 'r') as read_data:
                schema[files.split(sep='\\')[2].split(sep='.')[0]] = json.load(read_data)

        for files in get_file_paths(condition='data'):
            results = ['File name: ' + files + '\n']
            validate_file(files, results, schema)
            # with open('validation_files.log', 'a') as result_file:
            result_file.writelines(results)
