from .go_src import Go_src

class GoChallengeC:

    def __init__(self, id=None, path_code=None, path_tests_code=None, repair_objective=None, complexity=None):
        self.id = id
        self.code = Go_src(path = path_code)
        self.tests_code = Go_src(path = path_tests_code)
        self.repair_objective = repair_objective
        self.complexity = complexity
        self.best_score = 0

    def get_id(self):
        return self.id

    def get_code(self):
        return self.code.get_path()

    def get_code_content(self):
        return self.code.get_content()

    def get_tests_code(self):
        return self.tests_code.get_path()

    def get_tests_code_content(self):
        return self.tests_code.get_content()

    def get_repair_objective(self):
        return self.repair_objective

    def get_complexity(self):
        return self.complexity

    def get_best_score(self):
        return self.best_score

    def get_content(self, id=True, tests_code=True):

        challenge = {
            'id': self.id,
            'code': self.get_code_content(),
            'tests_code': self.get_tests_code_content(), 
            'repair_objective': self.repair_objective,
            'complexity': self.complexity,
            'best_score': self.best_score
        }

        if id and tests_code: 
            return challenge
        elif id and not tests_code:
            del challenge['tests_code']
            return challenge
        elif not id and tests_code:
            del challenge['id']
            return challenge
        
        challenge['code'] = self.code.get_path()
        challenge['tests_code'] = self.tests_code.get_path()
        return challenge

    def set_code(self, path_code):
        self.code.set_path(path_code)

    def set_tests_code(self, path_tests_code):
        self.tests_code.set_path(path_tests_code)

    def set_repair_objective(self, repair_objective):
        self.repair_objective = repair_objective

    def set_complexity(self, complexity):
        self.complexity = complexity

    def set_best_score(self, best_score):
        self.best_score = best_score

    def code_compiles(self):
        return self.code.compiles(is_code=True)

    def tests_compiles(self):
        return self.tests_code.compiles(is_code=False)

    def tests_fail(self):
        return self.tests_code.tests_fail()
