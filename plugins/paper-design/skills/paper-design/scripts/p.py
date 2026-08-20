"""Paper MCP helpers — call-budget-aware.
tool(name, **args) -> (text, images) | write(target, html) -> [created ids]
html(target, html) -> raw text (legacy) | art(name, w, h, **styles) -> artboard id
shot(node, path, scale=1|0.5) -> saves JPEG | ids_of(text) -> created ids
"""
import json, base64, sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import call

def tool(_tool, **args):
    res = call("tools/call", {"name": _tool, "arguments": args})
    texts, imgs = [], []
    for m in res:
        if "error" in m: raise SystemExit("RPC error: " + json.dumps(m["error"]))
        r = m.get("result", {})
        if r.get("isError"): raise SystemExit(f"{_tool} error: " + "".join(c.get('text','') for c in r.get('content',[])))
        for c in r.get("content", []):
            if c.get("type") == "text": texts.append(c["text"])
            elif c.get("type") == "image": imgs.append(c)
    return "\n".join(texts), imgs

def ids_of(text):
    """Created-node ids from a write_html / create_artboard result, in document order."""
    try:
        d = json.loads(text)
        if "createdNodes" in d: return [n["id"] for n in d["createdNodes"]]
        if "id" in d: return [d["id"]]
    except Exception: pass
    return re.findall(r'"id":\s*"([^"]+)"', text)

def art(name, w, h, **styles):
    t, _ = tool("create_artboard", name=name, styles={"width": f"{w}px", "height": f"{h}px", **styles})
    return ids_of(t)[0]

def html(target, h, mode="insert-children"):
    t, _ = tool("write_html", html=h, targetNodeId=target, mode=mode); return t

def write(target, h, mode="insert-children"):
    """Preferred: returns the created ids (root first). Capture these — never re-query the tree."""
    return ids_of(html(target, h, mode))

def shot(node, path, scale=1):
    assert scale in (1, 0.5, 2), "scale 0.6 returns a black image; use 1, 0.5 or 2"
    t, imgs = tool("get_screenshot", nodeId=node, scale=scale)
    if imgs:
        open(path, "wb").write(base64.b64decode(imgs[0]["data"])); print("saved", path)
    else: print(t[:300])
