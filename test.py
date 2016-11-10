"""Chewing the Fat Quotes."""

from alexa import Alexa
import random
import json
alexa = Alexa('Chewing the Fat')
respond = alexa.response


def lambda_handler(e, c):
    """Handler method."""
    # print(json.dumps(e))

    return alexa.route(e)


# @alexa.intent("LaunchRequest", mapping={"city": "Edinburgh"})
@alexa.launch
def launch():
    """Launch Intent."""
    return(
        respond.statement(
            "<p><audio src=\"https://s3-eu-west-1.amazonaws.com"
            "/njsnet-deployments/lambda/Alexa/chewin/sounds/chewin_intro.mp3\""
            "/></p> <p>Welcome to chew-ing the Fat Quotes! Ya Dobber</p>"
        )
    )


@alexa.session_end
def session_end():
    """Session end method."""
    return (
        respond.statement(
            "Goodbye!"
        )
    )

@alexa.intent("SessionEndedRequest", mapping={"city": "Edinburgh"})
def close():
    """Close method."""
    return(respond.statement("Thank you for using Quotes!"))


@alexa.intent("GetQuote", mapping={"character": "character"})
def get_quote(session, character):
    """Get Quote Method."""
    print character

    """Get Quote intent."""
    if 'last_quote' not in session.keys():
        quotes = {
            "teacher": [
                "teacher_bag.mp3",
                "teacher_neck_new.mp3"
            ],
            "the teacher": [
                "teacher_bag.mp3",
                "teacher_neck.mp3"
            ],
            "the big man": [
                "bigman_counseller.mp3",
                "bigman_fanny_baws.mp3",
                "bigman_bike.mp3",
                "bigman_pish.mp3"
            ],
            "big man": [
                "bigman_counseller.mp3",
                "bigman_fanny_baws.mp3",
                "bigman_bike.mp3",
                "bigman_pish.mp3"
            ],
            "ronald villes": [
                "ronald_villes_zortal.mp3"
            ],
            "the actor": [
                "ronald_villes_zortal.mp3"
            ],
            "actor": [
                "ronald_villes_zortal.mp3"
            ],
            "random": [
                "smell_shite_1.mp3",
                "gonne_no_dae_that.mp3",
                "smell_shite_2.mp3",
                "simmer_down.mp3",
                "random_psychic.mp3",
                "bigman_counseller.mp3",
                "bigman_fanny_baws.mp3",
                "bigman_bike.mp3",
                "bigman_pish.mp3",
                "ronald_villes_zortal.mp3",
                "teacher_bag.mp3",
                "teacher_neck_new.mp3"
            ]
        }
        c = random.choice(quotes.keys())
        if character is not None:
            c = character
        else:
            c = random.choice(quotes.keys())

        quote = random.choice(quotes[c])
        respond.session.set_attribute('last_quote', quote)
        respond.card(
            "How about this one by {}".format(c),
            image={
                "large": "https://s3-eu-west-1.amazonaws.com/njsnet-"
                "deployments/lambda/Alexa/chewin/sounds/chewing_img.jpeg",
                "small": "https://s3-eu-west-1.amazonaws.com/njsnet-"
                "deployments/lambda/Alexa/chewin/sounds/chewing_img.jpeg"
            }
        )
        return(
            respond.statement(
                "<p>How about this one by {}</p><p><audio src=\"https:"
                "//s3-eu-west-1.amazonaws.com/njsnet-deployments/"
                "lambda/Alexa/chewin/sounds/{}\" /></p>".format(
                    c,
                    quote
                )
            )
        )

    else:
        return(
            respond.statement(
                """You've already had yir quote. Now piss aff"""
            )
        )


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

    test_lambda = False

    if test_lambda:
        r = c.invoke(
            FunctionName='lambda_skill_test',
            InvocationType='RequestResponse',
            Payload=json.dumps(
                data['new_intent']
            )
        )

        print json.dumps(json.loads(r['Payload'].read()), indent=2)
    else:
        print(
            json.dumps(
                lambda_handler(
                    data['chwin_session_cont'],
                    2
                ), indent=2
            )
        )
