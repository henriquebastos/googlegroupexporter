import logging
from mailbox import mbox, Message

from googlegroupexporter.exporters import Exporter
from googlegroupexporter.pages import GroupPage, TopicPage

logger = logging.getLogger(__name__)


def message(url, content):
    id_ = fid, tid, mid = tuple(url.split('=')[-1].split('/'))

    headers = {
        'GGE-Url': url,
        'GGE-Id': '{}/{}/{}'.format(*id_),
        'GGE-Forum-Id': fid,
        'GGE-Topic-Id': tid,
        'GGE-Message-Id': mid,
    }

    msg = Message(content)
    for k, v in headers.items():
        msg.add_header(k, v)

    return msg


class MailExporter(Exporter):
    def __init__(self, group_name, filename):
        super().__init__(group_name)
        self.mbox = mbox(filename)

        self.summary = dict(indexes=0, topics=0, messages=0)

    def __str__(self):
        return '{indexes} index pages listing {topics} topics with {messages} messages.'.format(**self.summary)

    def close(self):
        self.mbox.close()

    def process_index(self, session, response):
        page = GroupPage(response.text)

        for url in page.links:
            session.get(url, background_callback=self.process_topic)

        session.get(next(page), background_callback=self.process_index)
        self.summary['indexes'] += 1

    def process_topic(self, session, response):
        for url in TopicPage(response.text).links:
            session.get(url, background_callback=self.process_message)

        self.summary['topics'] += 1

    def process_message(self, session, response):
        self.mbox.add(message(response.url, response.text))
        self.summary['messages'] += 1
