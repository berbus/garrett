import os

import requests

import api.models as models
from .confluence_html import get_html_for_elem


class ConfluenceWrapper(object):
    SITE = os.getenv('ATLASSIAN_SITE')
    TOKEN = os.getenv('ATLASSIAN_API_TOKEN')

    def __init__(self):
        self.auth_data = ('aldelrio@protonmail.com', self.TOKEN)

    def get_html_report(self, elem):
        html = ''
        service = elem.services.first()
        if service:
            html = get_html_for_elem(elem)
        return html

    def write_results(self, elem):
        ep = '/wiki/rest/api/content'
        for service in elem.services.all():
            if service.confluence_parent_id and service.confluence_space:
                html = get_html_for_elem(elem)
                title = self.get_title(elem, service.name)
                confluence_json = self.get_confluence_json(title, html, service.confluence_space,
                                                           service.confluence_parent_id)
                self._do_request(ep, confluence_json)

    def _do_request(self, ep, data):
        headers = {'content-type': 'application/json'}
        url = f'{self.SITE}{ep}'
        r = requests.post(url, auth=self.auth_data, json=data, headers=headers)
        r.raise_for_status()

    def get_title(self, elem, service_name):
        title = ''
        if type(elem) is models.SecurityTest:
            title = f'Security Test for {service_name} - {elem.title}'
        elif type(elem) is models.ThreatModel:
            title = f'Threat Model for {service_name} - {elem.title}'
        return title

    def get_confluence_json(self, title, html, space_id, parent_id):
        data = {
            'type': 'page',
            'title': title,
            'ancestors': [{
                'id': parent_id
            }],
            'space': {
                'key': space_id
            },
            'body': {
                'storage': {
                    'value': html,
                    'representation': 'storage'
                }
            }
        }

        return data
