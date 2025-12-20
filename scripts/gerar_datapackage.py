# scripts/gerar_datapackage.py
import json
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT = Path("datapackage/datapackage.json")

# =========================
# Schema padrão dos CSVs
# =========================
SCHEMA_FIELDS = [
    {
        "name": "matricula",
        "title": "Matrícula do empregado terceirizado",
        "type": "string",
        "description": "Identificador do empregado terceirizado"
    },
    {
        "name": "nome",
        "title": "Nome completo do empregado terceirizado",
        "type": "string"
    },
    {
        "name": "orgao",
        "title": "Órgão de trabalho do empregado",
        "type": "string"
    },
    {
        "name": "cargo",
        "title": "Cargo exercido pelo empregado",
        "type": "string"
    },
    {
        "name": "empresa",
        "title": "Nome da empresa terceirizada",
        "type": "string"
    },
    {
        "name": "cnpj_empresa",
        "title": "CNPJ da empresa terceirizada",
        "type": "string",
        "description": "CNPJ com 14 dígitos, sem formatação"
    },
    {
        "name": "mes_referencia",
        "title": "Mês de referência do contrato",
        "type": "string",
        "description": "Mês do contrato no formato abreviado (ex: jan-25)"
    }
]

resources = []

for csv in sorted(DATA_DIR.glob("terceirizados_*.csv")):
    ano = csv.stem.split("_")[-1]

    resources.append({
        "name": f"terceirizados-{ano}",
        "title": f"Empregados Terceirizados – {ano}",
        "path": f"data/{csv.name}",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "utf-8",
        "description": f"Dados de empregados terceirizados do ano de {ano}",
        "schema": {
            "fields": SCHEMA_FIELDS,
            "primaryKey": ["matricula", "mes_referencia"]
        }
    })

datapackage = {
    "profile": "data-package",
    "name": "empregados-terceirizados-mg",
    "title": "Empregados Terceirizados do Governo de Minas Gerais",
    "description": "Base anual de empregados terceirizados do Governo do Estado de Minas Gerais.",

    # 👇 OBRIGATÓRIO PARA dpckan
    "owner_org": "controladoria-geral-do-estado-cge",

    # 👇 Compatibilidade CKAN
    "ckan": {
        "owner_org": "controladoria-geral-do-estado-cge",
        "private": False,
        "state": "active"
    },

    "license": {
        "type": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/"
    },
    "resources": resources
}

OUTPUT.parent.mkdir(exist_ok=True)
OUTPUT.write_text(
    json.dumps(datapackage, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("datapackage.json gerado com schema das colunas.")


