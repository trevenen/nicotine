import getpass
import sys
import vapor

from jira import JIRA

class SmokeFree:
    def __init__(self, jira_url='https://jira.domain.com/', username, password, project=''
                 summary='nicotine patch applied',
                 description='automated nicotine patch' + \
                 'testing', issuetype={'name': 'Task'},
                 customfield_SOMEINT={"value": 'something'}):
        self.jira_url = jira_url
        self.username = username
        self.password = password
        self.project = project
        self.summary = summary
        self.description = description
        self.issuetype = issuetype
        self.customfield_SOMEINT = customfield_SOMEINT

    def smoke_free(self):
        try:
            jira_client = JIRA(self.jira_url, auth=(self.username, self.password))
            response = jira_client.create_issue(project=self.project, summary=self.summary, description=self.description, issuetype=self.issuetype, customfield_SOMEINT=self.customfield_SOMEINT)
            vapor.vapors('JIRA PBI created successfully! Congratualtions on being smoke free.')
        except Exception as e:
            vapor.vapors('something failed when creating JIRA ticket. see error below:\n', e)
            raise
