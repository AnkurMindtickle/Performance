import configparser
from locust import HttpUser, HttpLocust, task, TaskSet, between, constant, tag, User
import json

config = configparser.ConfigParser()
config.read('common//config.ini')


def includeexclude(url):
    if config[url]['include'] == 'true':
        return 'tag1'
    else:
        return 'tag2'

class GetApi(TaskSet):

    print(includeexclude('URL1'))
    @tag(includeexclude('URL1'))
    @task(1)
    def get_api(self):
        #self.client.get(config['URL1']['url'])
        with self.client.get(config['URL1']['url'], catch_response=True) as response:
            if "Still" not in response.text:
                print("failed")
                response.failure("Got wrong response")
            else:
                print("success")
                response.success()


class PostApi(TaskSet):
    print("URL2: " + includeexclude('URL2'))

    @tag(includeexclude('URL2'))
    @task(1)
    def post_api(self):
        headers = {'content-type': 'application/json'}
        data = {"users": [
            {"id": "3a7ede5f42d62611", "scope": {"company": "benaam", "entity": "984323340738724425", "version": 1}}],
                "scope": {"company": "benaam"}}
        # response = self.client.post(config['URL2']['url'], data=json.dumps(data),headers=headers)
        with self.client.post(config['URL2']['url'], data=json.dumps(data), headers=headers,
                              catch_response=True) as response:
            json_response = json.loads(response.text)
            print(json_response['users']['3a7ede5f42d62611']['id'])
            if json_response['users']['3a7ede5f42d62611']['id'] != "3a7ede5f42d62611":
                print("failed")
                response.failure("Got wrong response")
            else:
                print("success")
                response.success()


class LoadTest(TaskSet):
    tasks = {GetApi:1,PostApi:5}
    #weight = 1
    #wait_time = constant(1)

class LoadTest1(HttpUser):
    tasks = {LoadTest:1}
    #tasks = {GetApi: 1, PostApi: 5}
    #weight = 1
    wait_time = constant(1)