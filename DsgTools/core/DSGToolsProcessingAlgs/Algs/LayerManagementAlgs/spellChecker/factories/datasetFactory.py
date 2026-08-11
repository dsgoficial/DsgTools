from ..datasets.ptBR import PtBR


class DatasetFactory:
    def getDataset(self, dataset):
        methods = {"pt-BR": PtBR}
        return methods[dataset]()
