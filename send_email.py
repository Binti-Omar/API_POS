import requests

# ELASTIC_API_KEY="02EA72D3F5EEA2895DDEB57E7269AA652FC506808A31E4AE62AE54B5BFE36E9805FEF0D3C78C72C863891E749C7C9FEB"
# FROM_EMAIL = "chombobintiomar5@gmail.com"

# url = "https://api.elasticemail.com/v2/email/send"

# def send_email(to,subject,message):
#     data={"apiKey":ELASTIC_API_KEY,"subject":subject,"from":FROM_EMAIL,"to":to,"bodytext":message}
#     res=requests.post(url,data=data)
#     print(res)
#     return res.status_code

# send_email("chombobintiomar5@gmail.com","Testing email","I am testing api")

import mailtrap as mt
MAILTRAP_API_KEY = "af19035505f85d42431a0b27d834d90c"

import mailtrap as mt

def email(to,subject,message):
    mail = mt.Mail(
        sender=mt.Address(email="hello@demomailtrap.co", name="Flask API"),
        to=[mt.Address(email=to)],
        subject=subject,
        text=message,
        category="Integration Test",
    )

    client = mt.MailtrapClient(token=MAILTRAP_API_KEY)
    response = client.send(mail)

    print(response)
    print("this is mailtrap--------")

# email("chombobintiomar5@gmail.com"," Testing APi 1","I am testing api") 
