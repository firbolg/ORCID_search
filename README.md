# orcid-search

**NOTE: This functionality is now supported directly by the search API.  You can ask it for CSV results!  See [Search results returned in CSV format](https://members.orcid.org/api/resources/find-myresearchers) for details.**

Python CLI for searching the ORCID public API

This script generates a CSV file of all ORCID records that match an affiliation search. You can search by organization name or identifier and multiple terms can be entered.

## Prerequisites

- Install [Python](https://www.python.org/downloads) 2.7.9
- Install [PIP](https://pip.pypa.io/en/stable/installing/) (this should be included with your Python installation, but if not, you will need to install it separately)
- ORCID public API or member API credentials. If you do not have credentials, you can [register a Public API Client](https://support.orcid.org/hc/en-us/articles/360006897174-Register-a-public-API-client-application).

Guides for installing Python/PIP: 

- [Get your Mac ready for Python programming](https://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/Get-Your-Mac-Ready-for-Python-Programming/)
- [How to install Python PIP on Windows, Mac and Linux](https://www.makeuseof.com/tag/install-pip-for-python/)

## Clone this repository to your machine

1. `git clone https://github.com/ORCID/orcid-search.git`

## Set up virtual environment 

1. `cd orcid-search`

2. `virtualenv venv`

3. `source ./venv/bin/activate` Mac/\*Nix systems (or emulators, such as Git Bash and Cygwin) `source venv\bin\activate` Windows Command Prompt

4. `pip2 install -r requirements.txt` 

*Note: If you are running MacOS High Sierra, you may receive an error installing the packages in requirements.txt. To fix, install Xcode command line tools* `xcode-select --install`

## Run script

Parameters

| Parameter   |      Value      |
|----------|-------------|
| search |  the value you are searching for, multiple terms can be separated with a semi colon followed by a space |
| type |  if the search value is an organization name, Ringgold identifier or GRID identifier (name is default)   |
| orcid\_client\_id | your client id |
| orcid\_client\_secret | your client secret |
| file | path to the file to save the output |

**Command line syntax**

Relace values in square brackets with your values in inverted commas.

`python search_orcid.py --search=[affiliation organization name(s) or identifiers] --type=[ringgold/grid/name] --orcid_client_id=[Your client iD] --orcid_client_secret=[Your client secret] --file=[path to save results file]`
    
**Command line examples**

`python search_orcid.py --search='National Taiwan Normal University; 國立臺灣師範大學; NTNU' --type='name' --orcid_client_id='APP-L3M68AY6XVSOKTCK' --orcid_client_secret='892***6' --file=results.csv`

`python search_orcid.py --search='385488' --type='ringgold' --orcid_client_id='0000-0001-8203-3567' --orcid_client_secret='193***7' --file=results.csv`

`python search_orcid.py --search='Oberlin' --orcid_client_id='APP-L3M68AY6XVSOKTCK' --orcid_client_secret='892***6' --file=folder/results.csv`
