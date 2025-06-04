import json
import os


class HTMLHelpCreator(object):
    def __init__(self):
        self.html_repository = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "html"
        )
        self.image_repository = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "images"
        )
        self.json_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "links_dictionary.json"
        )

    def getLinkDictionary(self):

        with open(self.json_file) as json_file:
            json_link_dictionary = json.loads(json_file.read())

        return json_link_dictionary

    def shortHelpString(self, algorithm_name):
        try:
            image_path = "{}/{}.png".format(self.image_repository, algorithm_name)
            html_path = "{}/{}.html".format(self.html_repository, algorithm_name)

            html_file = open(html_path, "r")
            html_string = html_file.read()

            return html_string.format(image_path)
        except:
            return "No help available for this algorithm."

    def helpUrl(self, algorithm_name):

        link_dictionary = self.getLinkDictionary()

        for algorithm, wiki_link in link_dictionary.items():
            if algorithm_name == algorithm:
                return wiki_link
