import subprocess
from .file_utils import get_filename

def valid_python_challenge(code_path, test_path, test_pass = False):
    #checks for any syntax errors in code
    if not no_syntax_errors(code_path):
        return {"Error": "Syntax error at " + get_filename(code_path)}
    #checks for any syntax errors in tests code
    elif not no_syntax_errors(test_path):
        return {"Error": "Syntax error at " + get_filename(test_path)}
    
    #checks for tests
    test_result = run_tests(test_path)
    if 'Error' in test_result:
        return test_result  #in case of importError we return error message
    #check if tests failed or not
    test_failed = test_result['Result'] == "Tests failed"
    
    if test_failed and test_pass:
        return {"Error": "Some test failed"}
    elif not test_failed and not test_pass:
        return {"Error": "At least one test must fail"}
    #program is fine 
    return { 'Result': 'ok' }

def no_syntax_errors(code_path):
    result = subprocess.run("python -m py_compile " + code_path ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result.returncode == 0   #0 is no syntax errors, 1 is the opposite

def run_tests(test_path):
    result = subprocess.run("python -m pytest " + test_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if "ImportError" in result.stdout.decode():
        return {"Error" : "Import error, tests can't run"}
    elif result.returncode != 0:    #0 means all tests passed, other value means some test/s failed
        return {"Result" : "Tests failed"}
    else:
        return {"Result" : "Tests passed"}
    
def delete_file(path):
    subprocess.call("rm " + path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)