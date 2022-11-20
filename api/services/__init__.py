from .jira import JiraWrapper
from .jira_auth import JiraAuth
from .confluence import ConfluenceWrapper

jira = JiraWrapper()
jira_auth = JiraAuth()
confluence = ConfluenceWrapper()
