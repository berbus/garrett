
import json
import uuid


SRC_FNAME = 'utils/owasp_asvs.json'
DST_FNAME = 'api/fixtures/requirements.json'
DST_TEMPLATE_FNAME = 'api/fixtures/templates.json'

def load_previous_data():
    data = []
    prev_data = {}
    with open(DST_FNAME) as fd:
        data = json.load(fd)

    for elem in data:
        prev_data[elem['fields']['readable_id']] = elem['fields']['oid']

    return prev_data


def create_template_fixtures(req_data):
    res_data = []
    lvl = 1

    for level, reqs in req_data.items():

        new_entry = {'model': 'api.template', 'fields': {
            'name': f'Default template - OWASP Level {lvl}',
            'requirements': reqs
            }}

        res_data.append(new_entry)
        lvl += 1


    json.dump(res_data, open(DST_TEMPLATE_FNAME, 'w'), indent=4)

def parse_owasp_data():
    prev_data = load_previous_data()
    owasp_data = json.load(open(SRC_FNAME))
    res_data = []
    template_data = {'l1': [], 'l2': [], 'l3': []}

    for req in owasp_data['requirements']:
        new_entry = {'model': 'api.requirement', 'fields': {}}
        new_entry['fields']['owasp_section'] = int(req['Section'][1:])
        new_entry['fields']['readable_id'] = req['Item']
        oid = prev_data.get(req['Item'], str(uuid.uuid4()))

        if 'deleted' in req['Description'].lower():
            continue

        if req['L1'] == 'X':
            new_entry['fields']['owasp_level'] = 1
            template_data['l1'].append(oid)
            template_data['l2'].append(oid)
            template_data['l3'].append(oid)
        elif req['L2'] == 'X':
            new_entry['fields']['owasp_level'] = 2
            template_data['l2'].append(oid)
            template_data['l3'].append(oid)
        else:
            new_entry['fields']['owasp_level'] = 3
            template_data['l3'].append(oid)

        new_entry['fields']['description'] = req['Description']
        new_entry['fields']['oid'] = oid
        res_data.append(new_entry)

    create_template_fixtures(template_data)
    json.dump(res_data, open(DST_FNAME, 'w'), indent=4)





if __name__ == '__main__':
    parse_owasp_data()
    # print(load_previous())
