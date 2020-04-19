# Megan Salvatore

# sources:
#	https://www.youtube.com/watch?v=VW8qJxy4XcQ
#	https://stackoverflow.com/questions/16877422/whats-the-best-way-to-parse-a-json-response-from-the-requests-library
#	https://stackoverflow.com/questions/50588755/api-call-for-marvel-developers-only-receiving-one-page
#	https://stackabuse.com/saving-text-json-and-csv-to-a-file-in-python/

import requests
import sys
from flask import Flask, request, make_response
from flask_httpauth import HTTPBasicAuth
from functools import wraps
import json
import time
from hashlib import md5

# tokens for Canvas and Marvel
from ServicesKeys import canvas_token
from ServicesKeys import marvel_public_key
from ServicesKeys import marvel_private_key

# get the port number specified
if sys.argv[1] == "-p" and sys.argv[2] != -1:
	port_num = sys.argv[2]

# start a new Flask object
app = Flask(__name__)
auth = HTTPBasicAuth()

# Make a login required when going to any site
def auth_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if auth and auth.username == 'admin' and auth.password == 'secret':
			return f(*args, **kwargs)
		return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
	
	return decorated

# Canvas method
@app.route("/Canvas")
@auth_required
def canvas():
	my_canvas_token = canvas_token 
	the_request = request.args
	
	# make sure the file is specified
	if 'file' in request.args:
		file_name = request.args.get('file')
		print(file_name)
		course_id = "104692"
		url = "https://vt.instructure.com/api/v1/courses/%s/files/?search_term=%s&access_token=%s" % (course_id, file_name, my_canvas_token)
		r = requests.get(url)
		json_text = r.text
		the_file = json.loads(json_text) # the_file is a dictionary

		# Download the file on system using the filename 
		for i in the_file:	
			if i['display_name'] == file_name:
				file_request = requests.get(url)
				open(file_name, 'wb').write(file_request.content)
				return_string = "Downloading the file: " + file_name
				return return_string
		return_tring = fileName + " was not found"
		return return_string
	
	return "Canvas"
	
# Marvel method
@app.route("/Marvel")
@auth_required
def marvel():
	public_key = marvel_public_key
	private_key = marvel_private_key
	
	# make sure story is in the request
	if 'story' in request.args:
		story_num = request.args.get('story')
		print(story_num)
		ts = str(time.time())
		combined = ''.join([ts, private_key, public_key])
		hash_value = md5(combined.encode('ascii')).hexdigest()
		
		url = "http://gateway.marvel.com/v1/public/stories/" + story_num + "?apikey=" + public_key + "&hash=" + hash_value + "&ts=" + ts
		r = requests.get(url)
		json_text = r.text
		the_file = json.loads(json_text) # the_file is a dictionary
		
		# get the file name
		title = the_file['data']['results'][0]['title']
		print(title)
		
		# download the file on system using filename
		with open(title, 'wb') as f:
			f.write(r.content)
			return_string = "Downloading the Marvel story." 
		return return_string
	return_string = "Marvel story was not found"
	return return_string

		
	return "Marvel"

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port_num, debug=True)
