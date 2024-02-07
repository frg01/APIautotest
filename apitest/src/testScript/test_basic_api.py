import os,sys

import allure
import allure_commons.types
import logging


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
import requests,allure_pytest
import re

from bs4 import BeautifulSoup
from ..utils.yaml_util import read_yaml

test_case_url = 'D:/project/pythonProject/APIautotest/apitest/src/data/users.yaml','users'



class TestAPI():


    def setup_class(self):
        pass


    @pytest.fixture()
    def setup_teardown(self,each_case):
        print(f'\n============测试接口{each_case.get("url")}开始，执行{each_case.get("num_attempts")}次==========')
        yield
        print("\n============测试用例结束===========")


    def teardown_class(self):
        pass


    @pytest.mark.xfail #这个装饰器的使用可以让pytest在断言失败后不去报告大量的失败信息
    @pytest.mark.demo
    @pytest.mark.parametrize('each_case',read_yaml('D:/project/pythonProject/APIautotest/apitest/src/data/users.yaml','users'))
    def test_api_request(self,each_case,setup_teardown):
        """
        对参数化数据进行解析,由于each_case是一个字典，setup_teardown时一个夹具，
        在参数化的过程中，只需要将each_case,setup_teardown一起传入，夹具会自己去找each_case传入夹具执行
        """

        self._api_request(**each_case)




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


        for attempt in range(num_attempts):

            request_params = {
                "method": method,
                "url": url,
                "headers": headers,
                "params": params,
                "data": data,
                "json": json
            }

            allure.attach("发送请求,请求参数为：", request_params)
            # 发送请求
            response = requests.request(**request_params)
            # 设置返回结果编码，防止中文乱码
            response.encoding = "utf-8"


            # 判断是返回的是html还是json
            content_type = response.headers.get('Content-Type', '').lower()

            #下面进行接口返回四种情况的处理及断言，状态码、json、html、其他
            body = response.text

            #判断expected_result是否为数字
            if isinstance(expected_result,int):
                allure.attach("请求响应,response状态码为：",response.status_code,"期望状态码：",expected_result)
                print(f"第{attempt+1}次请求响应,response状态码为：",response.status_code,"期望状态码：",expected_result)
                assert response.status_code == expected_result
            elif 'json' in content_type:
                # 判断expected_result是否在json字符串中
                json_data = response.json()
                allure.attach(f"在JOSN中查找字符串：'{expected_result}'",json_data,attachment_type=allure_commons.types.AttachmentType.JSON)
                print(f"第{attempt+1}次请求响应,期望结果：",expected_result,"是否找到：",expected_result in json.dumps(json_data))
                assert expected_result in json.dumps(json_data)
            elif 'html' in content_type:
                #使用bs4对html进行解析
                soup = BeautifulSoup(body,'html.parser')
                found_element = soup.find(text=re.compile(expected_result))
                allure.attach(f"在HTML中查找字符串：'{expected_result}'", body,
                              attachment_type=allure_commons.types.AttachmentType.HTML)
                print(f"第{attempt+1}次请求响应,期望结果:", expected_result, "是否找到:",found_element is not None)
                assert found_element is not None, f"在HTML中未找到包含 '{expected_result}' 的元素"
            # elif response.status_code >= 400:
            #     allure.attach("请求失败，response状态码为：",response.status_code)
            #     print(f"第{attempt+1}次请求响应请求失败，状态码",response.status_code)
            #     assert False,f"请求失败，response状态码为{response.status_code}"
            else:
                print(f"第{attempt+1}次请求,响应状态码",response.status_code)









