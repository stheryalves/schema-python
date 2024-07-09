import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Função para remover texto indesejado e converter para inteiro
def remover_texto_e_converter_para_int(string):
    if isinstance(string, str):
        texto_indesejado = ['minutos', 'litros', ',0']
        for texto in texto_indesejado:
            string = string.replace(texto, '')
        string = string.replace(",", "").replace(".", "")
        # Tentar converter para inteiro
        try:
            valor_int = int(string)
        except ValueError:
            # Se não for possível converter, retornar a string original
            return string
        return valor_int
    else:
        return string

# Caminho do arquivo CSV
csv_path = 'C:/Users/sther/Desktop/DNC/Equipacare/SQL/autoclaves_a_vapor.csv'
df = pd.read_csv(csv_path, delimiter=';')

# Aplicar a função de limpeza aos dados
for column in df.columns:
    df[column] = df[column].apply(remover_texto_e_converter_para_int)

# Conectar ao banco de dados MySQL
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

# Inserir os dados no banco de dados SQL
df.to_sql('autoclave', engine, if_exists='append', index=False)

print("Dados importados com sucesso!")