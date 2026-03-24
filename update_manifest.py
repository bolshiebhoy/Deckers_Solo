import os, json, re, base64

manifest = {}
folders = ["command", "advanced", "copper", "silver", "gold", "smcs", "deckers"]
for f in folders:
    path = os.path.join("images", "cards", f)
    if os.path.isdir(path):
        files = sorted(
            [
                x
                for x in os.listdir(path)
                if x.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
            ]
        )
        manifest[f] = [f"images/cards/{f}/{x}" for x in files]
    else:
        manifest[f] = []

# Add color-specific command card subfolders
for color in ["red", "green", "blue", "yellow"]:
    path = os.path.join("images", "cards", "command", color)
    key = f"command{color.capitalize()}"
    if os.path.isdir(path):
        files = sorted(
            [
                x
                for x in os.listdir(path)
                if x.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
            ]
        )
        manifest[key] = [f"images/cards/command/{color}/{x}" for x in files]
    else:
        manifest[key] = []

# Build decker data URLs (base64) for WebGL compatibility on file:// protocol
decker_data = {}
for path in manifest.get("deckers", []):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            b64 = base64.b64encode(img_file.read()).decode("utf-8")
            ext = path.rsplit(".", 1)[-1].lower()
            mime = {
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "png": "image/png",
                "webp": "image/webp",
            }.get(ext, "image/jpeg")
            name = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
            decker_data[name] = f"data:{mime};base64,{b64}"

manifest_json = json.dumps(manifest)
decker_data_json = json.dumps(decker_data)

# Update the HTML file
html_path = "Deckers Play.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

html = re.sub(
    r"const cardManifest = \{.*?\};",
    f"const cardManifest = {manifest_json};",
    html,
    count=1,
)

html = re.sub(
    r"const deckerDataUrls = \{.*?\};",
    f"const deckerDataUrls = {decker_data_json};",
    html,
    count=1,
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated manifest: {sum(len(v) for v in manifest.values())} total cards")
for k, v in manifest.items():
    print(f"  {k}: {len(v)} cards")
print(f"Embedded {len(decker_data)} decker images as base64")
