import os
import json
import requests
from pathlib import Path

CKAN_URL = "https://www.dados.mg.gov.br"
API_KEY = os.environ.get("CKAN_API_KEY")

if not API_KEY:
    raise RuntimeError("CKAN_API_KEY não encontrada como variável de ambiente")

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

DATASET_NAME = "empregados-terceirizados"
OWNER_ORG = "controladoria-geral-do-estado-cge"

datapackage = json.loads(
    Path("datapackage/datapackage.json").read_text(encoding="utf-8")
)

# =================================================
# 1. Criar ou atualizar dataset
# =================================================
dataset_payload = {
    "name": DATASET_NAME,
    "title": datapackage["title"],
    "notes": datapackage["description"],
    "owner_org": OWNER_ORG,
    "license_id": "cc-by",
    "state": "active"
}

r = requests.post(
    f"{CKAN_URL}/api/3/action/package_show",
    headers=HEADERS,
    json={"id": DATASET_NAME}
)

if r.status_code == 200:
    print("Dataset existe, atualizando...")
    action = "package_update"
else:
    print("Dataset não existe, criando...")
    action = "package_create"

r = requests.post(
    f"{CKAN_URL}/api/3/action/{action}",
    headers=HEADERS,
    json=dataset_payload
)

if not r.ok:
    raise RuntimeError(f"Erro ao criar/atualizar dataset: {r.text}")

# =================================================
# 2. Criar recursos (um por CSV)
# =================================================
for res in datapackage["resources"]:
    resource_payload = {
        "package_id": DATASET_NAME,
        "name": res["title"],
        "url": f"https://raw.githubusercontent.com/transparencia-mg/empregados_terceirizados/main/{res['path']}",
        "format": "CSV",
        "description": res["description"],
        "schema": res.get("schema")
    }

    r = requests.post(
        f"{CKAN_URL}/api/3/action/resource_create",
        headers=HEADERS,
        json=resource_payload
    )

    if not r.ok:
        print(f"⚠️ Erro ao criar recurso {res['name']}: {r.text}")
    else:
        print(f"Recurso publicado: {res['title']}")

print("✔️ Publicação no CKAN finalizada.")

