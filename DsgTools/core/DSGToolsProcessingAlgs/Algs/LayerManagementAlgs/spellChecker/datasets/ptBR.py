import bz2
from dataclasses import dataclass
import pickle
import os
from ..structures.ternarySearchTree import Trie, Node
from DsgTools.core.NetworkTools.ExternalFilesHandler import ExternalFileHandlerConfig, ExternalFileDownloadProcessor

WORLIST_FILE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '..',
    'data',
    'wordDatasetPtBR.pbz2'
)

@dataclass
class WordDatasetPtBRFileConfig(ExternalFileHandlerConfig):
    url = 'https://github.com/dsgoficial/external_files_plugins/releases/download/spell_checker_files/wordDatasetPtBR.pbz2'
    file_name = 'wordDatasetPtBR.pbz2'
    output_folder = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '..',
        'data',
    )

@dataclass
class PalavrasFileConfig(ExternalFileHandlerConfig):
    url = 'https://github.com/dsgoficial/external_files_plugins/releases/download/spell_checker_files/palavras.txt'
    file_name = 'palavras.txt'
    output_folder = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '..',
        'data',
    )

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'Trie':
            return Trie
        if name == 'Node':
            return Node
        return super().find_class(module, name)

class PtBR:
    def __init__(self):
        if not os.path.exists(WORLIST_FILE_PATH):
            raise Exception('Word list file not found.')
        self.trie = self.decompress_pickle(WORLIST_FILE_PATH)

    def compressed_pickle(self, filePath, data):
        with bz2.BZ2File(filePath, 'w') as f: 
            pickle.dump(data, f)

    def decompress_pickle(self, filePath):
        data = bz2.BZ2File(filePath, 'rb')
        data = CustomUnpickler(data).load()
        return data

    def hasWord(self, word):
        return word in self.trie