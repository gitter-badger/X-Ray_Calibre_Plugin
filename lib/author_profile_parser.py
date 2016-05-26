# author_profile_parser.py
import re
from httplib import HTTPConnection
from calibre.ebooks.BeautifulSoup import BeautifulSoup

class AuthorProfileParser(Object):
    HEADERS = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0"}
	def __init__(self, real_asin, custom_asin, connection):
		self._real_asin = real_asin
		self._custom_asin = custom_asin
		self._connection = connection

	def parse(self):
		self.get_author_url()
        self.get_bio()

    def get_author_url(self):
        response = self.get_url_response('/dp/' + self._real_asin)

        # check to make sure there are results
        if '(Author)' not in response or 'Visit Amazon\'s' not in response:
            raise Exception('Could not find page.')

        soup = BeautifulSoup(response)
        author = soup.findAll('span', text='(Author)')[0].parent.parent.parent
        self._author_url = author.findAll('a', text=re.compile('Visit Amazon\'s .+ Page'))[0]['href']

    def get_bio(self):
        response = self.get_url_response(self._author_url)
        soup = BeautifulSoup(response)
        bio = soup.findAll('div', {'id': 'ap-bio'})[0]
        self._bio = bio.find('span')['text'].strip()

	def get_url_response(self, url):
        try:
            self._connection.request('GET', url, headers=self.HEADERS)
            response = self._connection.getresponse().read()
        except:
            try:
                self._connection.close()
                if self._proxy:
                    self._connection = HTTPConnection(self._http_address, self._http_port)
                    self._connection.set_tunnel('www.amazon.com', 80)
                else:
                    self._connection = HTTPConnection('www.amazon.com')

            	self._connection.request('GET', url, headers=self.HEADERS)
                response = self._connection.getresponse().read()
            except:
                raise Exception('Could not find page.')

        return response