# This client can be used to interact with the LOST interface prior to encryption
# implementation

import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    # Check the CLI arguments
    if len(sys.argv)<3 :
        print("Usage: python3 %s <url> <username>"%sys.argv[0])
        return
    
    # Prep the arguments ##Make sure this is the same as the form:
    args = dict()
    args['username']  = sys.argv[2]


    # Print a message to let the user know what is being tried
    print("Suspending user: %s"%args['username'])

    # Setup the data to send
    data = urlencode(args)
    #print("sending:\n%s"%data)
    
    # Make the resquest
    my_route = sys.argv[1] + "revoke_user" #From out account -> Use create_user
    req = Request(my_route, data.encode('ascii'),method='POST')

   
    #From the webserver: change from a render template to return a text string:
    res = urlopen(req)
    
    
    # Print the result code
    print("Call to LOST returned: %s"%res.read().decode('ascii'))
    

if __name__=='__main__':
    main()
    
