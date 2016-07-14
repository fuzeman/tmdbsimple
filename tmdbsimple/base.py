# -*- coding: utf-8 -*-

"""
tmdbsimple.base
~~~~~~~~~~~~~~~
This module implements the base class of tmdbsimple.

Created by Celia Oakley on 2013-10-31.

:copyright: (c) 2013-2014 by Celia Oakley
:license: GPLv3, see LICENSE for more details
"""

from .client import Client


class TMDB(object):
    BASE_PATH = ''
    URLS = {}

    def _get_path(self, key):
        return self.BASE_PATH + self.URLS[key]

    def _get_id_path(self, key):
        return self._get_path(key).format(id=self.id)

    def _get_guest_session_id_path(self, key):
        return self._get_path(key).format(
            guest_session_id=self.guest_session_id)
    
    def _get_credit_id_path(self, key):
        return self._get_path(key).format(credit_id=self.credit_id)

    def _get_id_season_number_path(self, key):
        return self._get_path(key).format(id=self.id,
            season_number=self.season_number)

    def _get_series_id_season_number_episode_number_path(self, key):
        return self._get_path(key).format(series_id=self.series_id,
            season_number=self.season_number,
            episode_number=self.episode_number)

    def _GET(self, path, params=None):
        return Client.get(path, params)

    def _POST(self, path, params=None, payload=None):
        return Client.post(path, params. payload)

    def _DELETE(self, path, params=None, payload=None):
        return Client.delete(path, params, payload)

    def _set_attrs_to_values(self, response={}):
        """
        Set attributes to dictionary values.

        - e.g.
        >>> import tmdbsimple as tmdb
        >>> movie = tmdb.Movies(103332)
        >>> response = movie.info()
        >>> movie.title  # instead of response['title']
        """
        if isinstance(response, dict):
            for key in response.keys():
                setattr(self, key, response[key])

