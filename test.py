"""Test py for Alexa library."""
from alexa import Alexa, Response
import json
import boto3
alexa = Alexa('VoiceOps')
r = Response()


def lambda_handler(e, c):
    """Handler."""
    return alexa.route(e)


@alexa.intent("LaunchRequest")
def launch():
    """Launch intent."""
    return r.statement(
        "<p>Welcome to the end</p>\
        <p>This is a test statment using the SSML</p>",
    )


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
    return(r.statement("Hello there!", style='plain'))

if __name__ == "__main__":

    import boto3

    c = boto3.session.Session(
        profile_name='njsnet-sceptre',
        region_name='eu-west-1'
    ).client('lambda')

    # Load json file
    with open('./test_events.json') as file:
        data = json.load(file)

    # print lambda_handler(data['launch'], 1)

    test_lambda = True

    if test_lambda:
        r = c.invoke(
            FunctionName='lambda_skill_test',
            InvocationType='RequestResponse',
            Payload=json.dumps(
                data['intent_get']
            )
        )

        print json.dumps(json.loads(r['Payload'].read()), indent=2)
    else:
        print json.dumps(
            lambda_handler(
                data['intent_get'],
                2
            ),
            indent=2
        )
    # print lambda_handler(data['end'], 1)
