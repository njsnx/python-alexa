"""Init py."""

from functools import wraps, partial


class Alexa():
    """Alexa Class."""

    def __init__(self, skill=None):
        """Init Method."""
        self.skill = skill  # Skill Name
        self.functions = {}  # Functions Dict, used later to run the appropriate function
        self.session = None  # Session attribute used later
        self.response = Response(skill)  # Response attribute
        self.session_attributes = {}  # Session attributes Dict
        self._intent_mappings = {}  # Intent Slot mappings
        self.request = None  # The original request
        self.launch_func = None  # Which function is associated with the LaunchRequest
        self.end_func = None  # The function associated with the SessionEndRequest

    def route(self, raw):
        """Route method.

        This methd deals with routing the raw request to the correct function
        It will figure out which function to run based on the requet type
        If it is an intent, it will also deal with mapping slots expected to
        function variables
        """
        self.session = Session(raw)  # Get a session object from the Session class, passing in the raw request
        self.session_attributes = self.session.attributes  # Set the session_attribute attribute to the attributes in the session
        self.request = Request(raw)  # Set the request attribute to a Request object - passing in the raw request

        """Route Request."""
        # Depending on the request type, get the correct function
        if self.request.type == 'LaunchRequest':
            return partial(self.launch_func)()  # LaunchRequest Function
        elif self.request.type == 'SessionEndedRequest':
            return partial(self.end_func)()  # SessionEndRequest funciton
        elif self.request.type == 'IntentRequest':  # Intent Function
            args = self.map_slots_to_mapping()  # Get the arguments to pass in based on mapping parameter to the decorator
            if args:  # Check if there is any args
                # Return the result of the matched function, passing in the sesison as well as the slot mappings as arguments
                return partial(
                    self.functions[self.request.intent],
                    self.session_attributes,
                    **args
                )()
            else:  # If no arguments to map
                # call the matched function with the correct session but no slot -> arguments
                return partial(
                    self.functions[self.request.intent],
                    self.session_attributes
                )()

    def map_slots_to_mapping(self):
        """Map slots to arguments.

        Deals with mapping slots to arguments - i.e DEVICE slot mapped to device argument

        """
        args = {}  # Start an empty dict to store arguments
        mappings = self._intent_mappings[self.request.intent]  # Set mappings to the dict of the decorator mapping argumnet

        # Check there is a mapping value and that there is at least 1 key to work with
        if mappings is not None and len(self.request.slots.keys()) > 0:

            # If there is, loop through them
            for to, fr in self._intent_mappings[self.request.intent].items():
                if fr in self.request.slots.keys():  # Check if the current slot has a mapping
                    args[to] = self.request.slots[fr]  # Add a key to the args dict setting it to the value of the slot
                else:
                    args[to] = None  # If there isn't a value for that slot, set it to None

        return args  # Return the args dict

    # Define the launch functiond decorator
    def launch(self, f):
        """Launch Intent."""
        self.launch_func = f  # Set the launch function attribute to be the function using this decorator

        @wraps(f)  # Set up wrapper so that the function passed in is callable with the arguments later
        def wrapper(*args, **kwargs):
            f()
        return f  # Return the wrapped function

    # Define the session end decorator function
    def session_end(self, f):
        """Launch Intent."""
        self.end_func = f

        @wraps(f)  # Set up wrapper so that the function passed in is callable with the arguments later
        def wrapper(*args, **kwargs):
            f()
        return f  # Return the wrapped function

    # Define the intent decorator function, with mapping attribute argument
    def intent(self, name, mapping=None):
        """Intent method."""
        def decorator(f):

            self.functions[name] = f
            self._intent_mappings[name] = mapping

            @wraps(f)
            def wrapper(*args, **kwds):
                return f()

        return decorator  # Retrun wrapped function.


class Session():
    """Session class.

    Used to represent both the incoming session and the session to send with a response.
    """

    def __init__(self, raw=None):
        """Init method."""
        self.attributes = {}  # Define attributes attribute as an empty dict
        self.user = None  # Define a user attribute to None to store user info later

        if raw is not None:  # Confirm a event has been passed in
            if "session" in raw.keys():  # Check if the event has a session key
                self.raw_session = raw['session']  # If it does, set a raw_session attribue to the value of the event's session objet
            else:
                self.raw_session = raw  # If not, assume the whole event is a session and set the raw_Session to the whole event

            self._get_attributes()  # Parse passed in session attributes

    def _get_attributes(self):
        """Get attributes.

        Used to get the session attributes passed in with the event
        Used to get the user details passed in with the event
        """
        if self.raw_session:  # Check if there is a raw session value
            if 'attributes' in self.raw_session:  # See if the raw session has n attributes key
                if self.raw_session['attributes'] is not None:  # Check if the attributes key is not empty/None
                    self.attributes = self.raw_session['attributes']  # Set the attributes class attribute to the value of the session attributes
                else:
                    self.attributes = {}  # If there is an empty attributes key, set class attributes attribute to an empty dict
            else:
                self.attributes = {}  # IF there is no attributes key, set class attributes attribute to an empty dict

            # Check if there is a user key in the raw session
            if 'user' in self.raw_session:
                self.user = self.raw_session['user']  # If there is, set class user attribute to the value of the session object
        else:
            self.self.attributes = self.raw_session  # If there is no attributes key, assume of the raw_session is the attributes dict

    def set_attribute(self, key=None, value=None):
        """Set attributes.

        Used to set attribute values to send back to the Echo/Alexa
        Takes in a ket and a value to set
        """
        if key:  # If the key is not none
            self.attributes[key] = value  # Set the value of the attribute key to the key value


class Response():
    """Response class."""

    def __init__(self, title):
        """Init Method."""
        self.skill_title = title  # Set the skill title attribute to the passed in title argument
        self.attributes = {}  # Create an empty dict for attributes
        self.session = Session()  # Create a new session to use when sending the response
        self.final_response = {  # Create start of the response object
            "version": "1.0",
            "response": {}
        }

    def card(self, text, image=None):
        """Create a card response.

        Allows a card to be sent as part of the response. This will show up in the users Alexa app
        Accepts text input at a minimum and allow images to be set

        If a single image string is provided, this will be used for both small and large settings
        Additionally, you can pass in a dict with small and large as keys with alternate URLs
        """
        # If image is set
        if image:
            card_img = {}  # Create empty image dict for the respone
            if type(image) is dict:  # Check if the image argument was a dict
                if 'small' in image:  # See if small is provided in the argument
                    card_img['smallImageUrl'] = image['small']  # Set the smallImageUrl to the small value

                if 'large' in image:
                    card_img['largeImageUrl'] = image['large']  # Set the largeImageUrl to the large value
            elif type(image) is str:  # Check if the type is str
                card_img = {  # Create a dict with small and large image url set to the string value
                    "smallImageUrl": image,
                    "largeImageUrl": image
                }

            # set the response card value to the values in the image_carg
            self.final_response['response']['card'] = {
                "type": "Standard",
                "title": self.skill_title,
                "text": text,
                "image": card_img
            }

        else:  # If no image is set
            # Create a response card object reflective of no image being se
            self.final_response['response']['card'] = {
                "type": "Simple",  # Card type
                "title": self.skill_title,  # Card title
                "content": text  # Content dict
            }

    # AudioStart method
    def audiostart(self, url, style='ssml'):
        """Start Rain.

        Used to return a response that doesn't expect further input
        """

        # Start
        self.final_response['response']['outputSpeech'] = {
            "type": "PlainText",
            "test": "Oh - Es beginnt zu regnen!"  
        }

        # Directives
        self.final_response['response']['directives'] = [
            {
                "type": "AudioPlayer.Play",
                "playBehavior": "ENQUEUE",
                "audioItem":
                {
                    "stream":
                    {
                        "token": "this-is-the-audio-token",
                        "url": url,
                        "offsetInMilliseconds": 0
                    }
                }
            }
        ]


        self.final_response['response']['shouldEndSession'] = True  # End session set to True as this is a statement, not a question

        # Set Repromt dict to None
        self.final_response['response']['reprompt'] = {
            "outputSpeech": {
                "type": "PlainText",
                "text": None
            }
        }

        return self.get_output()  # Get the output and return it


    # Statement method
    def statement(self, raw, style='ssml'):
        """Statement class.

        Used to return a response that doesn't expect further input
        """
        styles = {
            "text": "PlainText",  # Response type PlainText
            "ssml": "SSML"  # Response type SSML
        }

        # Check if the style argument is in the styles dict
        if style in styles.keys():

            if style == 'ssml':  # If the style is SSML
                response = "<speak>{}</speak>".format(raw)  # Response is surrounded by speak tags to make it SSML
            else:
                response = raw  # Else the Response is just the input of raw
            self.final_response['response']['shouldEndSession'] = True  # End session set to True as this is a statement, not a question

            # Create outputspeech dict with response and styl
            self.final_response['response']['outputSpeech'] = {
                "type": styles[style],  # Style value is value from styles dict using passed in style argument
                style: response  # Set key to the style passed in and the response as the value
            }

            # Set Repromt dict to None
            self.final_response['response']['reprompt'] = {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": None
                }
            }

        else:
            # If the style is invalid, return a sad face response
            self.final_response['response']['outputSpeech'] = {
                "type": "PlainText",
                "text": "There was was an issue. Sad face."
            }

        return self.get_output()  # Get the output and return it

    # question method used to return a response that expects user input
    def question(self, raw, style='ssml'):
        """Question method."""
        styles = {
            "text": "PlainText",
            "ssml": "SSML"
        }
        # If the style is SSML
        if style in styles.keys():

            if style == 'ssml':  # If the style is SSML
                response = "<speak>{}</speak>".format(raw)  # Response is surrounded by speak tags to make it SSML
            else:
                response = raw  # Else the Response is just the input of raw
            self.final_response['response']['shouldEndSession'] = False  # End session set to False as this is a question, expecting further input
            self.final_response['response']['outputSpeech'] = {
                "type": styles[style],  # Style value is value from styles dict using passed in style argument
                style: response  # Set key to the style passed in and the response as the value
            }

            self.final_response['response']['reprompt'] = {
                "outputSpeech": {
                    "type": "PlainText",  # Set the type to PlainText
                    "text": "How can I help?"  # Set the text to reprompt for (Need to add custom raw_input)
                }
            }

        else:
            # If the style is invalid, return a sad face response
            self.final_response['response']['outputSpeech'] = {
                "type": "PlainText",
                "text": "There was was an issue. Sad face."
            }

        # Get the output and return it
        return self.get_output()

    def set_attribute(self, key=None, value=None):
        """Set attributes.

        Used to set attribute values to send back to the Echo/Alexa
        Takes in a ket and a value to set
        """
        if key:
            self.attributes[key] = value

    # Get output to send back
    def get_output(self):
        """Get response."""
        self.set_session(self.session)  # Sets the session to the passed in session
        return self.final_response  # Return the final response

    # Set the session to send back
    def set_session(self, session):
        """Set session method."""
        if bool(self.session.attributes):  # Check if session attributes is set
            self.final_response['sessionAttributes'] = session.attributes  # Add sesison attributes to final response


class Request():
    """Request class."""

    def __init__(self, raw):
        """Init method."""
        self.type = None  # Request type
        self.intent = None  # The intent name
        self.slots = None  # Slots provided by request
        self.user = None  # User in the request
        self.args = {}  # Empty args dict

        # Check if request is in the event
        if "request" in raw.keys():
            self.raw_request = raw['request']  # Set the request attribute to the request object in the event
        else:
            self.raw_request = raw  # Else set raw_requsto entire event

        self._get_request()  # Call the get request method

    def _get_request(self):
        """Get request attributes."""
        # Check raw_request exists
        if self.raw_request:
            self.type = self.raw_request['type']  # Set type
            if self.type == 'IntentRequest':  # Check if type is IntentRequest
                self.intent = self.raw_request['intent']['name']  # Set intent to intent name
                self.slots = {}  # Set empty slots dict
                if 'slots' in self.raw_request['intent'].keys():  # Check if slots is in the request keys

                    # Loop through each slot in the request
                    for k, slot in self.raw_request['intent']['slots'].items():
                        if 'value' in slot.keys():  # If the slot has a value, se the slot key to the value
                            self.slots[slot['name']] = slot['value']
                        else:
                            self.slots[slot['name']] = None  # Else set the value of the slot key to None

                    self.args['slots'] = self.slots  # Set the object args slots key to the slots
            else:
                self.intent = self.raw_request['type']  # Set intent to request ype if it is not IntentRequest

        else:
            self.attributes = self.raw_session  # Set attributes to the raw session if no raw_request
