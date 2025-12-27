#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import hashlib
from pathlib import Path
from gerar_schema import gerar_schema

DATA_DIR = Path("data")
OUTPUT = Path("datapackage/datapackage.json")

resources = []

for csv in sorted(DATA_DIR.glob("terceirizados_*.csv")):
    ano = csv.stem.split("_")[-1]

    hash_md5 = hashlib.md5(csv.read_bytes()).hexdigest()
    schema = gerar_schema(csv)

    resources.append({
        # 🔑 ID lógico do recurso (não muda)
        "name": f"terceirizados_{ano}",
        "title": f"Empregados Terceirizados – {ano}",
        "description": (
            "Conjunto de dados de empregados terceirizados do Estado de Minas Gerais. "
            "Dados disponíveis a partir de 2021. Atualização mensal."
        ),
        "path": f"data/{csv.name}",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "latin1",
        "hash": f"md5:{hash_md5}",
        "schema": schema
    })

datapackage = {
    "profile": "tabular-data-package",
    "name": "empregados-terceirizados-mg",
    "title": "Empregados Terceirizados do Governo de Minas Gerais",
    "owner_org": "controladoria-geral-do-estado-cge",
    "license": "CC-BY-4.0",
    "resources": resources
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(
    json.dumps(datapackage, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"✔ datapackage.json gerado com {len(resources)} recursos")


