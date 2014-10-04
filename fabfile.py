from fabric.api import *


staging = ['voer@dev.voer.vn']
production = ['']


@hosts(staging)
def deploy_staging():
    project_dir = '/home/voer/vpw/vpw'
    with cd(project_dir):
        run('git pull')
        run('sudo supervisorctl restart vpw')


@hosts(production)
def deploy_production():
    pass
