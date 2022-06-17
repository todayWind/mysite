import requests


class CmsLogin:

    def __init__(self, method: str, url: str, headers: dict = {}, params: dict = {}, data: dict = {}, json: dict = {}):
        self.method = method
        self.url = url
        self.headers = headers
        self.params = params
        self.data = data
        self.json = json

    def login(self):
        response = requests.request(method=self.method, url=self.url, headers=self.headers, params=self.params,
                                    data=self.data,
                                    json=self.json)
        return response.cookies


cms = CmsLogin('post', 'http://124.220.179.221:8081/cms/manage/loginJump.do',
               data={"userAccount": 'admin', "loginPwd": '123456'})
