# alexa
Simple Python library to make Alexa skill development in AWS Lambda super simple and easy.

Inspired by flask-ask and some other libraries, this library includes features to make response building and request routing really easy.

## Install
Coming Soon


## Usage
```python
from pyalexa import Alexa

alexa = Alexa("Hello World") # Setup a object for the Alexa class
response = alexa.response  # Use the Alexa response attribute to return responses

# Create your Lambda handler
def lambda_handler(event, context):
	return alexa.route(event)


@alexa.launch
def launch():
	return response.statment("Welcome to hello world!")
	
@alexa.intent("GetHello", mapping={"person":"name"})
def get_hello(session, person):
	if "previous" in session.keys():
		response.card("Welcome to Hello World!")
		return response.question("<p>Welcome</p><p>Hello to you {}".format(name))
	else:
		response.session.set_attribute("previous", True)
		return response.question("<p>Welcome</p><p>Hello AGAIN to you {}".format(name))
	
@alexa.session_end:
def close():
	return response.statement("Good bye")
	

```

