import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "blockchaininfo"

    custom_settings = {
        'DOWNLOAD_DELAY': 4
    }

    def start_requests(self):

        urls = []
        # offset increment = 50
        # offset limit 2:2500, 4:4650, 8:3550, 16:26450

        limits = {2:2500, 4:4650, 8:3550, 16:26450}
        offsetInc = 50
        for f in [2, 4, 8, 16]:
            offset = 0
            while offset <= limits[f]:
                urls.append('https://blockchain.info/tags?filter={0}&offset={1}'.format(f, offset))
                offset += offsetInc

        # # test
        # urls = [
        #     'https://blockchain.info/tags?filter=2&offset=1000',
        # ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # example source: <td><span class="tag" id="134ZnmvWpGDGSwU6AnkgSEqP3kZ2cKqruh">asdfafdsarewr</span></td>
        filename = 'results.txt'

        results = re.findall(r'<td><span class="tag" id=".+">.+</span></td>', response.body)
        results = [s.replace('<td><span class="tag" id="', '') for s in results]
        results = [s.replace('</span></td>', '') for s in results]
        results = [s.split('">') for s in results]

        with open(filename, 'ab') as f:
            for s in results:
                f.write(s[0] + '\t' + s[1] + '\n')

        self.log('Saved file %s' % filename)