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


    def get_content_get_all(self):
        return {
            'id': self.id,
            'code': self.code.get_content(),
            'repair_objective': self.repair_objective,
            'complexity': self.complexity,
            'best_score': self.best_score
        }

    def get_content_get_by_id(self):
        return {
            'code': self.code.get_content(),
            'tests_code': self.tests_code.get_content(),
            'repair_objective': self.repair_objective,
            'complexity': self.complexity,
            'best_score': self.best_score
        }

    def get_content_post(self):
        return {
            'id': self.id,
            'code': self.get_code_content(),
            'tests_code': self.get_tests_code_content(),
            'repair_objective': self.repair_objective,
            'complexity': self.complexity,
            'best_score': self.best_score
        }

    ####Lo cree porque se rompia con los otros, podriamos ahcer uno generico
    def get_content(self):
        return {
            'id': self.id,
            'code': self.code.get_path(),
            'tests_code': self.tests_code.get_path(),
            'repair_objective': self.repair_objective,
            'complexity': self.complexity,
            'best_score': self.best_score
        }

    def get_content_put(self):
        return {
            'code': self.code.get_content(),
            'tests_code': self.tests_code.get_content(),
            'repair_objective': self.repair_objective,
            'complexity': self.complexity,
            'best_score': self.best_score
        }


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
        return self.code.compiles(True)

    def tests_compiles(self):
        return self.tests_code.compiles(False)

    def tests_fail(self):
        return self.tests_code.tests_fail()

    def remove_dir(self):
        self.code.remove_dir()

    def delete_file(self, is_code=True):
        self.code.delete_files() if is_code else self.tests_code.delete_files()