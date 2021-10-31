
def valid_python_challenge(code_path,test_path):
    #checks for any syntax errors in code
    if not no_syntax_errors(code_path):
        return {"Error": "Syntax error at " + code_path}
    #checks for any syntax errors in tests code
    elif not no_syntax_errors(test_path):
        return {"Error": "Syntax error at " + test_path}
    #checks if at least one test don't pass
    elif not tests_fail(test_path):
        return {"Error": "At least one test must fail"}
    else:   #program is fine 
        return { 'Result': 'ok' }

def no_syntax_errors(code_path):
    try:
        p = subprocess.call("python -m py_compile " + code_path ,stdout=subprocess.PIPE, shell=True)
        return p == 0   #0 is no syntax errors, 1 is the opposite
    except CalledProcessError as err:
        return False

def tests_fail(test_path):
    try:
        p = subprocess.call("python -m pytest " + test_path ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return p != 0 #0 means all tests passed, other value means some test/s failed
    except CalledProcessError as err:
        return True

def delete_file(path):
  subprocess.call("rm " + path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)