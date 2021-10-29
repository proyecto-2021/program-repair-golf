from .. import db
from ..javascript import files_controller
from flask import jsonify, make_response
from pathlib import PurePath, PurePosixPath

class JavascriptChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256))
    tests_code = db.Column(db.String(256))
    repair_objective = db.Column(db.String(128))
    complexity = db.Column(db.Integer)
    best_score =  db.Column(db.Integer)

    def to_dict(self):
        return{
            "id": self.id,
            "code": self.code,
            "tests_code": self.tests_code,
            "repair_objective": self.repair_objective,
            "complexity": self.complexity,
            "best_score": self.best_score
        }

    def find_challenge(id_challenge):
        return JavascriptChallenge.query.filter_by(id=id_challenge).first()
    
    """
    version1
    def compileRunTest(file_path): #Problem Types... ver eso
        compiles_out = files_controller.compile_js(code_file_path)

        if compiles_out:
            files_controller.remove_files(code_file_path,test_file_path)
            return make_response(jsonify({'challenge': f'Error File not compile {compiles_out}'}), 404)

        test_out = files_controller.run_test(test_file_path)   
        if not files_controller.test_fail(test_out):
            files_controller.remove_files(code_file_path,test_file_path)
            return make_response(jsonify({'challenge': f'The test has to fail at least once {test_out}'}), 404)
    
    """
    """
    version2
    def compileRunTest(path_file): #Problem Types.. ver
        compiles_out_err = files_controller.compile_js(file_test_path_upd)
        test_out = files_controller.run_test(file_test_path_upd)

        if compiles_out_err or not files_controller.test_fail(test_out):
            files_controller.remove_files(code_path_upd, test_path_upd)
            err = f'Error File not compile {compiles_out_err}' if compiles_out_err else f'The test has to fail at least once {test_out}'
            return make_response(jsonify({'challenge': f'Error File not compile {err}'}), 404)
    """