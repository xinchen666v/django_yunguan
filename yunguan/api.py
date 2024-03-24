"""
EasyDL 图像分类 调用模型公有云API Python3实现
"""

import json

import requests

"""
使用 requests 库发送请求
使用 pip（或者 pip3）检查我的 python3 环境是否安装了该库，执行命令
  pip freeze | grep requests
若返回值为空，则安装该库
  pip install requests
"""


def yun_guan_api(base64_str):
    # 目标图片的 本地文件路径，支持jpg/png/bmp格式

    # 可选的请求参数
    # top_num: 返回的分类数量，不声明的话默认为 6 个
    PARAMS = {"top_num": 2}

    # 服务详情 中的 接口地址
    MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/yunguan"

    # 调用 API 需要 ACCESS_TOKEN。若已有 ACCESS_TOKEN 则于下方填入该字符串
    # 否则，留空 ACCESS_TOKEN，于下方填入 该模型部署的 API_KEY 以及 SECRET_KEY，会自动申请并显示新 ACCESS_TOKEN
    ACCESS_TOKEN = "24.ce37b479efaf6b75e467d5bdccac2033.2592000.1712913247.282335-32591024"
    API_KEY = "o9zZGFihv1WbU6ghSYQXX44z"
    SECRET_KEY = "7kRQ1LOHi5bvEzl2QxuTAhUALAjhFptF"

    PARAMS["image"] = base64_str

    if not ACCESS_TOKEN:
        print("2. ACCESS_TOKEN 为空，调用鉴权接口获取TOKEN")
        auth_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials"               "&client_id={}&client_secret={}".format(
            API_KEY, SECRET_KEY)
        auth_resp = requests.get(auth_url)
        auth_resp_json = auth_resp.json()
        ACCESS_TOKEN = auth_resp_json["access_token"]
        print("新 ACCESS_TOKEN: {}".format(ACCESS_TOKEN))
    else:
        print("2. 使用已有 ACCESS_TOKEN")

    print("3. 向模型接口 'MODEL_API_URL' 发送请求")
    request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
    response = requests.post(url=request_url, json=PARAMS)
    response_json = response.json()
    response_str = json.dumps(response_json, indent=4, ensure_ascii=False)

    # Extract the names of the two highest scores
    log_id = response_json["log_id"]
    results = response_json["results"]

    print("结果:{}".format(response_str))
    print("log_id:", log_id)
    # for result in highest_scores:
    #     if result["score"] > 0.8:
    #         return "name:", result["name"], "score:", result["score"]
    return results
