from . import compat
from .exceptions import APIKeyError

from appdirs import user_cache_dir
import json
import os
import requests

API_VERSION = '3'

DEFAULT_CACHE_TTL = 86400  # 24 hours (cached responses are refreshed every 24 hours)
DEFAULT_USER_AGENT = "tmdbsimple"


class Client(object):
    base_uri = 'https://api.themoviedb.org/{version}'.format(version=API_VERSION)
    configured = False
    session = None

    @classmethod
    def configure(cls, cache=True, cache_expire_after=DEFAULT_CACHE_TTL, user_agent=DEFAULT_USER_AGENT):
        if cls.configured:
            return

        # Build requests session
        cls._build_session(cache, cache_expire_after, user_agent)

        # Mark client as configured
        cls.configured = True

    @classmethod
    def get(cls, path, params=None):
        return cls.request('GET', path, params=params)

    @classmethod
    def post(cls, path, params=None, payload=None):
        return cls.request('POST', path, params=params, payload=payload)

    @classmethod
    def delete(cls, path, params=None, payload=None):
        return cls.request('DELETE', path, params=params, payload=payload)

    @classmethod
    def request(cls, method, path, params=None, payload=None):
        # Ensure client is configured
        cls.configure()

        # Send request
        url = cls._get_complete_url(path)
        params = cls._get_params(params)

        response = cls.session.request(
            method, url, params=params,
            data=json.dumps(payload) if payload else payload
        )

        # Process response
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.json()

    @classmethod
    def _build_session(cls, cache, cache_expire_after, user_agent):
        # Retrieve cache directory
        if isinstance(cache, compat.string_types):
            cache_dir = cache
        else:
            cache_dir = user_cache_dir('tmdbsimple')

        # Ensure cache directory exists
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        if cache:
            # Construct cached requests session
            import requests_cache

            cls.session = requests_cache.CachedSession(
                allowable_codes=(200, 404),
                expire_after=cache_expire_after,
                backend='sqlite',
                cache_name=os.path.join(cache_dir, 'tmdbsimple'),
            )
        else:
            # Construct simple requests session
            cls.session = requests.Session()

        # Set user agent
        cls.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Connection': 'close',
            'User-Agent': user_agent
        })

    @classmethod
    def _get_complete_url(cls, path):
        return '{base_uri}/{path}'.format(base_uri=cls.base_uri, path=path)

    @classmethod
    def _get_params(cls, params):
        from . import API_KEY
        if not API_KEY:
            raise APIKeyError

        api_dict = {'api_key': API_KEY}
        if params:
            params.update(api_dict)
        else:
            params = api_dict
        return params
