import os, json, re

manifest = {}
folders = ["command", "advanced", "copper", "silver", "gold", "smcs"]
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

manifest_json = json.dumps(manifest)

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

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated manifest: {sum(len(v) for v in manifest.values())} total cards")
for k, v in manifest.items():
    print(f"  {k}: {len(v)} cards")
