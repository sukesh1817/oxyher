import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check_email(email):
	try:
		if(re.fullmatch(regex, email)):
			return True
		else:
			return False
	except Exception as e:
		print(e)

