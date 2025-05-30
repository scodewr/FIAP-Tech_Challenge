
class Util:
    """
    Classe Util com métodos estáticos para manipulação de strings.
    """

    @staticmethod
    def extract_prefix(control: str) -> str:
        """
        Extrai o prefixo do campo 'control' antes do primeiro '_'.
        """
        underscore_position: int = control.find("_")
        if(underscore_position == -1):
            return control[:1]
        return control[:underscore_position]