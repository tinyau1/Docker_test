import os, subprocess, pathlib

project_path = pathlib.Path(subprocess.check_output('git rev-parse --show-toplevel', shell=True).decode('ascii').strip())
idf_path = os.path.join(project_path, 'esp-idf-signify')
idf_tag = subprocess.check_output('git submodule status ' + idf_path, shell=True).decode().lstrip('- ')[:12].split(' ')[0]

print(f'project_path:{project_path}, idf_path:{idf_path}, idf_tag:{idf_tag}')

docker_image = 'fw-esp32-v1.x-builder-env:' + idf_tag

args = [
    'DOCKER_BUILDKIT=1', 'docker', 'build',
    '--no-cache',
    '--progress=plain',
    '--build-arg', 'SSH_PRIVATE_KEY="$(cat /home/`whoami`/.ssh/id_rsa)"', '--build-arg', 'IDF_CHECKOUT_REF='+idf_tag,
    '-t ', docker_image,
    '.'
]

result = subprocess.run('docker image inspect ' + docker_image, shell=True, capture_output=True)
if int(result.returncode) == 0:
    print("Dockerimage exists in local")
else:
    cmd = ' '.join(args)
    print(cmd)
    os.system(cmd)
    
    input('...Done')
