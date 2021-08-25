from pywidevine.decrypt.wvdecrypt import WvDecrypt
import requests
import base64
import binascii
import argparse


parser = argparse.ArgumentParser() 
parser.add_argument('-p', action='store', dest='pssh',  type=str, required=True)
parser.add_argument('-l', action='store', dest='lic',  type=str, required=True)
args = parser.parse_args()

# headers={}
# pssh='AAAAp3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAAIcSEFF0U4YtQlb9i61PWEIgBNcSEPCTfpp3yFXwptQ4ZMXZ82USEE1LDKJawVjwucGYPFF+4rUSEJAqBRprNlaurBkm/A9dkjISECZHD0KW1F0Eqbq7RC4WmAAaDXdpZGV2aW5lX3Rlc3QiFnNoYWthX2NlYzViZmY1ZGM0MGRkYzlI49yVmwY='
# license_url='https://cwip-shaka-proxy.appspot.com/no_auth'

#vmp test 
pssh=args.pssh
license_url=args.lic
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

cert=requests.post(license_url,b'\x08\x04').content

wvdecrypt = WvDecrypt(pssh)

wvdecrypt.set_certificate(base64.b64encode(cert))

challenge = wvdecrypt.get_challenge()

license=requests.post(license_url,challenge,headers=headers).content

wvdecrypt.update_license(base64.b64encode(license))

keys=wvdecrypt.start_process()

for k in keys:
    print(k)
