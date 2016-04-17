import datetime
from pathlib import Path
from unittest import TestCase

from googlegroupexporter.exporters import CsvExporter
from googlegroupexporter.pages import IndexPage

BASE_DIR = Path(__file__).parent


class TestCsvExporter(TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = BASE_DIR / 'index.html'
        page = IndexPage(
            'https://groups.google.com/forum/?_escaped_fragment_=forum/wttd-2015%5B1-100%5D',
            fixture.read_text()
        )

        cls.topic_data = list(CsvExporter.topic_data(page))

    def test_data(self):
        expected = (
            ('wttd-2015', '-Sgu19ezcbA'),
            'https://groups.google.com/d/topic/wttd-2015/-Sgu19ezcbA',
            'Estrela em Orçamentos no GitHub',
            'regis.santos.100',
            datetime.datetime(2016, 3, 30),
        )

        self.assertTupleEqual(expected, self.topic_data[6])

    def test_datetime_from_time(self):
        dt = self.topic_data[0][-1]

        self.assertEqual(7, dt.hour)
        self.assertEqual(56, dt.minute)
