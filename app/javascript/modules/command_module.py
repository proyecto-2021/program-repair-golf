import subprocess 


def run_command(command):
    return subprocess.run(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    
def command_output(pro):
    return str(pro.stdout)

def run_command_ok(proc):
    return proc.returncode == 0
    


