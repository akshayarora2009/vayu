from __future__ import with_statement
from fabric.api import env
from fabric.api import local, settings, abort, run, cd
from fabric.operations import run, put, sudo
import sys


def installGit():
	env.warn_only = True 
	user = env.user
	code_dir = '/home/'+user+'/.vayu'
	run('mkdir -p '+ code_dir )
	codeResult = run('java -version')
	
	if codeResult.return_code != 0:
		with cd(code_dir): 
			put('setup_files/setupgit_ubuntu.sh',code_dir)
			sudo('chmod 777 setupgit_ubuntu.sh')
			sudo('./setupgit_ubuntu.sh')
			sudo('rm setupgit_ubuntu.sh')
	else: 
		print("git is already installed")
	env.warn_only = False


def copyMultipleFiles(projectName='default',files='.'):
	user = env.user
	code_dir = '/home/'+user+'/.vayu'
	code_dir_project = code_dir + '/'+projectName
	run('mkdir -p '+ code_dir )
	run('mkdir -p '+ code_dir_project )
	
	files = files.split(';')
	for file in files:
		put(file, code_dir_project)

    # our local 'testdirectory' - it may contain files or subdirectories ...
    #
