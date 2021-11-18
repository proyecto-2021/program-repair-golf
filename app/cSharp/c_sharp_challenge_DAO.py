from app.cSharp.models import CSharpChallengeModel
from app import db
import os
import shutil


class CSharpChallengeDAO:

    CHALLENGE_SAVE_PATH = "./example-challenges/c-sharp-challenges/"
    CHALLENGE_VALIDATION_PATH = "./public/challenges/"

    def __init__(self):
        pass

    def get_challenge_db(self, id, show_files_content=False):
        challenge = db.session.query(CSharpChallengeModel).filter_by(id=id).first().__repr__()
        if show_files_content:
            challenge['code'] = open(challenge['code'], "r").read()
            challenge['tests_code'] = open(challenge['tests_code'], "r").read()
        return challenge

    def exist(self, id):
        return db.session.query(CSharpChallengeModel).filter_by(id=id).first() is not None

    def save_to_db(self, repair_objective, complexity, code_name, test_name):
        code_name = os.path.splitext(code_name)[0]
        test_name = os.path.splitext(test_name)[0]
        code_path = self.CHALLENGE_SAVE_PATH + code_name + '/' + code_name + '.cs'
        test_path = self.CHALLENGE_SAVE_PATH + code_name + '/' + test_name + '.cs'
        new_challenge = CSharpChallengeModel(code=code_path,
                                             tests_code=test_path,
                                             repair_objective=repair_objective,
                                             complexity=int(complexity),
                                             best_score=0)
        db.session.add(new_challenge)
        db.session.commit()
        return new_challenge.id

    def update_challenge_data(self, id, data):
        db.session.query(CSharpChallengeModel).filter_by(id=id).update(data)
        db.session.commit()

    def save_best_score(self, score, previous_best_score, chall_id):
        if previous_best_score == 0 or previous_best_score > score:
            challenge = db.session.query(CSharpChallengeModel).filter_by(id=chall_id)
            challenge.update(dict(best_score=score))
            db.session.commit()
            return 0
        else:
            return 1

    def remove(self, *paths):
        for path in paths:
            if os.path.exists(path) and os.path.isfile(path):
                os.remove(path)

    def handle_put_files(self, result, prev_src_path, prev_test_path, src_path=None, test_path=None):
        if src_path is not None:
            exe_new = src_path.replace('.cs', '.exe')
        if test_path is not None:
            dll_new = test_path.replace('.cs', '.dll')
        exe_prev = prev_src_path.replace('.cs', '.exe')
        dll_prev = prev_test_path.replace('.cs', '.dll')

        if result == -1:
            self.remove(src_path)
            if test_path is not None:
                self.remove(test_path)
        elif result == 0:
            if src_path is not None:
                self.remove(src_path, exe_new, dll_prev)
            if test_path is not None:
                self.remove(test_path, exe_prev, dll_new)
        elif result == 2:
            if src_path is not None:
                self.remove(src_path, exe_new)
            if test_path is not None:
                self.remove(test_path, exe_prev)
        else:
            if src_path is not None:
                self.remove(exe_new, dll_prev, prev_src_path)
                shutil.move(src_path, prev_src_path)
            if test_path is not None:
                self.remove(dll_new, exe_prev, prev_test_path)
                shutil.move(test_path, prev_test_path)

    def create_challenge_dir(self, challenge_name):
        challenge_dir = self.CHALLENGE_SAVE_PATH + os.path.splitext(challenge_name)[0]
        os.mkdir(create_challenge_dir)
        return challenge_dir + '/'

