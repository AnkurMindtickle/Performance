import configparser
from locust import HttpUser, task, between , constant, tag
import json


config = configparser.ConfigParser()
config.read('common//config.ini')

class Api(HttpUser):
    wait_time = constant(1)
    if config['URL1']['include']=='true':
        tag_value = 'tag1'
    else:
        tag_value = 'tag2'
    @tag(tag_value)
    @task(1)
    def first_api(self):
        #self.client.get(config['URL1']['url'])
        with self.client.get(config['URL1']['url'], catch_response=True) as response:
            if "Still" not in response.text:
                print("failed")
                response.failure("Got wrong response")
            else:
                print("success")
                response.success()

    if config['URL2']['include']=='true':
        tag_value = 'tag1'
    else:
        tag_value = 'tag2'

    @tag(tag_value)
    @task(1)
    def view_item(self):
        headers = {'content-type': 'application/json'}
        data = {"users": [{"id": "3a7ede5f42d62611", "scope": {"company": "benaam", "entity": "984323340738724425", "version": 1}}],"scope": {"company": "benaam"}}
        #response = self.client.post(config['URL2']['url'], data=json.dumps(data),headers=headers)
        with self.client.post(config['URL2']['url'], data=json.dumps(data),headers=headers, catch_response=True) as response:
            json_response = json.loads(response.text)
            print(json_response['users']['3a7ede5f42d62611']['id'])
            if json_response['users']['3a7ede5f42d62611']['id'] != "3a7ede5f42d62611":
                print("failed")
                response.failure("Got wrong response")
            else:
                print("success")
                response.success()
        #print(response.text)
        #a = response.text
