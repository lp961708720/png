from __future__ import annotations
import hashlib
import json
from pathlib import Path
from shutil import copyfile
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

root = Path(__file__).parent
repo = root / "oba-live-tool"
assert (repo / "LICENSE").exists(), "Missing upstream license"
src_logo = root / "assets" / "langli-logo.png"
assert src_logo.exists(), "Missing branded logo asset"

builder_path = repo / "electron-builder.json"
cfg = json.loads(builder_path.read_text(encoding="utf-8"))
cfg["productName"] = "朗丽直播助手"
cfg["appId"] = "com.langli.liveassistant"
builder_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

header_path = repo / "src" / "components" / "common" / "Header.tsx"
header = header_path.read_text(encoding="utf-8")
assert "直播助手</h1>" in header and "<Package className" in header, "Header upstream structure changed"
header = header.replace("import { Package } from 'lucide-react'\n", "", 1)
header = header.replace('<Package className="h-6 w-6 text-primary" />', '<img src="/favicon.png" alt="朗丽" className="h-8 w-8 rounded-lg object-contain" />', 1)
header = header.replace(">直播助手</h1>", ">朗丽直播助手</h1>", 1)
header_path.write_text(header, encoding="utf-8")

electron_path = repo / "electron" / "main" / "app.ts"
electron = electron_path.read_text(encoding="utf-8")
old = "title: `OBA 直播工具 - v${app.getVersion()}`"
assert old in electron, "Electron window title upstream structure changed"
electron_path.write_text(electron.replace(old, "title: `朗丽直播助手 - v${app.getVersion()}`", 1), encoding="utf-8")

html_path = repo / "index.html"
html = html_path.read_text(encoding="utf-8")
assert "<head>" in html and "<title>" not in html, "HTML upstream structure changed"
html_path.write_text(html.replace("<head>", "<head>\n    <title>朗丽直播助手</title>", 1), encoding="utf-8")

out = repo / "public"
with Image.open(src_logo) as im:
    im = im.convert("RGBA")
    im.resize((512, 512), Image.Resampling.LANCZOS).save(out / "favicon.png", optimize=True)
    im.resize((256, 256), Image.Resampling.LANCZOS).save(out / "favicon.ico", format="ICO", sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
import base64
data = base64.b64encode((out / "favicon.png").read_bytes()).decode("ascii")
(out / "favicon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><image width="512" height="512" href="data:image/png;base64,{data}"/></svg>\n',encoding="utf-8")

print("Applied brand: 朗丽直播助手")
print("Logo SHA256:", hashlib.sha256(src_logo.read_bytes()).hexdigest())
print("Only display name, top bar image, window title, and icon assets changed.")
