import csv
import re
from collections import OrderedDict
import html
from dateutil.parser import parse as dt


from googlegroupexporter.exporters import Exporter

TOPIC_DATA = re.compile(
    r'href="(https?://groups.google.com/d/topic/([-_\w.]+)/([-_\w.]+))" '
    r'title="(.+?)".+?<span>(.+?)</span>.+?'
    r'<td class="lastPostDate">(.+?)</td>',
    re.DOTALL
)


class CsvExporter(Exporter):
    def __init__(self, *args, **kwargs):
        super(CsvExporter, self).__init__(*args, **kwargs)

        self.csv_file = None
        self.csv = None

        self.topics = OrderedDict()

    def before_export(self, group_name):
        output = group_name + '.csv'

        self.csv_file = open(output, 'w', encoding='utf-8')
        self.csv = csv.writer(self.csv_file, delimiter=';')
        self.csv.writerow(('url', 'title', 'author', 'date', 'messages'))

    def __str__(self):
        return '{0} topics listed.'.format(len(self.topics))

    def after_export(self):
        for row in self.topics.values():
            self.csv.writerow(row)

        self.csv_file.close()

    def process_index(self, page):
        for id_, *row in self.topic_data(page):
            self.topics[id_] = row

    def process_topic(self, page):
        self.topics[page.id].append(len(page.children))

    @staticmethod
    def topic_data(page):
        return (((forum, topic), link, html.unescape(title), author, dt(date))
                for link, forum, topic, title, author, date
                in TOPIC_DATA.findall(str(page)))
