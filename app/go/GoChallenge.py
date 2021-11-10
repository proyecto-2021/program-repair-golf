#from app.go.src_code import .......

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

    #Dependiendo lo que necesitemos, deberiamos tener 2 creo.
    #Uno que retorne el path y otro el contenido
    def get_tests_code(self):
        return self.tests_code

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