import logging

import requests,re
from bs4 import BeautifulSoup


def assert_utils(self,response,status_code,status,desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))

def request_third_api(form_data):
    # 解析form表单中的内容，并提取第三方请求的参数
    #str = e='MerCustId' type='hidden' value='6000060007313892'/><input name='BgRetUrl' type='hidden' value='https://www.baidu.com/'/><input name='RetUrl' type='hidden' value='http://user-p2p-test.itheima.net/trust/chinapnr/register/return/23010511314234145160'/><input name='UsrId' type='hidden' value=''/><input name='UsrName' type='hidden' value=''/><input name='IdType' type='hidden' value='00'/><input name='IdNo' type='hidden' value='340823198807136113'/><input name='UsrMp' type='hidden' value='13033547611'/><input name='UsrEmail' type='hidden' value=''/><input name='MerPriv' type='hidden' value='23010511314234145160'/><input name='ChkValue' type='hidden' value='-101'/><input name='CharSet' type='hidden' value='UTF-8'/></form><script>document.forms['easypaysubmit'].submit();</script>'''
    geshi = "input name='(.*?)' type.*?value='(.*?)'/>"
    r = re.findall(geshi, str(form_data))
    url = re.findall("action='(.*?)'>", str(form_data))[0]
    logging.info(url)
    data = {}
    for x in r:
        key, value = x
        data.setdefault(key, value)
    logging.info(data)
    response = requests.post(url, data=data)
    logging.info(response.text)
    return response
import json
import logging

import requests,pymysql
from bs4 import BeautifulSoup

import app

import base64
import hashlib
import json
import re
import traceback

from Crypto.Cipher import AES

def assert_utils(self,response,status_code,status,desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))

def request_third_api(form_data):
    # 解析form表单中的内容，并提取第三方请求的参数
    soup = BeautifulSoup(form_data, "html.parser")
    third_url = soup.form['action']
    logging.info("third request url = {}".format(third_url))
    data = {}
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value'])
    logging.info("third request data = {}".format(data))
    # 发送第三方请求
    response = requests.post(third_url, data=data)
    return response

class DButils:
    @classmethod
    def get_conn(cls,db_name):
        conn = pymysql.connect(app.DB_URL,app.DB_USERNAME,app.DB_PASSWORD,db_name,autocommit=True)
        return conn

    @classmethod
    def close(cls,cursor=None,conn=None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def delete(cls,db_name,sql):
        try:
            conn = cls.get_conn(db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close(cursor,conn)

def read_imgVerify_data(file_name):
    file = app.BASE_DIR + "/data/" + file_name
    test_case_data = []
    with open(file,encoding="utf-8") as f:
        verify_data = json.load(f)
        test_data_list = verify_data.get("test_get_img_verify_code")
        for test_data in test_data_list:
            test_case_data.append((test_data.get("type"),test_data.get("status_code")))
    print("json data={}".format(test_case_data))
    return test_case_data

def read_register_data(file_name):
    #注册的测试数据的文件路径
    file = app.BASE_DIR + "/data/" + file_name
    test_case_data = []
    with open(file,encoding="utf-8") as f:
        #将json的数据格式，转化为字典的数据格式
        register_data = json.load(f)
        #获取所有的测试数据的列表
        test_data_list = register_data.get("test_register")
        #依次读取测试数据列表中的每一条数据，并进行相应字段的提取
        for test_data in test_data_list:
            test_case_data.append((test_data.get("phone"),test_data.get("pwd"),test_data.get("imgVerifyCode"),test_data.get("phoneCode"),test_data.get("dyServer"),test_data.get("invite_phone"),test_data.get("status_code"),test_data.get("status"),test_data.get("description")))
        print("test_case_data = {}".format(test_data_list))
    return test_case_data

#定义统一的读取所有参数数据文件的方法
def read_param_data(filename,method_name,param_names):
    #filename： 参数数据文件的文件名
    #method_name: 参数数据文件中定义的测试数据列表的名称，如：test_get_img_verify_code
    #param_names: 参数数据文件一组测试数据中所有的参数组成的字符串，如："type,status_code"

    #获取测试数据文件的文件路径
    file = app.BASE_DIR + "/data/" + filename
    test_case_data = []
    with open(file,encoding="utf-8") as f:
        #将json字符串转换为字典格式
        file_data = json.load(f)
        #获取所有的测试数据的列表
        test_data_list = file_data.get(method_name)
        for test_data in test_data_list:
            #先将test_data对应的一组测试数据，全部读取出来，并生成一个列表
            test_params = []
            for param in param_names.split(","):
                #依次获取同一组测试数中每个参数的值，添加到test_params中，形成一个列表
                test_params.append(test_data.get(param))
            #每完成一组测试数据的读取，就添加到test_case_data后，直到所有的测试数据读取完毕
            test_case_data.append(test_params)
    print("test_case_data = {}".format(test_case_data))
    return test_case_data

# 加解密工具类
class EncryptUtil:
    # 发送请求时，加密密码
    SEND_AES_KEY = ";3jm$>/p-ED^cVz_j~.KV&V)k9jn,UAH"
    # 发送请求时，签名密钥
    SEND_SIGN_KEY = "DY34fdgsWET@#$%wg#@4fgd345sg"
    # 接收数据时，解密密钥
    RECEIVE_AES_KEY = "54Ms5bkE6UEdyrRviJ0![OR]g+i79x]k"

    @staticmethod
    def padding_pkcs5(value):
        BS = AES.block_size
        return str.encode(value + (BS - len(value) % BS) * chr(BS - len(value) % BS))

    # 替换空字符
    @staticmethod
    def replace_blank(str_data):
        str_data = re.compile("\t|\r|\n").sub("", str_data)
        print("replace_blank str_data=", str_data)
        return str_data

    @staticmethod
    def aes_encrypt(key, data):
        """
        AES加密
        :param key: 密钥
        :param data: 待加密数据
        :return: 加密后数据
        """
        data = base64.encodebytes(data.encode()).decode()
        # 替换特殊字符
        data = EncryptUtil.replace_blank(data)
        print("data=", data)

        # 初始化加密器
        aes = AES.new(key.encode(), AES.MODE_ECB)

        # 加密
        padding_value = EncryptUtil.padding_pkcs5(data)
        encrypt_aes = aes.encrypt(padding_value)

        # 用base64转成字符串形式
        encrypted_text = base64.encodebytes(encrypt_aes).decode()
        return encrypted_text

    @staticmethod
    def aes_decrypt(key, data):
        """
        AES解密
        :param key: 密钥
        :param data: 待解密数据
        :return: 解密后数据
        """
        # 初始化加密器
        aes = AES.new(key.encode(), AES.MODE_ECB)
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(data.encode())

        # 执行解密
        decrypted_bytes = base64.decodebytes(aes.decrypt(base64_decrypted))
        # 转换为字符串
        decrypted_text = str(decrypted_bytes, encoding="utf-8")

        # 把Unicode转成中文
        result = decrypted_text.encode().decode("unicode_escape")
        return result

    @staticmethod
    def md5value(data):
        print("md5value data=", data)
        md5 = hashlib.md5()
        md5.update(data.encode())
        return md5.hexdigest()

    @staticmethod
    def get_diyou(data):
        # 把字典转换为JSON字符串
        if isinstance(data, dict):
            data = json.dumps(data)
        aes_encrypt_data = EncryptUtil.aes_encrypt(EncryptUtil.SEND_AES_KEY, data)
        return EncryptUtil.replace_blank(aes_encrypt_data)

    @staticmethod
    def get_xmdy(data):
        return EncryptUtil.md5value(
            EncryptUtil.SEND_SIGN_KEY + EncryptUtil.replace_blank(data) + EncryptUtil.SEND_SIGN_KEY)

    @staticmethod
    def decrypt_data(data):
        return EncryptUtil.aes_decrypt(EncryptUtil.RECEIVE_AES_KEY, data)

def encryted_Request(url,req_data):
    # 对数据进行加密
    diyou = EncryptUtil.get_diyou(req_data)
    xmdy = EncryptUtil.get_xmdy(diyou)
    # 发送请求
    req_param = {"diyou": diyou, "xmdy": xmdy}
    response = requests.post(url, data=req_param)
    # 接收响应并解密
    diyou_data = response.json().get("diyou")
    data = EncryptUtil.decrypt_data(diyou_data)
    result = json.loads(data)
    # 返回解密后结果
    return result