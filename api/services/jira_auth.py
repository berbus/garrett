import logging
import os
import random
import requests
import time

CLIENT_ID = os.getenv('ATLASSIAN_CLIENT_ID')
CLIENT_SECRET = os.getenv('ATLASSIAN_CLIENT_SECRET')
GARRETT_URL = os.getenv('GARRETT_URL')

confluence_scope = 'write:confluence-content'
jira_scope = ('read:jira-work write:jira-work read:jira-user '
              'manage:jira-configuration')


class JiraCreds(object):

    def __init__(self, secret):
        self.secret = secret
        self.token = None
        self.token_expires = -1
        self.refresh_token = None
        self.refresh_token_expires = -1

    def update_token(self, access_token, expires_in, refresh_token):
        self.refresh_token = refresh_token
        self.token = access_token
        self.token_expires = expires_in + int(time.time()) - 1


class JiraAuth(object):

    creds = {}

    def get_authorization_url(self, email):
        logging.info(f'Returning authorization URL for {email}')
        user_secret = random.randbytes(50).hex()
        self.creds[email] = JiraCreds(user_secret)
        scope = f'offline_access {confluence_scope} {jira_scope}'
        return ('https://auth.atlassian.com/authorize?audience=api.atlassian.com'
                f'&client_id={CLIENT_ID}'
                f'&scope={scope}'
                f'&redirect_uri={GARRETT_URL}/api/jira_auth/authorize/'
                f'&state={user_secret}&response_type=code&prompt=consent')

    def get_email_from_secret(self, user_secret):
        logging.info('Getting email from secret')
        res = None
        for email, creds in self.creds.items():
            if creds.secret == user_secret:
                res = email
                break
        logging.info(f'Getting email from secret: {res is not None}')
        return res

    def exchange_code_for_token(self, email, auth_code, user_secret):
        logging.info(f'Exchanging code for token: {email}')
        res = False
        server_secret = self.creds[email].secret
        self.creds[email].secret = None

        if server_secret != user_secret:
            raise Exception('Invalid secret code')

        json_data = {
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': auth_code,
            'redirect_uri': 'https://localhost:8000/',
        }
        r = requests.post('https://auth.atlassian.com/oauth/token', json=json_data)
        if r.status_code == 200:
            j = r.json()
            self.creds[email].update_token(j['access_token'], j['expires_in'], j['refresh_token'])
            res = True
        return res

    def refresh_token(self, email):
        logging.info(f'Refreshing token for {email}')
        res = False
        refresh_token = self.creds[email].refresh_token
        json_data = {
            'grant_type': 'refresh_token',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': refresh_token,
        }
        r = requests.post('https://auth.atlassian.com/oauth/token', data=json_data)
        if r.status_code == 200:
            j = r.json()
            self.creds[email].update_token(j['access_token'], j['expires_in'], j['refresh_token'])
            res = True
        return res

    def do_test_request(self, email):
        logging.info(f'Doing test request for {email}')
        test_endpoint = 'oauth/token/accessible-resources'
        token = self.creds[email].token
        headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
        url = f'https://api.atlassian.com/{test_endpoint}'
        r = requests.get(url, headers=headers)
        logging.info(f'Test request for {email}: {r}')
        return r.status_code == 200

    def user_authenticated(self, email):
        res = False
        if email in self.creds:
            res = self.do_test_request(email)
            if not res:
                res = self.refresh_token(email)
            if not res and self.creds[email] is None:
                del self.creds[email]
        logging.info(f'User {email} authenticated: {res}')
        return res

    def get_token(self, email):
        return self.creds[email].token if self.user_authenticated(email) else None
