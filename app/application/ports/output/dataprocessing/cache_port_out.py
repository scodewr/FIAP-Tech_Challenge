import pandas as pd

class CachePortOut:
    """
    Interface para abstrair os casos de uso relacionados ao cache.
    """

    def save_csv_to_cache(self, url: str, df: pd.DataFrame, sep: str = ";") -> str:
        """
        Salva um DataFrame como um arquivo CSV no cache.

        :param url: URL do CSV.
        :param df: DataFrame a ser salvo.
        :param sep: Delimitador do CSV (padrão: ";").
        :return: Caminho completo do arquivo salvo.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")

    def get_csv_file_path(self, url: str) -> str:
        """
        Retorna o caminho do arquivo CSV no cache com base na URL.

        :param url: URL do CSV.
        :return: Caminho completo do arquivo no cache.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")

    def is_file_in_cache(self, file_path: str) -> bool:
        """
        Verifica se o arquivo existe no cache.

        :param file_path: Caminho do arquivo.
        :return: True se o arquivo existir, False caso contrário.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")

    def is_cache_expired(self, file_path: str, max_days: int = 30) -> bool:
        """
        Verifica se um arquivo em cache tem mais de `max_days` dias.

        :param file_path: Caminho para o arquivo.
        :param max_days: Dias máximos permitidos antes do cache expirar.
        :return: True se o cache expirou, False caso contrário.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")