import requests


class OrchHelper:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.url_prefix = "https://" + url + "/gms/rest"
        self.session = requests.Session()
        self.headers = {}

    def login (self):
        # basic login function without multi-factor authentication
        try:
            response = self.post("/authentication/login", {"user": self.user, "password": self.password})
            if response.status_code == 200:
                print ("{0}: Orchestrator login success".format(self.url))
                # get and set X-XSRF-TOKEN
                for cookie in response.cookies:
                    if cookie.name == "orchCsrfToken":
                        self.headers["X-XSRF-TOKEN"] = cookie.value
                return True
            else:
                print ("{0}: Orchestrator login failed: {1}".format(self.url, response.text))
                return False
        except:
            print("{0}: Exception - unable to connect to Orchestrator".format(self.ipaddress))
            return False

    def mfa_login (self, mfacode):
        # alternative login function for multi-factor authentication
        # mfacode is integer value that is provided by Orchestrator after providing initial userid and passwd
        
        self.send_mfa( self.user, self.password()) #send the MFA code to end user
        try:
            response = self.post("/authentication/login", {"user": self.user, "password": self.password, "token": int(mfacode)})
            if response.status_code == 200:
                print ("{0}: Orchestrator MFA login success".format(self.url))
                # get and set X-XSRF-TOKEN
                for cookie in response.cookies:
                    if cookie.name == "orchCsrfToken":
                        self.headers["X-XSRF-TOKEN"] = cookie.value
                return True
            else:
                print ("{0}: Orchestrator MFA login failed: {1}".format(self.url, response.text))
                return False
        except:
            print("{0}: Exception - unable to connect to Orchestrator".format(self.ipaddress))
            return False
             
    def send_mfa(self, user, passwd):
        # send request to Orchestrator to issue MFA token to user
        try:
            self.post("/authentication/loginToken",{"user": user, "password": passwd, "TempCode": True})
        except:
            print("Exception - unable to submit token request")
        
    def logout(self):
        try:
            r = self.get("/authentication/logout")
            if r.status_code == 200:
                print ("{0}: Orchestrator logout success".format(self.url))
            else:
                print ("{0}: Orchestrator logout failed: {1}".format(self.url, r.text))
        except:
            print("{0}: Exception - unable to logout of Orchestrator".format(self.ipaddress))


    def post(self, url, data):
        return self.session.post(self.url_prefix + url, json=data, verify=False, timeout=120, headers=self.headers)

    def get(self, url):
        return self.session.get(self.url_prefix + url, verify=False, timeout=120, headers=self.headers)

    def delete(self, url):
        return self.session.delete(self.url_prefix + url, verify=False, timeout=120, headers=self.headers)

    def put(self, url, data):
        return self.session.put(self.url_prefix + url, json=data, verify=False, timeout=120, headers=self.headers)

    def get_appliances(self):
        r = self.get("/appliance")
        if r.status_code == 200:
            return r.json()
        else:
            print ("{0}: unable to get appliance list: {1}".format(self.url, r.text))
            return []
