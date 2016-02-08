Flowroute Messaging for Python
=================
This API SDK is built and managed by the Flowroute team.

Due to the UniRest package dependency this SDK only works under Python 2.7
It will not work using Python 3.x

How To Configure:
=================
The generated code needs to be configured with your API credentials. To do that,
provide the credentials and configuration values as constructor parameters for the controllers.

    controller = APIController(username=YOUR_ACCESS_KEY, password=YOUR_API_SECRET_KEY)

How To Build: 
=============
The generated code uses Python libraries named UniRest and Jsonpickle. 

PIP is a popular tool for managing python packages[1].
To resolve these packages:
1) From terminal/cmd navigate to the root directory
2) Invoke 'pip install -r requirements.txt'

Note: You will need internet access to resolve these dependencies.

How To Use:
===========
The following shows how to make invoke the APIController controller.
It is also shown in [2].

    1. Create a "APIControllerTest.py" file in the root directory.
    2. Add the following import statement 
        'from FlowrouteMessagingLib.Controllers.APIController import *'
    3. Create a new instance using 'controller = APIController()'
    4. Invoke an endpoint with the appropriate parameters, for example
        'response = controller.create_messages(<required parameters if any>)'
    5. "response" will now be an object of type String.

[1] PIP - https://pip.pypa.io

[2] from FlowrouteMessagingLib.Controllers.APIController import *

	controller = APIController(username=YOUR_ACCESS_KEY, password=YOUR_API_SECRET_KEY)
    response = controller.create_messages()

    print response
