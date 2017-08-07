#Command to install git on a machine 139.59.35.6 with user jatin and password '****'
fab --host 139.59.35.6 -u jatin -p **** installGit

#Command to copy multipleFiles to a machine with IP 139.59.35.6 with user jatin and password '****'
fab --host 139.59.35.6 -u jatin -p **** copyMultipleFiles:projectName=testProject,files="setup_files/setupgit_ubuntu.sh;fabfile.py"
