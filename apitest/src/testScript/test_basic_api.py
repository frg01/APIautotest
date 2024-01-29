import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest,requests,allure_pytest,bs4
import re








def api_request(url,method='GET',headers=None,params=None,data=None,json=None,num_attempts=1,expected_result=200):
    """
        :param url: API 的 URL
        :param method: 请求方法，默认为 'GET'
        :param headers: 请求头部信息，可为 None
        :param params: 请求的 URL 参数，可为 None
        :param data: 请求的表单数据，可为 None
        :param json: 请求的 JSON 数据，可为 None
        :param num_attempts: 请求重试次数，默认为 1
        :param expected_result: 预期 HTTP请求返回的结果，数字去判断状态码 默认为 200，其他情况下使用正则表达式去判断请求体中匹配成功的信息
        :return: API 响应对象
    """
    for attempt in range(num_attempts):
        request_params = {
            'url': url,
            'method': method,
            'headers': headers,
            'params': params,
            'data': data,
            'json': json
        }

        # 发送请求
        response = requests.request(request_params)

        #先取出expected_result
        expected_result = request_params.get('expected_result')

        if expected_result.isdigit():
            assert response.status_code == expected_result
        else:
            body = response.text
            assert re.match(expected_result,body) != None