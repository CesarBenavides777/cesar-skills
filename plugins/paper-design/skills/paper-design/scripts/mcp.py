#!/usr/bin/env python3
"""Minimal MCP streamable-http client for Paper Desktop (127.0.0.1:29979)."""
import json, sys, urllib.request, os
URL="http://127.0.0.1:29979/mcp"
SESS_FILE=os.path.join(os.path.dirname(os.path.abspath(__file__)),".paper_session")
def post(payload, sid=None):
    req=urllib.request.Request(URL,data=json.dumps(payload).encode(),headers={
        "Content-Type":"application/json","Accept":"application/json, text/event-stream",
        **({"Mcp-Session-Id":sid} if sid else {})})
    with urllib.request.urlopen(req, timeout=300) as r:
        sid=r.headers.get("Mcp-Session-Id") or sid
        body=r.read().decode()
    msgs=[]
    for line in body.splitlines():
        if line.startswith("data:"):
            try: msgs.append(json.loads(line[5:].strip()))
            except: pass
    if not msgs:
        try: msgs=[json.loads(body)]
        except: pass
    return sid, msgs
def session():
    if os.path.exists(SESS_FILE):
        return open(SESS_FILE).read().strip() or None
    sid,_=post({"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"claude-code-curl","version":"0"}}})
    post({"jsonrpc":"2.0","method":"notifications/initialized"},sid)
    open(SESS_FILE,"w").write(sid or "")
    return sid
def call(method, params=None):
    sid=session()
    _,msgs=post({"jsonrpc":"2.0","id":1,"method":method,"params":params or {}},sid)
    return msgs
if __name__=="__main__":
    method=sys.argv[1]
    params=json.loads(sys.argv[2]) if len(sys.argv)>2 else {}
    for m in call(method, params):
        if "result" in m:
            r=m["result"]
            if "content" in r:
                for c in r["content"]:
                    print(c.get("text") if c.get("type")=="text" else json.dumps(c)[:2000])
            else:
                print(json.dumps(r,indent=2))
        else:
            print(json.dumps(m,indent=2))
