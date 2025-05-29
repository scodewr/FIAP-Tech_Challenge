from typing import List, Type, Optional
from enum import Enum
import pandas as pd
from pydantic import BaseModel
from deep_translator import GoogleTranslator

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
        df = pd.read_csv(filepath_or_buffer=file_path, delimiter=delimiter)
        df = self.translate_column_names(df=df)
    
        df = self.preprocess_data(df, model, category_enum, value_name_column)
        return df
    
    def translate_column_names(self, df: pd.DataFrame, target_lang: str = "en") -> pd.DataFrame:
        """
        Traduz automaticamente os nomes das colunas do DataFrame para o idioma desejado.

        :param df: DataFrame cujas colunas serão traduzidas.
        :param target_lang: Idioma de destino (padrão: inglês).
        :return: DataFrame com os nomes das colunas traduzidos.
        """
        translator = GoogleTranslator(source="auto", target=target_lang)
        translated_columns = {col: translator.translate(col) for col in df.columns}
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
        - Remove espaços extras das colunas e células.
        - Substitui valores nulos por "N/A".
        - Remove linhas onde todas as colunas numéricas (anos) estão vazias.
        - Remove linhas onde qualquer célula contém um valor igual a algum valor da Enum fornecida.
        - Aplica a transformação "melt" no DataFrame
        - Usa a coluna 'control' para gerar o BaseModel, mas remove-a da exibição final.

        :param df: DataFrame a ser processado.
        :param model: O BaseModel para mapear os dados.
        :param category_enum: Enum opcional para filtrar categorias.
        :return: Lista de instâncias do BaseModel.
        """
        # Remove espaços extras dos nomes das colunas
        df.columns = df.columns.str.strip()

        # Remove espaços extras de todas as células
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        # Substitui valores nulos por "N/A"
        df.fillna("N/A", inplace=True)

        # Remove linhas onde todas as colunas numéricas (anos) estão vazias ou zero
        numeric_columns = df.select_dtypes(include=["number"]).columns
        if not numeric_columns.empty:
            df = df[df[numeric_columns].sum(axis=1) > 0]

        # Remove linhas onde qualquer célula contém um valor igual a algum valor da Enum
        if category_enum:
            enum_values = set(item.value.upper() for item in category_enum)
            rows_to_remove = df.apply(lambda row: any(str(cell).upper() in enum_values for cell in row), axis=1)
            df = df[~rows_to_remove]

        # Aplica a transformação "melt" no DataFrame, se solicitado
        
        colunas_years = [col for col in df.columns if str(col).isdigit()]
        colunas_info = [col for col in df.columns if col not in colunas_years]
        df = df.melt(id_vars=colunas_info, value_vars=colunas_years, var_name='year', value_name=value_name_column)

        # Gera o field_map automaticamente
        model_fields = model.model_fields.keys()
        field_map = {field: field for field in model_fields if field in df.columns}

        # Converte o DataFrame em uma lista de BaseModel
        base_model_list = []
        for _, row in df.iterrows():
            # Usa a coluna 'control' para gerar o BaseModel
            data = {model_field: row.get(df_field) for model_field, df_field in field_map.items()}
            base_model_list.append(model(**data))

        # Remove a coluna 'control' do DataFrame para exibição final

        return base_model_list