# flowroute-messaging-python
## What is it?

Flowroute-messaging-python is a Python SDK that provides methods for sending outbound SMSs with [Flowroute's](https://www.flowroute.com) API v2. These methods can be used to accomplish the following:

* Send outbound SMS
* Retrieve MDRs (message detail records)

## Documentation 
The full documentation for Flowroute's v2 API is available at [flowroute.readme.io](https://flowroute.readme.io/).

## How To Install 

The SDK uses the UniRest and Jsonpickle Python libraries, which will need to be installed before you can use the SDK. To install these packages, open a terminal session and execute the following commands

	cd flowroute-messaging-python/
	pip install -r requirements.txt

> Note: You will need to be connected to the internet in order to install the required packages
  
## How To Get Setup

The following shows how to import the SDK and setup your API credentials.

1) Import the SDK module:

	from FlowrouteMessagingLib.Controllers.APIController import *
	from FlowrouteMessagingLib.Models import *         
   
2) Configure your API Username and Password from [Flowroute Manager](https://manage.flowroute.com/accounts/preferences/api/).
 > If you do not have an API Key contact support@flowroute.com:

	controller = APIController(username="TECH PREFIX", password="SECRET KEY")		

## List of Methods and Example Uses

### APIController

The APIController contains the methods neccesary to both send outbuond SMSs and to retrieve MDRs.

#### create_message(self, message)

The create_message method is used to send outbound messages from SMS enabled Flowroute numbers.

| Parameter | Required | Usage                                                                                |
|-----------|----------|--------------------------------------------------------------------------------------|
| message   | True     | The message parameter that includes your To Number, From Number, and Message Content |

##### Example Usage

	msg = Message(to="15305557784", from_="18444205700", content="Mark it zero")
	response = controller.create_message(msg)

> In the msg variable we have to set the from number as "from_" because from is a reserved word in Python 
	
#### get_message_lookup(self, record_id)

The get_message_lookup method is used to retrieve a MDR (message detail record).

| Parameter | Required | Usage                                                 |
|-----------|----------|-------------------------------------------------------|
| recordId  | True     | The ID for the record that you would like to retrieve |

##### Example Usage

	response = controller.get_message_lookup("mdr1-fab29a740129404a8ca794efc1359e12")