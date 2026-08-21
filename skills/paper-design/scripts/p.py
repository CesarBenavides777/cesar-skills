"""Paper MCP helpers — call- and context-budget-aware.
tool(name, **args) -> (text, images) | write(target, html) -> [created ids]
html(target, html) -> raw text (legacy) | art(name, w, h, **styles) -> artboard id
shot(node, path, scale=1|0.5) -> saves JPEG | ids_of(text) -> created ids
sheet(paths, out) -> one contact sheet (read ONE image instead of N)
"""
import json, base64, sys, re, os, subprocess
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

def shot(node, path, scale=0.5):
    """Default 0.5: image tokens scale with pixel AREA, so half scale is a quarter the
    context cost. Use scale=1 only when you need to judge fine type or hairline borders."""
    assert scale in (1, 0.5, 2), "scale 0.6 returns a black image; use 1, 0.5 or 2"
    t, imgs = tool("get_screenshot", nodeId=node, scale=scale)
    if imgs:
        open(path, "wb").write(base64.b64decode(imgs[0]["data"])); print("saved", path)
    else: print(t[:300])

def sheet(paths, out, cols=3, width=1440, bg=(10, 10, 10), label=True):
    """Stitch review captures into ONE contact sheet.

    Reviewing 8 boards as 8 images costs ~8x the image tokens of a single sheet, and every
    one of them rides along in every later request. Capture with shot(), stitch here, read
    the sheet. Falls back to ImageMagick `montage`, then to a plain list of paths."""
    paths = [p for p in paths if os.path.exists(p)]
    if not paths: print("sheet: nothing to stitch"); return None
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        if subprocess.run(["which", "montage"], capture_output=True).returncode == 0:
            subprocess.run(["montage", *paths, "-background", "#0a0a0a", "-geometry",
                            f"{width//cols}x+8+8", "-tile", f"{cols}x", out], check=True)
            print("saved", out, f"({len(paths)} tiles, via montage)"); return out
        print("sheet: install Pillow or ImageMagick; review these individually:", *paths, sep="\n  ")
        return None
    cell = width // cols
    tiles = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        im.thumbnail((cell - 16, 4000))
        tiles.append((os.path.basename(p), im))
    rows = (len(tiles) + cols - 1) // cols
    row_h = [max((t[1].height for t in tiles[r*cols:(r+1)*cols]), default=0) + (26 if label else 8)
             for r in range(rows)]
    canvas = Image.new("RGB", (width, sum(row_h) + 8), bg)
    draw = ImageDraw.Draw(canvas)
    y = 8
    for r in range(rows):
        for c, (name, im) in enumerate(tiles[r*cols:(r+1)*cols]):
            x = c * cell + 8
            if label:
                draw.text((x, y), name, fill=(180, 180, 180))
            canvas.paste(im, (x, y + (18 if label else 0)))
        y += row_h[r]
    canvas.save(out, quality=82)
    print("saved", out, f"({len(tiles)} tiles, {canvas.width}x{canvas.height})")
    return out
