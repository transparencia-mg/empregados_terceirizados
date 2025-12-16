#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
normalizar_mes_referencia.py

Converte a coluna 'MÊS REFERÊNCIA' do formato:
DD/MM/AAAA  →  MM/AAAA

Regras:
- NÃO altera outras colunas
- NÃO converte tipos
- Mantém células vazias vazias
- Atualiza os arquivos CSV na pasta /data
"""

from pathlib import Path
import pandas as pd

# =========================
# CONFIGURAÇÕES
# =========================
DATA_DIR = Path("data")
COLUNA_DATA = "MÊS REFERÊNCIA"

# =========================
# FUNÇÃO DE CONVERSÃO
# =========================
def converter_mes_ano(valor: str) -> str:
    if not valor or not isinstance(valor, str):
        return ""
    partes = valor.split("/")
    if len(partes) == 3:
        # DD/MM/AAAA → MM/AAAA
        return f"{partes[1]}/{partes[2]}"
    return valor

# =========================
# PROCESSAMENTO
# =========================
def main():
    if not DATA_DIR.exists():
        raise FileNotFoundError("Pasta /data não encontrada")

    arquivos = sorted(DATA_DIR.glob("terceirizados_*.csv"))

    if not arquivos:
        print("Nenhum CSV encontrado para processar")
        return

    for arquivo in arquivos:
        print(f"Processando: {arquivo.name}")

        df = pd.read_csv(
            arquivo,
            dtype=str,
            keep_default_na=False,
            encoding="utf-8"
        )

        if COLUNA_DATA not in df.columns:
            print(f"  ⚠ Coluna '{COLUNA_DATA}' não encontrada — ignorado")
            continue

        df[COLUNA_DATA] = df[COLUNA_DATA].apply(converter_mes_ano)

        df.to_csv(
            arquivo,
            index=False,
            encoding="utf-8"
        )

        print(f"  ✔ Normalizado com sucesso")

if __name__ == "__main__":
    main()
