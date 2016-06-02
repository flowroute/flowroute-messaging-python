# -*- coding: utf-8 -*-
"""
   FlowrouteMessagingLib.APIHelper

    Copyright Flowroute, Inc. 2016
"""
import jsonpickle
import re


class APIHelper:
    """
    A Helper Class for various functions associated with API Calls.

    This class contains static methods for operations that need to be
    performed during API requests. All of the methods inside this class are
    static methods, there is no need to ever initialise an instance of this
    class.
    """

    @classmethod
    def json_serialize(cls, obj):
        """
        JSON Serialization of a given object.

        Args:
            obj (object): The object to serialise.

        Returns:
            str: The JSON serialized string of the object.

        """
        if obj is None:
            return None

        # Resolve any Names if it's one of our objects
        # that needs to have this called on
        if isinstance(obj, list):
            value = list()

            for item in obj:
                try:
                    value.append(item.resolve_names())
                except (AttributeError, TypeError):
                    value.append(item)

            obj = value
        else:
            try:
                obj = obj.resolve_names()
            except (AttributeError, TypeError):
                obj = obj

        return jsonpickle.encode(obj, False)

    @classmethod
    def json_deserialize(cls, json):
        """
        JSON Deerialization of a given string.

        Args:
            json (str): The JSON serialized string to deserialize.

        Returns:
            dict: A dictionary representing the data contained in the
                JSON serialized string.

        """
        if json is None:
            return None

        return jsonpickle.decode(json)

    @classmethod
    def append_url_with_template_parameters(cls, url, parameters):
        """
        Replaces template parameters in the given url.

        Args:
            url (str): The query url string to replace the template parameters.
            parameters (dict): The parameters to replace in the url.

        Returns:
            str: Url with replaced parameters.

        """
        # Parameter validation
        if url is None:
            raise ValueError("url is null")
        if parameters is None:
            return url

        # Iterate and replace parameters
        for key in parameters:
            element = parameters[key]
            replace_value = ""

            # Load parameter value
            if element is None:
                replace_value = ""
            elif isinstance(element, list):
                replace_value = "/".join(element)
            else:
                replace_value = str(element)

            url = url.replace('{{{0}}}'.format(key), str(replace_value))

        return url

    @classmethod
    def append_url_with_query_parameters(cls, url, parameters):
        """
        Appends the given set of parameters to the given query string.

        Args:
            url (str): The query url string to append the parameters.
            parameters (dict): The parameters to append.

        Returns:
            str: Url with appended query parameters.

        """
        # Perform parameter validation
        if url is None:
            raise ValueError("url is null")
        if parameters is None:
            return url

        # Does the query string already have parameters?
        has_params = '?' in url

        # Iterate and replace parameters
        for key in parameters:
            element = parameters[key]

            # Ignore null values
            if element is None:
                continue

            # If already has parameters, use the &amp; to append new parameters
            separator = '&' if has_params else '?'

            if isinstance(element, list):
                url = url + '{0}{1}[]={2}'.format(
                    separator, key, '&{0}[]='.format(key).join(element))
            else:
                url = url + '{0}{1}={2}'.format(separator, key,
                                                str(parameters[key]))

            # Indicate the url has params
            has_params = True

        return url

    @classmethod
    def clean_url(cls, url):
        """
        Validates and processes the given query Url to clean empty slashes.

        Args:
            url (str): The given query Url to process.

        Returns:
            str: Clean Url as string.

        """
        # Ensure that the urls are absolute
        regex = "^https?://[^/]+"
        match = re.match(regex, url)
        if match is None:
            raise ValueError('Invalid Url format.')

        # Remove redundant forward slashes
        protocol = match.group(0)
        query_url = url[len(protocol):]
        query_url = re.sub("//+", "/", query_url)

        return protocol + query_url

    @classmethod
    def form_encode(cls, obj, instanceName):
        """
        Encodes a model in a form-encoded manner such as person[Name]

        Args:
            obj (object): The given Object to form encode.
            instanceName (string): The base name to appear before each entry
                for this object.

        Returns:
            dict: A dictionary of form encoded properties of the model.

        """
        # Resolve the names first
        value = APIHelper.resolve_name(obj)
        retval = dict()

        if value is None:
            return None

        # Loop through every item we need to send
        for item in value:
            if isinstance(value[item], list):
                # Loop through each item in the list and add it by number
                i = 0
                for entry in value[item]:
                    retval.update(APIHelper.form_encode(
                        entry, instanceName + "[" + item + "][" + str(
                            i) + "]"))
                    i += 1
            elif isinstance(value[item], dict):
                # Loop through each item in the dictionary and add it
                retval.update(APIHelper.form_encode(value[item], instanceName +
                                                    "[" + item + "]"))
            else:
                # Add the current item
                retval[instanceName + "[" + item + "]"] = value[item]

        return retval

    @classmethod
    def resolve_names(cls, obj, names, retval):
        """
        Resolves parameters from their Model names to their API names.

        Args:
            obj (object): The given Object to resolve names for.
            names (dict): A dictionary containing a mapping from model name
                to API name.
            retval (dict): The dictionary to return which may or may not be
                empty (but must not be None).

        Returns:
            dict: A dictionary form of the model with properties in their API
                formats.

        """
        # Loop through all properties in this model
        for name in names:
            value = getattr(obj, name)

            if isinstance(value, list):
                # Loop through each item
                retval[names[name]] = list()
                for item in value:
                    retval[names[name]].append(APIHelper.resolve_name(item))
            elif isinstance(value, dict):
                # Loop through each item
                retval[names[name]] = dict()
                for key in value:
                    retval[names[name]][key] = APIHelper.resolve_name(value[
                        key])
            else:
                retval[names[name]] = APIHelper.resolve_name(value)

        # Return the result
        return retval

    @classmethod
    def resolve_name(cls, value):
        """
        Resolves name for a given object

        If the object needs to be recursively resolved, this method will
        perform that recursive call.

        Args:
            value (object): A parameter to check if it needs to be recursively
                resolved.

        Returns:
            object: A resolved parameter which may either be a dict or a
                primative object.

        """
        # Check if the item also has to be resolved
        if value is not None and hasattr(value, "resolve_names") and \
                callable(getattr(value, "resolve_names")):
            return value.resolve_names()
        else:
            # Not an object that needs resolving
            return value
