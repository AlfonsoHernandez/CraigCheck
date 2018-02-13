import smtplib


def send_email_notification(content, host_email, password, destination_email):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(host_email, password)

	server.sendmail(host_email, destination_email, content)

	server.quit()