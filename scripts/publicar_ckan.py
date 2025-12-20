#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from pathlib import Path
import re

# =============================
# CONFIGURAÇÕES
# =============================

CKAN_URL = os.environ.get("CKAN_HOST", "https://www.dados.mg.gov.br")
CKAN_KEY = os.environ.get("CKAN_KEY")

if not CKAN_KEY:
    raise RuntimeError("❌ CKAN_KEY não encontrada nas variáveis de ambiente")

HEADERS = {
    "Authorization": CKAN_KEY,
    "Content-Type": "application/json"
}

DATASET_NAME = "empregados-terceirizados"
OWNER_ORG = "controladoria-geral-do-estado-cge"

GITHUB_REPO = "transparencia-mg/empregados_terceirizados"
GITHUB_BRANCH = "main"

# =============================
# FUNÇÕES
# =============================

def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_-]+", "-", value)
    return value.strip("-")

# =============================
# CARREGAR DATAPACKAGE
# =============================

datapackage_path = Path("datapackage/datapackage.json")

if not datapackage_path.exists():
    raise RuntimeError("❌ datapackage.json não encontrado")

datapackage = json.loads(datapackage_path.read_text(encoding="utf-8"))

# =============================
# CRIAR OU ATUALIZAR DATASET
# =============================

dataset_payload = {
    "name": DATASET_NAME,
    "title": datapackage.get("title", DATASET_NAME),
    "notes": datapackage.get("description", ""),
    "owner_org": OWNER_ORG,
    "license_id": "cc-by",
    "state": "active"
}

check = requests.post(
    f"{CKAN_URL}/api/3/action/package_show",
    headers=HEADERS,
    json={"id": DATASET_NAME}
)

action = "package_update" if check.ok else "package_create"

resp = requests.post(
    f"{CKAN_URL}/api/3/action/{action}",
    headers=HEADERS,
    json=dataset_payload
)

if not resp.ok:
    raise RuntimeError(f"❌ Erro ao criar/atualizar dataset:\n{resp.text}")

print("✔ Dataset criado/atualizado")

# =============================
# PUBLICAR RECURSOS
# =============================

for res in datapackage["resources"]:
    resource_name = slugify(res["name"])

    resource_url = (
        f"https://raw.githubusercontent.com/"
        f"{GITHUB_REPO}/{GITHUB_BRANCH}/{res['path']}"
    )

    payload = {
        "package_id": DATASET_NAME,
        "name
