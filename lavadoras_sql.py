import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

csv_path = 'C:/Users/sther/Desktop/DNC/Equipacare/SQL/lavadoras.csv'
df = pd.read_csv(csv_path, delimiter=';')

def remover_texto_e_converter_para_numero(string):
    if isinstance(string, str):
        texto_indesejado = [' minutos', ' cirurgias', ' U.E.', ' litros', ' leitos', ',0']
        for texto in texto_indesejado:
            string = string.replace(texto, '')
    return string

for column in df.columns:
    if df[column].dtype == 'object':  # Verifica se a coluna é do tipo 'object' (string)
        df[column] = df[column].apply(remover_texto_e_converter_para_numero)

engine = create_engine('mysql+pymysql://root:031224@localhost:3306/equipamentos-cme-teste') 

# Teste de conexão
try:
    with engine.connect() as connection:
        print("Conexão ao banco de dados MySQL foi bem-sucedida.")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    exit()

df['createdAt'] = datetime.now()
df['updatedAt'] = datetime.now()

df.to_sql('lavadora', engine, if_exists='append', index=False)

print("Dados importados com sucesso!")