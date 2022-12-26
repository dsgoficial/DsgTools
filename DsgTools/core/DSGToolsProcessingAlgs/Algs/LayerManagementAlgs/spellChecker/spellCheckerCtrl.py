from .factories.datasetFactory import DatasetFactory


class SpellCheckerCtrl:
    def __init__(self, dataset, datasetFactory=None, **kwargs):
        self.datasetFactory = (
            DatasetFactory() if datasetFactory is None else datasetFactory
        )
        self.dataset = DatasetFactory().getDataset(dataset, **kwargs)

    def hasWord(self, word):
        return self.dataset.hasWord(word)
