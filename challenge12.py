#!/usr/bin/env python

import os
import ConfigParser
import requests
from werkzeug.datastructures import MultiDict

def get_credentials(credential_file):
    """
    Shamelessly stolen from pyrax

    Reads in the credentials from the supplied file. It should be
    a standard config file in the format:
   
    [mailgun]
    api_key = 1234567890abcdef

    """
    _creds_file = credential_file
    cfg = ConfigParser.SafeConfigParser()
    try:
        if not cfg.read(credential_file):
            # If the specified file does not exist, the parser will
            # return an empty list
            raise exc.FileNotFound("The specified credential file '%s' "
                    "does not exist" % credential_file)
    except ConfigParser.MissingSectionHeaderError as e:
        # The file exists, but doesn't have the correct format.
        raise exc.InvalidCredentialFile(e)
    try:
        api_key = cfg.get("mailgun", "api_key")
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
        raise exc.InvalidCredentialFile(e)

    return api_key


cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')
api_key = get_credentials(cred_file)
print api_key
'''
curl -s --user api:{key} \
    https://api.mailgun.net/v2/routes \
    -F priority=1 \
    -F description='Challenge route' \
    -F expression='match_recipient("david.grier@apichallenges.mailgun.org")' \
    -F action='forward("http://cldsrvr.com/challenge1")'\
    -F action='stop()'
'''
def get_routes():
    return requests.get(
        "https://api.mailgun.net/v2/routes",
        auth=("api", api_key),
        params={"skip": 1,
                "limit": 1})

def create_route():
    return requests.post(
        "https://api.mailgun.net/v2/routes",
        auth=("api", api_key),
        data=MultiDict([
		("priority", 1),
		("description", "Challenge12 route"),
		("expression", "match_recipient('david.grier@apichallenges.mailgun.org')"),
		("action", "forward('http://cldsrvr.com/challenge1')"),
		("action", "stop()")
	])) 

create_route()
#get_routes()
