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

# =============================
# Criar ou atualizar dataset
# =============================
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

action = "package_update" if r.ok else "package_create"

r = requests.post(
    f"{CKAN_URL}/api/3/action/{action}",
    headers=HEADERS,
    json=dataset_payload
)

if not r.ok:
    raise RuntimeError(f"Erro ao criar/atualizar dataset: {r.text}")

print("✔️ Dataset publicado/atualizado com sucesso.")

# =============================
# Criar recursos
# =============================
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

    if r.ok:
        print(f"✔️ Recurso publicado: {res['title']}")
    else:
        print(f"⚠️ Erro ao criar recurso {res['title']}: {r.text}")

print("🏁 Publicação no CKAN finalizada.")


