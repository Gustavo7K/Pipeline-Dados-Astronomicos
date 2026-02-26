import lightkurve as lk
import pandas as pd
import re
from typing import List

def get_available_sectors(tic_id: int):
    target = f"TIC {tic_id}"
    print(f"🔍 Consultando o MAST para {target}...")

    try:
        #Busca usando TESScut
        search = lk.search_tesscut(target)
        
        if len(search) == 0:
            return None

        #Converte para DataFrame para facilitar a extração
        df = search.table.to_pandas()

        #Extração do número do setor da coluna 'mission' (ex: "TESS Sector 04" -> 4)
        def extrair_setor(missao_str):
            match = re.search(r'Sector\s+(\d+)', missao_str)
            return int(match.group(1)) if match else None

        #Criando as colunas limpas
        df['sector_num'] = df['mission'].apply(extrair_setor)
        
        #Criando um resumo único (removendo duplicatas de setor/ano/missão)
        resumo = df[['sector_num', 'mission', 'year']].drop_duplicates()
        resumo = resumo.sort_values(by='sector_num').dropna()

        return resumo

    except Exception as e:
        print(f"❌ Erro ao processar tabela: {e}")
        return None