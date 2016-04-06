from pathlib import Path
from unittest import TestCase

import datetime

from googlegroupexporter.pages import GroupPage, TopicPage


class PageTest(TestCase):
    BASE_DIR = Path(__file__).parent

    @classmethod
    def setUpClass(cls):
        fixture = cls.BASE_DIR / cls.fixture
        with fixture.open() as f:
            cls.page = cls.page_class(f.read())


class TestGroupPage(PageTest):
    page_class = GroupPage
    fixture = 'topic-index.html'

    def test_ids_len(self):
        self.assertEqual(20, len(self.page.ids))

    def test_ids(self):
        self.assertEqual('wttd-2015/BqKNl92tGG8', self.page.ids[0])

    def test_links_len(self):
        self.assertEqual(20, len(self.page.links))

    def test_links(self):
        expected = 'https://groups.google.com/forum/?_escaped_fragment_=topic/wttd-2015/BqKNl92tGG8'
        self.assertEqual(expected, self.page.links[0])

    def test_next(self):
        expected = 'https://groups.google.com/forum/?_escaped_fragment_=forum/wttd-2015%5B21-40%5D'
        self.assertEqual(expected, next(self.page))

    def test_data(self):
        expected = (
            'https://groups.google.com/d/topic/wttd-2015/-Sgu19ezcbA',
            'Estrela em Orçamentos no GitHub',
            'regis.santos.100',
            datetime.datetime(2016, 3, 30),
        )
        self.assertTupleEqual(expected, self.page.data[6])

    def test_datetime_from_time(self):
        dt = self.page.data[0][-1]

        self.assertEqual(7, dt.hour)
        self.assertEqual(56, dt.minute)


class TestTopicPage(PageTest):
    page_class = TopicPage
    fixture = 'message-index.html'

    def test_ids_len(self):
        self.assertEqual(88, len(self.page.ids))

    def test_ids(self):
        self.assertEqual('wttd-2015/BqKNl92tGG8/b62NyYWpAwAJ', self.page.ids[0])

    def test_links_len(self):
        self.assertEqual(88, len(self.page.links))

    def test_links(self):
        expected = 'https://groups.google.com/forum/message/raw?msg=wttd-2015/BqKNl92tGG8/b62NyYWpAwAJ'
        self.assertEqual(expected, self.page.links[0])

    def test_next(self):
        self.assertEqual('', next(self.page))
