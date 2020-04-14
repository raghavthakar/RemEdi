from twilio.rest import Client
import json

#a = '{"name": "Parth", "number": "9766587030"}'

#y = json.loads(a)

def send_sms_transcript(TRANSCRIPT_FILE_DIR):

	JSON_FILE_DIR='../saved_data/students_register/students_register.json'

	f = open(JSON_FILE_DIR)
	data = json.load(f)
	# Your Account SID from twilio.com/console
	account_sid = "AC2a01391bae17c2cdb443a1f43e5cd4ec"
	# Your Auth Token from twilio.com/console
	auth_token  = "5b4734fae302600b45d76eb95d0e2e54"

	client = Client(account_sid, auth_token)

	script = open(TRANSCRIPT_FILE_DIR, mode = 'r')
	content = script.read()
	script.close()

	for name in list(data):
		number=data.get(name)
		# message = client.messages.create(
		# 	to = number,
		# 	from_ = "+12055768179",
		# 	body = "Hi " + name + ", here is the transcript of your lecture.\n " + content)
		#
		# print(message.sid)
		print(name+content)
