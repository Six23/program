import json
import requests
import webbrowser
from aip import AipSpeech
import playsound

urls = 'http://openapi.tuling123.com/openapi/api/v2'  # 请求地址


def respond(res):
    data_dict = {"reqType": 0,
                 "perception": {
                     "inputText": {
                         "text": res
                     },
                 },
                 "userInfo": {
                     "apiKey": "f763618b26d14d6f9203c1cd5213502a",
                     "userId": "29b9fcaf71a6051b"
                 }
                 }

    result = requests.post(urls, json=data_dict)  # post请求
    content = result.content.decode('utf-8')  # 获取返回结果
    str = json.loads(content)  # 反序列化
    print('One:', str['results'][0]['values']['text'])

    if "我想听歌" in res:
        keywords = input("请输入关键词:")
        WYY_url = "https://music.163.com/#/search/m/?s=" + keywords
        webbrowser.get().open(WYY_url)
    if "我想搜索" in res:
        keywords = input("请输入关键词:")
        BaiDu_url = "https://www.baidu.com/s?wd=" + keywords
        webbrowser.get().open(BaiDu_url)




#
# def Two_speek(say):
#     """我的APPID AK SK"""
#     APP_ID = '19942398'
#     API_KEY = 'jVFGXK0sqBykrQtgEaC3SRGf'
#     SECRET_KEY = 'Ek7gae6yrdIUYEgG5VWhTPAIklIjifSN'
#
#     client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
#     result = client.synthesis(say, 'zh', 1, {
#         'vol': 5,
#         'per': 4,
#     })
#     # 识别正确返回语音二进制 错误则返回dict
#     if not isinstance(result, dict):
#         with open('auido.mp3', 'wb') as f:
#             f.write(result)
#
#     playsound.playsound('auido.mp3')
#
#     Two_speek(str['results'][0]['values']['text'])
    # return result
    # print('Two:',str['results'][0]['values']['text'])


print("主人，你好！我是您的专属AI机器人——One,请问您需要什么帮助？")

while True:
    data = input("你:")
    respond(data)





# 待完善
