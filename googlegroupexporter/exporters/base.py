from googlegroupexporter.pages import IndexPage, TopicPage, MessagePage


class Exporter:
    GROUP_URL = 'https://groups.google.com/forum/?_escaped_fragment_=forum/{}%5B1-100%5D'

    def __init__(self, session):
        self._session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._call_hook('after_export')

    def __str__(self):
        return ''

    def __iter__(self):
        return iter(self._session.status)

    def _has_hook(self, hook):
        """
        Return true if hook method exist.
        :param hook: a subclass method name.
        :type hook: str
        """
        return hasattr(type(self), hook)

    def _call_hook(self, hook, *args):
        """
        Call a subclass method if implemented, to process
        the downloaded content.

        :param hook: a subclass method name.
        :type hook: str
        :param args: hook arguments
        """
        if self._has_hook(hook):
            fn = getattr(self, hook)
            fn(*args)

    def export(self, group_name):
        start_url = self.GROUP_URL.format(group_name)

        self._call_hook('before_export', group_name)

        self._session.get(start_url, background_callback=self.export_index)

    def export_index(self, session, response):
        page = IndexPage(response.url, response.text)

        # TODO: Put this after the crawler
        self._call_hook('process_index', page)

        # Crawl one more level if we actually use the data.
        if self._has_hook('process_topic'):
            for url in page.links:
                session.get(url, background_callback=self.export_topic)

        session.get(next(page), background_callback=self.export_index)

    def export_topic(self, session, response):
        page = TopicPage(response.url, response.text)

        # TODO: Put this after the crawler
        self._call_hook('process_topic', page)

        # Crawl one more level if we actually use the data.
        if self._has_hook('process_message'):
            for url in page.links:
                session.get(url, background_callback=self.export_message)

    def export_message(self, session, response):
        page = MessagePage(response.url, response.text)

        self._call_hook('process_message', page)
