import urllib.request
import sys

req = urllib.request.Request("https://resume-yzer-api-ifwuciwwiv.cn-hangzhou.fcapp.run/api/health")
try:
    resp = urllib.request.urlopen(req, timeout=10)
    print("Status:", resp.status)
    print(resp.read().decode())
except urllib.error.HTTPError as e:
    print("Status:", e.code)
    print(e.read().decode())
except Exception as e:
    print("Error:", str(e))
