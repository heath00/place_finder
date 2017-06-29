import imaplib
import email
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys

def send_newmail(location):
	msg = MIMEMultipart()
	msg['Subject'] = 'New leads for ' + location
	msg['From'] = ''
	msg['Reply-to'] = ''

	filename = "out.csv"
	f = open(filename)
	attachment = MIMEText(f.read())
	attachment.add_header('Content-Disposition', 'attachment', filename = filename)
	msg.attach(attachment)
	mailer = smtplib.SMTP("smtp.gmail.com:587")
	mailer.ehlo()
	mailer.starttls()
	mailer.login("", "")
	mailer.sendmail(msg['From'], "", msg.as_string())
	mailer.quit()




def check_newmail():
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login('', '')
	mail.list()
	# Out: list of "folders" aka labels in gmail.
	mail.select("inbox") # connect to inbo 

	result, data = mail.search(None, "ALL")
	 
	ids = data[0] # data is a list.
	id_list = ids.split() # ids is a space separated string
	latest_email_id = id_list[-1] # get the latest
	 
	result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
	 
	raw_email = data[0][1]# here's the body, which is raw text of the whole email
	# including headers and alternate payloads

	parsed = email.message_from_bytes(raw_email)

	payload = str(parsed.get_payload()[0])

	city_index = payload.index("City: ")
	radius_index = payload.index("Radius: ")
	keyword_index = payload.index("Keyword: ")
	city = payload[city_index + len("City: "):payload.index("#", city_index)]
	radius = payload[radius_index + len("Radius: "):payload.index("#", radius_index)]
	keyword = payload[keyword_index + len("Keyword: "):payload.index("#", keyword_index)]

	print(city)
	print(radius)
	print(keyword)
	return [city, radius, keyword]