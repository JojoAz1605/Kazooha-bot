import requests
a = """a











































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































<@957719559903784961>





















































































































































































































































































































































































































































































































































































































































































































































































































































































b
"""
url = "https://discord.com/api/webhooks/1119245963073159251/q49Y4pyb9BkHDB51jDeixR6FKjPIVo_2ubjeT_PLYuvVQPw8oI2r5d0gjWV8tf6BOvIq"  # webhook url, from here: https://i.imgur.com/f9XnAew.png
url2 = "https://discord.com/api/webhooks/1120796686164443287/6UB9WryxwCb0HIFAvrrJHQ1TcvQuiqRHXLLJg6xqMZWp-GH7YPnORrBKxk_eKrDqgO-y"

data = {"content": f"{a}", "username": "custom username", "embeds": [
    {
        "description": "text in embed",
        "title": "embed title"
    }
]}

data2 = {"content": f"{a}", "username": "J'aime faire chier"}

result = requests.post(url2, json=data2)