import requests
import time
import logging

logger = logging.getLogger("HttpClient")


class HttpClient:

    def __init__(self, base_url="http://127.0.0.1:8000", timeout=5):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        kwargs.setdefault('timeout', self.timeout)
        logger.info(f'请求{method} -> {url}')
        start = time.time()
        resp = self.session.request(method, url, **kwargs)
        logger.info(f'响应{resp.status_code}, 耗时{time.time() - start:.2f}s')
        return resp

    def get(self, path, params=None):
        return self._request('GET', path, params=params)

    def post(self, path, json=None):
        return self._request('POST', path, json=json)

    def delete(self, path, headers=None):
        return self._request('DELETE', path, headers=headers)
