# Python Alexa
## First Release v1.0

This is the first release of *alexa* so this release note will list some of the features it provides

* Simple request routing
* Simple Session management
* Simple response crafting

This module is aimed at those who want to worry about the cool things you can do with Alexa and Lambda rather than having to worry about how you get the data in or out too much.

It is still recommended to use the Alexa Skills documentation to understand how to actually create a skill but this module will do the heavy lifting... or rather the tedious lifting for you.

I am planning to make this module more robust by making the code more fail-safe as well as adding some extra features like Utterance generation and Intent Scheme generation

Please let me know of bugs or feature requests in the Issues section

## Install
##Install via pip
`$ pip install git+ssh://github.com/nmyster/python-alexa.git`

### Upgrade via pip
`$ pip install git+ssh://github.com/nmyster/python-alexa.git - U`

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
