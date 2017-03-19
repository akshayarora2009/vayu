from __future__ import with_statement
from fabric.api import settings,cd
from vayu.core.constants.commands import Linux
from os.path import isfile
from fabric.operations import run, put, sudo,_AttributeString
import vayu.core.constants.local
import os
import zgitignore
import vayu.core.constants.consoleoutput
#returns a list with the below index
#0 -s, --kernel-name        the kernel name
#1  -n, --nodename           the network node hostname
#2  -r, --kernel-release     the kernel release
#3  -v, --kernel-version     the kernel version
#4  -m, --machine            the machine hardware name
#5  -p, --processor          the processor type or "unknown"
#6  -i, --hardware-platform  the hardware platform or "unknown"
#7  -o, --operating-system   the operating system
def connect(machine_info):
    with settings(warn_only=True,user=machine_info.user,host_string = machine_info.host,password=machine_info.password):
        result = []
        result.append(_AttributeString(run(Linux.get_kernal_name)))
        result.append(_AttributeString(run(Linux.get_node_name)))
        result.append(_AttributeString(run(Linux.get_kernal_release)))
        result.append(_AttributeString(run(Linux.get_kernal_version)))
        result.append(_AttributeString(run(Linux.get_machine)))
        result.append(_AttributeString(run(Linux.get_processor)))
        result.append(_AttributeString(run(Linux.get_hardware)))
        result.append(_AttributeString(run(Linux.get_operating_system)))
        installgit(machine_info)
    return result

def installgit(machine_info):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,password=machine_info.password):
        code_dir = vayu.core.constants.local.BASE_DIR_HOST
        run(Linux.make_dir + code_dir)
        codeResult = run(Linux.Ubuntu.check_git)
        if codeResult.return_code != 0:
            with cd(code_dir):
                sudo(Linux.Ubuntu.apt_update)
                sudo(Linux.Ubuntu.install_git)
        else :
            print(vayu.core.constants.consoleoutput.GIT_ALREADY_INSTALLED)

def copyMultipleFiles(machine_info,projectName,files=['.']):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,password=machine_info.password):
        user = machine_info.user
        code_dir = vayu.core.constants.local.BASE_DIR_HOST
        code_dir_project = code_dir + projectName
        run(Linux.make_dir + code_dir)
        run(Linux.make_dir + code_dir_project)

        for file in files:
            put(file, code_dir_project)

def moveProject(machine_info , projectPath , projectName):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,
                  password=machine_info.password):

        ignoredFiles = zgitignore.ZgitIgnore(ignore_case=False)
        try:
            if (checkForVayuIgnore(projectPath)):
                with open(projectPath+"/"+vayu.core.constants.local.VAYU_IGNORE, 'r') as f:
                    ignoredFiles.add_patterns(f.read().splitlines())
            elif (checkForGitIgnore(projectPath)):
                with open(projectPath + "/" + vayu.core.constants.local.GIT_IGNORE, 'r') as f:
                    ignoredFiles.add_patterns(f.read().splitlines())
        except:
                pass

        files = []
        paths = []
        readIgnoredFile(projectPath,projectPath,ignoredFiles,files)

        code_dir = vayu.core.constants.local.BASE_DIR_HOST
        code_dir_project = code_dir + projectName
        run(Linux.make_dir + code_dir)
        run(Linux.make_dir + code_dir_project)

        #check if relative path is '.' . If true that means it is in home directory
        for file in files :
            if(file[1]=='.') :
                put(file[0], code_dir_project)
            else :
                run(Linux.make_dir + os.path.join(code_dir_project, file[1]))
                put(file[0],os.path.join(code_dir_project,file[1]))

def checkForGitIgnore(projectPath) :
    files = os.listdir(projectPath)
    found = False
    for file in files:
        if (file == vayu.core.constants.local.GIT_IGNORE):
            found = True
            break
    return found

def checkForVayuIgnore(projectPath) :
    files = os.listdir(projectPath)
    found = False
    for file in files:
        if (file == vayu.core.constants.local.VAYU_IGNORE):
            found = True
            break
    return found

def readIgnoredFile(projectPath,Path,ignoredFiles,files):
    allFilesInPath =  os.listdir(Path)
    relDir = os.path.relpath(Path,projectPath)
    for file in allFilesInPath :
        if(isfile( os.path.join(Path,file)) and not ignoredFiles.is_ignored(os.path.join(relDir,file))) :
            files.append((os.path.join(Path,file),os.path.join(relDir)))
        elif (os.path.isdir(os.path.join(Path,file)) and not ignoredFiles.is_ignored(os.path.join(relDir,file))):
            readIgnoredFile(projectPath,os.path.join(Path,file),ignoredFiles,files)