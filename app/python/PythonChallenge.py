from .subprocess_utils import valid_python_challenge
from .file_utils import save_file
from .PythonSourceCode import PythonSourceCode

class PythonChallenge:

  def __init__(self, **data):
    challenge_data = data['challenge_data']
    code = data.get('code')
    
    if code is None: #if no explicit code, then we have the path
      self.code = PythonSourceCode(path=challenge_data.code)
      self.test = PythonSourceCode(path=challenge_data.tests_code)
      self.repair_objective = challenge_data.repair_objective
      self.complexity = challenge_data.complexity
    else: #we have code but not path for it
      self.code = PythonSourceCode(code=data['code'], name=challenge_data['source_code_file_name'])
      self.test = PythonSourceCode(code=data['test'], name=challenge_data['test_suite_file_name'])
      self.repair_objective = challenge_data['repair_objective']
      self.complexity = challenge_data['complexity']

  def is_valid(self):
    return valid_python_challenge(self.code.path, self.test.path)
  
  def code_path(self):
    return self.code.path

  def test_path(self):
    return self.test.path

  #saves source code ath new path
  def save_at(self, path):
    new_code_path = path + self.code.name
    save_file(new_code_path, "wb", self.code.content)
    self.code.path = new_code_path

    new_test_path = path + self.test.name
    save_file(new_test_path, "wb", self.test.content)
    self.test.path = new_test_path

  #if content is true the json will contain code, otherwise it will contain the paths of code
  def to_json(self, content = True):
    challenge_data = {'repair_objective': self.repair_objective, 'complexity': self.complexity}
    
    if content:
      challenge_data['code'] = self.code.get_content()
      challenge_data['tests_code'] = self.test.get_content()
    else:
      challenge_data['code'] = self.code.path
      challenge_data['tests_code'] = self.test.path
    
    return challenge_data