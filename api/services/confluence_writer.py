
import api.models as models

# TODO -Error control. If the page exists, it's not replaced.
# Format reference: https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html


def prepare_confluence_data(elem):
    if type(elem) is models.SecurityTest:
        return get_data_for_security_test(elem)
    else:
        raise NotImplementedError('nope')


def get_data_for_security_test(security_test):
    data = {
        'type': 'page',
        'title': security_test.title,
        'ancestors': [],
        'space': {},
        'body': {
            'storage': {
                'value': security_test_to_html(security_test),
                'representation': 'storage'
            }
        }
    }

    return data


def security_test_to_html(security_test):
    res_html = ''
    res_html += (f'<h1>{security_test.title}</h1>')

    findings = models.Finding.objects.filter(
        security_test=security_test.oid).order_by('creation_date')
    if findings:
        res_html += ('<h2>Findings</h2>')
        for idx, finding in enumerate(findings):
            res_html += finding_to_html(finding, idx)

    test_cases = models.TestCase.objects.filter(
        security_test=security_test.oid).order_by('requirement__readable_id')
    res_html += ('<h2>Test cases</h2>')
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
