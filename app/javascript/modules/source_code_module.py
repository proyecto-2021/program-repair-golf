
from .. import folders_and_files
from .dependences_module import ok_dep,extract,install
from ..exceptions.CommandRunException import CommandRunException
import subprocess
from .command_module import run_command, command_output, run_command_ok

def compile_js(path_file):
    command = 'node '+path_file
    run_compile = run_command(command)
    if run_command_ok(run_compile):
        raise CommandRunException(f'Compile not found {command}', CommandRunException.HTTP_NOT_FOUND)
    return command_output(run_compile) 

def run_test(path_file):
    #si no existen las dependecias las copia
    if not dependences.ok_dep(folders_and_files.CHALLENGES_PATH):
        dependences.extract()
    
    command_test = f'cd {folders_and_files.CHALLENGES_PATH}; npm test {path_file}' 
    run_test = run_command(command_test)

    if not run_command_ok(run_test) and not test_run_ok(command_output(run_test)): 
        dependences.install()
        run_test = run_command(command_test)
  
    if not run_command_ok(run_test) or not test_is_from_to_code(path_file):
        raise CommandRunException(f"The Test not found {run_test}", CommandRunException.HTTP_NOT_FOUND)
    return command_output(run_test)

def run_test_fail(path_file):
    test_out = ''
    try:
        test_out = run_test(path_file)
    except CommandRunException as e:
        if not test_fail(e.msg) or not test_is_from_to_code(path_file): 
            raise CommandRunException(f"The Test Not Fail {e.msg}", CommandRunException.HTTP_NOT_FOUND)
    return test_out

def test_run_ok(sh_output):
    return str(sh_output).find("Test Suites:") != -1

def test_is_from_to_code(path_file_test): 
    from ..Controllers.files_controller import get_name_file   
    grep_run = f'grep require cat {path_file_test};'
    code_file = get_name_file(path_file_test).split(".")[0]
    code_require = f"require('./{code_file}')"
    return command_output(run_command(grep_run)).find(code_require) != -1
    
def test_fail(sh_output):
    return str(sh_output).find('FAIL') != -1