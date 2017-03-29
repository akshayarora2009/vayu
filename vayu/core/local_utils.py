import re
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


def add_new_host(host_id, host_details):
    """
    Adds a new host with the given details
    :param host_details:
    :return:
    """
    hosts = shelve.open(constants.HOSTS_DB, writeback=True)
    if constants.CONFIGURED not in hosts:
        hosts[constants.CONFIGURED] = dict()

    if host_id in hosts[constants.CONFIGURED]:
        raise ValueError("Host with the same IP/hostname already exists")

    try:
        hosts[constants.CONFIGURED][host_id] = host_details
        return host_id
    finally:
        hosts.close()


def delete_configured_host(host_id):
    """
    Deletes a given host permanently
    :param host_id: 
    :return: 
    """
    hosts = shelve.open(constants.HOSTS_DB, writeback=True)

    try:
        if constants.CONFIGURED in hosts:
            del hosts[constants.CONFIGURED][host_id]
    finally:
        hosts.close()

#delete_configured_host("139.59.79.62")


def check_if_host_is_configured(host_id):
    """
    Checks if the host with the given host_id is configured in the hosts.db
    :param host_id:
    :return:
    """
    hosts = shelve.open(constants.HOSTS_DB, writeback=True)
    configured = hosts[constants.CONFIGURED]

    try:
        if host_id in configured:
            return True
        return False
    finally:
        hosts.close()


def add_host_to_data_center(project_id, data_center_id, host_id):
    """
    Adds a host to a data center for a given project
    Only adds the host id in the array, actual host details should be fetched from host db
    :param project_id:
    :param data_center_id:
    :param host_id:
    :return:
    """
    projects = shelve.open(constants.PROJECTS_DB, writeback=True)
    configured_projects = projects[constants.CONFIGURED]
    try:
        if project_id in configured_projects:
            if constants.FLEET in configured_projects[project_id]:
                if data_center_id in configured_projects[project_id][constants.FLEET]:
                    data_center = configured_projects[project_id][constants.FLEET][data_center_id]
                    if constants.HOSTS not in data_center:
                        data_center[constants.HOSTS] = list()

                    if host_id not in data_center[constants.HOSTS]:
                        data_center[constants.HOSTS].append(host_id)

    finally:
        projects.close()


def get_list_of_hosts():
    """
    Returns the list of all hosts
    :return: 
    """
    hosts = shelve.open(constants.HOSTS_DB, writeback=True)
    res = dict()
    res[constants.HOSTS] = dict()
    try:
        if constants.CONFIGURED in hosts:
            res[constants.HOSTS] = hosts[constants.CONFIGURED]

        return res
    finally:
        hosts.close()


def validate_new_host_details(req):
    """
    Validates the host details passed to connect/add new host
    :param req: 
    :return: 
    """
    errors = []

    host_id = req[constants.HOST_ID]
    host_alias = req[constants.HOST_ALIAS]
    auth_method = req[constants.AUTH_METHOD]
    host_auth_user = req[constants.HOST_AUTH_USER]
    host_auth_password = req[constants.HOST_AUTH_PASSWORD]

    if not host_id:
        errors.append("Host ID cannot be empty")

    ip_regex = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$"
    hostname_regex = r"^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$"

    if not (re.search(ip_regex, host_id) and re.search(hostname_regex, host_id)):
        errors.append("Invalid Host name or IP address")

    if not host_alias:
        errors.append("Host Alias cannot be empty")

    if auth_method == "ssh_keys":
        errors.append("Using SSH keys is not yet supported")

    if not host_auth_user:
        errors.append("User cannot be empty")

    if not host_auth_password:
        errors.append("User password cannot be empty")

    hosts = shelve.open(constants.HOSTS_DB)
    try:
        if constants.CONFIGURED in hosts:
            if host_id in hosts[constants.CONFIGURED]:
                errors.append("Host with same id is already configured")
    finally:
        hosts.close()

    return errors


def delete_association_of_host_with_datacenter(project_id, data_center_id, host_id):
    """
    Deletes association of a host with a data center
    :param project_id: 
    :param data_center_id: 
    :param host_id: 
    :return: 
    """
    projects = shelve.open(constants.PROJECTS_DB, writeback=True)

    if constants.CONFIGURED in projects:
        configured_projects = projects[constants.CONFIGURED]
    try:
        if project_id in configured_projects:
            if constants.FLEET in configured_projects[project_id]:
                if data_center_id in configured_projects[project_id][constants.FLEET]:
                    data_center = configured_projects[project_id][constants.FLEET][data_center_id]

                    if host_id in data_center[constants.HOSTS]:
                        data_center[constants.HOSTS].remove(host_id)

    finally:
        projects.close()


def get_project_details_by_id(project_id):
    """
    Returns the details of project by given id
    :param project_id: 
    :return: 
    """
    projects = shelve.open(constants.PROJECTS_DB)

    try:
        if constants.CONFIGURED in projects:
            if project_id in projects[constants.CONFIGURED]:
                return projects[constants.CONFIGURED][project_id]
    finally:
        projects.close()
