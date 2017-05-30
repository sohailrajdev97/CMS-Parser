import urllib.request
import urllib.parse
import http.cookiejar
import lxml.html

class Login:
    
    def __init__(self , username , password):
        self.username = username
        self.password = password
        
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler(),
            urllib.request.HTTPHandler(debuglevel=0),
            urllib.request.HTTPSHandler(debuglevel=0),
            urllib.request.HTTPCookieProcessor(self.cj)
        )
        
        self.opener.addheaders = [
                    ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                                   'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]
        
        self.cmsLogin()
        self.cmsLogin()

    def cmsLogin(self):
        loginDetails = urllib.parse.urlencode({"username":self.username , "password":self.password}).encode()
        rq = urllib.request.Request("http://id.bits-hyderabad.ac.in/moodle/login/index.php" , data = loginDetails)
        response = self.opener.open(rq)
    
    def openForParse(self , url):
        req = urllib.request.Request(url)
        resp = self.opener.open(req).read()
        return resp