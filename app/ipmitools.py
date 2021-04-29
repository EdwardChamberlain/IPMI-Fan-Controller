import subprocess


def run_IPMI_command(command):
    pipe = subprocess.PIPE
    result = subprocess.Popen(command, shell=True, stderr=pipe, stdout=pipe)
    result = result.stderr.read().decode("utf-8").strip()

    if 'Error' in result:
        return result
    else:
        return None
