from core.mailer import mailer
from core.mails import send_email_async
import asyncio

m = mailer(subject='Hello', body='Hello world',
           sender='ckam@me.com', to=['abbc@mail.com'])
c = asyncio.run(send_email_async(
    subject='Privet', body={'message': 'Privet ti', 'email': 'abbc@mail.com'}, to=['abbc@mail.com'], template_name='mail/test.html'))

print(c)
