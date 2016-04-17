"""
We use page objects to represent and extract information from each
GoogleGroup's page.

A group will have one or more indexes pages listing topics urls ordered
by recent activity. Index pages are paginated by 100 topics.

Each topic page list all messages urls.

Each message page is a raw email message text.

Our page objects are meant only to make it easy to crawl the group. Any
specific content processing must be implemented in an Exporter subclass.
"""

import re


class Page:
    """
    Base "abstract" class with commons methods to extract information from the HttpResponse.

    Each method must must be supported by subclasses implementing their regex dependencies.
    """
    def __init__(self, url, content):
        self.url = url
        self.content = content

    @property
    def id(self):
        """
        Extract the resource id from GoogleGroup's url.

        It enables you to easily identify a resource while processing your group's data.

        Examples:

        Forum url: https://groups.google.com/forum/?_escaped_fragment_=forum/python-brasil
        Forum id: ('python-brasil',)

        Topic url: https://groups.google.com/forum/?_escaped_fragment_=topic/python-brasil/gQZUryEr_NQ
        Topic id: ('python-brasil', 'gQZUryEr_NQ')

        Message url: https://groups.google.com/forum/message/raw?msg=python-brasil/gQZUryEr_NQ/QKWZHpWFBAAJ
        Message id: ('python-brasil', 'gQZUryEr_NQ', 'QKWZHpWFBAAJ')

        :return: Tuple representing the page id.
        """
        match = self.ID.match(self.url)
        return match.groups() if match else ()

    @property
    def children(self):
        """
        Find all the page's children ids, like topic ids from indexes pages or messages ids from topic pages.
        :return: a list of tuple ids representing each child resource.
        """
        return self.CHILDREN.findall(self.content)

    @property
    def links(self):
        """
        Returns a list of urls to crawl each children.
        :return: list of url strings.
        """
        return [self.LINK.format(*id_) for id_ in self.children]

    def __str__(self):
        """
        Returns the original page body.
        """
        return self.content

    def __next__(self):
        """
        Returns the url for the next page or an empty string.
        """
        return ''


class TopicPage(Page):
    """
    Page object for a single topic with one or more messages.
    """
    ID = re.compile(r'https?://groups.google.com/forum/\?_escaped_fragment_=topic/([-\w_]+)/([-\w_]+)')
    CHILDREN = re.compile(r'https?://groups.google.com/d/msg/([-\w_]+)/([-\w_]+)/([-\w_]+)')
    LINK = 'https://groups.google.com/forum/message/raw?msg={}/{}/{}'
    TITLE = re.compile(r'<h2>(.+)</h2>')

    @property
    def title(self):
        """
        Topic's title.
        """
        match = self.TITLE.search(self.content)
        return match.group(1) if match else ''


class IndexPage(Page):
    """
    Page object for the group's index of topics.
    """
    ID = re.compile(r'https?://groups.google.com/forum/\?_escaped_fragment_=forum/([-\w_]+)')
    CHILDREN = re.compile(r'https?://groups.google.com/d/topic/([-\w_]+)/([-\w_]+)')
    LINK = 'https://groups.google.com/forum/?_escaped_fragment_=topic/{}/{}'
    NEXT = re.compile(r'https?://groups.google.com/forum/\?_escaped_fragment_=forum/'
                      r'(?P<group>[-_\w]+)%5B(?P<next_first>\d+)-(?P<next_last>\d+)%5D')

    def __next__(self):
        match = self.NEXT.search(self.content)
        return match.group(0) if match else ''

class MessagePage(Page):
    """
    Page object for a single message.
    """
    ID = re.compile(r'https?://groups.google.com/forum/message/raw\?msg=([-\w_]+)/([-\w_]+)/([-\w_]+)')
