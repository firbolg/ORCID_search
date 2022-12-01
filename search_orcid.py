import argparse
import io
from io import BytesIO
import sys
import config
import string
import pycurl
#import unicodecsv as csv
import csv
import urllib
import json
import orcid


#Check if an access token has already been generated
def token_check():
	#If there is an existing saved access token, use that
	try:
		with open ("token.txt", "r") as myfile:
			token=myfile.read()
			print ("Using existing access token from token.txt")
			return str(token)
	#If there is not an existing token, create one and save it
	except:
		print ("Generating new access token")
		institution_key = 'APP-J19Q1Z3RMF2E9W60'
		institution_secret = '72e8548c-1726-4d7a-b429-fe3e70188a53'
		api = orcid.PublicAPI(institution_key, institution_secret, sandbox=True)
		token = api.get_search_token_from_orcid()
		return token
			
#Generate a /read-public token
def get_orcid_token():
    #set request variables
    client_id = config.client_id
    client_secret = config.client_secret
    token_endpoint = config.token_endpoint
    data = BytesIO()
    #create post data
    post_data = {'client_id': client_id, 'client_secret': client_secret, 'scope': '/read-public', 'grant_type': 'client_credentials'}
    #url encode post data
    postfields = urllib.urlencode(post_data)
    #create and send http request
    c = pycurl.Curl()
    c.setopt(c.URL, token_endpoint)
    c.setopt(c.HTTPHEADER, ['Accept: application/json'])
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, data.write)
    c.setopt(pycurl.SSL_VERIFYPEER, 1)
    c.setopt(pycurl.SSL_VERIFYHOST, 2)
    c.setopt(pycurl.CAINFO, "cacert.pem")
    c.perform()
    c.close()
    #get request response
    json_object = json.loads(data.getvalue())
    #get and save the token so it can be reused or return the error if there was one
    if 'access_token' in json_object:
    	token = json_object['access_token']
    	with open("token.txt", "w") as text_file:
    		text_file.write(token)
    	return token
    else:
    	print ("Could not generate token. " + str(json_object))

#Run Search
def search_affiliations(token, start=0):
	startRow = 0
	numRows = 200
	output = []
	#Create search string using search terms and type
	search = config.search
	type = config.type
	if type == 'ringgold':
		search_type = 'ringgold-org-id:'
	elif type == 'grid':
		search_type = 'grid-org-id:'
	elif type == 'name':
		search_type = 'affiliation-org-name:'
	else:
		print ("Invalid search type: " + type)
		return
	#build search query
	search_string = search_type + "(%22" + "%22+OR+%22".join(search) + "%22)"
	#encode any spaces in search terms
	search_string = search_string.replace(" ", "%20")
	#build search url
	base_url = config.search_endpoint
	while(True):
		data = BytesIO()
		#create request string
		request_string = base_url + "q=" + search_string + "&rows=200&start=" + str(startRow)
		#create and send http request
		c = pycurl.Curl()
		c.setopt(c.URL, request_string)
		c.setopt(c.HTTPHEADER, ['Accept: application/json', 'Authorization: Bearer %s' % token])
		c.setopt(c.POST, 0)
		c.setopt(c.WRITEFUNCTION, data.write)
		c.setopt(pycurl.SSL_VERIFYPEER, 1)
		c.setopt(pycurl.SSL_VERIFYHOST, 2)
		c.setopt(pycurl.CAINFO, "cacert.pem")
		c.perform()
		c.close()
		json_object = json.loads(data.getvalue())
		if 'result' in json_object:
			new_results = json_object['result']
			num_results = json_object['num-found']
			#If there are no results
			if new_results is None:
				break
			#Page through results
			if startRow + numRows > num_results:
				print ("Getting results " + str(num_results) + " out of " + str(num_results))
			else:
				print ("Getting results " + str(startRow + numRows) + " out of " + str(num_results))
			for result in new_results:
				temp_row = []
				temp_row.append(result['orcid-identifier']['path'])
				names = getName(result['orcid-identifier']['path'])
				if names['name']:
					if names['name']['given-names']:
						temp_row.append(names['name']['given-names']['value'])
					else:
						temp_row.append('')
					if names['name']['family-name']:
						temp_row.append(names['name']['family-name']['value'])
					else:
						temp_row.append('')
				else:
					temp_row.append('')
					temp_row.append('')
				output.append(temp_row)
			startRow += numRows
        	#if startRow > num_results:
        		#break
		else:
			print ("Error running search. " + str(json_object))
			break
	csv_to_file(output)

def getName(orcid):
	base_url = config.api_endpoint
	data = BytesIO()
	#create request string
	request_string = base_url + orcid + '/person'
	#create and send http request
	c = pycurl.Curl()
	c.setopt(c.URL, request_string)
	c.setopt(c.HTTPHEADER, ['Content-Type: application/orcid+xml', 'Accept: application/json'])
	c.setopt(c.POST, 0)
	c.setopt(c.WRITEFUNCTION, data.write)
	c.setopt(pycurl.SSL_VERIFYPEER, 1)
	c.setopt(pycurl.SSL_VERIFYHOST, 2)
	c.setopt(pycurl.CAINFO, "cacert.pem")
	c.setopt(c.WRITEFUNCTION, data.write)
	c.perform()
	c.close()
	#get request response
	json_object = json.loads(data.getvalue())
	return json_object
			
#Write the output results to a CSV file
def csv_to_file(output):
    with open("ORCID.csv", "w", newline='') as f:
        wr = csv.writer(f)
        wr.writerows(output)

def main():
	token = token_check()
	search_affiliations(token)


if __name__ == '__main__':
  main()