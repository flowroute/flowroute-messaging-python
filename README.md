# flowroute-messaging-python
## What is it?

**flowroute-messaging-python** is a Python SDK that provides methods for sending outbound SMS texts and retrieving Message Detail Records (MDRs) using version 2 (**v2**) of the [Flowroute](https://www.flowroute.com") API.

## Documentation 
The full documentation for v2 of the Flowroute API is available [here](https://flowroute.readme.io/).

## Install the required libraries

The SDK uses the UniRest and jsonpickle Python libraries, which must be installed before you can use the SDK. 

* To install these libraries, open a terminal session, and then run the following two commands:
#####
	`cd flowroute-messaging-python/`
	
	`pip install -r requirements.txt`

> **Note:** You must be connected to the Internet in order to install the required libraries.
  
## Import the SDK

The following describes importing the SDK and setting up your API credentials.

1. Run the following two commands to import the SDK module:
#####
	`from FlowrouteMessagingLib.Controllers.APIController import *`
	
	`from FlowrouteMessagingLib.Models import *    `   

2.  Configure your API credentials. 
		
	Run the following after replacing the `Access Key` and `Secret Key` values within the quotes (" ") with your own Access Key and Secret Key. If you do not know these, they can be found on the **Preferences > API Control** page of the [Flowroute](https://manage.flowroute.com/accounts/preferences/api/) portal:

	`controller = APIController(username="Access Key", password="Secret Key")`	

>**Note:** If you do not have API Credentials, contact <mailto:support@flowroute.com>.

With the SDK imported you can use the APIController to send an SMS or retrieve the details of a sent message.

## APIController

The APIController contains the methods required to send outbound SMS texts and to retrieve MDRs.

### Methods 
The following sections describe the use of the APIController and its two methods,` create_message ` and `get_message_lookup`. 

#### Definitions
The URLs for the send a message and retrieve message details endpoints are:

* Send a message: https://api.flowroute.com/v2/messages
* Retrieve message details: https://api.flowroute.com/v2/messages/:record_id

##### <font color="blue">`create_message(self, message)`</font>

The `create_message` method is used to send outbound messages from SMS-enabled Flowroute numbers.

| Parameter | Required | Usage                                                                                |
|-----------|----------|--------------------------------------------------------------------------------------|
| `Message`   | True     | The message parameter. It is composed of `to`, `from`, and `content`parameters, described below.  

#####`Message` parameters
The following describe the parameters that compose the `create_message` method:

| Parameter | Required | Usage                                                                            |
|----------|----------|-----------------------------------------------------------------------------------|
| `to`     | True     | Target phone number for the message. Must use an _1NPANXXXXXX_ E.164 format. | 
|`from`|True|Source phone number. It must be a number registered with Flowroute, must be SMS-enabled, and must use an _1NPANXXXXXX_ E.164 format. |
| `content`| True     | The message itself. An unlimited number of characters can be used, but message length rules and encoding apply. See [Message Length & Concatenation](https://developer.flowroute.com/docs/message-length-concatenation) for more information. | 

###### Example usage

First run the following:

	msg = Message(to="15305557784", from_="18444205700", content="This is the message content.")
> **Note:** Because `from` is a word reserved by Python, Flowroute uses `from_` in the `msg` variable. 

And then run this:	

	response = controller.create_message(msg)

###### Example response

No response is returned for a sent message. Error messages can be returned, however. 

##### Retrieve the message identifier

To get details about the sent message, use the `get_message_lookup` method, described below. Before running `get_message_lookup`, however, you must first get the record identifier from the sent message. Run the following:

	print response
	
The response returns a record containing the message identifier as shown in the following example JSON response:

	{"data": {"id": "mdr1-fab29a740129404a8ca794efc1359e12'}}

#####Error response
The following error codes can be returned:

| Error code | Message | Description                                                 |
|-------|----------|-------------------------------------------------------|
|`401`   |UNAUTHORIZED|The API credentials are incorrect.
|`403`  | FORBIDDEN  | The `from` number is not authorized.|
	
##### <font color="blue">`get_message_lookup(self, record_id)`</font>

The `get_message_lookup` method is used to retrieve an MDR by passing the record identifier of a previously sent message.

| Parameter | Required | Usage                                                 |
|-----------|----------|-------------------------------------------------------|
| `id`      | True     | The identifier of an existing record to retrieve. The value should include the`mdr1-`prefix. |

###### Example usage

	response = controller.get_message_lookup("mdr1-fab29a740129404a8ca794efc1359e12")
###### Example response
> **Note:** The following shows a sample formatted response. It is formatted only to more easily identify the fields returned in the response.

	{
  	"data": {
      "attributes": {
     	  "body": "This is the message content.",
     	  "direction": "outbound",
     	  "amount_nanodollars": 4000000,
    	  "message_encoding": 0,
    	  "timestamp": "2016-05-03T17:41:00.478893+00:00",
    	  "has_mms": false,
    	  "to": "15305557784",
    	  "amount_display": "$0.0040",
    	  "from": "18444205700",
   		  "callback_url": null,
     	  "type": "messages",
    	  "message_type": "long-code"
   		            },
   	  "type": "message",
      "id": "mdr1-cfab29a740129404a8ca794efc1359e12"
  		     }
  	}
######Response message field descriptions
 Parameter | Description                                                 |
|-----------|----------|-------------------------------------------------------|
| `data`  | Object composed of `attributes`, `type`, and `id`. |
|`attributes`    |Object composed of the following:</br>
|  |`body`: The message text.|
|  |`direction`:  The direction of the message. For a sent message, this is `outbound`. For a received message this is`inbound`.|
|  |`amount_nanodollars`: The cost of the message in nanodollars. Because Flowroute uses eight decimal points of precision, the amount in nanodollars is the USD `amount_display` value multipled by 100,000,000 (one hundred million) for a corresponding whole number.
|  |`message_encoding`: Indicates the encoding type, which will be either `0` (UTF-8) or `8` (UCS-2). See [Message Length & Concatenation](https://developer.flowroute.com/docs/message-length-concatenation) for more information.| 
|  |`timestamp`: Date and time, to the second, on which the message was sent. This field displays UTC time using an ISO 8601 format.|
|  |`to`: The phone number to which the message was sent.
|  |`has_mms`: Boolean indicating whether or not the message includes a multimedia file. `true` indicates yes, while `false` indicates no. Currently, MMS is not supported; therefore, this field will always display`false`.
|  |`amount_display`: The total cost of the message in USD. If a message was broken into multiple pieces due to concatenation, this amount will be the total amount for all message pieces. This field does _not_ display out to eight decimal points. See _Message cost_ in [Message Length & Concatenation](https://developer.flowroute.com/docs/message-length-concatenation) for more information.|
|  |`from`: The Flowroute SMS-enabled number from which the message was sent.|
|  |`callback_URL`The callback URL defined for the Flowroute number on the [Preferences > API Control](https://manage.flowroute.com/accounts/preferences/api/) page, the URL appears in this field; otherwise, the value is `null`.|
|  |`type`: Defines the object. Because SMS is the only supported object type, this field will always display `messages`.|
|  |`message_type`: Indicates whether the type of message. If the message was sent to another phone number, this field displays `long-code`; if sent to a toll-free number, this field displays `toll-free`.|
|`type`| Defines the object. Because SMS is the only supported object type, this field will always display `message`.|
|`id` | The unique identifier of a sent message.|
                          

#####Error response
The following error can be returned:

| Error code | Message | Description                                                 |
|-------|----------|-------------------------------------------------------|
|No code number  |Response Not OK|This error is most commonly returned when the `id` passed in the method is incorrect.|
	