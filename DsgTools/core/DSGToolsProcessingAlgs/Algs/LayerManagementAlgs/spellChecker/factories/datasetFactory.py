from ..datasets.ptBR import PtBR
from ..structures.ternarySearchTree import Trie


class DatasetFactory:
    def getDataset(self, dataset):
        methods = {"pt-BR": PtBR}
        return methods[dataset]()
