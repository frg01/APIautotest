import os,sys

import allure

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest,requests,allure_pytest,bs4
import re
from ..utils.yaml_util import get_data_from_yaml

test_case_url = 'D:/project/pythonProject/APIautotest/apitest/src/data/users.yaml','users'



class TestAPI():


    def setup_class(self):
        pass


    @pytest.fixture()
    def setup_teardown(self):
        print("============测试用例开始==========")
        yield
        print("============测试用例结束===========")


    def teardown_class(self):
        pass



    @pytest.mark.parametrize('each_case',get_data_from_yaml('D:/project/pythonProject/APIautotest/apitest/src/data/users.yaml','users'))
    def test_api_request(self,each_case):

        """
        对参数化数据进行解析,由于each_case是一个列表，所以我们进行遍历解析
        """
        print(each_case)
        for x in range(0,len(each_case)):
            each = each_case[x]

            url = each.get('url')
            method = each.get('method')
            headers = each.get('headers')
            params = each.get('params')
            data = each.get('data')
            json = each.get('json')
            num_attempts = each.get('num_attempts')
            expected_result = each.get('expected_result')

            self._api_request(url=url,method=method,headers=headers,params=params,data=data,json=json,num_attempts=num_attempts,expected_result=expected_result)




    #请求和断言的函数
    def _api_request(self,url,method='GET',headers=None,params=None,data=None,json=None,num_attempts=1,expected_result=200):
        """
            :param url: API 的 URL
            :param method: 请求方法，默认为 'GET'
            :param headers: 请求头部信息，可为 None  (requests默认接收字典)
            :param params: 请求的 URL 参数，可为 None   (requests默认接收字典)
            :param data: 请求的表单数据，可为 None
            :param json: 请求的 JSON 数据，可为 None
            :param num_attempts: 请求重试次数，默认为 1
            :param expected_result: 预期 HTTP请求返回的结果，数字去判断状态码 默认为 200，其他情况下使用正则表达式去判断请求体中匹配成功的信息
                    这里的正则匹配限制较为宽泛，所以要注意预期结果的填写，不要能匹配到多个，断言会失准
            :return: API 响应对象
        """

        expected_result_match_reg = '.*'+ expected_result + '.*'

        for attempt in range(num_attempts):
            request_params = {
                'url': url,
                'method': method,
                'headers': headers,
                'params': params,
                'data': data,
                'json': json
            }

            allure.attach("发送请求,请求参数为：", request_params)
            # 发送请求
            response = requests.request(request_params)


            #先取出expected_result
            expected_result = request_params.get('expected_result')

            #判断expected_result是否为
            if expected_result.isdigit():
                allure.attach("请求完成,response状态码为：",response.status_code,"期望状态码：",expected_result)
                assert response.status_code == expected_result
            else:
                body = response.text
                if re.match(expected_result_match_reg,body) != None:
                    allure.attach("断言成功,得到结果 -> ", expected_result)
                else:
                    allure.attach("断言失败,得不到结果 -> ", expected_result)
                assert re.match(expected_result_match_reg,body) != None

