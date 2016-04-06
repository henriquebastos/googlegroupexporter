import html
import re

from dateutil.parser import parse as dt


class Page:
    def __init__(self, content):
        self.content = content

    @property
    def ids(self):
        return self.IDS.findall(self.content)

    @property
    def links(self):
        return [self.LINK.format(id_) for id_ in self.ids]

    def __str__(self):
        return self.content

    def __next__(self):
        return ''


class TopicPage(Page):
    IDS = re.compile(r'https?://groups.google.com/d/msg/([-\w_/]+)')
    LINK = 'https://groups.google.com/forum/message/raw?msg={}'


class GroupPage(Page):
    IDS = re.compile(r'https?://groups.google.com/d/topic/([-\w_./]+)')
    LINK = 'https://groups.google.com/forum/?_escaped_fragment_=topic/{}'
    NEXT = re.compile(r'https?://groups.google.com/forum/\?_escaped_fragment_=forum/'
                      r'(?P<group>[-_\w]+)%5B(?P<next_first>\d+)-(?P<next_last>\d+)%5D')
    DATA = re.compile(r'href="(https?://[-_/\w.]+?)" title="(.+?)".+?<span>(.+?)</span>.+?'
                      r'<td class="lastPostDate">(.+?)</td>', re.DOTALL)

    def __next__(self):
        match = self.NEXT.search(self.content)
        return match.group(0) if match else ''

    @property
    def data(self):
        return [(link, html.unescape(title), author, dt(date))
                for link, title, author, date in self.DATA.findall(str(self))]
