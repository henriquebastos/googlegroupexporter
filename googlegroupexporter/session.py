import logging
from http.cookiejar import MozillaCookieJar

import requests
from requests_futures.sessions import FuturesSession
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from cachecontrol.heuristics import ExpiresAfter


logger = logging.getLogger(__name__)


class ProgressStatus:
    def __init__(self):
        self._total, self._done = 0, 0

    def add(self, future):
        self._total += 1

    def done(self, future):
        self._done += 1

    def progress(self):
        return self._done, self._total

    def finished(self):
        return self._total == self._done

    def __iter__(self):
        while True:
            yield self.progress()

            if self.finished():
                yield self.progress()  # make sure we inform the final status
                raise StopIteration


class ProgressFuturesSession(FuturesSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.status = ProgressStatus()

    def request(self, *args, **kwargs):
        future = super().request(*args, **kwargs)
        future.add_done_callback(self.status.done)
        self.status.add(future)


def session_factory(cookie_file=None, max_workers=10, cache_dir=None, cache_days=7, cache_forever=False):
        session = requests.Session()

        if cookie_file:
            cookies = MozillaCookieJar(cookie_file)
            cookies.load()
            session.cookies = cookies

        if cache_dir:
            session = CacheControl(
                session,
                cache=FileCache(cache_dir, forever=cache_forever),
                heuristic=ExpiresAfter(days=cache_days)
            )

        session = ProgressFuturesSession(max_workers=max_workers, session=session)

        return session
