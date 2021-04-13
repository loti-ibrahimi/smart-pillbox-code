# #!/usr/bin/python3
import os
from twilio.rest import Client

def main():
    # Account SID and Token stored in my local env. variable file twilio.env
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    # Sample mock data (as if fetched from main schedules DB)
    pillType = 'PillA'
    pillQuantity = 1
    '''
    <Summary Checklist> 
    * Check TwilioSMSAlert event in the realtime database
    * Trigger SMS ALert if TwilioSMSAlert = True.
    * Set the event to False once Alert is complete.

    Cost is 7c per SMS, budget is €14. Roughly 200 SMS.
    '''

    # Text message to be sent.
    message = client.messages.create(
        body='Schedule Pill is now Due. \n * Pill Type: '+ pillType +'\n * Quantity: '+ str(pillQuantity) +' \n Please access your Pillbox.',
        from_='+16124306181',
        # Stored in my local env. variable file twilio.env
        to=os.environ['MY_PHONE_NUMBER']
    )
    print(message.sid)
main()

    
