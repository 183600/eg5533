import http.client,json
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
BASE={"User-Agent":UA,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8","Accept-Language":"en-US,en;q=0.9","sec-ch-ua":'"Chromium";v="131", "Google Chrome";v="131", "Not_A Brand";v="24"',"sec-ch-ua-mobile":"?0","sec-ch-ua-platform":'"Windows"',"Sec-Fetch-Dest":"document","Sec-Fetch-Mode":"navigate","Sec-Fetch-Site":"none","Sec-Fetch-User":"?1","Upgrade-Insecure-Requests":"1"}
from urllib.parse import urlsplit
def call(method,url,body=None,extra=None):
    p=urlsplit(url); host=p.hostname; port=p.port or 443; path=(p.path or '/')+('?'+p.query if p.query else '')
    h=dict(BASE)
    if extra: h.update(extra)
    try:
        c=http.client.HTTPSConnection(host,port,timeout=40); c.request(method,path,body=body,headers=h)
        r=c.getresponse(); b=r.read().decode('utf-8','replace'); hd={k.lower():v for k,v in r.getheaders()}; c.close()
        return r.status,hd,b
    except Exception as e: return -1,{},'ERR '+repr(e)
reg={"client_name":"probe5533","redirect_uris":["http://localhost:8777/callback"],"grant_types":["password","authorization_code","refresh_token","urn:ietf:params:oauth:grant-type:device_code"],"token_endpoint_auth_method":"client_secret_post","application_type":"native"}
tests=[
 ("GET","https://auth-dev.zuplo.com/.well-known/openid-configuration",None,None),
 ("POST","https://auth-dev.zuplo.com/dbconnections/signup",json.dumps({"email":"eg5533b@example.com","password":"Xk9#mPq2!vLr7wZt","connection":"Username-Password-Authentication"}),{"content-type":"application/json","accept":"application/json"}),
 ("POST","https://auth-dev.zuplo.com/oidc/register",json.dumps(reg),{"content-type":"application/json","accept":"application/json"}),
 ("GET","https://management-api-staging.self-staging.zuplo.com/v1/health",None,None),
 ("GET","https://management-api-staging.self-staging.zuplo.com/v1/accounts",None,None),
 ("GET","https://management-api-staging.self-staging.zuplo.com/__zuplo/ping",None,None),
 ("GET","https://api.self-staging.zuplo.com/v1/health",None,None),
 ("GET","https://api.self-staging.zuplo.com/v1/who-am-i",None,None),
]
for m,u,b,e in tests:
    st,hd,body=call(m,u,b,e)
    print("===%s %s==="%(m,u)); print("ST=%s ct=%s loc=%s"%(st,hd.get('content-type',''),hd.get('location','')[:100]))
    print("BODY:",body[:700].replace("\n"," "))
    print()
print("DONE")
