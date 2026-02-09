import requests as r
AUTH = ('chiranjib.bhattacharyya@pwc.com','Change@123456')
AEM_BASE = "https://hq.pwc.com/link-index.html"

ret = r.get(AEM_BASE, auth=AUTH)
print(ret.status_code)
