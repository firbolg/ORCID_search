import argparse
import time
import calendar

parser = argparse.ArgumentParser()
parser.add_argument('--search', type=str)
parser.add_argument('--type', type=str, default='name')
parser.add_argument('--orcid_client_id', type=str)
parser.add_argument('--orcid_client_secret', type=str)
parser.add_argument('--file', type=str)
args = parser.parse_args()
type = args.type
org_str = args.search
search = org_str.split("; ")
outputFile = args.file
client_id = args.orcid_client_id
client_secret = args.orcid_client_secret
token_endpoint = "https://orcid.org/oauth/token"
search_endpoint='https://pub.orcid.org/v3.0/search/?'
api_endpoint='https://pub.orcid.org/v3.0/'