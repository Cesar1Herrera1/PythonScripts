from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from email.message import EmailMessage
import smtplib

#url of website I'm checking
url = ''

uClient = uReq(url)
page_info = uClient.read()
uClient.close()

page_soup = soup(page_info, 'html.parser')

job_container = page_soup.find('span', {'class', 'smaller muted'})

j_string = job_container.text.strip()

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = ''			# Username goes here
    msg['from'] = user
    password = ''		# Password goes here

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':

    try:

        # strip the string of any parenthesis using regex?
        string_to_int = int(j_string.strip('()'))

        if string_to_int >= 1:
            email_alert('Update!', 'Job post found!\n\n Number of Results:' + str(string_to_int) + '\n\n' + url, 'UserPhone')
# Visit following link to get appropriate way to send text to your carrier and to your device: https://www.digitaltrends.com/mobile/how-to-send-a-text-from-your-email-account/
    except ValueError:
        print('A Value error has occured')
