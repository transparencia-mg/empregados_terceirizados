import json
import os
import requests

CKAN_HOST = os.environ["CKAN_HOST"]
CKAN_KEY = os.environ["CKAN_KEY"]
DATASET = os.environ["DATASET"]
GITHUB_REPO = os.environ["GITHUB_REPO"]
GITHUB_BRANCH = os.environ["GITHUB_BRANCH"]

headers = {
    "Authorization": CKAN_KEY,
    "Content-Type": "application/json"
}

with open("datapackage/datapackage.json", encoding="utf-8") as f:
    dp = json.load(f)

for res in dp["resources"]:
    name = res["name"]
    title = res["title"]
    path = res["path"]
    desc = res.get("description", "")

    url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{path}"

    search = requests.post(
        f"{CKAN_HOST}/api/3/action/resource_search",
        headers=headers,
        json={"query": f"name:{name}", "package_id": DATASET}
    ).json()

    payload = {
        "package_id": DATASET,
        "name": name,
        "title": title,
        "url": url,
        "url_type": "link",
        "format": "CSV",
        "description": desc
    }

    if search["result"]["count"] > 0:
        payload["id"] = search["result"]["results"][0]["id"]
        action = "resource_update"
        print(f"🔄 Atualizando {name}")
    else:
        action = "resource_create"
        print(f"🆕 Criando {name}")

    r = requests.post(
        f"{CKAN_HOST}/api/3/action/{action}",
        headers=headers,
        json=payload
    )

    r.raise_for_status()

print("✅ Publicação CKAN finalizada com sucesso")
