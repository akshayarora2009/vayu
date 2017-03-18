import shelve
import vayu.core.constants.local as constants
import os


def add_new_project(project_id, project_details):
    """
    Adds a new project to the Shelve storage
    :param project_id: The unique project ID
    :param project_details: A dictionary object which contains all the metadata about the project
    :return:
    """
    # writeback is required
    projects = shelve.open(constants.PROJECTS_DB, writeback=True)
    if constants.CONFIGURED not in projects:
        projects[constants.CONFIGURED] = dict()

    if project_id in projects[constants.CONFIGURED]:
        raise ValueError("Project with same ID already exists")

    try:
        projects[constants.CONFIGURED][project_id] = project_details
        return project_id
    finally:
        projects.close()


def get_list_of_projects():
    """
    Method to get the list of projects to show on `Projects` home page
    :return:
    """
    projects = shelve.open(constants.PROJECTS_DB)
    try:
        if constants.CONFIGURED in projects:
            return projects[constants.CONFIGURED]
        return None
    finally:
        projects.close()


def delete_project(project_id):
    """
    Delete a project from list of configured projects with the given id
    :param project_id:
    :return:
    """
    projects = shelve.open(constants.PROJECTS_DB, writeback=True)

    try:
        if project_id in projects[constants.CONFIGURED]:
            del projects[constants.CONFIGURED][project_id]
    finally:
        projects.close()


def make_sure_vayu_root_exists():
    """
    This method makes sure that the vayu root is initialised in the home
    directory of the user.
    :return:
    """
    if not os.path.exists(constants.BASE_DIR):
        print("Creating")
        os.mkdir(constants.BASE_DIR)
