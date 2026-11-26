import http.client,json,re
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
BASE={"User-Agent":UA,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"en-US,en;q=0.9","sec-ch-ua":'"Chromium";v="131", "Google Chrome";v="131", "Not_A Brand";v="24"',"sec-ch-ua-mobile":"?0","sec-ch-ua-platform":'"Windows"',"Sec-Fetch-Dest":"document","Sec-Fetch-Mode":"navigate","Sec-Fetch-Site":"none","Upgrade-Insecure-Requests":"1"}
from urllib.parse import urlsplit
def call(method,url,body=None,extra=None):
    p=urlsplit(url); host=p.hostname; port=p.port or 443; path=(p.path or '/')+('?'+p.query if p.query else '')
    h=dict(BASE)
    if extra: h.update(extra)
    try:
        c=http.client.HTTPSConnection(host,port,timeout=40)
        c.request(method,path,body=body,headers=h)
        r=c.getresponse(); b=r.read().decode('utf-8','replace'); hd={k.lower():v for k,v in r.getheaders()}; c.close()
        return r.status,hd,b
    except Exception as e:
        return -1,{},'ERR '+repr(e)
def grep(tag,s):
    for pat in [r'client[_I]d["\']?\s*[:=]\s*["\']([A-Za-z0-9]{20,40})', r'auth-dev\.zuplo\.com', r'zuplo-dev\.us\.auth0\.com', r'AUTH0_CLIENT_ID["\']?\s*[:=]\s*["\']([A-Za-z0-9]{20,40})', r'domain["\']?\s*[:=]\s*["\']([a-z0-9.-]*auth[^"\']*)']:
        for m in re.finditer(pat,s):
            a=max(0,m.start()-80); print(tag,'MATCH',m.group(0)[:120],'::',s[a:m.end()+80].replace('\n',' ')[:260])
for host in ["portal-staging.zuplo.com","portal-dev.zuplo.com","dev-portal-staging.zuplo.com"]:
    st,hd,html=call("GET",f"https://{host}/")
    print(f"=== {host} / ST={st} ct={hd.get('content-type','')} len={len(html)}")
    print("HTML:",html[:400].replace('\n',' '))
    grep(host+"-html",html)
    srcs=re.findall(r'<script[^>]+src=["\']([^"\']+)["\']',html)
    print("scripts:",srcs[:10])
    for s in srcs[:8]:
        u=s if s.startswith('http') else f"https://{host}"+("/"+s.lstrip('/'))
        st2,hd2,js=call("GET",u)
        print(f"  -- {u} ST={st2} len={len(js)}")
        grep(u,js)
    for cfg in ['/config.json','/env.js','/runtime-config.json','/assets/config.json','/.well-known/zuplo.json']:
        st3,hd3,b3=call("GET",f"https://{host}{cfg}")
        if st3==200:
            print(f"  CFG {cfg} ST={st3} len={len(b3)} :: {b3[:250]}")
            grep(cfg,b3)
print("DONE")
