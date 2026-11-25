import json

with open("slides_categorized.json", "r", encoding="utf-8") as f:
    data = json.load(f)

js_content = f"window.DECK_DATA = {json.dumps(data, ensure_ascii=False, indent=2)};\n"

with open("data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("data.js created successfully!")
