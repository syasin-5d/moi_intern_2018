import sys
import requests
import json
import copy


class Numeron():
    def __init__(self, level):
        self.level = level
        self.headers = self.get_headers()
        self.game_id = self.get_game_id()
        
    def get_access_token(self):
        f = open("./credentials/credential", "r")
        access_token = f.read()
        f.close()
        return access_token
    
    def get_headers(self):
        access_token = self.get_access_token()
        headers = {'Authorization' : "Bearer " + access_token}
        return headers

    def get_game_id(self):
        r = requests.get("https://apiv2.twitcasting.tv/internships/2018/games?level={0}".format(self.level), headers=self.headers)
        if r.status_code != 200:
            print(r.text)
            sys.exit(1)
        return r.json()['id']

    def post_answer(self, answer):
        answer_endpoint = "https://apiv2.twitcasting.tv/internships/2018/games/{0}".format(self.game_id)
        answer_json = json.dumps({"answer" : str(answer.answer)})
        print("answer : {0}".format(answer.answer))
        r = requests.post(answer_endpoint, headers=self.headers, data=answer_json)
        if r.status_code != 200:
            print(r.text)
            r.raise_for_status()
        print(r.text)
        if r.json()['hit'] is self.level:
            print("conguratulation.")
            sys.exit(0)
        answer.set_status(r.json())


class Answer():
    def __init__(self, answer):
        self.answer = answer
        self.used = [False for x in range(10)] # 0-9のうち、answerが使っている数字はどれか
        self.what_is_blow = [False for x in range(10)] # 0-9のうち、answerに使われている数字(blow)
        self.what_is_hit = [False for x in range(10)] # i 桁目の答えが確定(hit)
        self.hits = 0
        self.blows = 0
        self.set_used()
        
    def set_used(self):
        self.used = [False for x in range(10)]
        for i in self.answer:
            self.used[int(i)] = True
            
    def set_status(self, res_post_ans):
        self.hits = res_post_ans['hit']
        self.blows = res_post_ans['blow']
        
    def __deepcopy__(self, memo):
        new_obj = Answer(self.answer)
        return new_obj 
