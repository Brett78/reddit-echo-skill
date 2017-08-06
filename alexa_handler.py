import os


class AlexaHandler(object):

    REQUEST_LAUNCH = 'LaunchRequest'
    REQUEST_INTENT = 'IntentRequest'
    REQUEST_ENDED = 'SessionEndedRequest'

    def __init__(self):
        self.app_id = os.environ.get('RS_ARN')
        if self.app_id is None:
            raise ValueError('Missing required environment variable: RS_ARN')

        self.request = {}
        self.intent_handlers = {}
        self.request_types = {
            AlexaHandler.REQUEST_LAUNCH: self.on_launch,
            AlexaHandler.REQUEST_INTENT: self.run_intent,
            AlexaHandler.REQUEST_ENDED: self.on_ended
        }
        self.reprompt = "Sorry, I couldn't help you with that request, please try again."

    def add_intent_handler(self, intent, callback):
        self.intent_handlers[intent] = callback

    def process_request(self, event):
        self.request = event
        self.validate_event()
        request_type = self.get_request_type()
        request_handler = self.request_types.get(request_type)

        if request_handler is None:
            raise ValueError('Invalid Request Type')

        return request_handler()

    def on_ended(self):
        pass

    def on_launch(self):
        return self.build_response(self.build_speechlet_response('Sorry that is not supported'), True)

    def run_intent(self):
        intent = self.get_intent().get('name')
        handler = self.intent_handlers.get(intent)

        if handler is None:
            raise ValueError('Invalid Intent')

        data = handler()
        speechlet = self.build_speechlet_response(data, True)
        return self.build_response(speechlet)

    def validate_event(self):
        session = self.request.get('session', {})
        application = session.get('application', {})
        application_id = application.get('applicationId')
        return application_id == self.app_id

    def get_params(self):
        intent = self.get_intent()
        return intent.get('slots')

    def build_speechlet_response(self, response_text, should_end_session):
        return {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": response_text
                },
                "reprompt": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": self.reprompt
                    }
                },
                "shouldEndSession": should_end_session
            }

    def build_response(self, speechlet_response):
        return {
            "version": "1.0",
            "response": speechlet_response
        }

    def get_intent(self):
        request = self.request.get('request', {})
        return request.get('intent', {})

    def get_request_type(self):
        request = self.request.get('request', {})
        request_type = request.get('type', None)
        if request_type is None:
            raise ValueError('Invalid request type')
        return request_type

    def intent(self, intent):
        def decorator(f):
            self.add_intent_handler(intent, f)
        return decorator

    def request_type(self, request_type):
        def decorator(f):
            self.request_types[request_type] = f
        return decorator
