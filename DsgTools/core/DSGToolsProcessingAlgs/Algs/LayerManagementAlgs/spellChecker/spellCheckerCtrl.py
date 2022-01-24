from .factories.datasetFactory import DatasetFactory 

class SpellCheckerCtrl:

    def __init__(self, dataset, datasetFactory=DatasetFactory()):
        self.datasetFactory = datasetFactory
        self.dataset = DatasetFactory().getDataset(dataset)

    def hasWord(self, word):
        return self.dataset.hasWord(word)