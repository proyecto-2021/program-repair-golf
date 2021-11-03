
from .. import folders_and_files
from ..exceptions.CommandRunException import CommandRunException
import subprocess
from .dependences_module import dependences_ok, extract_dependences, install_dependece 
from .command_module import run_command, command_output, run_command_ok
from ..controllers.files_controller import get_name_file   

def compile_js(path_file):
    command = 'node '+path_file
    run_compile = run_command(command)
    if run_command_ok(run_compile):
        raise CommandRunException(f'Compile not found {command}', CommandRunException.HTTP_NOT_FOUND)
    return command_output(run_compile) 

def test_run(path_file):
    #si no existen las dependecias las copia
    if not dependences_ok(folders_and_files.CHALLENGES_PATH):
        extract_dependences()
    
    command_test = f'cd {folders_and_files.CHALLENGES_PATH}; npm test {path_file}' 
    test_run = run_command(command_test)

    if not run_command_ok(test_run) and not test_run_ok(command_output(test_run)): 
        install()
        test_run = run_command(command_test)
  
    if not run_command_ok(test_run) or not test_is_from_to_code(path_file):
        raise CommandRunException(f"The Test not found {test_run}", CommandRunException.HTTP_NOT_FOUND)
    return command_output(test_run)

def test_fail_run(path_file):
    test_out = ''
    try:
        test_out = test_run(path_file)
    except CommandRunException as e:
        if not test_fail(e.msg): 
            raise CommandRunException(f"The Test Not Fail {e.msg}", CommandRunException.HTTP_NOT_FOUND)
    return test_out

def test_run_ok(sh_output):
    return str(sh_output).find("Test Suites:") != -1

def test_is_from_to_code(path_file_test): 
    
    grep_run = f'grep require cat {path_file_test};'
    code_file = get_name_file(path_file_test).split(".")[0]
    code_require = f"require('./{code_file}')"
    return command_output(run_command(grep_run)).find(code_require) != -1
    
def test_fail(sh_output):
    return str(sh_output).find('FAIL') != -1