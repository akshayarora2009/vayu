import shelve
import vayu.core.constants.local as constants


def add_new_project(project_id, project_details):
    """
    Adds a new project to the Shelve storage
    :param project_id: The unique project ID
    :param project_details: A dictionary object which contains all the metadata about the project
    :return:
    """
    # writeback not required
    projects = shelve.open(constants.PROJECTS_DB)
    try:
        existing = projects[project_id]
    except Exception:
        raise ValueError("Project with same ID already exists.")
    try:
        projects[project_id] = project_details
        return project_id
    finally:
        projects.close()
        return None


def get_list_of_projects():
    """
    Method to get the list of projects to show on `Projects` home page
    :return:
    """
    projects = shelve.open(constants.PROJECTS_DB)
    try:
        return projects
    finally:
        projects.close()

