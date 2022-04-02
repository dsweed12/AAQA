import requests, math
from time import sleep
from datetime import date


def get_aa_id():
    req = f"{URL}/get_projects"
    try:
        r = requests.get(req, params=None, auth=AUTH, headers=header, verify=True)
        if r.status_code == 429:
            wait_amount = int(r.headers['Retry-After'])
            sleep(wait_amount)
            raise Exception("Too many API requests")
        if r.status_code == 503:
            raise Exception("Service Temporarily Unavailable")
        if r.status_code == 200:
            response = r.json()
            projects = response['projects']
            for p in projects:
                if p['name'] == "Automation Anywhere":
                    return p['id']
    except Exception as e:
        print(e)


# def implement_plan():
#     plan_xml = open("AAQA_TEST.xml", 'r').read()


def add_run(project_id):
    req = f'{URL}/add_run/{project_id}'
    run = {
        "suite_id": 32,
        "name": f"Staging Regression {date.today()}",
        "include_all": True,
    }
    try:
        r = requests.post(req, json=run, auth=AUTH, verify=True)
        if r.status_code == 429:
            wait_amount = int(r.headers['Retry-After'])
            sleep(wait_amount)
            raise Exception("Too many API requests")
        if r.status_code == 503:
            raise Exception("Service Temporarily Unavailable")
        if r.status_code == 200:
            print(f"successfully created new run to 'Automation Anywheres' (id: {project_id}] )")
            return r
    except Exception as e:
        print(e)


def modify_run(r):
    run_id = r.json()['id']
    tests_to_perform = r.json()['untested_count']
    offset = 0
    cycles = math.ceil(tests_to_perform / 250)

    print("creating run...")
    while tests_to_perform > 0:
        try:
            r = requests.get(f"{URL}/get_tests/{run_id}&offset={offset}", params=None, auth=AUTH, headers=header,verify=True)
            tests = r.json()['tests']
            results = {'results': [{"test_id": x['id'], "custom_preconds": x["custom_preconds"]} for x in tests]}
            for res in results['results']:
                if res["custom_preconds"] == "This test cannot be tested in the current test plan (will be marked " \
                         "'Blocked' on the test run":
                    res['status_id'] = 2
                else:
                    res['status_id'] = 1

            req = f"{URL}/add_results/{run_id}"
            try:
                print(f"Writing - {math.floor(offset / 250) + 1}/{cycles} √")
                r = requests.post(req, json=results, auth=AUTH, verify=True)
                if r.status_code == 429:
                    wait_amount = int(r.headers['Retry-After'])
                    sleep(wait_amount)
                    raise Exception("Too many API requests")
                if r.status_code == 503:
                    raise Exception("Service Temporarily Unavailable")
                if r.status_code == 200:
                    r = requests.get(f"{URL}/get_run/{run_id}", params=None, auth=AUTH, headers=header,verify=True)
                    tests_to_perform = r.json()['untested_count']
                    if tests_to_perform > 0:
                        offset += 250
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)


config = dict(email='****', key='*****',
              url='****')
api_path = '/index.php?/api/v2'
AUTH = (config['email'], config['key'])
URL = f"https://{config['url']}{api_path}"
header = {'Content-Type': 'application/json'}

#modify_run(add_run(get_aa_id()))
modify_run(add_run(12)) # for Mcafee
