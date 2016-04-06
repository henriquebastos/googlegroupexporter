import csv
import logging
from mailbox import mbox

from googlegroupexporter.pages import GroupPage, TopicPage


logger = logging.getLogger(__name__)


class Summary:
    def __init__(self):
        self.data = dict(indexes=0, topics=0, messages=0)

    def __str__(self):
        return '{indexes} index pages listing {topics} topics with {messages} messages.'.format(**self.data)

    def add(self, **kwargs):
        for k, v in kwargs.items():
            self.data[k] += v


class Exporter:
    GROUP_URL = 'https://groups.google.com/forum/?_escaped_fragment_=forum/{}%5B1-100%5D'

    def __init__(self, session):
        self._session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        pass

    def __iter__(self):
        return iter(self._session.status)

    def export(self, group_name):
        start_url = self.GROUP_URL.format(group_name)
        self._session.get(start_url, background_callback=self.process_index)

    def process_index(self, session, response):
        raise NotImplementedError

    def process_topic(self, session, response):
        raise NotImplementedError

    def process_message(self, session, response):
        raise NotImplementedError


class MailExporter(Exporter):
    def __init__(self, group_name, filename):
        super().__init__(group_name)
        self.mbox = mbox(filename)

        self.summary = Summary()

    def close(self):
        self.mbox.close()

    def process_index(self, session, response):
        page = GroupPage(response.text)

        for url in page.links:
            session.get(url, background_callback=self.process_topic)

        session.get(next(page), background_callback=self.process_index)
        self.summary.add(indexes=1)

    def process_topic(self, session, response):
        for url in TopicPage(response.text).links:
            session.get(url, background_callback=self.process_message)

        self.summary.add(topics=1)

    def process_message(self, session, response):
        self.mbox.add(response.text)
        self.summary.add(messages=1)


class TopicExporter(Exporter):
    def __init__(self, session, filename):
        super().__init__(session)

        self.csv_file = open(filename, 'w', encoding='utf-8')
        self.csv = csv.writer(self.csv_file, delimiter=';')
        self.csv.writerow(('url', 'title', 'author', 'date'))

        self.summary = Summary()

    def close(self):
        self.csv_file.close()

    def process_index(self, session, response):
        page = GroupPage(response.text)
        data = page.data
        logger.debug('Data len: {} from {}'.format(len(data), response.url))

        self.summary.add(indexes=1, topics=len(data))
        self.csv.writerows(data)

        session.get(next(page), background_callback=self.process_index)

