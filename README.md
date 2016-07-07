# flowroute-messaging-python
**flowroute-messaging-python** is a Python SDK that provides methods to send an outbound SMS from a Flowroute phone number and also to retrieve a Message Detail Record (MDR). These methods use **v2** (version 2) of the [Flowroute](https://www.flowroute.com) API.

>**Note:** This SDK does not cover searching for a set of MDRs based on a date range. For searching on a date range, see [Look up a Set of Messages](https://developer.flowroute.com/docs/lookup-a-set-of-messages) on the Flowroute Developer Portal.

## Documentation 
The full documentation for v2 of the Flowroute API is available [here](https://developer.flowroute.com/v2.0/docs).

##Before you begin

The following are required before you can deploy the SDK.

### Have your API credentials

You will need your Flowroute API credentials (Access Key and Secret Key). These can be found on the **Preferences > API Control** page of the [Flowroute](https://manage.flowroute.com/accounts/preferences/api/) portal. If you do not have API credentials, contact <mailto:support@flowroute.com>.

### Know your Flowroute phone number

To create and send a message, you will need your Flowroute phone number, which should be enabled for SMS. If you do not know your phone number, or if you need to verify whether or not it is enabled for SMS, you can find it on the [DIDs](https://manage.flowroute.com/accounts/dids/) page of the Flowroute portal.

### Get a code text editor

Steps in this SDK describe creating one or more script files that allow you to execute the methods. Script files can be created either using a terminal window shell or through using a code text editor. For example, *Sublime Text*. 

## Install the libraries

The SDK uses the **Unirest** and **jsonpickle** Python libraries, which must be installed before you can use the SDK. 

> **Important:** The SDK supports only Python 2.x. Python 1.x and 3.x are not supported.

1. Open a terminal session. 

2. If needed, create a parent directory folder where you want to install the SDK.
 
3. Go to the newly created folder, and run the following:

 	`git clone https://github.com/flowroute/flowroute-messaging-python.git`
 	
 	The `git clone` command clones the **flowroute-messaging-python** repository as a sub directory within the parent folder.
 	
4.	Change directories to the newly created **flowroute-messaging-python** directory.

5.	Run the following:

	`pip install -r requirements.txt`

6.	Import the SDK.
  
## Create a script to import the SDK and send a message

Importing the SDK requires that you run commands either by creating and running a script or through a shell. The following instructions describe importing the SDK and running the `APIController` by creating and running a script.

>**Note:** A **demo_send.py** file is located at the top-level of the **flowroute-messaging-python** directory. Instead of creating a new file, you can modify **demo_send.py** and use that file. 

1.	Using a code text editor — for example, *Sublime Text* — to create a new file.

2.	Add the following lines to the top of the file:

		#Import the Controllers
		from FlowrouteMessagingLib.Models.Message import Message
		from FlowrouteMessagingLib.Controllers.APIController import APIController
		
3.	Next, add the lines to pass your API credentials:

		#Pass your API crredentials
		controller = APIController(username="Access Key", password="Secret Key")   

4.	Replace `Access Key` and `Secret Key` with your own Access Key and Secret Key.

5.	Add the APIController methods as needed between `msg = Message(to="To Phone Number", from_="From Phone Number", content="Message Content.")` and `#Print the response`. See [APIController](#controller) for information about invoking each of the methods and their parameters.

6.	Optionally, if you want the script to return the message identifier on sending, add the following line:

		print response 
	
	>**Important:** Throughout this SDK, `response` is used in method examples. `response` is a variable name that can be changed to a name of your own choosing. It can support an unlimited number of characters. If you choose to rename `response`, make sure that any method that references that variable name is also changed to use the new name. In the following example, `response` is changed to `blob` wherever `response` is used:
>
>`#Create and Send a Message`<br>
>`...`<br>
>`blob = controller.create_message(msg)`<br>
>`print blob`

7.	Save the file with a **.py** extension in the top-level **flowroute-messaging-python** directory. For this example, the file is named **createmsg.py**.

8.	From the **flowroute-messaging-python** directory in a terminal window, run the file, as shown in the following example:

		python createmsg.py

### Example Python file

The following shows an example Python file, **createmsg.py**, that includes all Controller methods:

		#Import the Controllers
		from FlowrouteMessagingLib.Models.Message import Message
		from FlowrouteMessagingLib.Controllers.APIController import APIController  
		
		#Pass your API credentials
		controller = APIController(username="12345678", password="m8axLA45yds7k22448aOQ7BshaADg6vr")

		#Create and Send a Message
		msg = Message(to="To Phone Number", from_="From Phone Number", content="Message Content")
		response = controller.create_message(msg)
		
		#Look up the MDR
		response = controller.get_message_lookup("Record identifier")
			
		#Print the response
		print response	

 
## APIController<a name=controller></a>

The APIController contains the functions required to send outbound SMS texts and to retrieve MDRs. 
The following sections describe the use of the APIController and its two functions:

*	[`create_message`](#create_message) 
* 	[`get_message_lookup`](#getmessage)

###`create_message`<a name=createmessage></a>

The `create_message` function is used to send outbound messages from an SMS-enabled Flowroute number, formatted as follows:

####Usage

Add the following lines to your Python file:

	#Create and Send a Message
	msg = Message(to="To Phone Number", from_="From Phone Number", content="Message Content")
	response = controller.create_message(msg)
	
 It is composed of the following variables:

| Parameter | Required | Type | Description                                                                                |
|-----------|----------|--------------|--------------------------------------------|
| `msg`   | True     |  string      | The variable name identifying the message parameters. The variable can have any name, and there is no limit on the length. The name assigned here will then be passed in the `create_message` response in the second line. The variable is further composed of the following parameters. 
| `To Phone Number`     | True   | string  |Target phone number for the message. It must use an _1NPANXXXXXX_ E.164 format.| 
|`From Phone Number`|True| string| Source phone number. It must be a number registered with Flowroute, must be SMS-enabled, and must use an _1NPANXXXXXX_ E.164 format. |
| `Message Content`| True     | string   |The message itself. An unlimited number of characters can be used, but message length rules and encoding apply. See [Message Length & Concatenation](https://developer.flowroute.com/docs/message-length-concatenation) for more information. | 

##### Example usage

	#Create and Send a Message
	msg = Message(to="15305557784", from_="18444205700", content="Gee, nice marmot!")
	response = controller.create_message(msg)

##### Example response

One of the following occurs:

1.	If you did *not* add `print response` to the file, no response is returned for a sent message; however, if an error is encountered an [error code and message](#errorresp) are returned.

2.	If you added `print response` to the file, the recordId is returned in the response. Note it down. You can later pass this in the [`get_message_lookup`](#getmessage) method to retrieve the MDR. For example, 

		{"data": {"id": "mdr1-fab29a740129404a8ca794efc1359e12'}}
		
	The `recordId` can then be passed in the [`getMessageLookup`](#getmsg) method to return details about the message.
		
3.	If an error is encountered, an error message is returned. The message is not sent.

#####Error response<a name=errorresp></a>

| Error code | Message | Description                                                 |
|-------|----------|-------------------------------------------------------|
|`401`   |UNAUTHORIZED|The API `Access Key` and/or `Secret Key` are incorrect. |
|`403`  | FORBIDDEN  | Typically this error might occur when the `To` number is not formatted as an 11-digit E.164 number, or the `From` number is not authorized to send an SMS.|
  	
### `get_message_lookup` <a name="getmessage"></a>

The `get_message_lookup` method is used to retrieve an MDR by passing the record identifier of a previously sent message.

####Usage

Add the following lines to your Python file before `print response`:

		#Get the MDR
		response = controller.get_message_lookup("recordId")
		
If you do not want to create a new message record at the same time as sending a message, comment out the following lines:

		# msg = Message(to="To Phone Number", from_="From Phone Number", content="Message Content.")
		# response = controller.create_message(msg)
	
It is composed of the following parameter:

| Parameter | Required | Type  | Description                                        |
|-----------|----------|--------|-----------------------------------------------|
| `recordID`      | True     | string  |The identifier of an existing record to retrieve. The value should include the`mdr1-`prefix. |

##### Example usage

	# Look up the MDR
	response = controller.get_message_lookup("mdr1-fab29a740129404a8ca794efc1359e12")

##### Example response<a name=getmdr></a>

> **Note:** The following shows a sample formatted response and is intended only to more easily identify the fields returned in the response.

	{
  	"data": {
      "attributes": {
     	  "body": "Gee, nice marmot!",
     	  "direction": "outbound",
     	  "amount_nanodollars": 4000000,
    	  "message_encoding": 0,
    	  "timestamp": "2016-05-03T17:41:00.478893+00:00",
    	  "has_mms": false,
    	  "to": "15305557784",
    	  "amount_display": "$0.0040",
    	  "from": "18444205700",
   		  "callback_url": None,
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
|  | <ul><li>`body`: The content of the message.<li>`direction`:  The direction of the message. For a sent message, this is `outbound`. For a received message this is`inbound`.<li>`amount_nanodollars`: The cost of the message in nanodollars. Because Flowroute uses eight decimal points of precision, the amount in nanodollars is the USD`amount_display` value multiplied by 100,000,000 (one hundred million) for a corresponding whole number. <li>`message_encoding`: Indicates the encoding type, which will be either `0` (UTF-8) or `8` (UCS-2). See [Message Length & Concatenation](https://developer.flowroute.com/docs/message-length-concatenation) for more information. <li>`timestamp`: Date and time, to the second, on which the message was sent. This field displays UTC time using an ISO 8601 format. <li>`to`: The phone number to which the message was sent. <li>`has_mms`: Boolean indicating whether or not the message includes a multimedia file. `true` indicates yes, while `false` indicates no. Currently, MMS is not supported; therefore, the default value for this field will always be `false`. <li>`amount_display`: The total cost of the message in USD. If a message was broken into multiple pieces due to concatenation, this amount will be the total amount for all message pieces. This field does _not_ display out to eight decimal points. See _Message cost_ in [Message Length & Concatenation](https://developer.flowroute.com/docs/message-length-concatenation) for more information. <li>`from`: The Flowroute SMS-enabled number from which the message was sent.<li>`callback_URL`The callback URL defined for the Flowroute number on the [Preferences > API Control](https://manage.flowroute.com/accounts/preferences/api/) page, the URL appears in this field; otherwise, the value is `null`. <li>`message_type`: Indicates the type of message, either `long-code` or `toll-free`. If the message was sent to or received from another phone number, this field displays `long-code`; if sent to or received from a toll-free number, this field displays `toll-free`. </li></ul>| 
|`type`| Defines what the object is. Because SMS is the only supported object type, this field will always display `message`.|
|`id` | The unique record identifier of a sent message, generated from a successful `create_message`.|
                        
##### Error response
The following error can be returned:

| Error code | Message | Description                                                 |
|-------|----------|-------------------------------------------------------|
|No code number  |Response Not OK|This error is most commonly returned when the `id` passed in the method is incorrect.|
	