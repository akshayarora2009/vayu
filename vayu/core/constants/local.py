import os



def get_user_home_path():
    """
    This method returns the home path of user
    eg. /home/jake in *nix
    C:\Users\jake in Windows
    :return:
    """
    return os.path.expanduser('~')


FLEET = 'fleet'
CONFIGURED = 'configured'
HOME_DIR = get_user_home_path()
BASE_DIR = os.path.join(HOME_DIR, ".vayu/")
PROJECTS_DB = BASE_DIR + "projects.db"
VAYU_IGNORE = ".vayuignore"
GIT_IGNORE = ".gitignore"
BASE_DIR_HOST = "~/.vayu/"
DATA_CENTER_ID = 'data_center_id'
DATA_CENTER_NAME = 'data_center_name'