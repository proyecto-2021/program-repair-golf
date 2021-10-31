
class PythonSourceCode:
  
  def __init__(self, code, path):
    self.content = code
    self.path = path
    self.name = (lambda x: x.split('/')[-1]) (path)