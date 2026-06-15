from verso.semantica.constants import SemanticError
from verso.sintaxe.constants import Statement


class SemanticAnalyzer:
    def __init__(self) -> None:
        self._symbols = {}

    def analyse(self, tree: list[Statement]) -> tuple[list[Statement], list[SemanticError]|None]:
        """ Realiza a análise semântica """
        


        return (tree, None)


