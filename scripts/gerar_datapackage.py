#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT = Path("datapackage/datapackage.json")

resources = []

for csv in sorted(DATA_DIR.glob("terceirizados_*.csv")):
    ano = csv.stem.split("_")[-1]

    resources.append({
        "name": f"terceirizados-{ano}",
        "title": f"Empregados Terceirizados – {ano}",
        "description": f"Conjunto de dados de empregados terceirizados do Estado de Minas Gerais. Dados disponíveis a partir de 2021. Os dados são atualizados mensalmente",
        "path": f"data/{csv.name}",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "utf-8",
        "profile": "tabular-data-resource",
        "schema": {
            "fields": [
                {"name": "matricula", "type": "string"},
                {"name": "nome", "type": "string"},
                {"name": "orgao", "type": "string"},
                {"name": "cargo", "type": "string"},
                {"name": "empresa", "type": "string"},
                {"name": "cnpj_empresa", "type": "string"},
                {"name": "mes_referencia", "type": "string"}
            ]
        }
    })

datapackage = {
    "profile": "data-package",
    "name": "empregados-terceirizados-mg",
    "title": "Empregados Terceirizados do Governo de Minas Gerais",
    "owner_org": "controladoria-geral-do-estado-cge",
    "resources": resources
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(
    json.dumps(datapackage, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"✔ datapackage.json gerado com {len(resources)} recursos")

