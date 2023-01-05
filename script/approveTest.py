import unittest
import logging

import requests

import api.loginAPI
from api import approveApiTest
from utils import assert_utils


class approveT(unittest.TestCase):

    def setUp(self) -> None:
        self.approveApi = approveApiTest.approve()
        self.session = requests.session()
        self.loginApi = api.loginAPI.loginAPI()
    def tearDown(self) -> None:
        self.session.close()
    def test01_success_approve(self):
        resp = self.loginApi.login(self.session)
        logging.info("login = {}".format(resp.json()))
        assert_utils(self,resp, 200, 200, "登录成功")
        realname="王龙生"
        card_id = '340823198807136113'
        resp = self.approveApi.approverealname(self.session,realname,card_id)
        logging.info("approve = {}".format(resp.json()))
        assert_utils(self,resp,200,200,"提交成功!")
    def test02_fail_approve_uername_is_null(self):
        resp = self.loginApi.login(self.session,phone=13468796111,pwd='t123456')
        logging.info("login = {}".format(resp.json()))
        assert_utils(self, resp, 200, 200, "登录成功")
        realname = ""
        card_id = '340823198807136113'
        resp = self.approveApi.approverealname(self.session, realname, card_id)
        logging.info("approve = {}".format(resp.json()))
        assert_utils(self, resp, 200, 100, "姓名不能为空")
    def test03_fail_approve_IdCard_is_null(self):
        resp = self.loginApi.login(self.session,phone=13468796111,pwd='t123456')
        logging.info("login = {}".format(resp.json()))
        assert_utils(self, resp, 200, 200, "登录成功")
        realname = "王龙生"
        card_id = ''
        resp = self.approveApi.approverealname(self.session, realname, card_id)
        logging.info("approve = {}".format(resp.json()))
        assert_utils(self, resp, 200, 100, "身份证号不能为空!")
    def test04_fail_approve_IdCard_had(self):
        resp = self.loginApi.login(self.session)
        logging.info("login = {}".format(resp.json()))
        assert_utils(self, resp, 200, 200, "登录成功")
        realname = "王龙生"
        card_id = '340823198807136113'
        resp = self.approveApi.approverealname(self.session, realname, card_id)
        logging.info("approve = {}".format(resp.json()))
        assert_utils(self, resp, 200, 200, "身份证号已存在!")
    def test05_fail_approve_Idcard_error(self):
        resp = self.loginApi.login(self.session,phone=13468796111,pwd='t123456')
        logging.info("login = {}".format(resp.json()))
        assert_utils(self, resp, 200, 200, "登录成功")
        realname = "王龙生"
        card_id = '34082319880713613'
        resp = self.approveApi.approverealname(self.session, realname, card_id)
        logging.info("approve = {}".format(resp.json()))
        assert_utils(self, resp, 200, 100, "身份证号格式不正确")
    def test06_success_approveSelectTure(self):
        resp = self.loginApi.login(self.session)
        logging.info("login = {}".format(resp.json()))
        assert_utils(self, resp, 200, 200, "登录成功")
        resp = self.approveApi.getapproveurl(self.session)
        logging.info("approve = {}".format(resp.json()))
        self.assertEqual(200,resp.status_code)
    def test07_fail_approveSeletFalse(self):
        resp = self.loginApi.login(self.session, phone=13468796111, pwd='t123456')
        logging.info("login = {}".format(resp.json()))
        assert_utils(self, resp, 200, 200, "登录成功")
        resp = self.approveApi.getapproveurl(self.session)
        logging.info("approve = {}".format(resp.json()))
        self.assertEqual(200, resp.status_code)




