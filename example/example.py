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
