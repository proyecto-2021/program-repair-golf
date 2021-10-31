from subprocess_utils import valid_python_challenge

class PythonChallenge:

  def __init__(self, challenge_data, code, code_path, test, test_path):
    self.code = PythonSourceCode(code, code_path)
    self.test = PythonSourceCode(test, test_path)
    self.repair_objective = challenge_data.get('repair_objective')
    self.complexity = challenge_data.get('complexity')

  def is_valid():
    return valid_python_challenge(code.path, test.path)
  
