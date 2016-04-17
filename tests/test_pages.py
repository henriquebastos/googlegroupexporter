from pathlib import Path
from unittest import TestCase

from googlegroupexporter.pages import IndexPage, TopicPage, MessagePage

BASE_DIR = Path(__file__).parent


class TestIndexPage(TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = BASE_DIR / 'index.html'
        cls.url = 'https://groups.google.com/forum/?_escaped_fragment_=forum/wttd-2015%5B1-100%5D'
        cls.page = IndexPage(cls.url, fixture.read_text())

    def test_url(self):
        self.assertEqual(self.url, self.page.url)

    def test_id(self):
        self.assertEqual(('wttd-2015',), self.page.id)

    def test_children_len(self):
        self.assertEqual(20, len(self.page.children))

    def test_children(self):
        self.assertEqual(('wttd-2015', 'BqKNl92tGG8'), self.page.children[0])

    def test_links_len(self):
        self.assertEqual(20, len(self.page.links))

    def test_links(self):
        expected = 'https://groups.google.com/forum/?_escaped_fragment_=topic/wttd-2015/BqKNl92tGG8'
        self.assertEqual(expected, self.page.links[0])

    def test_next(self):
        expected = 'https://groups.google.com/forum/?_escaped_fragment_=forum/wttd-2015%5B21-40%5D'
        self.assertEqual(expected, next(self.page))


class TestTopicPage(TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = BASE_DIR / 'topic.html'
        cls.url = 'https://groups.google.com/forum/?_escaped_fragment_=topic/wttd-2015/BqKNl92tGG8'
        cls.page = TopicPage(cls.url, fixture.read_text())

    def test_url(self):
        self.assertEqual(self.url, self.page.url)

    def test_children_len(self):
        self.assertEqual(88, len(self.page.children))

    def test_children(self):
        self.assertEqual(('wttd-2015', 'BqKNl92tGG8', 'b62NyYWpAwAJ'), self.page.children[0])

    def test_id(self):
        self.assertEqual(('wttd-2015', 'BqKNl92tGG8'), self.page.id)

    def test_links_len(self):
        self.assertEqual(88, len(self.page.links))

    def test_links(self):
        expected = 'https://groups.google.com/forum/message/raw?msg=wttd-2015/BqKNl92tGG8/b62NyYWpAwAJ'
        self.assertEqual(expected, self.page.links[0])

    def test_next(self):
        self.assertEqual('', next(self.page))

    def test_title(self):
        self.assertEqual('Roadmap WTTD', self.page.title)


class TestMessagePage(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = 'https://groups.google.com/forum/message/raw?msg=wttd-2015/BqKNl92tGG8/b62NyYWpAwAJ'
        cls.page = MessagePage(cls.url, 'CONTENT')

    def test_url(self):
        self.assertEqual(self.url, self.page.url)

    def test_content(self):
        self.assertEqual('CONTENT', str(self.page))
