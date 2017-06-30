from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

message = client.api.account.messages.create(to="+14042261886",
                                             from_="+19724504982",
                                             body="Hello there! Thank you for joining the yacht club.")