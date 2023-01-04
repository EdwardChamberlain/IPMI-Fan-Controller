import subprocess
import config

def set_manual_mode():
    return run_IPMI_command(f"ipmitool -I lanplus -H {config.IPMI_HOST} -U {config.IPMI_USER} -P {config.IPMI_PASS} raw 0x30 0x30 0x01 0x00")

def set_auto_mode():
    return run_IPMI_command(f"ipmitool -I lanplus -H {config.IPMI_HOST} -U {config.IPMI_USER} -P {config.IPMI_PASS} raw 0x30 0x30 0x01 0x01")

def set_fan_speed(speed):
    fan_speed = str(hex(int(speed)))
    return run_IPMI_command(f"ipmitool -I lanplus -H {config.IPMI_HOST} -U {config.IPMI_USER} -P {config.IPMI_PASS} raw 0x30 0x30 0x02 0xff {fan_speed}")

def run_IPMI_command(command):
    pipe = subprocess.PIPE
    result = subprocess.Popen(command, shell=True, stderr=pipe, stdout=pipe)
    result = result.stderr.read().decode("utf-8").strip()

    if 'Error' in result:
        return result
    else:
        return None

