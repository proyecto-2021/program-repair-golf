from .go.src_code import Go_src

class GoChallenge:

    def __init__(self, path_code, path_tests_code, repair_objective, complexity):
        self.code = path_code
        self.tests_code = path_tests_code
        self.repair_objective = repair_objective
        self.complexity = complexity
        self.best_score = 0

    #Dependiendo lo que necesitemos, deberiamos tener 2 creo.
    #Uno que retorne el path y otro el contenido
    def get_code(self):
        return self.code

    def get_code_content(self):
        self.code = Go_src(path=path_code)
        return self.code.get_content()

    #Dependiendo lo que necesitemos, deberiamos tener 2 creo.
    #Uno que retorne el path y otro el contenido
    def get_tests_code(self):
        return self.tests_code

    def get_tests_content(self):
        self.tests_code = Go_src(path=path_tests_code)
        return self.code.get_content()

    def get_best_score(self):
        return self.best_score

    #Code y tests_code tienen que ser el codigo. Usar metodo de src_code
    def get_content(self):
        return {
            self.code,
            self.tests_code,
            self.repair_objective,
            self.complexity,
            self.best_score,
        }

    #Se le debe asignar un src_code
    def set_code(self, path_code):
        self.code = path_code

    #Se le debe asignar un src_code            
    def set_tets_code(self, path_tests_code):
        self.tests_code = path_tests_code

    def set_repair_objective(self, repair_objective):
        self.repair_objective = repair_objective

    def set_complexity(self, complexity):
        self.complexity = complexity

    def codes_compiles():
        return self.code.code_compiles() and self.tests_code.test_compiles()

    def code_compiles():
        return self.code.code_compiles()

    def tests_compiles():
        return self.code.test_compiles()