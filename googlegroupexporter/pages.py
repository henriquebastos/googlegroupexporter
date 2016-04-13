import html
import re

from dateutil.parser import parse as dt


class Page:
    def __init__(self, content):
        self.content = content

    @property
    def id(self):
        match = self.ID.search(self.content)
        return match.groups() if match else ''

    @property
    def children(self):
        return self.CHILDREN.findall(self.content)

    @property
    def links(self):
        return [self.LINK.format(*id_) for id_ in self.children]

    def __str__(self):
        return self.content

    def __next__(self):
        return ''


class TopicPage(Page):
    ID = re.compile(r'https?://groups.google.com/d/topic/([-\w_]+)/([-\w_]+)')
    CHILDREN = re.compile(r'https?://groups.google.com/d/msg/([-\w_]+)/([-\w_]+)/([-\w_]+)')
    LINK = 'https://groups.google.com/forum/message/raw?msg={}/{}/{}'
    TITLE = re.compile(r'<h2>(.+)</h2>')

    @property
    def title(self):
        match = self.TITLE.search(self.content)
        return match.group(1) if match else ''


class GroupPage(Page):
    ID = re.compile(r'https?://groups.google.com/d/forum/([-\w_]+)')
    CHILDREN = re.compile(r'https?://groups.google.com/d/topic/([-\w_]+)/([-\w_]+)')
    LINK = 'https://groups.google.com/forum/?_escaped_fragment_=topic/{}/{}'
    NEXT = re.compile(r'https?://groups.google.com/forum/\?_escaped_fragment_=forum/'
                      r'(?P<group>[-_\w]+)%5B(?P<next_first>\d+)-(?P<next_last>\d+)%5D')
    DATA = re.compile(r'href="(https?://groups.google.com/d/topic/([-_\w.]+)/([-_\w.]+))" title="(.+?)".+?<span>(.+?)</span>.+?'
                      r'<td class="lastPostDate">(.+?)</td>', re.DOTALL)

    def __next__(self):
        match = self.NEXT.search(self.content)
        return match.group(0) if match else ''

    @property
    def data(self):
        return [((forum, topic), link, html.unescape(title), author, dt(date))
                for link, forum, topic, title, author, date in self.DATA.findall(str(self))]
