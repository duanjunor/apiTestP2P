import app

class trustApi():
    hearder = {}
    def __init__(self):
        self.trust_url = app.BASE_URL+"/trust/trust/register"
        self.otherTrustUrl ='http://121.43.169.97:8000/muser/publicRequests'
        self.rechargeUrl = "/common/public/verifycode/{}"
        self.rechargeUrl_money = '/trust/trust/recharge'
    def req_trust_url(self,session):
        response = session.post(self.trust_url)
        return response
    def otherTrust(self,session,data):
        response = session.post(self.trust_url,data=data)
        return response
    def get_recharge_verify_code(self,session,r):
        url =app.BASE_URL+self.rechargeUrl.format(r)
        response = session.get(url)
        return response
    def get_rechargeUrl_money(self,session,data):
        url =app.BASE_URL+self.rechargeUrl_money
        response = session.post(url,data)
        return response
