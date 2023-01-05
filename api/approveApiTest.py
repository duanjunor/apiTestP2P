import unittest
import app
class approve():
    headers = {
        'Content-Type': 'multipart/form-data; boundary=--------------------------824870342576740638076880'
    }
    def __init__(self):
        self.approverealname_url = app.BASE_URL+"/member/realname/approverealname"
        self.getapproveurl_url = app.BASE_URL+'/member/member/getapprove'
    def approverealname(self,session,realname,card_id):
        data = {
            'realname': realname ,#"于海燕"
            'card_id': card_id# "622226198711032526"
        }
        response = session.post(self.approverealname_url,headers = self.headers,data=data,)
        return response
    def getapproveurl(self,session):

        response = session.post(self.getapproveurl_url)
        return response
if __name__ == '__main__':
    a = approve()
    print(a.getapproveurl_url)
    print(a.approverealname_url)