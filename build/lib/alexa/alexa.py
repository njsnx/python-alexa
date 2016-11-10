"""Init py."""

from functools import wraps, partial


class Alexa():
    """Alexa Class."""

    def __init__(self, skill=None):
        """Init Method."""
        self.skill = skill
        self.functions = {}
        self.session = None
        self.response = Response(skill)
        self.session_attributes = {}

    # def start_skill(self, app):
    #     """Start Skill method."""
    #     app.alexa = self

    def route(self, raw):
        """Route method."""
        self.session = Session(raw)
        self.session_attributes = self.session.attributes
        self.request = Request(raw)
        """Route Request."""

        session_func = self.functions[self.request.intent]
        print "hello"
        return partial(session_func, self.request.args)()

    def intent(self, name):
        """Intent method."""
        def decorator(f):

            self.functions[name] = f

            @wraps(f)
            def wrapper(*args, **kwds):
                return f()

        return decorator

    def _intent_func(self, *args, **kwargs):
        pass


# End
class Session():
    """Session class."""

    def __init__(self, raw=None):
        """Init method."""
        self.attributes = {}
        if raw is not None:
            if "session" in raw.keys():
                self.raw_session = raw['session']
            else:
                self.raw_session = raw

            self._get_attributes()

    def _get_attributes(self):
        """Get attributes."""
        if self.raw_session:
            if 'attributes' in self.raw_session:
                self.attributes = self.raw_session['attributes']
            else:
                self.attributes = {}
        else:
            self.self.attributes = self.raw_session

    def set_attribute(self, key=None, value=None):
        """Set attributes."""
        if key:
            self.attributes[key] = value


# End


class Response():
    """Response class."""

    def __init__(self, title):
        """Init Method."""
        self.skill_title = title
        self.attributes = {}
        self.session = Session()
        self.final_response = {
            "version": "1.0",
            "shouldEndSession": False,
            "response": {}
        }

    def card(self, text, image=None):
        """Create a card response."""
        if image:
            card_img = {}
            if type(image) is dict:
                if 'large' in image:
                    card_img['smallImageUrl'] = image['small']

                if 'large' in image:
                    card_img['largeImageUrl'] = image['large']
            elif type(image) is str:
                card_img = {
                    "smallImageUrl": image,
                    "largeImageUrl": image
                }

            self.final_response['response']['card'] = {
                "type": "Standard",
                "title": self.skill_title,
                "text": text,
                "image": card_img
            }

        else:
            self.final_response['response']['card'] = {
                "type": "Simple",
                "title": self.skill_title,
                "content": text
            }

    def statement(self, raw, style='ssml'):
        """Statement class."""
        styles = {
            "text": "PlainText",
            "ssml": "SSML"
        }
        if style in styles.keys():

            if style == 'ssml':
                response = "<speak>{}</speak>".format(raw)
            else:
                response = raw

            self.final_response['response']['outputSpeech'] = {
                "type": styles[style],
                style: response
            }

            self.final_response['response']['reprompt'] = {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": None
                }
            }

        else:
            self.final_response['response']['outputSpeech'] = {
                "type": "PlainText",
                "text": "There was was an issue. Sad face."
            }

        return self.get_output()

    def set_attribute(self, key=None, value=None):
        """Set attributes."""
        if key:
            self.attributes[key] = value

    def get_output(self):
        """Get response."""
        self.set_session(self.session)
        return self.final_response

    def set_session(self, session):
        """Set session method."""
        if bool(self.session.attributes):
            self.final_response['sessionAttributes'] = session.attributes


class Request():
    """Request class."""

    def __init__(self, raw):
        """Init method."""
        self.type = None
        self.intent = None
        self.slots = None
        self.args = {}

        if "request" in raw.keys():
            self.raw_request = raw['request']
        else:
            self.raw_request = raw

        self._get_request()

    def _get_request(self):
        """Get attributes."""
        if self.raw_request:
            self.type = self.raw_request['type']
            if self.type == 'IntentRequest':
                self.intent = self.raw_request['intent']['name']
                if 'slots' in self.raw_request['intent'].keys():
                    self.slots = {}
                    for k, slot in self.raw_request['intent']['slots'].iteritems():
                        if 'value' in slot.keys():
                            self.slots[slot['name']] = slot['value']
                        else:
                            self.slots[slot['name']] = None
                        # print slot

                    self.args['slots'] = self.slots
                else:
                    self.slots = {}
            else:
                self.intent = self.raw_request['type']
        else:
            self.attributes = self.raw_session
