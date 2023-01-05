import random
import unittest
import logging

import requests,re

import utils
from api import loginAPI, TrustTestApi

from api import approveApiTest
from utils import assert_utils
class trusttest(unittest.TestCase):
    def setUp(self) -> None:
        self.loginApi =loginAPI.loginAPI()
        self.session = requests.session()
        self.trustapi = TrustTestApi.trustApi()
    def tearDown(self) -> None:
        self.session.close()
    def test01_success_trust(self):
        response = self.loginApi.login(self.session)
        # logging.info("login",response.json())
        assert_utils(self,response,200,200,'登录成功')
        response = self.trustapi.req_trust_url(self.session)
        data = response.json()['description']['form']
        logging.info("login:{}".format(data))
        self.assertEqual(200,response.status_code)
        logging.info('data：{}'.format(data))
        response = utils.request_third_api(data)
        logging.info('response：{}'.format(response.text))
        self.assertEqual('UserRegister OK',response.text)
    def test02_success_recharge_verify_code(self):
        response = self.loginApi.login(self.session)
        assert_utils(self, response, 200, 200, '登录成功')
        r = random.random()
        logging.info(r)
        response = self.trustapi.get_recharge_verify_code(self.session,r)
        self.assertEqual(200,response.status_code)
    def test03_success_reacharge_verify_code_int(self):
        response = self.loginApi.login(self.session)
        assert_utils(self, response, 200, 200, '登录成功')
        r = random.randint(1,99999)
        logging.info(r)
        response = self.trustapi.get_recharge_verify_code(self.session, r)
        self.assertEqual(200, response.status_code)
    def test04_fail_recharge_veriify_code_isNull(self):
        response = self.loginApi.login(self.session)
        assert_utils(self, response, 200, 200, '登录成功')
        r = ''
        logging.info(r)
        response = self.trustapi.get_recharge_verify_code(self.session, r)
        self.assertEqual(404, response.status_code)
    def test05_fail_recharge_verify_code_isStr(self):
        response = self.loginApi.login(self.session)
        assert_utils(self, response, 200, 200, '登录成功')
        r = random.sample("abcdefghijg",5)
        r = "".join(r)
        logging.info(r)
        response = self.trustapi.get_recharge_verify_code(self.session, r)
        self.assertEqual(400, response.status_code)
    def test06_success_recharge(self):
        response = self.loginApi.login(self.session)
        assert_utils(self, response, 200, 200, '登录成功')
        r = random.random()
        logging.info(r)
        response = self.trustapi.get_recharge_verify_code(self.session, r)
        self.assertEqual(200, response.status_code)
        data = {'paymentType':"chinapnrTrust",
                    'amount':"10000",
                    'formStr':"reForm",
                    'valicode':"8888"}
        response = self.trustapi.get_rechargeUrl_money(self.session,data)
        data = response.json()['description']['form']
        logging.info(response.json()['description']['form'])
        self.assertEqual(200,response.status_code)
        response = utils.request_third_api(data)
        self.assertEqual('NetSave OK',response.text)
    def test07_fail_recharge_codeError(self):
        response = self.loginApi.login(self.session)
        assert_utils(self, response, 200, 200, '登录成功')
        r = random.random()
        logging.info(r)
        response = self.trustapi.get_recharge_verify_code(self.session, r)
        self.assertEqual(200, response.status_code)
        data = {'paymentType': "chinapnrTrust",
                'amount': "10000",
                'formStr': "reForm",
                'valicode': "8889"}
        response = self.trustapi.get_rechargeUrl_money(self.session, data)
        logging.info(response.json())
        utils.assert_utils(self,response,200,100,'验证码错误')
