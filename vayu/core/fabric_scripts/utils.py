from __future__ import with_statement
from fabric.api import settings,cd
from vayu.core.constants.commands import Linux
from os.path import isfile
from fabric.operations import run, put, sudo,_AttributeString,local
import vayu.core.constants.local
import os
import zgitignore
import vayu.core.constants.consoleoutput
import sys


def assignouterr():
    sys.stdout = open('/home/jatin/PycharmProjects/vayu/console.log', 'w')

def connect(machine_info,installGit=False):
    with settings(warn_only=True,user=machine_info.user,host_string = machine_info.host,password=machine_info.password):
        result = {}
        result["kernal_name"] = _AttributeString(run(Linux.get_kernal_name));
        result["node_name"] = _AttributeString(run(Linux.get_node_name));
        result["kernal_release"] = _AttributeString(run(Linux.get_kernal_release));
        result["kernal_version"] = _AttributeString(run(Linux.get_kernal_version));
        result["machine"] = _AttributeString(run(Linux.get_machine));
        result["hardware"] = _AttributeString(run(Linux.get_hardware));
        result["processor"] = _AttributeString(run(Linux.get_processor));
        result["operating_system"] = _AttributeString(run(Linux.get_operating_system));
        result["ping_details"] = local(Linux.ping + machine_info.host + Linux.ping_complete , capture=True).replace("rtt","")
        result["lsb_release"] = _AttributeString(run(Linux.lsb_release)).replace("\t","").replace("\r","").split("\n");
        if(installGit) :
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


def installPythonDependencies(machine_info):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,
                  password=machine_info.password):
        code_dir = vayu.core.constants.local.BASE_DIR_HOST
        run(Linux.make_dir + code_dir)
        run("wget https://bootstrap.pypa.io/get-pip.py")
        run("python get-pip.py")
        sudo(Linux.Ubuntu.PythonDependencies.freeportinstall)
        codeResult = run(Linux.Ubuntu.check_node)
        if codeResult.return_code != 0:
            with cd(code_dir):
                sudo(Linux.Ubuntu.PythonDependencies.install_python_setup_tools)
                sudo(Linux.Ubuntu.PythonDependencies.install_python_dev_tools)
        else:
            print(vayu.core.constants.consoleoutput.PYTHON_ALREADY_INSTALLED)


def installNodeJsDependicies(machine_info):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,
                  password=machine_info.password):
        code_dir = vayu.core.constants.local.BASE_DIR_HOST
        run(Linux.make_dir + code_dir)
        codeResult = run(Linux.Ubuntu.check_node)
        if codeResult.return_code != 0:
            with cd(code_dir):
                sudo(Linux.Ubuntu.apt_update)
                sudo(Linux.Ubuntu.install_npm)
                sudo(Linux.Ubuntu.install_nvmfromnpm)
                sudo(Linux.Ubuntu.install_node_js)
                sudo(Linux.Ubuntu.install_node_legacy)
                sudo(Linux.Ubuntu.install_pm2fromnpm)
        else:
            print(vayu.core.constants.consoleoutput.NODE_ALREADY_INSTALLED)

def copyMultipleFiles(machine_info,projectName,files=['.']):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,password=machine_info.password):
        user = machine_info.user
        code_dir = vayu.core.constants.local.BASE_DIR_HOST
        code_dir_project = code_dir + projectName
        run(Linux.make_dir + code_dir)
        run(Linux.make_dir + code_dir_project)

        for file in files:
            put(file, code_dir_project)

def deployCode (machine_info,projectInfo):
    if projectInfo.type == "Node.js" :
        deployNodeJs(machine_info,projectInfo)
    if projectInfo.type == "Python":
        deployPython(machine_info, projectInfo)

def deployPython(machine_info,projectInfo):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,
                  password=machine_info.password):
        installPythonDependencies(machine_info)
        projectName = projectInfo.id
        startingFile = projectInfo.entry_point
        sudo("kill $(sudo lsof -t -i:"+projectInfo.port+")")
        #print "DETAILS OF PREIVOUS RUNNING " + projectName

        #codeResult = run(Linux.Ubuntu.show_nodejsappplication_pm2+projectName)
        #if codeResult.return_code == 0:
         #   run(Linux.Ubuntu.delete_nodejsappplication_pm2+projectName)

        with cd(os.path.join(vayu.core.constants.local.BASE_DIR_HOST,projectName)):
            run("python3 setup.py install")
            run("python3 "+startingFile)

        #print "DETAILS OF NEW RUNNING " + projectName
        #run(Linux.Ubuntu.show_nodejsappplication_pm2 + projectName)



def deployNodeJs(machine_info,projectInfo):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,
                  password=machine_info.password):
        installNodeJsDependicies(machine_info)
        projectName = projectInfo.id
        startingFile = projectInfo.entry_point
        print "DETAILS OF PREIVOUS RUNNING " + projectName

        codeResult = run(Linux.Ubuntu.show_nodejsappplication_pm2+projectName)
        if codeResult.return_code == 0:
            run(Linux.Ubuntu.delete_nodejsappplication_pm2+projectName)

        with cd(os.path.join(vayu.core.constants.local.BASE_DIR_HOST,projectName)):
            run(Linux.Ubuntu.npm_install)

        run(Linux.Ubuntu.run_nodejsappplication_pm2+os.path.join(vayu.core.constants.local.BASE_DIR_HOST,projectName,startingFile)+Linux.Ubuntu.pm2_name+projectName) #~/.vayu/nodeTest/server.js

        print "DETAILS OF NEW RUNNING " + projectName
        run(Linux.Ubuntu.show_nodejsappplication_pm2 + projectName)

def stopDeploy(machine_info,projectName):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,
                  password=machine_info.password):
        run(Linux.Ubuntu.stop_nodejsappplication_pm2+projectName) #~/.vayu/nodeTest/server.js

def deleteDeploy(machine_info,projectName):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,
                  password=machine_info.password):
        run(Linux.Ubuntu.delete_nodejsappplication_pm2+projectName) #~/.vayu/nodeTest/server.js

def addProject(projectPath):
    with settings(warn_only=True):
            local("cd "+projectPath+" | "+Linux.Ubuntu.git_init)
            local(Linux.Ubuntu.git_add)
            local(Linux.Ubuntu.git_commit)

def moveProject(machine_info ,project_info1):
    with settings(warn_only=True, user=machine_info.user, host_string=machine_info.host,
                  password=machine_info.password):
        projectPath = project_info1.path
        projectName = project_info1.id
        ignoredFiles = zgitignore.ZgitIgnore(ignore_case=False)
        try:
            if (checkForVayuIgnore(projectPath)):
                print "VAYUIGNORE FOUND"
                with open(projectPath+"/"+vayu.core.constants.local.VAYU_IGNORE, 'r') as f:
                    ignoredFiles.add_patterns(f.read().splitlines())
            elif (checkForGitIgnore(projectPath)):
                print "GITIGNORE FOUND"
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




