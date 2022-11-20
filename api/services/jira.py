import os
import logging

import requests

import api.models as models
import api.services as services

# https://api.atlassian.com/oauth/token/accessible-resources
CLOUD_ID = os.getenv('JIRA_CLOUD_ID')
WORKFLOW_ID = os.getenv('JIRA_WORKFLOW_ID')
BASE_URL = f'https://api.atlassian.com/ex/jira/{CLOUD_ID}'
ATLASSIAN_PROJECT = os.getenv('ATLASSIAN_PROJECT')
ISSUES_JQL = os.getenv('JIRA_ISSUES_JQL')
ATLASSIAN_SITE = os.getenv('ATLASSIAN_SITE')


class JiraWrapper(object):

    def _do_request(self, ep, email, data=None):
        token = services.jira_auth.get_token(email)
        headers = {'authorization': f'Bearer {token}'}
        url = f'{BASE_URL}{ep}'
        if data:
            r = requests.post(url, json=data, headers=headers)
        else:
            r = requests.get(url, headers=headers)

        logging.debug(f'Jira request {url} -> {r}')
        return r

    def validate_jql(self, email, jql):
        res = True
        data = {}
        data['queries'] = [jql] if type(jql) is str else [jql]

        r = self._do_request('/rest/api/3/jql/parse', email, data)

        for query in r.json()['queries']:
            if 'errors' in query.keys():
                res = False
                break

        logging.debug(f'Validate jql: {r}')
        return res

    def parse_issue(self, issue):
        keys = ['key']
        res = {}
        for k in keys:
            res[k] = issue[k]
        return res

    def get_issue(self, email, issue_id):
        r = self._do_request(f'/rest/api/3/issue/{issue_id}', email)
        res = {}

        if r.status_code == 200:
            res = r.json()
        else:
            logging.error(f'Could not retrieve issue {issue_id}')

        return res

    def get_issues(self, email):
        res = {}
        chunk_size = 100
        data = {'jql': ISSUES_JQL, 'maxResults': chunk_size, 'startAt': 0}

        while True:
            r = self._do_request('/rest/api/3/search', email, data)
            if r.status_code != 200:
                logging.error(f'Could not retrieve issues for {email}')
                break
            json_res = r.json()
            for issue in json_res['issues']:
                res[str(issue['id'])] = self.parse_issue(issue)
            data['startAt'] += chunk_size
            if len(res) >= json_res['total']:
                break

        logging.debug(f'Get issues -> {len(res)}')
        return res

    def get_transitions(self, email, issue_key):
        '''
            id -> transition ID
            name -> transition name
            to.name -> new state name
        '''
        r = self._do_request(f'/rest/api/3/issue/{issue_key}/transitions', email)
        logging.debug(f'Get transitions: {r}')
        return r.json()['transitions']

    def get_transition_from_new_state(self, issue_key, new_state):
        transitions = self.get_transitions(issue_key)
        transition_id = None

        for transition in transitions:
            if transition['to']['name'] == new_state:
                transition_id = transition['id']
                break

        logging.debug(f'Get transition {issue_key} ({new_state}) -> {transition_id}')
        return transition_id

    def get_transition_for_status(self, email, issue_key, to_status):
        r = self._do_request(f'/rest/api/3/issue/{issue_key}/transitions', email)
        res = None
        if r.status_code == 200:
            js = r.json()
            for transition in js['transitions']:
                if str(transition['to']['id']) == str(to_status):
                    res = transition['id']
                    break

        logging.info(f'Get transition for status {to_status}: {r} - {res}')
        return res

    def transition_issue(self, email, issue_key, garrett_action):
        if type(issue_key) is models.JiraIssue:
            issue_key = issue_key.jira_key
        garrett_transition = models.JiraTransition.objects.filter(
            garrett_action=garrett_action).first()

        logging.info(f'Transitioning jira issue: {issue_key}')

        if garrett_transition:
            to_status = garrett_transition.transition_id
            transition_id = self.get_transition_for_status(email, issue_key, to_status)

            if transition_id:
                data = {'transition': {'id': transition_id}}
                r = self._do_request(f'/rest/api/3/issue/{issue_key}/transitions', email, data)
                logging.debug(f'Transition issue {issue_key} ({transition_id}): {r}')
            else:
                logging.debug(f'No transition found for {garrett_action}')

    def get_name_for_transition(self, email, transition_id):
        res = ''
        for tid, tname in self.get_jira_statuses(email).items():
            if tid == transition_id:
                res = tname
                break
        logging.debug(f'Found name ({res}) for transition ({transition_id})')
        return res

    def get_jira_statuses(self, email):
        statuses = set()

        r = self._do_request(f'/rest/api/3/project/{ATLASSIAN_PROJECT}/statuses', email)
        if r.status_code == 200:
            js = r.json()
            for workflow in js:
                if workflow['id'] == WORKFLOW_ID:
                    statuses = {status['id']: status['name'] for status in workflow['statuses']}
                    break
            else:
                logging.warning(f'Workflow {WORKFLOW_ID} not found')
        else:
            logging.warning(f'Failed to retrieve statuses: {r}')

        return statuses

    def get_url_for_issue(self, issue):
        return f'{ATLASSIAN_SITE}/browse/{issue.jira_key}'
