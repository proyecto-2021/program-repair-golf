import subprocess 
from ..exceptions.CommandRunException import CommandRunException


def run_command(command):
    proc = subprocess.run(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    if  proc!= 0:
        raise CommandRunException("Command error:",404)
    return proc
    
def command_output(pro):
    return str(pro.stdout)
    


