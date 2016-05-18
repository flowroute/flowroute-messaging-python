# -*- coding: utf-8 -*-

"""
   FlowrouteMessagingLib.APIException

    Copyright Flowroute, Inc. 2016
"""


class APIException(Exception):
    """
    Class that handles HTTP Exceptions when fetching API Endpoints.

    Attributes:
        reason (string): The reason (or error message) for the Exception to be
            raised.
        response_code (int): The HTTP Response Code from the API Request that
            caused this exception to be raised.
        response_body (string): The body that was retrieved during the API
            request.
    """

    def __init__(self, reason, response_code, response_body):
        Exception.__init__(self, reason)
        self.response_code = response_code
        self.response_body = response_body
