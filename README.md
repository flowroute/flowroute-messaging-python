# flowroute-messaging-python
## About the flowroute-messaging-python SDK

**flowroute-messaging-python** is a Python SDK that provides methods to send an outbound SMS from a Flowroute phone number and also to retrieve a Message Detail Records (MDR). These methods use **v2** (version 2) of the [Flowroute](https://www.flowroute.com") API.

**Note:** This SDK does not cover searching for a set of MDRs based on a date range. For searching on a date range, see [Look up a Set of Messages](https://developer.flowroute.com/docs/lookup-a-set-of-messages) on the Flowroute Developer Portal.

## Documentation 
The full documentation for v2 of the Flowroute API is available [here](https://flowroute.readme.io/).

## Install the required libraries

The SDK uses the **Unirest** and **jsonpickle** Python libraries, which must be installed before you can use the SDK. 

> **Note:** You must be connected to the Internet in order to install the required libraries.

1. Open a terminal session. 

2. If needed, create a parent directory folder where you want to install the SDK.
 
3. Go to the newly created folder, and run the following:

 	`git clone https://github.com/flowroute/flowroute-messaging-python.git`
 	
 	The `git clone` command clones the **flowroute-messaging-python** respository as a sub directory within the parent folder.
 	
4.	Change directories to the newly created **flowroute-messaging-python** directory.

5.	Run the following:

	`pip install -r requirements.txt`

6.	Import the SDK.
  
## Import the SDK

The following describes how to import the Python SDK and set up your API credentials. Before you start, you should have your API credentials (Access Key and Secret Key). These can be found on the **Preferences > API Control** page of the [Flowroute](https://manage.flowroute.com/accounts/preferences/api/) portal.

>**Note:** If you do not have API credentials, contact <mailto:support@flowroute.com>.

1. From the **flowroute-messaging-python** directory, run

	`python`
		
2.	At the `>>>` prompt run the following import commands:

	`from FlowrouteMessagingLib.Models.Message import Message`
	
	`from FlowrouteMessagingLib.Controllers.APIController import APIController  `   

2.  Run the following, replacing the *`Access Key`* and *`Secret Key`* variables within the quotes (`""`) with your own Access Key and Secret Key:
	
		controller = APIController(username="Access Key", password="Secret Key")

	The SDK is imported.

You can now use the APIController to send an SMS or retrieve the details of a sent message.

## APIController

The APIController contains the functions required to send outbound SMS texts and to retrieve MDRs.

### Methods 
The following sections describe the use of the APIController and its two functions,` create_message ` and `get_message_lookup`. 

#### Definitions
The URLs for the send a message and retrieve message details endpoints are:

* Send a message: https://api.flowroute.com/v2/messages
* Retrieve message details: https://api.flowroute.com/v2/messages/:record_id

##### <font color="blue">`create_message(self, message)`</font>

The `create_message` function is used to send outbound messages from an SMS-enabled Flowroute number, formatted as follows:

	msg = Message(to="to_number", from_="from_number", content="message_body")
	
 It is composed of the following variable:

| Parameter | Required | Usage                                                                                |
|-----------|----------|-------------------------------------------------------------------------------|
| *`msg`*   | True     | The message variable, which is composed of the `Message` model, described below. The variable can have any name, and there is no limit on the length. </br>For this method, `msg` will be used. 

#####`Message` parameters
The following describe the parameters that compose the `Message` object:

| Parameter | Required | Usage                                                                            |
|----------|----------|-----------------------------------------------------------------------------|
| `to`     | True     | Target phone number for the message. Must use an _1NPANXXXXXX_ E.164 format. | 
|`from_`|True|Source phone number. It must be a number registered with Flowroute, must be SMS-enabled, and must use an _1NPANXXXXXX_ E.164 format.</br> **Note:** Because `from` is a word reserved by Python, Flowroute uses `from_` in the `Message` object. |
| `content`| True     | The message itself. An unlimited number of characters can be used, but message length rules and encoding apply. See [Message Length & Concatenation](https://developer.flowroute.com/docs/message-length-concatenation) for more information. | 

###### Example usage

1. Run the following, replacing the `msg`, `to`, `from_number`, and `content` variables with your own values:

	`msg = Message(to="15305557784", from_="18444205700", content="This is the message content.")`
	
2. Next, run the following command, replacing *`msg`* with the variable you defined above:
	
	`response = controller.create_message(msg)`
	
	The message is sent.

###### Example response

No response is returned for a sent message. Response error messages can be returned, however. 

##### Retrieve the message identifier

To get details about a sent message, use the `get_message_lookup` method, described [below](#getmessage). Before running `get_message_lookup`, however, you must first get the identifier for that message. 

* Run the following:

	`print response`
	
The response returns a record containing the message identifier (`id`), as shown in the following example JSON response:

	{"data": {"id": "mdr1-fab29a740129404a8ca794efc1359e12'}}

#####Error response
The following table describes the possible `create_message` error codes and messages that can be returned:

| Error code | Message | Description                                                 |
|-------|----------|-------------------------------------------------------|
|`401`   |UNAUTHORIZED|The API credentials are incorrect.
|`403`  | FORBIDDEN  | The `from` number is not authorized.|
	
##### <font color="blue">`get_message_lookup(self, record_id)`</font> <a name="getmessage"></a>

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
|`attributes`    |Object composed of the following:
|  | <ul><li>`body`: The content of the message.<li>`direction`:  The direction of the message. For a sent message, this is `outbound`. For a received message this is`inbound`.<li>`amount_nanodollars`: The cost of the message in nanodollars. Because Flowroute uses eight decimal points of precision, the amount in nanodollars is the USD`amount_display` value multipled by 100,000,000 (one hundred million) for a corresponding whole number. <li>`message_encoding`: Indicates the encoding type, which will be either `0` (UTF-8) or `8` (UCS-2). See [Message Length & Concatenation](https://developer.flowroute.com/docs/message-length-concatenation) for more information. <li>`timestamp`: Date and time, to the second, on which the message was sent. This field displays UTC time using an ISO 8601 format. <li>`to`: The phone number to which the message was sent. <li>`has_mms`: Boolean indicating whether or not the message includes a multimedia file. `true` indicates yes, while `false` indicates no. Currently, MMS is not supported; therefore, the default value for this field will always be `false`. <li>`amount_display`: The total cost of the message in USD. If a message was broken into multiple pieces due to concatenation, this amount will be the total amount for all message pieces. This field does _not_ display out to eight decimal points. See _Message cost_ in [Message Length & Concatenation](https://developer.flowroute.com/docs/message-length-concatenation) for more information. <li>`from`: The Flowroute SMS-enabled number from which the message was sent.<li>`callback_URL`The callback URL defined for the Flowroute number on the [Preferences > API Control](https://manage.flowroute.com/accounts/preferences/api/) page, the URL appears in this field; otherwise, the value is `null`. <li> `type`: Defines what the object is. Because SMS is the only supported object type, this field will always display `messages`. <li>`message_type`: Indicates the type of message, either `long-code` or `toll-free`. If the message was sent to or received from another phone number, this field displays `long-code`; if sent to or received from a toll-free number, this field displays `toll-free`. </li></ul>| 
|`type`| Defines what the object is. Because SMS is the only supported object type, this field will always display `message`.|
|`id` | The unique record identifier of a sent message, generated from a successful `create_message`.|
                        

#####Error response
The following error can be returned:

| Error code | Message | Description                                                 |
|-------|----------|-------------------------------------------------------|
|No code number  |Response Not OK|This error is most commonly returned when the `id` passed in the method is incorrect.|
	