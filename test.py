#!/usr/bin/env python3

import sys, os, subprocess, pathlib, time

cmd_setenv='. setenv.sh'
cmd_copy_key='cp /project/signature_verification_key.bin /opt/esp/idf/components/bootloader/subproject/'
cmd_make='make app'

project_path = pathlib.Path(subprocess.check_output('git rev-parse --show-toplevel', shell=True).decode('ascii').strip())
idf_path = os.path.join(project_path, 'esp-idf-signify')
idf_tag = subprocess.check_output('git submodule status ' + idf_path, shell=True).decode().lstrip('- ')[:12].split(' ')[0]
src_path = project_path / "app"
docker_image = 'fw-esp32-v1.x-builder-env:' + idf_tag

arg_len=len(sys.argv)
if(arg_len>=2):
	cmd_make=cmd_make+sys.argv[1]

bash_cmd = [cmd_copy_key,cmd_make]

args = [
    'docker', 'run',
    '--rm',                                     # remove container after build
    '--device=/dev/ttyUSB0',
    '-v', '{}:/project'.format(src_path),   # mount current dir to /project
    '-w', '/project',                           # set working dir /project
    docker_image,
    '/bin/bash', '-c',                          # run bash commands
    '"{}"'.format(' && '.join(bash_cmd))
]

cmd = ' '.join(args)
print(cmd)

time_start = time.time()
os.system(cmd)
time_end = time.time()

print("Time elapsed: {}s".format(time_end - time_start))
input('...Done')





# print(sys.argv)
# print(sys.argv[1],sys.argv[3],sys.argv[5])

