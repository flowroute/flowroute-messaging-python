# -*- coding: utf-8 -*-
"""
   FlowrouteMessagingLib.Controllers.APIController

    Copyright Flowroute, Inc. 2016
"""
import requests

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

    def create_message(self, message) -> dict:
        """Does a POST request to /messages.

        Send a message.

        Args:
            message (Message): Message Object to send.

        Returns:
            dict: Response from the API.

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
        response = requests.post(
            url=query_url,
            headers=headers,
            data=APIHelper.json_serialize(message),
            auth=(self.__username, self.__password))
        json_content = APIHelper.json_deserialize(response.content)

        # Error handling using HTTP status codes
        if response.status_code == 401:
            raise APIException("UNAUTHORIZED", 401, json_content)

        elif response.status_code == 403:
            raise APIException("FORBIDDEN", 403, json_content)

        elif response.status_code < 200 or response.status_code > 206:  # 200 = HTTP OK
            raise APIException("HTTP Response Not OK", response.status_code,
                               json_content)

        return json_content

    def get_message_lookup(self, record_id: str) -> dict:
        """Does a GET request to /messages/{record_id}.

        Lookup a Message by MDR.

        Args:
            record_id (str): Unique MDR ID

        Returns:
            dict: Response from the API.

        Raises:
            APIException:
                When an error occurs while fetching the data from
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
        response = requests.get(
            url=query_url,
            auth=(self.__username, self.__password))
        json_content = APIHelper.json_deserialize(response.content)

        # Error handling using HTTP status codes
        if response.status_code < 200 or response.status_code > 206:  # 200 = HTTP OK
            raise APIException("HTTP Response Not OK", response.status_code,
                               json_content)

        return json_content
