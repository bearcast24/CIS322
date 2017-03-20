# This client can be used to interact with the LOST 
#From  in class code:
import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

roles = {'logofc' : 'Logistics Officer', 'facofc' : 'Facilities Officer'}

def main():
    # Check the CLI arguments
    if len(sys.argv)<5 :
        print("Usage: python3 %s <url> <username> <password> <role>"%sys.argv[0])
        return
    
    # Prep the arguments ##Make sure this is the same as the form:
    args = dict()
    args['username']  = sys.argv[2]
    args['password']  = sys.argv[3]
    args['role']  = roles[sys.argv[4]]


    # Print a message to let the user know what is being tried
    print("Activating user: %s"%args['username'])

    # Setup the data to send
    data = urlencode(args)
    #print("sending:\n%s"%data)
    
    # Make the resquest
    my_route = "active_user" #From out account -> Use create_user
    req = Request(sys.argv[1]+ my_route, data.encode('ascii'),method='POST')


    #See if way to change the user password:
    
    #From the webserver: change from a render template to return a text string:
    res = urlopen(req)
    
    
    # Print the result code
    print("Call to LOST returned: %s"%res.read().decode('ascii'))
    

if __name__=='__main__':
    main()
    
