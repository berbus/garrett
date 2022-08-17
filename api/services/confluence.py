
import os

import requests

from .confluence_writer import prepare_confluence_data


class ConfluenceWrapper(object):
    SITE = os.getenv('ATLASSIAN_SITE')
    TOKEN = os.getenv('ATLASSIAN_API_TOKEN')

    def __init__(self):
        self.auth_data = ('aldelrio@protonmail.com', self.TOKEN)

    def write_results(self, elem):
        ep = '/wiki/rest/api/content'
        for service in elem.services.all():
            if service.confluence_parent_id and service.confluence_space:
                data = prepare_confluence_data(elem, service.name)
                data['ancestors'].append({'id': service.confluence_parent_id})
                data['space']['key'] = service.confluence_space
                self._do_request(ep, data)

    def _do_request(self, ep, data):
        headers = {'content-type': 'application/json'}
        url = f'{self.SITE}{ep}'
        r = requests.post(url, auth=self.auth_data, json=data, headers=headers)
