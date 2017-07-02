from twilio.rest import Client

class twilioAPI():
    def __init__(self, message):
        self.message = message

    def sendMessage(self):
        # Find these values at https://twilio.com/user/account
        account_sid = ""
        auth_token = ""
        client = Client(account_sid, auth_token)

        message = client.api.account.messages.create(to="+19405942980",
                                                     from_="+19724504982",
                                                     body=self.message)
    def setMessage(self, message):
        self.message = message