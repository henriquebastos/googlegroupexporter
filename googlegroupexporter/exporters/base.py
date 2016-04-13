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

    def __str__(self):
        return ''

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
