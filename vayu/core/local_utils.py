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


def add_new_data_center(project_id, center_details):
    """
    Adds a new data center for the given project_id
    :param project_id:
    :param center_details:
    :return:
    """

    projects = shelve.open(constants.PROJECTS_DB, writeback=True)
    configured_projects = projects[constants.CONFIGURED]
    try:
        if project_id in configured_projects:
            if constants.FLEET not in configured_projects[project_id]:
                configured_projects[project_id][constants.FLEET] = dict()

            fleet = configured_projects[project_id][constants.FLEET]

            if center_details[constants.DATA_CENTER_ID] not in fleet:
                fleet[center_details[constants.DATA_CENTER_ID]] = center_details
            else:
                raise ValueError("Data Center with same UID is already present")
    finally:
        projects.close()


def delete_data_center(project_id, data_center_id):
    """
    This method deletes a data center from a given project
    :param project_id:
    :param data_center_id:
    :return:
    """
    projects = shelve.open(constants.PROJECTS_DB, writeback=True)
    configured_projects = projects[constants.CONFIGURED]
    try:
        if project_id in configured_projects:
            if constants.FLEET in configured_projects[project_id]:
                if data_center_id in configured_projects[project_id][constants.FLEET]:
                    del configured_projects[project_id][constants.FLEET][data_center_id]
    finally:
        projects.close()


def get_fleet_details(project_id):
    """
    Returns the details of the fleet for the given project_id
    :param project_id:
    :return:
    """
    projects = shelve.open(constants.PROJECTS_DB, writeback=True)
    configured_projects = projects[constants.CONFIGURED]
    try:
        if project_id in configured_projects:
            if constants.FLEET in configured_projects[project_id]:
                return configured_projects[project_id][constants.FLEET]
    finally:
        projects.close()
