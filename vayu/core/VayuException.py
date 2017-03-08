from flask import jsonify


class VayuException(Exception):
    """
    The class which handles all exceptions
    """

    def __init__(self, status_code, message, payload=None):
        """
        The class constructor
        :param status_code: The status code for the exception
        :param message: The message to be passed in response of API
        :param payload: The payload to be sent in response in the `errors` field
        """
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_json(self):
        """
        Converts the exception to JSON to be directly sent as an API response
        :return: The API response
        """
        res = dict()
        res['error'] = dict()
        res['error']['code'] = self.status_code
        res['error']['message'] = self.message
        if self.payload is not None:
            res['error']['errors'] = self.payload

        return jsonify(res)
