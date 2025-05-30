from typing import List, Type, Optional
from enum import Enum
import pandas as pd
from pydantic import BaseModel
from collections import defaultdict

class CSVService:
    """
    Serviço para manipulação de dados de arquivos CSV.
    """

    def process_csv_data(
        self,
        file_path: str,
        model: Type[BaseModel],
        category_enum: Optional[Type[Enum]] = None,
        value_name_column: str = "production",
        delimiter: str = ";"
    ) -> List[BaseModel]:
        """
        Processa os dados de um arquivo CSV e retorna uma lista de instâncias do BaseModel.

        :param file_path: Caminho do arquivo CSV.
        :param model: O BaseModel para mapear os dados.
        :param category_enum: Enum opcional para filtrar categorias.
        :param value_name_column: Nome da coluna de valores (padrão: "production").
        :param delimiter: Delimitador do CSV (padrão: ";").
        :return: Lista de instâncias do BaseModel.
        """
        # Lê o arquivo CSV
        df = pd.read_csv(filepath_or_buffer=file_path, delimiter=delimiter, encoding='utf-8')
        df = self.translate_column_names(df=df, model=model)
    
        df = self.preprocess_data(df, model, category_enum, value_name_column)
        return df
    
    def translate_column_names(self, df: pd.DataFrame, model: Type[BaseModel]) -> pd.DataFrame:
        """
        Traduz os nomes das colunas do DataFrame para o schema do BaseModel.

        :param df: DataFrame cujas colunas serão traduzidas.
        :param model: O BaseModel cujos nomes de campo serão usados para a tradução.
        :return: DataFrame com os nomes das colunas traduzidos.
        """
        
        translated_columns = {col: model.schema_equivalence[str.lower(col)] for col in df.columns if str.lower(col) in model.schema_equivalence}
        return df.rename(columns=translated_columns)

    def preprocess_data(
        self,
        df: pd.DataFrame,
        model: Type[BaseModel],
        category_enum: Optional[Enum] = None,
        value_name_column: str = "production"
    ) -> List[BaseModel]:
        """
        Realiza o tratamento inicial dos dados do DataFrame e retorna uma lista de instâncias do BaseModel.
        """
        # Remove espaços extras dos nomes das colunas
        df.columns = df.columns.str.strip()

        # Remove espaços extras de todas as células
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        # Substitui valores nulos por 0 inicialmente
        df.fillna(0, inplace=True)

        # Conta quantas colunas compartilham o mesmo prefixo antes do `.`
        column_groups = defaultdict(list)

        for col in df.columns:
            base_name = col.split('.')[0]  # Pega o nome base da coluna
            column_groups[base_name].append(col)

        # Agora agrupe e some os grupos com mais de uma coluna
        for base_name, cols in column_groups.items():
            if len(cols) > 1:
                df[base_name] = df[cols].sum(axis=1)
                df.drop(columns=[col for col in cols if col != base_name], inplace=True)

        # Remove linhas onde todas as colunas numéricas (anos) estão vazias ou zero
        numeric_columns = df.select_dtypes(include=["number"]).columns
        if not numeric_columns.empty:
            df = df[df[numeric_columns].sum(axis=1) > 0]

        # Remove linhas onde qualquer célula contém um valor igual a algum valor da Enum
        '''if category_enum:
            enum_values = set(item.value.upper() for item in category_enum)
            rows_to_remove = df.apply(lambda row: any(str(cell).upper() in enum_values for cell in row), axis=1)
            df = df[~rows_to_remove]
        '''
        if 'control' in df.columns:
            df = df[df['control'].astype(str).str.contains('_')]

        # Trata colunas de ano
        colunas_years = [col for col in df.columns if str(col).isdigit()]
        for col in colunas_years:
            df[col] = df[col].replace({'nd': None, '*': None}) 
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

        for col in df.columns:
            if col not in colunas_years:
                df[col] = df[col].astype(str).str.replace('(', '', regex=False)
                df[col] = df[col].astype(str).str.replace(')', '', regex=False)

        # Aplica transformação melt
        colunas_info = [col for col in df.columns if col not in colunas_years]
        df = df.melt(id_vars=colunas_info, value_vars=colunas_years, var_name='year', value_name=value_name_column)

        # Remove linhas com NaN na coluna que vai pro campo numérico no Pydantic
        df = df[df[value_name_column].notna()]
        df = df[df['year'].notna()]
        # Alternativamente, para definir como 0.0 (cuidado: só se fizer sentido!)
        df = df[:].replace({'(':'', ')': ''})

        # Gera o field_map automaticamente
        model_fields = model.model_fields.keys()
        df.columns = df.columns.str.lower()  # se quiser padronizar
        field_map = {field: field for field in model_fields if field in df.columns}


        # Converte o DataFrame em uma lista de BaseModel
        base_model_list = []
        for _, row in df.iterrows():
            data = {}
            for model_field, df_field in field_map.items():
                value = row.get(df_field)

                # Tratamento de NaN para campos numéricos
                if pd.isna(value):
                    value = None

                data[model_field] = value

            try:
                base_model_list.append(model(**data))
            except Exception as e:
                # Log opcional, você pode remover ou levantar uma exceção personalizada se preferir
                print(f"Erro ao criar instância do modelo: {e}\nDados: {data}")


        return base_model_list
