from mailbox import mbox, Message

from googlegroupexporter.exporters import Exporter


class MailExporter(Exporter):
    def __init__(self, *args, **kwargs):
        super(MailExporter, self).__init__(*args, **kwargs)

        self.mbox = None
        self.summary = {}

    def before_export(self, group_name):
        output = f'{group_name}.mbox'

        self.mbox = mbox(output)
        self.summary = dict(indexes=0, topics=0, messages=0)

    def __str__(self):
        return '{indexes} index pages listing {topics} topics with {messages} messages.'.format(**self.summary)

    def after_export(self):
        self.mbox.close()

    def process_index(self, page):
        self.summary['indexes'] += 1

    def process_topic(self, page):
        self.summary['topics'] += 1

    def process_message(self, page):
        id_ = fid, tid, mid = page.id

        headers = {
            'GGE-Url': page.url,
            'GGE-Id': '{}/{}/{}'.format(*id_),
            'GGE-Forum-Id': fid,
            'GGE-Topic-Id': tid,
            'GGE-Message-Id': mid,
        }

        msg = Message(str(page))
        for k, v in headers.items():
            msg.add_header(k, v)

        self.mbox.add(msg)

        self.summary['messages'] += 1
