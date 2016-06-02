# -*- coding: utf-8 -*-
"""
   FlowrouteMessagingLib.Controllers.APIController

    Copyright Flowroute, Inc. 2016
"""
import unirest

from FlowrouteMessagingLib.APIHelper import APIHelper
from FlowrouteMessagingLib.Configuration import Configuration
from FlowrouteMessagingLib.APIException import APIException


class APIController(object):
    """
    A Controller to access Endpoints in the FlowrouteMessagingLib API.

    Args:
        username (str): Username for authentication
        password (str): password for authentication
    """

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def create_message(self, message):
        """
        Does a POST request to /messages.

        Send a message

        Args:
            message (Message): Message Object to send.

        Returns:
            string: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        # The base uri for api requests
        query_builder = Configuration.BASE_URI

        # Prepare query string for API call
        query_builder += "/messages"

        # Validate and preprocess url
        query_url = APIHelper.clean_url(query_builder)

        # Prepare headers
        headers = {
            "user-agent": "Flowroute Messaging SDK 1.0",
            "content-type": "application/json; charset=utf-8",
        }

        # Prepare and invoke the API call request to fetch the response
        response = unirest.post(query_url,
                                headers=headers,
                                params=APIHelper.json_serialize(message),
                                auth=(self.__username, self.__password))

        # Error handling using HTTP status codes
        if response.code == 401:
            raise APIException("UNAUTHORIZED", 401, response.body)

        elif response.code == 403:
            raise APIException("FORBIDDEN", 403, response.body)

        elif response.code < 200 or response.code > 206:  # 200 = HTTP OK
            raise APIException("HTTP Response Not OK", response.code,
                               response.body)

        return response.body

    def get_message_lookup(self, record_id):
        """
        Does a GET request to /messages/{record_id}.

        Lookup a Message by MDR

        Args:
            record_id (string): Unique MDR ID

        Returns:
            string: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        # The base uri for api requests
        query_builder = Configuration.BASE_URI

        # Prepare query string for API call
        query_builder += "/messages/{record_id}"

        # Process optional template parameters
        query_builder = APIHelper.append_url_with_template_parameters(
            query_builder, {
                "record_id": record_id,
            })

        # Validate and preprocess url
        query_url = APIHelper.clean_url(query_builder)

        # Prepare headers
        headers = {"user-agent": "Flowroute Messaging SDK 1.0", }

        # Prepare and invoke the API call request to fetch the response
        response = unirest.get(query_url,
                               headers=headers,
                               params={},
                               auth=(self.__username, self.__password))

        # Error handling using HTTP status codes
        if response.code < 200 or response.code > 206:  # 200 = HTTP OK
            raise APIException("HTTP Response Not OK", response.code,
                               response.body)

        return response.body
