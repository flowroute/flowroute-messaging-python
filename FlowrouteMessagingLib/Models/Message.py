# -*- coding: utf-8 -*-

"""
   FlowrouteMessagingLib.Models.Message

   This file was automatically generated for flowroute
   by APIMATIC BETA v2.0 on 02/08/2016
"""
from FlowrouteMessagingLib.APIHelper import APIHelper


class Message(object):
    """
    Implementation of the 'Message' model.

    A simple message.

    Attributes:
        to (string): Phone number in E.164 format to send a message to.
        mfrom (string): Phone number in E.164 format where the message is sent
            from.
        content (string): The content of the message.

    """

    def __init__(self, **kwargs):
        # Set all of the parameters to their default values
        self.to = None
        self.mfrom = None
        self.content = None

        # Create a mapping from API property names to Model property names
        replace_names = {
            "to": "to",
            "from_": "mfrom",
            "content": "content",
        }

        # Parse all of the Key-Value arguments
        if kwargs is not None:
            for key in kwargs:
                # Only add arguments that are actually part of this object
                if key in replace_names:
                    setattr(self, replace_names[key], kwargs[key])

    def resolve_names(self):
        """
        Creates a dictionary representation of this object.

        This method converts an object to a dictionary that represents the
        format that the model should be in when passed into an API Request.
        Because of this, the generated dictionary may have different
        property names to that of the model itself.

        Returns:
            dict: The dictionary representing the object.

        """
        # Create a mapping from Model property names to API property names
        replace_names = {
            "to": "to",
            "mfrom": "from",
            "content": "content",
        }

        retval = dict()

        return APIHelper.resolve_names(self, replace_names, retval)
