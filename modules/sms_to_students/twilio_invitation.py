from twilio.rest import Client
import json

def send_invitation(TOPIC_NAME):
	# Your Account SID from twilio.com/console
	account_sid = "AC2a01391bae17c2cdb443a1f43e5cd4ec"
	# Your Auth Token from twilio.com/console
	auth_token  = "5b4734fae302600b45d76eb95d0e2e54"

	client = Client(account_sid, auth_token)

	JSON_FILE_DIR='../saved_data/students_register/students_register.json'

	f = open(JSON_FILE_DIR)
	data = json.load(f)

	for name in list(data):
		print(name)

	# for name in list(data):
	# 	number=data.get(name)
	# 	message = client.messages.create(
	# 		to = number,
	# 		from_ = "+12055768179",
	# 		body = " Hi", name, " your class on ", TOPIC_NAME, "is scheduled. Please call +12055768179 to join the call.")
	#
	# 		print(message.sid)

	for name in list(data):
		number=data.get(name)
		print(" Hi", name, " your class on ", TOPIC_NAME, "is scheduled")
		print("Please call +12055768179 to join the call")
