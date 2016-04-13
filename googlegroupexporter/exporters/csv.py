import csv
import logging
from collections import OrderedDict

from googlegroupexporter.exporters import Exporter
from googlegroupexporter.pages import GroupPage, TopicPage

logger = logging.getLogger(__name__)


class CsvExporter(Exporter):
    def __init__(self, session, filename):
        super().__init__(session)

        self.csv_file = open(filename, 'w', encoding='utf-8')
        self.csv = csv.writer(self.csv_file, delimiter=';')
        self.csv.writerow(('url', 'title', 'author', 'date', 'messages'))

        self.topics = OrderedDict()

    def close(self):
        for data in self.topics.values():
            self.csv.writerow(data)

        self.csv_file.close()

    def process_index(self, session, response):
        page = GroupPage(response.text)

        for id_, *data in page.data:
            self.topics[id_] = data

        for url in page.links:
            session.get(url, background_callback=self.process_topic)

        session.get(next(page), background_callback=self.process_index)

    def process_topic(self, session, response):
        page = TopicPage(response.text)
        self.topics[page.id].append(len(page.children))

    def __str__(self):
        return '{0} topics listed.'.format(len(self.topics))
