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

print("📦 Atualizando dataset")
ckan.action.package_update(
    name=DATASET,
    title="Empregados Terceirizados do Governo de Minas Gerais",
    notes="Base anual de empregados terceirizados do Governo do Estado de Minas Gerais.",
    state="active"
)

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
# 1️⃣ PUBLICAR / ATUALIZAR CSVs (a partir do datapackage)
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
# 2️⃣ PUBLICAR datapackage.json
# ======================================================

upsert_resource(
    name="datapackage-json",
    title="Datapackage do conjunto de dados",
    url=f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/datapackage/datapackage.json",
    description="Arquivo datapackage.json com metadados e schema dos recursos.",
    fmt="JSON"
)

# ======================================================
# 3️⃣ PUBLICAR README.md (EXATAMENTE O SEU)
# ======================================================

upsert_resource(
    name="readme",
    title="Descrição e metodologia do dataset",
    url=f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/README.md",
    description="Documento com contextualização, metodologia e orientações de uso dos dados.",
    fmt="MD"
)

print("✅ Dataset, CSVs, datapackage e README publicados com sucesso")

