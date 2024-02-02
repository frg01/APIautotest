import yaml

#通过文件名获取yaml文件中的数据
def read_yaml(file_path):
    """
    返回字典格式
    :param file_path: YAML文件的路径
    :return: YAML文件中的数据
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

#通过文件名和关键字获取yaml文件中的数据
def get_data_from_yaml(file_path, key):
    """
    从YAML文件中获取指定键的数据
    :param file_path: YAML文件的路径
    :param key: 要获取的数据的键
    :return: 对应键的数据
    """
    yaml_data = read_yaml(file_path).get("users")
    return yaml_data





if __name__ == '__main__':
    # users = read_yaml('D:/project/pythonProject/APIautotest/apitest/src/data/users.yaml')
    # print(users)

    users2 = get_data_from_yaml('D:/project/pythonProject/APIautotest/apitest/src/data/users.yaml','users')
    print(users2)