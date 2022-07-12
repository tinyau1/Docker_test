#!/usr/bin/env python3

# requires docker image built by fw-esp32-v2/docker/images/fw-esp32-v2-builder-env/build.py

import os, subprocess, pathlib, time

project_path = pathlib.Path(subprocess.check_output('git rev-parse --show-toplevel', shell=True).decode('ascii').strip())
idf_path = os.path.join(project_path, 'esp-idf-signify')
idf_tag = subprocess.check_output('git submodule status ' + idf_path, shell=True).decode().lstrip('- ')[:12].split(' ')[0]
src_path = project_path / "app"
docker_image = 'fw-esp32-v1.x-builder-env:' + idf_tag

bash_cmd = [
   'cp /project/signature_verification_key.bin /opt/esp/idf/components/bootloader/subproject/',
   '/bin/bash'
   # 'make'
]

args = [
    'docker', 'run', '-it',
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

