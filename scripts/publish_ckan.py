#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from ckanapi import RemoteCKAN

CKAN_HOST = "https://www.dados.mg.gov.br"
CKAN_KEY = os.environ.get("CKAN_KEY")
DATASET = "empregados-terceirizados-mg"
GITHUB_REPO = "transparencia-mg/empregados_terceirizados_mg"
GITHUB_BRANCH = "main"

if not CKAN_KEY:
    raise RuntimeError("CKAN_KEY não definida")

ckan = RemoteCKAN(CKAN_HOST, apikey=CKAN_KEY)

# ======================================================
# 1️⃣ LER README.md PARA USAR COMO DESCRIÇÃO DO DATASET
# ======================================================

readme_path = Path("README.md")
if not readme_path.exists():
    raise RuntimeError("README.md não encontrado")

readme_text = readme_path.read_text(encoding="utf-8")

# ======================================================
# 2️⃣ ATUALIZAR DATASET (DESCRIÇÃO = README)
# ======================================================

print("📦 Atualizando dataset (descrição a partir do README.md)")
ckan.action.package_update(
    name=DATASET,
    title="Empregados Terceirizados do Governo de Minas Gerais",
    notes=readme_text,
    state="active"
)

# ======================================================
# FUNÇÃO AUXILIAR
# ======================================================

def upsert_resource(name, title, url, description, fmt):
    search = ckan.action.resource_search(
        query=f'name:"{name}"',
        package_id=DATASET
    )

    payload = {
        "package_id": DATASET,
        "name": name,
        "title": title,
        "url": url,
        "url_type": "link",
        "format": fmt,
        "description": description
    }

    if search["count"] > 0:
        payload["id"] = search["results"][0]["id"]
        ckan.action.resource_update(**payload)
        print(f"🔄 Atualizado: {name}")
    else:
        ckan.action.resource_create(**payload)
        print(f"🆕 Criado: {name}")

# ======================================================
# 3️⃣ PUBLICAR / ATUALIZAR CSVs (via datapackage)
# ======================================================

dp_path = Path("datapackage/datapackage.json")
datapackage = json.loads(dp_path.read_text(encoding="utf-8"))

for res in datapackage["resources"]:
    name = res["name"]
    title = res.get("title", name)
    path = res["path"]
    desc = res.get("description", "")
    fmt = res.get("format", "CSV").upper()

    url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{path}"

    upsert_resource(
        name=name,
        title=title,
        url=url,
        description=desc,
        fmt=fmt
    )

# ======================================================
# 4️⃣ PUBLICAR datapackage.json (COMO RECURSO)
# ======================================================

upsert_resource(
    name="datapackage-json",
    title="Datapackage do conjunto de dados",
    url=f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/datapackage/datapackage.json",
    description="Arquivo datapackage.json com metadados e schema dos recursos.",
    fmt="JSON"
)

print("✅ Dataset atualizado com descrição (README), CSVs e datapackage")


