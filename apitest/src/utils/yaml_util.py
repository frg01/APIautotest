import yaml

#通过文件名获取yaml文件中的数据
def read_yaml(file_path:str,key:str):
    """
    返回字典格式
    :param file_path: YAML文件的路径
    :return: YAML文件中的数据
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        #获取指定键对应的数据
        key_data = data.get(key,{})
        #将每个用例放入列表中
        test_cases = list(key_data.values())

    return test_cases





if __name__ == '__main__':
    # users = read_yaml('D:/project/pythonProject/APIautotest/apitest/src/data/users.yaml')
    # print(users)

    users2 = read_yaml('D:/project/pythonProject/APIautotest/apitest/src/data/users.yaml','users')
    print(isinstance(users2,str),users2[0].get("url"))