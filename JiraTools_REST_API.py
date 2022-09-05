import requests
from requests.auth import HTTPBasicAuth
import json

# Username and password for basic auth. Understanding basic auth it not often the recomended form of authentication. OAuth 2.0 is more secure.
UN = '<basicAuthUsername>'
PW = '<basicAuthPassword>'
JiraURL = 'https://jira.company.com/rest/api/2'


class JiraTools:
    # Get entire json payload of the jira story
    def getJiraIssue(issueID):
        url = '{}/issue/{}'.format(JiraURL, issueID)
        r = requests.get(url, auth=HTTPBasicAuth(UN, PW)).json()
        return r

    # Create a new Jira story on the select project board. There are many fields that can be added here, so this is just a few.
    def createJiraStory(projectID, summary, description, requestorID):
        url = '{}/issue'.format(JiraURL)
        headers = {"content-type": "application/json"}
        body = {
            "fields": {
                "project":
                {
                    "key": "{}".format(projectID)
                },
                "summary": "{}".format(summary),
                "reporter": {  # or add watcher?
                    "name": "{}".format(requestorID)
                },
                "description": "{}".format(description),
                "issuetype": {
                    "name": "Story"
                }
            }
        }
        r = requests.post(
            url,
            headers=headers,
            auth=HTTPBasicAuth(UN, PW),
            data=json.dumps(body)
        ).json()
        return r

    # Comment on existing Jira story
    def addComment2JiraStory(issueID, comment):
        headers = {"content-type": "application/json"}
        url = '{}/issue/{}/comment'.format(JiraURL, issueID)
        body = {
            "body": "{}".format(comment)
        }
        r = requests.post(
            url,
            headers=headers,
            auth=HTTPBasicAuth(UN, PW),
            data=json.dumps(body)
        ).json()
        return r

    # Toggle Jira 'Impediment' flag, Takes in Jira issue ID (ex. 'ABC-1234') as well as a boolean value for flag value. 
    # NOTE: The custom field value may differ depending on your Jira implementation. I will upload a function using greenhoper in a later verison.
    def flagJiraStory(issueID, isFlagged: bool):
        url = '{}/issue/{}'.format(JiraURL, issueID)
        headers = {"content-type": "application/json"}
        if isFlagged == True:
            body = {
                "fields": {
                    "customfield_10100": [{"value": "Impediment"}]
                }
            }
        else:
            body = {
                "fields": {
                    "customfield_10100": None
                }
            }
        r = requests.put(
            url,
            headers=headers,
            auth=HTTPBasicAuth(UN, PW),
            data=json.dumps(body)
        ).json()
        return r

    # Get all available story status. ie. To Do, In Progress, etc.
    def getJiraTransitions(issueID):
        url = '{}/issue/{}/transitions'.format(JiraURL, issueID)
        r = requests.get(url, auth=HTTPBasicAuth(UN, PW)).json()
        r = r['transitions']
        return r

    # Transition Jira story to a new status. ie. 'To do' to 'In Progress'
    def updateJiraStatus(issueID, statusName):
        t = JiraTools.getJiraTransitions(issueID)
        statusID = None
        for i in t:
            if i['name'] == statusName:
                statusID = i['id']
                break
        if statusID == None:
            raise Exception(
                "Status does not exist or was not found, please try the getJiraTransitions(issueID) function to see avaialable status")

        url = '{}/issue/{}/transitions'.format(JiraURL, issueID)
        headers = {"content-type": "application/json"}
        body = {
            "transition": {
                "id": "{}".format(statusID)
            }
        }
        r = requests.post(
            url,
            headers=headers,
            auth=HTTPBasicAuth(UN, PW),
            data=json.dumps(body)
        ).json()
        return r
