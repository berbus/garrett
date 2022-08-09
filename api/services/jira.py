import os
import sys
import time
import threading

import jira

import api.models as models


class JiraWrapper(object):
    TOKEN = os.getenv('ATLASSIAN_API_TOKEN')
    SITE = os.getenv('ATLASSIAN_SITE')
    EMAIL = os.getenv('ATLASSIAN_EMAIL')
    PROJECT = os.getenv('ATLASSIAN_PROJECT')
    INITIAL_ISSUE_STATE = os.getenv('JIRA_INITIAL_ISSUE_STATE', 'done').lower()
    SERVICE_FIELD = os.getenv('JIRA_SERVICE_FIELD', 'components')
    UPDATE_TIMEOUT = os.getenv('JIRA_UPDATE_TIMEOUT', 60)
    jc = jira.JIRA(SITE, basic_auth=(EMAIL, TOKEN))

    def __init__(self):
        if type(self.UPDATE_TIMEOUT) is str:
            self.UPDATE_TIMEOUT = int(self.UPDATE_TIMEOUT)
        self.scheduler = threading.Thread(target=self.run_scheduler)

        # So the thread does not run with migrations
        if sys.argv[1] == 'runserver' and not os.getenv('DJ_DEBUG'):
            print('Launching Jira scheduler')
            self.scheduler.start()

    def run_scheduler(self):
        while True:
            print('Updating all issues in Jira DB')
            self.update_jira_issues_db(only_open=False)
            time.sleep(self.UPDATE_TIMEOUT)

    def get_all_open_issues(self):
        return self.jc.search_issues(f'project={self.PROJECT}'
                                     f'&status={self.INITIAL_ISSUE_STATE}'
                                     f'&component IS NOT empty')

    def get_all_issues(self):
        return self.jc.search_issues(f'project={self.PROJECT}'
                                     f'&status={self.INITIAL_ISSUE_STATE}'
                                     f'&component IS NOT empty')

    def update_jira_issues_db(self, only_open=True):
        print(f'Updating Jira issues: {only_open}')
        if only_open:
            issues = self.get_all_open_issues()
        else:
            issues = self.get_all_issues()

        for issue in issues:
            print(f'Updating {issue}')
            db_issue = models.JiraIssue.objects.filter(jira_id=issue.key)
            if db_issue.exists():
                db_issue = db_issue.first()
                db_issue.status = issue.fields.status.name.lower()
                db_issue.save()
            else:
                issue_obj = models.JiraIssue(jira_id=issue.key,
                                             status=issue.fields.status.name.lower())

                issue_obj.save()

                components = [component.name for component in issue.fields.components]
                services = models.Service.objects.filter(name__in=components)
                issue_obj.services.set(services)

    def transition_jira_issue(self, issue, garrett_action):
        jira_transition = models.JiraTransition.objects.filter(
            garrett_action=garrett_action).first()

        if jira_transition:
            transition_name = jira_transition.transition_name
            jira_issue = self.jc.issue(issue.jira_id)
            transition_id = self.find_transition_by_name(jira_issue, transition_name)
            if transition_id:
                self.jc.transition_issue(jira_issue, transition_id)
                issue.status = jira_transition.transition_name
                issue.save()
            else:
                print(f'Invalid Jira transition: {jira_issue} -> {transition_id}')
        else:
            print(f'No transition defined for Garret Action: {garrett_action}')

    def find_transition_by_name(self, issue, name):
        transition_id = self.jc.find_transitionid_by_name(issue, name)
        if not transition_id:
            transitions = self.jc.transitions(issue)
            for transition in transitions:
                if transition['to']['name'].lower() == name.lower():
                    transition_id = transition['id']
                    break
        return transition_id

    def get_jira_statuses(self):
        res = []
        statuses = self.jc.statuses()
        _ = [res.append(s.name.upper()) for s in statuses]
        return res

    def get_url_for_issue(self, issue):
        return f'{self.SITE}/browse/{issue.jira_id}'
