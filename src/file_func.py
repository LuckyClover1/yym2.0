import json
from src import global_
import os
from src.tklog import Log


def read_json(file):
    file = global_.config_path + file
    Log.debug("读取json文件：", file)
    f = open(file, encoding='utf-8')  # 打开‘product.json’的json文件
    res = f.read()  # 读文件
    return json.loads(res)


def list_config():
    Log.debug("json文件路径：", global_.config_path)
    files = os.listdir(global_.config_path)
    if len(files):
        for file in files:
            if file == "config.json":
                continue
            file_josn = read_json(file)
            global_.config_file_arr.append(file_josn["module_type"])


