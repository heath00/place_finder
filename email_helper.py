import imaplib
import email
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys
import important_info

def send_newmail(location, length, sender):
	msg = MIMEMultipart()
	msg['Subject'] = str(length) + ' potential leads for ' + location
	msg['From'] = important_info.from_user
	msg['Reply-to'] = important_info.from_user

	filename = "out.csv"
	f = open(filename)
	attachment = MIMEText(f.read())
	attachment.add_header('Content-Disposition', 'attachment', filename = filename)
	msg.attach(attachment)
	mailer = smtplib.SMTP("smtp.gmail.com:587")
	mailer.ehlo()
	mailer.starttls()
	mailer.login(important_info.from_user, important_info.from_pass)
	mailer.sendmail(msg['From'], sender, msg.as_string())
	mailer.quit()




def check_newmail():
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(important_info.from_user, important_info.from_pass)
	mail.list()
	# Out: list of "folders" aka labels in gmail.
	mail.select("inbox") # connect to inbox 

	if len(mail.search(None, 'UnSeen')[1][0].split())  == 0:
		return None

	result, data = mail.search(None, "ALL")
	 
	ids = data[0] # data is a list.
	id_list = ids.split() # ids is a space separated string
	latest_email_id = id_list[-1] # get the latest
	 
	result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
	 
	raw_email = data[0][1]# here's the body, which is raw text of the whole email
	# including headers and alternate payloads

	parsed = email.message_from_bytes(raw_email)

	sender = email.utils.parseaddr(parsed['From'])[1]

	payload = str(parsed.get_payload()[0])



	radius_index = payload.index("Radius: ")
	keyword_index = payload.index("Keyword: ")
	radius = payload[radius_index + len("Radius: "):payload.index("#", radius_index)]
	keyword = payload[keyword_index + len("Keyword: "):payload.index("#", keyword_index)]

	if 'State: ' in payload:
		state_index = payload.index("State: ")
		states = payload[state_index + len("State: "):payload.index("#", state_index)].split()
		
		print(states)
		print(radius)
		print(keyword)

		return [1, states, radius, keyword, sender]
	else: 
		location_index = payload.index("Location: ")
		location = payload[location_index + len("Location: "):payload.index("#", location_index)]
		
		print(location)
		print(radius)
		print(keyword)

		return [location.replace(' ', '+'), radius, keyword, sender]