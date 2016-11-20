# Python Alexa
Simple Python library to make Alexa skill development in AWS Lambda super simple and easy.

Inspired by flask-ask and some other libraries, this library includes features to make response building and request routing really easy.

## Install
Coming Soon


## Usage
```python
"""Example skill using alexa module."""

from alexa import Alexa
import json
alexa = Alexa("Hello World")  # Setup a object for the Alexa class
response = alexa.response  # Use the Alexa response attribute to return responses


# Create your Lambda handler
def lambda_handler(event, context):
    """Lambda Handler."""
    return alexa.route(event)


@alexa.launch
def launch():
    """Launch Function."""
    return response.statement("Welcome to hello world!")


@alexa.intent("GetHello", mapping={"person": "name"})
def get_hello(session, person):
    """Get Hello Intent."""
    if "previous" in session.keys():
        response.card("Welcome to Hello World!")
        return response.question("<p>Welcome</p><p>Hello to you {}".format(person))
    else:
        response.session.set_attribute("previous", True)
        return response.question("<p>Welcome</p><p>Hello AGAIN to you {}".format(person))


@alexa.session_end
def close():
    """Close function."""
    return response.statement("Good bye")


if __name__ == '__main__':

    with open("./test_events.json") as d:
        tests = json.load(d)

    print(
        json.dumps(
            lambda_handler(
                tests['launch'],
                2
            ),
            indent=2
        )
    )
    print(
        json.dumps(
            lambda_handler(
                tests['intent_hello'],
                2
            ),
            indent=2
        )
    )
    print(
        json.dumps(
            lambda_handler(
                tests['end'],
                2
            ),
            indent=2
        )
    )

```

### Example Output
**Launch Request**
```
{
  "version": "1.0", 
  "response": {
    "outputSpeech": {
      "ssml": "<speak>Welcome to hello world!</speak>", 
      "type": "SSML"
    }, 
    "shouldEndSession": true, 
    "reprompt": {
      "outputSpeech": {
        "text": null, 
        "type": "PlainText"
      }
    }
  }
}
```

**GetHello Intent**
```
{
  "version": "1.0", 
  "response": {
    "outputSpeech": {
      "ssml": "<speak><p>Welcome</p><p>Hello AGAIN to you John Smith</speak>", 
      "type": "SSML"
    }, 
    "shouldEndSession": false, 
    "reprompt": {
      "outputSpeech": {
        "text": "How can I help?", 
        "type": "PlainText"
      }
    }
  }, 
  "sessionAttributes": {
    "previous": true
  }
}
````

**End Session**
```
{
  "version": "1.0", 
  "response": {
    "outputSpeech": {
      "ssml": "<speak>Good bye</speak>", 
      "type": "SSML"
    }, 
    "shouldEndSession": true, 
    "reprompt": {
      "outputSpeech": {
        "text": null, 
        "type": "PlainText"
      }
    }
  }, 
  "sessionAttributes": {
    "previous": true
  }
}
```
