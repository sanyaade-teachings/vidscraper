# Copyright 2009 - Participatory Culture Foundation
#
# This file is part of vidscraper.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import datetime
import re
import os
import unittest
import urllib
import urlparse

import feedparser

from vidscraper.errors import CantIdentifyUrl
from vidscraper.suites.youtube import YouTubeSuite


CARAMELL_DANSEN_ATOM_DATA = {
    'link': u'http://www.youtube.com/watch?v=J_DV9b0x7v4',
    'title': u'CaramellDansen (Full Version + Lyrics)',
    'description': u'English:\ndo-do-do-oo, yeah-yeah-yeah-yeah\n\nWe wonder are you ready to join us now\nhands in the air\nwe will show you how\ncome and try\ncaramell will be your guide\n\nSo come and move your hips sing wha-a-a\nlook at hips, do it La-la-la\nyou and me can sing this melody\n\nOh-wa-a-a-a\nDance to the beat\nWave your hands together\nCome feel the heat forever and forever\nListen and learn it is time for prancing\nNow we are here with caramel dancing\n\nO-o-oa-oa\nO-o-oa-oa-a-a\nO-o-oa-oa\nO-o-oa-oa-a-a\n\nFrom Sweden to UK we will bring our song, Australia, USA and people of Hong Kong.\nThey have heard this meaning all around the world\n\nSo come and move your hips sing wha-a-a\nLook at your hips, do it La-la-la\nYou and me can sing this melody\n\nSo come and dance to the beat\nWave your hands together\nCome feel the heat forever and forever\nListen and learn it is time for prancing\nNow we are here with caramel dancing\n\n(Dance to the beat\nwave your hands together\ncome feel the heat forever and forever\nlisten and learn it is time for prancing\nnow we are here with caramel dancing)\n\nU-u-ua-ua\nU-u-ua-ua-a-a\nU-u-ua-ua\nU-u-ua-ua-a-a\n\nSo come and dance to the beat\nWave your hands together\nCome feel the heat forever and forever\nListen and learn it is time for prancing\nNow we are here with caramel dancing...\nDance to the beat\nWave your hands together\nCome feel the heat forever and forever\nListen and learn it is time for prancing\nNow we are here with caramel dancing \n\nSwedish:\nVi undrar \xe4r ni redo att vara med\nArmarna upp nu ska ni f\xe5 se\nKom igen\nVem som helst kan vara med\n\nS\xe5 r\xf6r p\xe5 era f\xf6tter\nOa-a-a\nOch vicka era h\xf6fter\nO-la-la-la\nG\xf6r som vi\nTill denna melodi\n\nDansa med oss\nKlappa era h\xe4nder\nG\xf6r som vi g\xf6r\nTa n\xe5gra steg \xe5t v\xe4nster\nLyssna och l\xe4r\nMissa inte chansen\nNu \xe4r vi h\xe4r med\nCaramelldansen\nO-o-oa-oa...\n\nDet blir en sensation \xf6verallt f\xf6rst\xe5s\nP\xe5 fester kommer alla att sl\xe4ppa loss\nKom igen\nNu tar vi stegen om igen\n\nS\xe5 r\xf6r p\xe5 era f\xf6tter\nOa-a-a\nOch vicka era h\xf6fter\nO-la-la-la\nG\xf6r som vi\nTill denna melodi\n\nS\xe5 kom och\nDansa med oss\nKlappa era h\xe4nder\nG\xf6r som vi g\xf6r\nTa n\xe5gra steg \xe5t v\xe4nster\nLyssna och l\xe4r\nMissa inte chansen\nNu \xe4r vi h\xe4r med\nCaramelldansen\n\nDansa med oss\nKlappa era h\xe4nder\nG\xf6r som vi g\xf6r\nTa n\xe5gra steg \xe5t v\xe4nster\nLyssna och l\xe4r\nMissa inte chansen\nNu \xe4r vi h\xe4r med\nCaramelldansen',
    'thumbnail_url': u'http://i.ytimg.com/vi/J_DV9b0x7v4/0.jpg',
    'user': u'DrunkenVuko',
    'user_url': u'http://www.youtube.com/user/DrunkenVuko',
    'flash_enclosure_url': u'http://www.youtube.com/watch?v=J_DV9b0x7v4&feature=youtube_gdata_player',
    'tags': set([
        u"caramell",
        u"dance",
        u"dansen",
        u"hip",
        u"hop",
        u"s\xfcchtig",
        u"geil",
        u"cool",
        u"lustig",
        u"manga",
        u"schweden",
        u"anime",
        u"musik",
        u"music",
        u"funny",
        u"caramelldansen",
        u"U-U-U-Aua",
        u"Music",
    ]),
    'publish_datetime': datetime.datetime(2007, 5, 7, 22, 15, 21),
}


CARAMELL_DANSEN_SEARCH_DESCRIPTION = u"English: do-do-do-oo, yeah-yeah-yeah-yeah We wonder are you ready to join us now hands in the air we will show you how come and try caramell will be your guide So come and move your hips sing wha-aa look at hips, do it La-la-la you and me can sing this melody Oh-wa-aaa Dance to the beat Wave your hands together Come feel the heat forever and forever Listen and learn it is time for prancing Now we are here with caramel dancing Oo-oa-oa Oo-oa-oa-aa Oo-oa-oa Oo-oa-oa-aa From Sweden to UK we will bring our song, Australia, USA and people of Hong Kong. They have heard this meaning all around the world So come and move your hips sing wha-aa Look at your hips, do it La-la-la You and me can sing this melody So come and dance to the beat Wave your hands together Come feel the heat forever and forever Listen and learn it is time for prancing Now we are here with caramel dancing (Dance to the beat wave your hands together come feel the heat forever and forever listen and learn it is time for prancing now we are here with caramel dancing) Uu-ua-ua Uu-ua-ua-aa Uu-ua-ua Uu-ua-ua-aa So come and dance to the beat Wave your hands together Come feel the heat forever and forever Listen and learn it is time for prancing Now we are here with caramel dancing... Dance to the beat Wave your hands together Come feel the heat forever and forever Listen and learn it is time for prancing Now we are here with caramel dancing Swedish: Vi undrar \xe4r ni redo att vara med Armarna upp nu ska ni f\xe5 se Kom <b>...</b>"


class YouTubeTestCase(unittest.TestCase):
    def setUp(self):
        self.suite = YouTubeSuite()

    @property
    def data_file_dir(self):
        if not hasattr(self, '_data_file_dir'):
            test_dir = os.path.abspath(os.path.dirname(
                                                os.path.dirname(__file__)))
            self._data_file_dir = os.path.join(test_dir, 'data', 'youtube')
        return self._data_file_dir


class YouTubeOembedTestCase(YouTubeTestCase):
    def setUp(self):
        YouTubeTestCase.setUp(self)
        self.base_url = "http://www.youtube.com/watch?v=J_DV9b0x7v4"
        self.video = self.suite.get_video(url=self.base_url)

    def test_short_url(self):
        url = 'http://youtu.be/J_DV9b0x7v4'
        self.assertTrue(self.suite.handles_video_url(url))

    def test_jumbled_param_url(self):
        url = 'http://www.youtube.com/watch?feature=youtu.be&v=J_DV9b0x7v4'
        self.assertTrue(self.suite.handles_video_url(url))

    def test_get_oembed_url(self):
        escaped_url = urllib.quote_plus(self.video.url)
        expected = "http://www.youtube.com/oembed?url=%s" % escaped_url
        oembed_url = self.suite.get_oembed_url(self.video)
        self.assertEqual(oembed_url, expected)

    def test_parse_oembed_response(self):
        oembed_file = open(os.path.join(
                            self.data_file_dir, 'oembed.json'))
        data = self.suite.parse_oembed_response(oembed_file.read())
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(set(data), self.suite.oembed_fields)
        expected_data = {
            'embed_code': u'<object width="459" height="344"><param '
                            'name="movie" value="http://www.youtube.com/v/'
                            'J_DV9b0x7v4?version=3"></param><param '
                            'name="allowFullScreen" value="true"></param>'
                            '<param name="allowscriptaccess" '
                            'value="always"></param><embed src="http://www.'
                            'youtube.com/v/J_DV9b0x7v4?version=3" '
                            'type="application/x-shockwave-flash" width="459" '
                            'height="344" allowscriptaccess="always" '
                            'allowfullscreen="true"></embed></object>',
            'user_url': u'http://www.youtube.com/user/DrunkenVuko',
            'thumbnail_url': u'http://i3.ytimg.com/vi/J_DV9b0x7v4/hqdefault.jpg',
            'user': u'DrunkenVuko',
            'title': u'CaramellDansen (Full Version + Lyrics)'
        }
        self.assertEqual(data, expected_data)


class YouTubeApiTestCase(YouTubeTestCase):
    def setUp(self):
        YouTubeTestCase.setUp(self)
        self.base_url = "http://www.youtube.com/watch?v=J_DV9b0x7v4"
        self.video = self.suite.get_video(url=self.base_url)

    def test_get_api_url(self):
        api_url = self.suite.get_api_url(self.video)
        self.assertEqual(api_url,
                        "http://gdata.youtube.com/feeds/api/videos/J_DV9b0x7v4")

    def test_parse_api_response(self):
        api_file = open(os.path.join(self.data_file_dir, 'api.atom'))
        data = self.suite.parse_api_response(api_file.read())
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(set(data), self.suite.api_fields)
        data['tags'] = set(data['tags'])
        expected_data = CARAMELL_DANSEN_ATOM_DATA
        self.maxDiff = None
        self.assertEqual(data, expected_data)


class YouTubeSearchTestCase(YouTubeTestCase):
    def setUp(self):
        YouTubeTestCase.setUp(self)
        search_file = open(os.path.join(self.data_file_dir, 'search.atom'))
        response = feedparser.parse(search_file.read())
        self.results = self.suite.get_search_results(response)

    def test_parse_search_result(self):
        self.maxDiff = None
        data = self.suite.parse_search_result(self.results[0])
        self.assertTrue(isinstance(data, dict))
        data['tags'] = set(data['tags'])
        expected_data = CARAMELL_DANSEN_ATOM_DATA.copy()
        expected_data['description'] = CARAMELL_DANSEN_SEARCH_DESCRIPTION
        # TODO: Perhaps google will fix this strange difference someday.
        if 'UUU-Aua' in data['tags']:
            data['tags'].remove('UUU-Aua')
            data['tags'].add('U-U-U-Aua')
        for key in expected_data:
            self.assertTrue(key in data)
            self.assertEqual(data[key], expected_data[key])

    def test_next_search_page_url(self):
        response = {
            'opensearch_startindex': '1',
            'opensearch_itemsperpage': '50',
            'opensearch_totalresults': '10',
        }
        new_url = self.suite.get_next_search_page_url("caramell dansen",
                                                      response)
        self.assertTrue(new_url is None)
        response['opensearch_totalresults'] = '100'
        new_url = self.suite.get_next_search_page_url("caramell dansen",
                                                      response)
        self.assertFalse(new_url is None)
        parsed = urlparse.urlparse(new_url)
        params = urlparse.parse_qs(parsed.query)
        self.assertEqual(params['start_index'][0], '51')
        self.assertEqual(params['max_results'][0], '50')