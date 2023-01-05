import logging
import unittest
import random
from time import sleep

import requests

from utils import assert_utils
from api.loginAPI import loginAPI


class logintest(unittest.TestCase):
    phone1 = 13147851477
    phone2 = 13147851470
    imgVerifyCode = 8888
    def setUp(self) -> None:
        self.loginAPi = loginAPI()
        self.session = requests.session()
    def tearDown(self) -> None:
        self.session.close()
    def test01_sucess(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session,str(r))
        self.assertEqual(200,resp.status_code)
    def test02_int_getImgCode(self):
        r = random.randint(1,99999)
        resp = self.loginAPi.getImgCode(self.session, str(r))

        self.assertEqual(200, resp.status_code)
    def test03_null_getImgCode(self):
        resp = self.loginAPi.getImgCode(self.session, '')

        self.assertEqual(404, resp.status_code)
    def test04_random_str_getImgCode(self):
        r = random.sample("abcdefghigkmlnokprst",10)
        result = ''.join(r)
        resp = self.loginAPi.getImgCode(self.session, result)
        self.assertEqual(400, resp.status_code)
    def test05_success_smsCode(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session, str(r))
        self.assertEqual(200, resp.status_code)
        resp = self.loginAPi.getSmsCode(self.session,phone=self.phone1,imgVerifyCode=self.imgVerifyCode)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(200, resp.json().get('status'))
        self.assertEqual('短信发送成功', resp.json().get('description'))
    def test06_fail_ImgCode_is_fail(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session, str(r))
        self.assertEqual(200, resp.status_code)
        resp = self.loginAPi.getSmsCode(self.session, phone=self.phone1, imgVerifyCode=6666)# 错误验证码
        assert_utils(self, response=resp, status_code=200, status=100, desc='图片验证码错误')
    def test07_fail_Phone_is_null(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session, str(r))
        self.assertEqual(200, resp.status_code)
        resp = self.loginAPi.getSmsCode(self.session, phone='', imgVerifyCode=self.imgVerifyCode)
        self.assertEqual(200,resp.status_code)
        self.assertEqual(100,resp.json().get('status'))
    def test08_fail_Imgcode_is_Null(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session, str(r))
        self.assertEqual(200, resp.status_code)
        resp = self.loginAPi.getSmsCode(self.session, phone='', imgVerifyCode='')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(100, resp.json().get('status'))
    def test09_success_register_must_parm(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session, str(r))
        self.assertEqual(200, resp.status_code)
        resp = self.loginAPi.getSmsCode(self.session, phone=self.phone1, imgVerifyCode=self.imgVerifyCode)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(200, resp.json().get('status'))
        self.assertEqual('短信发送成功', resp.json().get('description'))
        resp= self.loginAPi.register(self.session,self.phone1,"t123456",imgVerifyCode=self.imgVerifyCode,phoneCode='666666',dyServer='on')
        assert_utils(self, response=resp, status_code=200, status=200, desc='注册成功')
    def test10_success_register_all_parm(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session, str(r))
        self.assertEqual(200, resp.status_code)
        resp = self.loginAPi.getSmsCode(self.session, phone=13259849647, imgVerifyCode=self.imgVerifyCode)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(200, resp.json().get('status'))
        self.assertEqual('短信发送成功', resp.json().get('description'))
        resp = self.loginAPi.register(self.session, 13259849647, "t123456", imgVerifyCode=self.imgVerifyCode, phoneCode='666666',
                                      dyServer='on',invite_phone="13800002222")
        logging.info("get sms code response = {}".format(resp.json()))
        assert_utils(self, response=resp, status_code=200, status=200, desc='注册成功')
    def test11_fail_register_errorIMg(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session, str(r))
        self.assertEqual(200, resp.status_code)
        resp = self.loginAPi.getSmsCode(self.session, phone=self.phone1, imgVerifyCode=self.imgVerifyCode)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(200, resp.json().get('status'))
        self.assertEqual('短信发送成功', resp.json().get('description'))
        resp = self.loginAPi.register(self.session, self.phone1, "t123456", imgVerifyCode="66666", phoneCode='666666',
                                      dyServer='on')
        logging.info("get sms code response = {}".format(resp.json()))
        assert_utils(self, response=resp, status_code=200, status=100, desc='验证码错误!')

    def test12_fail_register_errorSms(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session, str(r))
        self.assertEqual(200, resp.status_code)
        resp = self.loginAPi.getSmsCode(self.session, phone=self.phone1, imgVerifyCode=self.imgVerifyCode)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(200, resp.json().get('status'))
        self.assertEqual('短信发送成功', resp.json().get('description'))
        resp = self.loginAPi.register(self.session, self.phone1, "t123456", imgVerifyCode=self.imgVerifyCode, phoneCode='888888',
                                      dyServer='on')
        logging.info("get sms code response = {}".format(resp.json()))
        assert_utils(self, response=resp, status_code=200, status=100, desc='验证码错误')
    def test13_fail_register_phone_is_had(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session, str(r))
        self.assertEqual(200, resp.status_code)
        resp = self.loginAPi.getSmsCode(self.session, phone=self.phone1, imgVerifyCode=self.imgVerifyCode)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(200, resp.json().get('status'))
        self.assertEqual('短信发送成功', resp.json().get('description'))
        resp = self.loginAPi.register(self.session, self.phone1, "t123456", imgVerifyCode=self.imgVerifyCode, phoneCode='666666',
                                      dyServer='on')
        assert_utils(self, response=resp, status_code=200, status=100, desc='手机已存在!')
    def test14_fail_register_password_is_null(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session, str(r))
        self.assertEqual(200, resp.status_code)
        resp = self.loginAPi.getSmsCode(self.session, phone=13478486480, imgVerifyCode=self.imgVerifyCode)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(200, resp.json().get('status'))
        self.assertEqual('短信发送成功', resp.json().get('description'))
        resp = self.loginAPi.register(self.session, 13478486480, "", imgVerifyCode=self.imgVerifyCode, phoneCode='666666',
                                      dyServer='on')
        logging.info("get sms code response = {}".format(resp.json()))
        assert_utils(self, response=resp, status_code=200, status=100, desc='密码不能为空')
    def test15_fail_register_dy_server_is_off(self):
        r = random.random()
        resp = self.loginAPi.getImgCode(self.session, str(r))
        self.assertEqual(200, resp.status_code)
        resp = self.loginAPi.getSmsCode(self.session, phone=14786541247, imgVerifyCode=self.imgVerifyCode)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(200, resp.json().get('status'))
        self.assertEqual('短信发送成功', resp.json().get('description'))
        resp = self.loginAPi.register(self.session, 14786541247, "t123456", imgVerifyCode=self.imgVerifyCode, phoneCode='666666',
                                      dyServer='off')
        logging.info("get sms code response = {}".format(resp.json()))
        assert_utils(self, response=resp, status_code=200, status=100, desc='请同意我们的条款')
    def test16_success_login(self):
        resp = self.loginAPi.login(self.session,self.phone1,pwd='t123456')
        logging.info("get sms code response = {}".format(resp.json()))
        assert_utils(self, response=resp, status_code=200, status=200, desc='登录成功')
    def test17_fail_login_usrname_is_not_had(self):
        resp = self.loginAPi.login(self.session, 11111211112, pwd='t123456')
        logging.info("get sms code response = {}".format(resp.json()))
        assert_utils(self, response=resp, status_code=200, status=100, desc='用户不存在')
    def test18_fail_login_password_is_null(self):
        resp = self.loginAPi.login(self.session, self.phone1, pwd='')
        logging.info("get sms code response = {}".format(resp.json()))
        assert_utils(self, response=resp, status_code=200, status=100, desc='密码不能为空')
    def test19_fail_login_passwordError(self):
        resp = self.loginAPi.login(self.session, self.phone1, pwd='t123457')
        logging.info("get sms code response = {}".format(resp.json()))
        assert_utils(self, response=resp, status_code=200, status=100, desc='密码错误1次,达到3次将锁定账户')

        resp = self.loginAPi.login(self.session, self.phone1, pwd='t123457')
        logging.info("get sms code response = {}".format(resp.json()))
        assert_utils(self, response=resp, status_code=200, status=100, desc='密码错误2次,达到3次将锁定账户')

        resp = self.loginAPi.login(self.session, self.phone1, pwd='t123457')
        logging.info("get sms code response = {}".format(resp.json()))
        assert_utils(self, response=resp, status_code=200, status=100, desc='由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录')
        sleep(60)
        def test23_select_successLogin(self):
            resp = self.loginAPi.login(self.session, self.phone1, pwd='t123456')
            logging.info("get sms code response = {}".format(resp.json()))
            assert_utils(self, response=resp, status_code=200, status=200, desc='登录成功')
    # def test22_fail_login_passwordError_lock(self):
    #     pass
    # def test23_select_successLogin(self):
    #     resp = self.loginAPi.login(self.session, self.phone1, pwd='t123456')
    #     logging.info("get sms code response = {}".format(resp.json()))
    #     assert_utils(self, response=resp, status_code=200, status=200, desc='登录成功')
    # def test_select_faillogin(self):
    #     pass

