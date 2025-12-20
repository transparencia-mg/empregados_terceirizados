#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from ckanapi import RemoteCKAN

CKAN_HOST = "https://www.dados.mg.gov.br"
CKAN_KEY = os.environ.get("CKAN_KEY")
DATASET = "empregados-terceirizados-mg"

if not CKAN_KEY:
    raise RuntimeError("CKAN_KEY não definida")

ckan = RemoteCKAN(CKAN_HOST, apikey=CKAN_KEY)

print("📦 Atualizando dataset (package_update)")
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

# 📄 Publicar datapackage.json
upsert_resource(
    name="datapackage-json",
    title="Datapackage do conjunto de dados",
    url="https://raw.githubusercontent.com/transparencia-mg/empregados_terceirizados_mg/main/datapackage/datapackage.json",
    description="Arquivo datapackage.json com metadados e schema dos recursos.",
    fmt="JSON"
)

# 📘 Publicar README.md
upsert_resource(
    name="readme",
    title="Descrição e metodologia do dataset",
    url="https://raw.githubusercontent.com/transparencia-mg/empregados_terceirizados_mg/main/README.md",
    description="Documento com contextualização, metodologia e orientações de uso dos dados.",
    fmt="MD"
)

print("✅ Publicação CKAN finalizada com sucesso")

