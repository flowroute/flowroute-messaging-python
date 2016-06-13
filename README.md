# flowroute-messaging-python
**flowroute-messaging-python** is a Python SDK that provides methods to send an outbound SMS from a Flowroute phone number and also to retrieve a Message Detail Records (MDR). These methods use **v2** (version 2) of the [Flowroute](https://www.flowroute.com) API.

>**Note:** This SDK does not cover searching for a set of MDRs based on a date range. For searching on a date range, see [Look up a Set of Messages](https://developer.flowroute.com/docs/lookup-a-set-of-messages) on the Flowroute Developer Portal.

## Documentation 
The full documentation for v2 of the Flowroute API is available [here](https://developer.flowroute.com/v2.0/docs).

##Before you begin

The following are required before you can deploy the SDK.

### Have your API credentials

You will need your Flowroute API credentials (Access Key and Secret Key). These can be found on the **Preferences > API Control** page of the [Flowroute](https://manage.flowroute.com/accounts/preferences/api/) portal. If you do not have API credentials, contact <mailto:support@flowroute.com>.

### Know your Flowroute phone number

To create and send a message, you will need your Flowroute phone number, which should be enabled for SMS. If you do not know your phone number, or if you need to verify whether or not it is enabled for SMS, you can find it on the [DIDs](https://manage.flowroute.com/accounts/dids/) page of the Flowroute portal.

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

		from FlowrouteMessagingLib.Models.Message import Message
		from FlowrouteMessagingLib.Controllers.APIController import APIController
		
3.	Add the lines to instantiate the controller:

		controller = APIController(username="Access Key", password="Secret Key")   

4.	Replace `Access Key` and `Secret Key` with your own Access Key and Secret Key.

5.	Add the following line, which creates the message.
	
		msg = Message(to="To Phone Number", from_="From Phone Number", content="Message Content.")

6.	Replace the following:
	
	*	`To Phone Number` with the recipient's phone number.
	* 	`From Phone Number` with your Flowroute phone number.
	*  `Message Content` with the message you want to send to the recipient.
	
	  >**NOTE:** See [`create_message`](#createmessage) for more information about parameters and allowed values.

6.	Next add the following line, which sends the message:

		response = controller.create_message(msg)

7.	Optionally, if you want the script to return the message identifier on sending, add the following line:

		print response 
	
	>**Note:** The message identifier is required when running the [`get_message_lookup`](#getmessage) method.

	Your file should now resemble the following:
	
		#Import the Flowroute Messaging SDK (Python)
		from FlowrouteMessagingLib.Models.Message import Message
		from FlowrouteMessagingLib.Controllers.APIController import APIController  
		
		#Set your credentials
		controller = APIController(username="12345678", password="m8axLA45yds7k22448aOQ7BshaADg6vr")
		
		#Create the message
		msg = Message(to="15305557784", from_="18444205700", content="You should be working, not surfing.")
		
		#Send the message
		response = controller.create_message(msg)
		
		#Print the response
		print response	

8.	Save the file with a **.py** extension in the top-level **flowroute-messaging-python** directory. For this example, the file is named **createmsg.py**.

9.	From the **flowroute-messaging-python** directory in a terminal window, run the file, as shown in the following example:

		python createmsg.py
		
	The script executes, and the message is sent. See [Response messages](#send_rsp) for possible response messages.
 
## APIController

The APIController contains the functions required to send outbound SMS texts and to retrieve MDRs. 
The following sections describe the use of the APIController and its two functions:

*	`create_message ` 
* 	`get_message_lookup` 

###`create_message`<a name=createmessage></a>

The `create_message` function is used to send outbound messages from an SMS-enabled Flowroute number, formatted as follows:

####Usage

	msg = Message(to="To Phone Number", from_="From Phone Number", content="Message Content")
	
 It is composed of the following variables:

| Parameter | Required | Type | Description                                                                                |
|-----------|----------|--------------|--------------------------------------------|
| `msg`   | True     |  string      | The message variable. The variable can have any name, and there is no limit on the length. </br>For this example, `msg` is used. 
| `To Phone Number`     | True   | string  |Target phone number for the message. It must use an _1NPANXXXXXX_ E.164 format.| 
|`From Phone Number`|True| string| Source phone number. It must be a number registered with Flowroute, must be SMS-enabled, and must use an _1NPANXXXXXX_ E.164 format. |
| `Message Content`| True     | string   |The message itself. An unlimited number of characters can be used, but message length rules and encoding apply. See [Message Length & Concatenation](https://developer.flowroute.com/docs/message-length-concatenation) for more information. | 

##### Example response

*	If you did *not* add `print response` to the file, no response is returned for a sent message; however, if an error is encountered an [error code and message](#errorresp) are returned.

*	If you added `print response` to the file, the identifier is returned in the response. Note it down. You can later pass this in the [`get_message_lookup`](#getmessage) method to retrieve the MDR. For example, 

		{"data": {"id": "mdr1-fab29a740129404a8ca794efc1359e12'}}

#####Error response<a name=errorresp></a>
The following table describes the possible `create_message` error codes and messages that can be returned:

| Error code | Message | Description                                                 |
|-------|----------|-------------------------------------------------------|
|`401`   |UNAUTHORIZED|The API credentials are incorrect.
|`403`  | FORBIDDEN  | The `from` number is not authorized.|
  	
### `get_message_lookup` <a name="getmessage"></a>

The `get_message_lookup` method is used to retrieve an MDR by passing the record identifier of a previously sent message.

####Usage

1.	Add the following lines to your Python file before `print response`:

		#Get the MDR
		response = controller.get_message_lookup("Record Identifier")
	
	It is composed of the following parameter:

	| Parameter | Required | Type  | Description                                        |
|-----------|----------|--------|-----------------------------------------------|
| `Record Identifier`      | True     | string  |The identifier of an existing record to retrieve. The value should include the`mdr1-`prefix. |


2.	Because you do not want to create a new message record, comment out the following lines:

		# msg = Message(to="To Phone Number", from_="From Phone Number", content="Message Content.")
		# response = controller.create_message(msg)
		# response = controller.get_message_lookup("Record identifier")

3.	From the **flowroute-messaging-python** directory in a terminal window, run the file, as shown in the following example:

		python createmsg.py
		
	The script executes, and the MDR is returned. See the [example response](#getmdr).
	
##### Example usage

Your file should resemble the following:

	Import the Flowroute Messaging SDK (Python)
	from FlowrouteMessagingLib.Models.Message import Message
	from FlowrouteMessagingLib.Controllers.APIController import APIController  
	
	Set your credentials
	controller = APIController(username="Access Key", password="Secret Key")
	
	# Create the message
	# msg = Message(to="15305557784", from_="18444205700", content="You should be working, not surfing.")
	
	# Send the message
	# response = controller.create_message(msg)
	
	# Look up the MDR
	# response = controller.get_message_lookup("Record identifier")
	
	# Look up the MDR
	response = controller.get_message_lookup("mdr1-fab29a740129404a8ca794efc1359e12")
	
	# Print the response
	print response

##### Example response<a name=getmdr></a>

> **Note:** The following shows a sample formatted response and is intended only to more easily identify the fields returned in the response.

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
                        

#####Error response
The following error can be returned:

| Error code | Message | Description                                                 |
|-------|----------|-------------------------------------------------------|
|No code number  |Response Not OK|This error is most commonly returned when the `id` passed in the method is incorrect.|
	