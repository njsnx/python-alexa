"""Test py for Alexa library."""
from alexa import Alexa, Response
import json

alexa = Alexa('VoiceOps')
r = Response()


def lambda_handler(e, c):
    """Handler."""
    return alexa.route(e)


@alexa.intent("LaunchRequest")
def launch():
    """Launch intent."""
    return r.statement("Welcome to the end")


@alexa.intent("HelloWorld")
def hello_intent():
    """Hello Intent."""
    return("Hello")


@alexa.intent("SessionEndedRequest")
def end_session():
    """End session."""
    r.session.set_attribute('hello', 'neil')
    return(r.statement("Good bye!"))


@alexa.intent("GetNextList")
def get_next_intent():
    """Hello Intent."""
    # r.session.set_attribute('wow', 'hahahahaha')
    return(r.statement("Hello asdasd"))

if __name__ == "__main__":

    # Load json file
    with open('./test_events.json') as file:
        data = json.load(file)

    print lambda_handler(data['launch'], 1)

    print lambda_handler(data['intent_2'], 1)

    print lambda_handler(data['end'], 1)
