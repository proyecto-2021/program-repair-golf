def get_data(code_name=None, tests_name=None, repair_objective=None, complexity=None, code=None, tests_code=None):
    data = dict()
    if code is not None:
        data.update({'source_code_file': open(f'tests/ruby/tests-data/{code}.rb', 'rb')})
    if tests_code is not None:
        data.update({'test_suite_file': open(f'tests/ruby/tests-data/{tests_code}.rb', 'rb')})

    data.update(get_json(code_name, tests_name, repair_objective, complexity))
    return data

def get_json(code_name=None, tests_name=None, repair_objective=None, complexity=None):
    dictionary = { 'source_code_file_name': code_name, 'test_suite_file_name': tests_name, 'repair_objective': repair_objective, 'complexity': complexity }
    data = '{ "challenge": { '
    first = True
    for key in dictionary:
        if dictionary[key] is not None:
            if first:
                data = data + f'"{key}" : "{dictionary[key]}"'
                first = False
            else:
                data = data + f', "{key}" : "{dictionary[key]}"'

    data = data + ' } }'
    return {'challenge': data}