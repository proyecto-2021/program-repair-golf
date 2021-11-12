from go_src import Go_src

class GoChallenge:

    def __init__(self, path_code, path_tests_code, repair_objective, complexity):
        self.code = Go_src(path = path_code)
        self.tests_code = Go_src(path = path_tests_code)
        self.repair_objective = repair_objective
        self.complexity = complexity
        self.best_score = 0

    def get_code(self):
        return self.code.get_path()

    def get_code_content(self):
        return self.code.get_content()

    def get_tests_code(self):
        return self.tests_code.get_path()

    def get_tests_content(self):
        return self.tests_code.get_content()

    def get_best_score(self):
        return self.best_score

    #Code y tests_code tienen que ser el codigo. Usar metodo de src_code
    def get_content_by_id(self):
        return {
            'code': self.code.get_content(),
            'tests_code': self.tests_code.get_content(),
            'repair_objective':self.repair_objective,
            'complexity':self.complexity,
            'best_score':self.best_score,
        }

    def set_code(self, path_code):
        self.code.set_path(path_code)

    def set_tets_code(self, path_tests_code):
        self.tests_code.set_path(path_tests_code)

    def set_repair_objective(self, repair_objective):
        self.repair_objective = repair_objective

    def set_complexity(self, complexity):
        self.complexity = complexity

    def codes_compiles(self):
        return self.code.code_compiles() and self.tests_code.test_compiles()

    def code_compiles(self):
        return self.code.code_compiles()

    def tests_compiles(self):
        return self.tests_code.test_compiles()

path_code = Go_src(path='example-challenges/go-challenges/median.go')
path_test = Go_src(path='example-challenges/go-challenges/median_test.go')
go_challenge = GoChallenge(path_code.get_path(), path_test.get_path(), 'Make asd pass.', '2')

go_challenge.set_code('app/go/views.py')
print(go_challenge.get_code())
print(go_challenge.get_tests_code())

