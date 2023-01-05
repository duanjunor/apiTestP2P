import re
str = '''<form name='easypaysubmit' id='easypaysubmit' target='_blank' method='post' action='http://121.43.169.97:8000/muser/publicRequests'><input name='Version' type='hidden' value='10'/><input name='CmdId' type='hidden' value='UserRegister'/><input name='MerCustId' type='hidden' value='6000060007313892'/><input name='BgRetUrl' type='hidden' value='https://www.baidu.com/'/><input name='RetUrl' type='hidden' value='http://user-p2p-test.itheima.net/trust/chinapnr/register/return/23010511314234145160'/><input name='UsrId' type='hidden' value=''/><input name='UsrName' type='hidden' value=''/><input name='IdType' type='hidden' value='00'/><input name='IdNo' type='hidden' value='340823198807136113'/><input name='UsrMp' type='hidden' value='13033547611'/><input name='UsrEmail' type='hidden' value=''/><input name='MerPriv' type='hidden' value='23010511314234145160'/><input name='ChkValue' type='hidden' value='-101'/><input name='CharSet' type='hidden' value='UTF-8'/></form><script>document.forms['easypaysubmit'].submit();</script>'''
geshi = "input name='(.*?)' type.*?value='(.*?)'/>"
r = re.findall(geshi, str)
url = re.findall("action='(.*?)'>", str)[0]
print(url)
data = {}
for x in r:
    key, value = x
    data.setdefault(key,value)
print(data)
import requests
response = requests.post(url,data=data)
print(response.text)