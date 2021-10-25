from . import cSharp
from app import db
from .models import CSharp_Challenge
from flask import jsonify
from flask import make_response

UPLOAD_FOLDER = "./example-challenges/c-sharp-challenges/"
@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('/c-sharp-challenges/<int:id>', methods=['PUT'])
def put_csharp_challenges():
    challenge= CSharp_Challenge.query.filter_by(id=id).first()
    data_Challenge = loads(request.form.get('challenge'))['challenge']

    if challenge is None:
        return make_response(jsonify({"challenge":"There is no challenge for this id"}), 404)

    update_code = request.files['source_code_file']
    update_test = request.files['test_suite_file']
        
    
    analyze_dictionary = loads(request.form.get('challenge'))
    update_challenge = analyze_dictionary['challenge']
    update_repair_objective = update_challenge['repair_objective']
    update_complexity = update_challenge['complexity']

   
    if update_code is not None:
        challenge.code=os.path.split(update_code.filename)[-1].split('.')[0]
        upload(update_code)

    if update_test is not None: 
        challenge.tests_code=os.path.split(update_test.filename)[-1].split('.')[0]
        upload(update_test)


    if update_repair_objective is not None:
        challenge.repair_objective = update_repair_objective

    if update_complexity is not None:
        challenge.complexity = update_complexity
        
    db.session.commit()
    return jsonify({"challenge":CSharp_Challenge.__repr__(challenge)})



def upload(file):
    if file is None:
        return make_response(jsonify({"error_message": "One of the provided files has syntax errors."}))
    if file.filename == '' :
        return make_response(jsonify("No name of file"), 404)
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename.replace(".cs", "/").replace("Test", "") + filename))
 

#verifican si una extensión es válida y que carga el archivo y redirige al usuario a la URL del archivo cargado            
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

