from requests.auth import HTTPBasicAuth
import requests
from Config import teamcity_creds
from bs4 import BeautifulSoup
from SlackUtils import print_to_slack
import time
import threading

url = "http://teamcity.mcc-tomsk.de/httpAuth/app/rest/buildQueue"
xml = """<build>
            <buildType id="{0}"/>
         </build>"""

headers = {'Content-Type': 'application/xml'}


def trigger_build(build_id):
    body = xml.format(build_id)
    response = requests.post(url, data=body, headers=headers, auth=HTTPBasicAuth(teamcity_creds["login"], teamcity_creds["password"]))

    return response


def observe_build_status(url):
    while True:
        response = requests.get("http://teamcity.mcc-tomsk.de" + url, auth=HTTPBasicAuth(teamcity_creds["login"],
                                                                                         teamcity_creds["password"]))

        soup = BeautifulSoup(response.text, "html.parser")
        if soup.build['state'] == "queued":
            print_to_slack("Build queued")
            time.sleep(30)

        if 'status' in soup.build and soup.build['status'] == "FAILURE":
            print_to_slack("Build Failed with status text:")
            print_to_slack(soup.statustext)
            break

        if 'status' in soup.build and soup.build['status'] == "SUCCESS":
            print_to_slack("Build Success with status text:")
            print_to_slack(soup.statustext)
            break
