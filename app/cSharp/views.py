from posixpath import basename
from . import cSharp
from app import db
from .models import CSharp_Challenge
from  flask import jsonify,make_response,json,request
import subprocess,os


@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('c-sharp-challenges/<int:id>/repair', methods=['POST'])
def repair_Candidate(id):
    #to do : implement this method
    # verify challenge's existence 
    if db.session.query(CSharp_Challenge).get(id) is not None:
        challenge = db.session.query(CSharp_Challenge).get(id).__repr__()
        file = request.files['source_code_file']
        file.save('public/challenges')
        file_name = os.path.basename(file)
        cmd = 'mcs ' + 'public/challenges/' + file_name
        if (subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0):
            test = challenge['tests_code']
            test_file_name = os.path.basename(test)
            #commands to run tests
            cmd_export = 'export MONO_PATH=./NUnit.3.13.2/lib/net35/'
            cmd_compile = 'mcs ' + file_name + ' ' + test_file_name + ' -target:library -r:NUnit.3.13.2/lib/net35/nunit.framework.dll -out:' + test_file_name.replace('.cs', '.dll')
            cmd_test = 'mono ./NUnit.ConsoleRunner.3.12.0/tools/nunit3-console.exe ' + test_file_name.replace('.cs', '.dll') + ' -noresult'
            cmd_run_test = 'cmd_export && cmd_compile && cmd_test' 
            if (subprocess.call(cmd_run_test, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0):
                #to do: calculate score
                return make_response(jsonify({'Repair candidate:' : 'Tests passed'}), 200)
            else:
                return make_response(jsonify({'Repair candidate:' : 'Tests not passed'}), 409)
        else:
            return make_response(jsonify({'repair candidate:' : 'Sintax error'}), 409)

    else: 
        return make_response(jsonify({'challenge': 'Not found'}),404)
    pass
