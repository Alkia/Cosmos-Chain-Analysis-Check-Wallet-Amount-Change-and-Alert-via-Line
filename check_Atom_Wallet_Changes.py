import time
import requests
import httpx
import json

api_base_url = "https://node.atomscan.com"
api_path_account = "/cosmos/auth/v1beta1/accounts/"
address_honeypot = "cosmos1fddnfpasamctmnu6a3cfmmz5zs4g74pceweczx"
address_safe = "cosmos1n5ygv5tde32qd5cpjqq5etd72slzj9wxdj3x6g"
address = address_honeypot
Line_Token = "tuma0cgCi9d65lcSU0zNsRMydiLaYD24kjjlhubrLMn"
old_amount = 0
new_amount = 0
mintscanlink = "https://www.mintscan.io/cosmos/account/"
api_path_ballance = "/cosmos/bank/v1beta1/balances/"

def send_Line(msg):
    payload = {'message' : 'Alert change in wallet value! \n' + msg
          ,'notificationDisabled' : False
          , 'stickerPackageId' : '11538'
          , 'stickerId' : '51626498'} # https://developers.line.biz/en/docs/messaging-api/sticker-list/#sticker-definitions
    r = requests.post('https://notify-api.line.me/api/notify'
                , headers={'Authorization' : 'Bearer {}'.format(Line_Token)}
                , params = payload)
    print("Message Sent : " + msg)
    

def check_wallet(address):
    reponse = httpx.get(api_base_url + api_path_ballance + address)
    y = json.loads(reponse.text)
    rep  = y["balances"]
    if len(rep) > 0:
        amount = rep[0]["amount"]
    else :
        amount = "0"
    print("Wallet amount(" + address + ") = " + str(amount))
    return amount

new_amount = check_wallet(address)
if new_amount != old_amount :
    send_Line(" amount(" + address + ") = " + str(new_amount) + "\n" + mintscanlink + address)
    old_amount = new_amount   

while True:
    time.sleep(30)
    new_amount = check_wallet(address)
    if new_amount != old_amount :
        send_Line(" amount(" + address + ") = " + str(new_amount) + "\n" + mintscanlink + address)
        old_amount = new_amount
