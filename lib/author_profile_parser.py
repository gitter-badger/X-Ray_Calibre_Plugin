# author_profile_parser.py

class AuthorProfileParser(Object):
	def __init__(self, real_asin, custom_asin, connection):
		self._real_asin = real_asin
		self._custom_asin = custom_asin
		self._connection = connection

	def parse(self):
		self.get_author_page()

	def get_author_page(self):
        try:
            self._connection.request('GET', '/dp/' + real_asin, headers=self.HEADERS)
            response = self._connection.getresponse().read()
        except:
            try:
                self._connection.close()
                if self._proxy:
                    self._connection = HTTPConnection(self._http_address, self._http_port)
                    self._connection.set_tunnel('www.amazon.com', 80)
                else:
                    self._connection = HTTPConnection('www.amazon.com')

            	self._connection.request('GET', '/dp/' + real_asin, headers=self.HEADERS)
                response = self._connection.getresponse().read()
            except:
                raise Exception('Could not find author page.')

        # check to make sure there are results
        if '(Author)' not in response:
            raise Exception('Could not find author page.')

        soup = BeautifulSoup(response)