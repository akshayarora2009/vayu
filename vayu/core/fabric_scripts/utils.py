from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd ,env
from vayu.core.constants.commands import Linux
from vayu.core.constants.model import machine_info
from fabric.operations import run, put, sudo

def connect(machine_info):
    with settings(warn_only=True,user=machine_info.user,host_string = machine_info.host,password=machine_info.password):
        result = run(Linux.get_all_details)
        installgit(machine_info)
    return result


def installgit(machine_info):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,password=machine_info.password):
        code_dir = '/home/' + machine_info.user + '/.vayu'
        run('mkdir -p ' + code_dir)
        codeResult = run(Linux.Ubuntu.check_git)
        if codeResult.return_code != 0:
            with cd(code_dir):
                sudo(Linux.Ubuntu.apt_update)
                sudo(Linux.Ubuntu.install_git)
        else :
            print("git is already installed")


def copyMultipleFiles(machine_info,projectName='default', files=['.']):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,password=machine_info.password):
        user = machine_info.user
        code_dir = '/home/' + user + '/.vayu'
        code_dir_project = code_dir + '/' + projectName
        run('mkdir -p ' + code_dir)
        run('mkdir -p ' + code_dir_project)

        for file in files:
            put(file, code_dir_project)