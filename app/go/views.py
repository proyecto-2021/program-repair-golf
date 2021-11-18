import json
from flask import jsonify, request, make_response, json
from app import db
from . import go
from .models_go import GoChallenge
import os, subprocess, math, nltk, shutil
from .go_challenge_dao import goChallengeDAO
from .go_src import Go_src
from .go_challenge import GoChallengeC
from .go_repair_candidate import GoRepairCandidate
from .go_directory_management import GoDirectoryManagement


dao = goChallengeDAO()


@go.route('api/v1/go-challenges/<int:id>/repair', methods=['POST'])
def repair_challenge_go(id):
    '''
    code_solution_file = request.files['source_code_file']
    subprocess.run(["mkdir","solution"],cwd="public/challenges",stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    code_solution_path = os.path.abspath('public/challenges/solution/code_solution.go')
    code_solution_file.save(code_solution_path)
    
    is_good_code_solution_file = subprocess.run(["go build"], cwd=os.path.abspath("public/challenges/solution"),stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)
    if is_good_code_solution_file.returncode == 2:
        return make_response((jsonify({"code_solution_file":"with errors"}),409))
    
    challenge_original = GoChallenge.query.filter_by(id=id).first()
    if challenge_original is None:
        return make_response(jsonify({'Challenge' : 'this challenge does not exist'}), 404)
    challenge_to_dict = challenge_original.convert_dict()
    tests_code = challenge_to_dict["tests_code"]
    
    shutil.copy (tests_code,"public/challenges/solution/code_test.go")
    
    the_challenge_is_solved = subprocess.run(["go test"],cwd=os.path.abspath("public/challenges/solution"),stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)
    if the_challenge_is_solved.returncode == 1:
        return make_response((jsonify({"the challenge":"not solved"}),409))  
    
    challenge_original_code = challenge_to_dict["code"]
    
    f = open (challenge_original_code,'r')
    original_code = f.read()
    f.close()

    f = open (code_solution_path,'r')
    solution_code = f.read()
    f.close()

    edit_distance = nltk.edit_distance(original_code,solution_code)

    current_best_score = challenge_to_dict["best_score"]
    if edit_distance < current_best_score:
        challenge_original.best_score = edit_distance
        db.session.commit()

    challenge_original_updated = GoChallenge.query.filter_by(id=id).first()
    challenge_to_dict_updated = challenge_original_updated.convert_dict()
        

    request_return = {
        "repair":{
            "challenge":{
                "repair_objective": challenge_to_dict["repair_objective"],
                "best_score": challenge_to_dict_updated["best_score"]
            },
            "score": edit_distance
        }
    }

    subprocess.run(["rm" "-r" "solution"],cwd=os.path.abspath("public/challenges"),stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)
    '''
    if not dao.exists(id):
        return make_response(jsonify({'challenge' : 'challenge does not exist'}), 404)

    c = dao.get_challenge_by_id(id)
    challenge = GoChallengeC(path_code=c.code,path_tests_code=c.tests_code,
        repair_objective=c.repair_objective,complexity=c.complexity)

    repair_code = request.files['source_code_file']
    dir = GoDirectoryManagement(path='public/challenges/solution/')
    code = Go_src(path='public/challenges/solution/code.go')
    tests = Go_src(path='public/challenges/solution/code_test.go')

    dir.create_dir()
    code.create_file()
    repair_code.save(code.get_path())
    tests.move(challenge.get_tests_code())

    repair_candidate = GoRepairCandidate(challenge=challenge, dir_path=dir.get_path(), file_path=code.get_path())

    if not repair_candidate.compiles():
        dir.remove_dir()
        return make_response(jsonify({"source_code_file" : "with sintax errors"}), 409)

    if not repair_candidate.tests_fail():
        dir.remove_dir()
        return make_response(jsonify({"challenge" : "not solved"}), 409) 

    score = repair_candidate.score()
    # Falta actualizar el best_score, se debe actualizar ?
    dir.remove_dir()

    show = repair_candidate.get_content(score)
    
    return jsonify({"repair" : show})



@go.route('/api/v1/go-challenges', methods=['GET'])
def get_all_challenges():
    challenges = dao.get_all_challenges()
    if not challenges:
        return make_response(jsonify({'challenges' : 'not found'}), 404)
    
    show = []

    for c in challenges:
        challenge = GoChallengeC(path_code=c.code,path_tests_code=c.tests_code,
            repair_objective=c.repair_objective,complexity=c.complexity)

        show.append(challenge.get_content_get_all())

    return jsonify({"challenges" : show})


@go.route('/api/v1/go-challenges/<id>', methods=['GET'])
def get_challenge_by_id(id):
    if not dao.exists(id):
        return make_response(jsonify({'challenge' : 'not found'}), 404)

    c = dao.get_challenge_by_id(id)

    challenge = GoChallengeC(path_code=c.code,path_tests_code=c.tests_code,
        repair_objective=c.repair_objective,complexity=c.complexity)

    show = challenge.get_content_get_by_id()

    return jsonify({"challenge" : show})



@go.route('/api/v1/go-challenges/<id>', methods=['PUT'])
def update_a_go_challenge(id):

    if not dao.exists(id):
        return make_response(jsonify({'challenge' : 'not found'}), 404)

    data = json.loads(request.form.get('challenge'))['challenge']
    challenge_dao = dao.get_challenge_by_id(id)
    challenge = GoChallengeC(challenge_dao.id, challenge_dao.code, challenge_dao.tests_code, challenge_dao.repair_objective, challenge_dao.complexity)
    old_code  = Go_src(path = challenge.get_code())
    old_tests = Go_src(path = challenge.get_tests_code())

    temporary_directory = GoDirectoryManagement(path='example-challenges/go-challenges/tmp/')
    if request.files and not(temporary_directory.is_dir()):
        temporary_directory.create_dir()

    new_code = 'source_code_file' in request.files 
    if new_code:
        if not ('source_code_file_name' in data):
            return make_response(jsonify({"source_code_file_name" : "not found"}), 409)

        path_to_code = Go_src.create_file_tmp(temporary_directory, data['source_code_file_name'], request.files['source_code_file'])
        challenge.set_code(path_to_code.get_path())

        if not challenge.code_compiles():
            temporary_directory.remove_dir()
            return make_response(jsonify({"source_code_file" : "source code with sintax errors"}), 409)           

    new_test = 'test_suite_file' in request.files
    if new_test: 
        if not ('test_suite_file_name' in data):
            return make_response(jsonify({"test_suite_file_name" : "not found"}), 409)
        
        path_to_tests = Go_src.create_file_tmp(temporary_directory, data['test_suite_file_name'], request.files['test_suite_file'])
        challenge.set_tests_code(path_to_tests.get_path())    

        if not challenge.tests_compiles():
            temporary_directory.remove_dir()
            return make_response(jsonify({"test_suite_file" : "tests with sintax errors"}), 409)

    if new_code and new_test:
        if not challenge.tests_fail():
            temporary_directory.remove_dir()
            return make_response(jsonify({'error' : 'tests must fails'}), 412)  
   
    elif new_code and not new_test:
        temp_test_file = Go_src(path = temporary_directory.get_path() + 'temp_test.go')
        temp_test_file.rewrite_file(old_tests.get_path())
        challenge.set_tests_code(temp_test_file.get_path())
        
        if not challenge.tests_fail():
            temporary_directory.remove_dir()
            return make_response(jsonify({'error' : 'source code must fails tests'}), 412)
        
        challenge.set_tests_code(old_tests.get_path())
   
    elif not new_code and new_test:
        temp_code_file = Go_src(path = temporary_directory.get_path() + 'temp.go')
        temp_code_file.rewrite_file(old_code.get_path())
        challenge.set_code(temp_code_file.get_path())
        
        if not challenge.tests_fail():
            temporary_directory.remove_dir()
            return make_response(jsonify({'error' : 'tests must fails'}), 412)
        
        challenge.set_code(old_code.get_path())

    if new_code:
        old_code.rewrite_file(challenge.get_code())
        challenge.set_code(old_code.get_path()) 

    if new_test:
        old_tests.rewrite_file(challenge.get_tests_code())
        challenge.set_tests_code(old_tests.get_path())
    
    if request.files:
        temporary_directory.remove_dir()

    if 'repair_objective' in data and data['repair_objective'] != challenge.get_repair_objective():
        challenge.set_repair_objective(data['repair_objective'])

    if 'complexity' in data and data['complexity'] != challenge.get_complexity():
       challenge.set_complexity(data['complexity'])
    
    dao.update_challenge(challenge.get_id(), challenge.get_content(id=False, tests_code=False))

    return jsonify({'challenge' : challenge.get_content(id=False)})
    

@go.route('/api/v1/go-challenges', methods=['POST'])
def create_go_challenge():
    challenge_data = json.loads(request.form.get('challenge'))['challenge']

    code_file = request.files["source_code_file"]
    code_path = 'public/challenges/' + challenge_data['source_code_file_name']
    code_file.save(code_path)

    test_suite_file = request.files["test_suite_file"]
    test_suite_path = 'public/challenges/' + challenge_data['test_suite_file_name']
    test_suite_file.save(test_suite_path)

    new_challenge = GoChallenge(
        code=code_path,
        tests_code=test_suite_path,
        repair_objective=challenge_data['repair_objective'],
        complexity=challenge_data['complexity'],
        best_score=math.inf)

    #all_the_challenges = db.session.query(GoChallenge).all()
    all_the_challenges = dao.get_all_challenges()
    for every_challenge in all_the_challenges:
        if every_challenge.code == new_challenge.code:
            return make_response(jsonify({"challenge": "repeated"}), 409)

    test_pass = subprocess.run(["go" "test"], cwd=os.path.abspath("public/challenges"), shell=True)
    test_compilation = subprocess.run(["go" "test" "-c"], cwd=os.path.abspath("public/challenges"),shell=True)
    code_compilation = subprocess.run(["go" "build", code_path], stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL,shell=True)

    codigo = Go_src(path=code_path)
    tests = Go_src(path="public/challenges")

    if code_compilation == 1:
        return make_response(jsonify({"code_file": "The code has syntax errors"}), 412)
    elif test_compilation == 1 or test_compilation.returncode == 2:
        return make_response(jsonify({"test_code_file": "The test code has syntax errors"}), 412)
    elif test_pass.returncode == 0:
        return make_response(jsonify({"ERROR: tests": "There must be at least one test that fails"}), 412)

    db.session.add(new_challenge)
    db.session.commit()

    new_challenge_to_dicc = new_challenge.convert_dict()
    from_file_to_str(new_challenge_to_dicc, "code")
    from_file_to_str(new_challenge_to_dicc, "tests_code")
    return jsonify({"challenge": new_challenge_to_dicc})


def from_file_to_str(challenge, attribute):
    file= open(str(os.path.abspath(challenge[attribute])),'r')
    content=file.readlines()
    file.close()
    challenge[attribute]=content
    return challenge

def compiles(commands, path):
    return (subprocess.run(commands, cwd=path, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL).returncode == 0)

def compiles(command):
    return (subprocess.call(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL) == 0)

def content(path):
    f = open(path, 'r')
    return f.read()

def rewrite_file(path_to_file_used_to_update, path_to_file_to_update):
    with open(path_to_file_used_to_update) as file_used_to_update:
            with open(path_to_file_to_update, 'w') as file_to_update:
                for line in file_used_to_update:
                    file_to_update.write(line)

def delete_files(path):
    for file in os.listdir(path):
      os.remove(os.path.join(path, file))