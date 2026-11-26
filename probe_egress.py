import http.client, json, ssl
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
BASE={"User-Agent":UA,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8","Accept-Language":"en-US,en;q=0.9","sec-ch-ua":'"Chromium";v="131", "Google Chrome";v="131", "Not_A Brand";v="24"',"sec-ch-ua-mobile":"?0","sec-ch-ua-platform":'"Windows"',"Sec-Fetch-Dest":"document","Sec-Fetch-Mode":"navigate","Sec-Fetch-Site":"none","Sec-Fetch-User":"?1","Upgrade-Insecure-Requests":"1"}
def call(method,url,body=None,extra=None):
    from urllib.parse import urlsplit
    p=urlsplit(url); host=p.hostname; port=p.port or 443
    path=p.path or '/'
    if p.query: path+='?'+p.query
    h=dict(BASE)
    if extra: h.update(extra)
    try:
        c=http.client.HTTPSConnection(host,port,timeout=30)
        c.request(method,path,body=body,headers=h)
        r=c.getresponse(); b=r.read().decode('utf-8','replace'); hd={k.lower():v for k,v in r.getheaders()}
        c.close(); return r.status,hd,b
    except Exception as e:
        return -1,{},'ERR '+repr(e)
tests=[
 ("GET","https://auth-dev.zuplo.com/.well-known/openid-configuration",None,None),
 ("GET","https://auth-dev.zuplo.com/authorize?client_id=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&response_type=code&redirect_uri=http%3A%2F%2Flocalhost&scope=openid",None,None),
 ("POST","https://auth-dev.zuplo.com/dbconnections/signup",json.dumps({"email":"eg5533@example.com","password":"Xk9#mPq2!vLr7wZt","connection":"Username-Password-Authentication"}),{"content-type":"application/json"}),
 ("GET","https://dev-agent-z.zuplo.com/health",None,None),
 ("GET","https://dev-agent-z.zuplo.com/.well-known/agent-card.json",None,None),
 ("GET","https://management-api-main.self-staging.zuplo.com/v1/health",None,None),
 ("GET","https://management-api-main.self-staging.zuplo.com/v1/accounts",None,None),
 ("GET","https://api.self-staging.zuplo.com/__zuplo/ping",None,None),
 ("GET","https://api.self-staging.zuplo.com/__zuplo/build",None,None),
 ("GET","https://auth.zuplo.com/.well-known/openid-configuration",None,None),
 ("GET","https://dev.zuplo.com/__zuplo/build",None,None),
 ("GET","https://zuplo-dev.us.auth0.com/.well-known/openid-configuration",None,None),
]
for m,u,b,e in tests:
    st,hd,body=call(m,u,b,e)
    print("===%s %s==="%(m,u))
    print("ST=%s server=%s ct=%s loc=%s cfray=%s"%(st,hd.get('server',''),hd.get('content-type',''),hd.get('location','')[:120],hd.get('cf-ray','')))
    print("BODY:",body[:400].replace("\n"," "))
    print()
print("DONE")
