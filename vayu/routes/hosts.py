from flask import Blueprint, render_template, request, make_response, jsonify
import os
import vayu.core.local_utils as lutils
from vayu.core.VayuException import VayuException
import vayu.core.constants.local as constants
import re
import vayu.core.fabric_scripts.utils as futils
from vayu.core.constants.model import machine_info


hosts_app = Blueprint('hosts_app', __name__)


@hosts_app.route('/hosts/connect', methods=['POST'])
def connect_host():
    """
    Connect to a host with given parameters and return the results
    :return: 
    """
    host_id = request.form[constants.HOST_ID]
    host_alias = request.form[constants.HOST_ALIAS]
    auth_method = request.form[constants.AUTH_METHOD]
    host_auth_user = request.form[constants.HOST_AUTH_USER]
    host_auth_password = request.form[constants.HOST_AUTH_PASSWORD]

    req = dict()
    req[constants.HOST_ID] = host_id
    req[constants.HOST_ALIAS] = host_alias
    req[constants.AUTH_METHOD] = auth_method
    req[constants.HOST_AUTH_USER] = host_auth_user
    req[constants.HOST_AUTH_PASSWORD] = host_auth_password

    errors = lutils.validate_new_host_details(req)

    if not errors:
        try:
            mm = machine_info(host_auth_user, host_id, host_auth_password)
            host_details = futils.connect(mm)
            return make_response(jsonify(host_details), 200)
        except Exception:
            errors.append("There was an error connecting to the host")

    if errors:
        v = VayuException(400, "There were some errors", errors)
        return make_response(v.to_json(), v.status_code)
