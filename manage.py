#!/usr/bin/python
import urllib2, json, time, credentials, sys

#Get our Bearer auth token from CS
def get_auth():
    method = "POST"
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    #pull from a file named credentials.py
    #File must contain two variables defined as
    #clientid = "1a2b3c4d"
    #clientsecret = "a1b2c3d4"
    data = "client_id="+credentials.clientid+"&client_secret="+credentials.clientsecret
    url = "https://api.crowdstrike.com/oauth2/token"
    request = urllib2.Request(url, data=data)
    request.add_header('accept', 'application/json')
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.get_method = lambda: method
    #try to connect to api and get token
    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e
        print e
        exit()
    #read cconnection data into var
    data = connection.read()
    #convert to json
    data1 = json.loads(data)
    #extract json to var
    token = data1['access_token']
    return token

#get host file from system
def load_hosts():
    hosts_file = sys.argv[1]
    with open(hosts_file) as f:
        hosts = f.read().splitlines()
    return hosts

#Send api request to add hosts
def add_hosts():
    hosts = load_hosts()
    token = get_auth()
    for i in range(len(hosts)):
        method = "POST"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        data = "{ \"action_parameters\": [{ \"name\": \"filter\",\"value\": \"(device_id: \'"+hosts[i]+"\')\" }],\"ids\": [\""+sys.argv[2]+"\"]}"
        url = "https://api.crowdstrike.com/devices/entities/host-group-actions/v1?action_name=add-hosts"
        request = urllib2.Request(url, data)
        request.add_header('Content-Type', 'application/json')
        request.add_header('Authorization', 'Bearer '+token)
        request.get_method = lambda: method
        try:
            connection = opener.open(request)
        except urllib2.HTTPError,e:
            connection = e
            print e
        data = connection.read()
        print data
        time.sleep(.12)

try:
    def main():
        add_hosts()



#check for ^C
except KeyboardInterrupt:
    print '\n'" Bye!"
    sys.exit()

#Call the main function
if __name__=='__main__':
    main()
    sys.exit()
