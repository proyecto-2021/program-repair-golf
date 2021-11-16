from app.python.file_utils import read_file

examples_path = 'tests/python/example_programs_test/'
api_url = 'http://localhost:5000/python/api/v1/python-challenges'

def request_creator(**params):
    #we check each param's presence and add it to dataChallenge
    dataChallenge = {}
    #file checking
    if params.get('code_path') is not None:
        dataChallenge['source_code_file'] = open(params.get('code_path'), 'rb')
    if params.get('test_path') is not None:
        dataChallenge['test_suite_file'] = open(params.get('test_path'), 'rb')
    
    #creating challenge data as string
    challenge_str = '{ "challenge": { '
    comma_needed = False
    challenge_str, comma_needed = check_and_concatenate(challenge_str, '"source_code_file_name" : "', params.get('code_name'), comma_needed)
    challenge_str, comma_needed = check_and_concatenate(challenge_str, '"test_suite_file_name" : "', params.get('test_name'), comma_needed)
    challenge_str, comma_needed = check_and_concatenate(challenge_str, '"repair_objective" : "', params.get('repair_objective'), comma_needed)
    challenge_str, comma_needed = check_and_concatenate(challenge_str, '"complexity" : "', params.get('complexity'), comma_needed)
    challenge_str += '} }'

    if comma_needed: #comma needed, thus at least one parameter was required
        dataChallenge['challenge'] = challenge_str

    return dataChallenge     

def check_and_concatenate(base_str, base_addition, addition, comma_needed):
    if addition is None: return base_str, comma_needed #nothing to be added
    if comma_needed: base_str += ', '
    comma_needed = True

    base_str += base_addition + addition + '"'    #concatenate strings
    return base_str, comma_needed   #return both string and comma_needed

def create_expected_response(best_score, code_name, complexity, repair_objective, test_name):
    code = read_file(examples_path + code_name, 'r')
    test = read_file(examples_path + test_name, 'r')
    expected_response = {
        'challenge': {
            'best_score': best_score,
            'code': code,
            'complexity': complexity,
            'repair_objective': repair_objective,
            'tests_code': test
        }
    }
    return expected_response

def send_post(client, code_name, test_name, repair_objective, complexity):
    code_path = examples_path + code_name
    test_path = examples_path + test_name
    
    dataChallengePost = request_creator(code_path=code_path, test_path=test_path, code_name=code_name,
    test_name=test_name, repair_objective=repair_objective, complexity=complexity)

    return client.post(api_url, data=dataChallengePost)
