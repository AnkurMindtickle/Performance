import configparser
from locust import HttpUser, HttpLocust, task, TaskSet, between, constant, tag, User
import json

config = configparser.ConfigParser()
config.read('common//config.ini')
USER_ID=[]
list_id = ["3a7ede5f42d62611","3a7ede5f42d626118"]

def includeexclude(url):
    if config[url]['include'] == 'true':
        return 'tag1'
    else:
        return 'tag2'

class Api(TaskSet):

    print(includeexclude('URL1'))
    @tag(includeexclude('URL1'))
    @task(0)
    def get_api(self):
        #self.client.get(config['URL1']['url'])
        with self.client.get(config['URL1']['url'], catch_response=True) as response:
            if "Still" not in response.text:
                print("failed")
                response.failure("Got wrong response")
            else:
                print("success",self.userid)
                response.success()

    print("URL2: " + includeexclude('URL2'))

    #this section to be used if each locust should have different useid for a list and repeat if list is empty
    '''
    def on_start(self):
        if len(USER_ID) > 0:
            self.userid = USER_ID.pop()
        else:
            for item in list_id:
                USER_ID.append(item)
            self.userid = USER_ID.pop()
    '''


    @tag(includeexclude('URL2'))
    @task(1)
    def post_api(self):
        # this section to be used if a single locust should have different userid for a list and repeat if list is empty
        if len(USER_ID) > 0:
            self.userid = USER_ID.pop()
        else:
            for item in list_id:
                USER_ID.append(item)
            self.userid = USER_ID.pop()

        headers = {'content-type': 'application/json'}
        data = {"users": [
            {"id": self.userid, "scope": {"company": "benaam", "entity": "984323340738724425", "version": 1}}],
                "scope": {"company": "benaam"}}
        # response = self.client.post(config['URL2']['url'], data=json.dumps(data),headers=headers)
        with self.client.post(config['URL2']['url'], data=json.dumps(data), headers=headers,
                              catch_response=True) as response:
            json_response = json.loads(response.text)
            print(self.userid)
            if self.userid not in json_response['users']:
                print("failed")
                response.failure("Got wrong response")
            else:
                print("success")
                response.success()

class LoadTest(HttpUser):
    global USER_ID
    if (len(USER_ID)==0):
        USER_ID=list_id.copy()
    print(list_id)
    tasks = [Api]
    wait_time = constant(1)
    host = "http://um.internal.pikachu.mindtickle.com/"
