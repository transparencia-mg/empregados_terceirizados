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
        "path": f"data/{csv.name}",
        "profile": "tabular-data-resource",
        "scheme": "file",
        "format": "csv",
        "encoding": "utf-8",
        "mediatype": "text/csv",
        "description": f"Dados de empregados terceirizados do ano de {ano}",
        "schema": {
            "fields": [
                {"name": "matricula", "type": "string", "title": "Matrícula"},
                {"name": "nome", "type": "string", "title": "Nome"},
                {"name": "orgao", "type": "string", "title": "Órgão"},
                {"name": "cargo", "type": "string", "title": "Cargo"},
                {"name": "empresa", "type": "string", "title": "Empresa"},
                {"name": "cnpj_empresa", "type": "string", "title": "CNPJ da Empresa"},
                {"name": "mes_referencia", "type": "string", "title": "Mês de referência"}
            ],
            "primaryKey": ["matricula", "mes_referencia"]
        }
    })

datapackage = {
    "profile": "data-package",
    "name": "empregados-terceirizados-mg",
    "title": "Empregados Terceirizados do Governo de Minas Gerais",
    "description": "Base anual de empregados terceirizados do Governo do Estado de Minas Gerais.",
    "owner_org": "controladoria-geral-do-estado-cge",
    "resources": resources
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(
    json.dumps(datapackage, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"✔ datapackage.json gerado com {len(resources)} recursos")
