import requests

import api.models as models

# TODO -Error control. If the page exists, it's not replaced.
# Format reference: https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html

CONFLUENCE_URL = 'https://adelrio.atlassian.net/wiki/rest/api/content'


def get_api_key():
    return open('/Users/albertodelrio/Documents/garrett/atlassian_api_token.txt').read().strip()


def get_auth_data():
    return ('aldelrio@protonmail.com', get_api_key())


def write_confluence_page(review, space_id, parent_page_id):
    html = review_to_html(review)
    headers = {'content-type': 'application/json'}
    auth = get_auth_data()
    data = {
        'type': 'page',
        'title': review.title,
        'ancestors': [{'id': parent_page_id}],
        'space': {
            'key': space_id,
        },
        'body': {
            'storage': {
                'value': review_to_html(review),
                'representation': 'storage'
            }
        }
    }

    _ = requests.post(CONFLUENCE_URL, auth=auth, json=data, headers=headers)


def review_to_html(review):
    res_html = ''
    res_html += (f'<h1>{review.title}</h1>')

    findings = models.Finding.objects.filter(review=review.oid).order_by('creation_date')
    if findings:
        res_html += (f'<h2>Findings</h2>')
        for idx, finding in enumerate(findings):
            res_html += finding_to_html(finding, idx)

    test_cases = models.TestCase.objects.filter(
        review=review.oid).order_by('requirement__readable_id')
    res_html += (f'<h2>Test cases</h2>')
    res_html += (
        '<table><thead><tr><td>Requirement</td><td>Status</td><td>Description</td></tr></thead>')
    for test_case in test_cases:
        res_html += test_case_to_html(test_case)
    res_html += ('</table>')

    return res_html


def finding_to_html(finding, fid):
    res_html = (f'<h3>Finding #{fid}</h3>'
                f'<table>'
                f'<tr>'
                f'<td>{finding.description}</td>'
                f'</tr>'
                f'<tr>'
                f'<td>Status</td><td>')

    res_html += '<span style="color: rgb('
    if finding.status == models.Finding.FindingStatus.PENDING:
        res_html += '255, 0, 0'
    else:
        res_html += '0, 255, 0'
    res_html += ');">'
    # res_html += '<span style="color: rgb(255, 0, 0);">'
    res_html += (f'{finding.status}</span></td>'
                 f'<td>Impact</td><td> {finding.impact}</td>'
                 f'</tr>'
                 f'</table>')
    return res_html


def test_case_to_html(test_case):
    requirement = test_case.requirement
    res_html = (f'<tr>'
                f'<td>{requirement.readable_id}</td>')

    res_html += '<td>'
    if test_case.status != models.TestCase.TestStatus.PENDING:
        res_html += '<span style="color: rgb('
        if test_case.status == models.TestCase.TestStatus.SUCCESS:
            res_html += '0, 255, 0'
        if test_case.status == models.TestCase.TestStatus.FAIL:
            res_html += '255, 0, 0'
        res_html += ');">'

    res_html += f'{test_case.status}'
    if test_case.status != models.TestCase.TestStatus.PENDING:
        res_html += '</span>'
    res_html += '</td>'

    if test_case.description:
        res_html += f'<td>{test_case.description}</td>'
    else:
        res_html += '<td>-</td>'
    res_html += '</tr>'

    return res_html
