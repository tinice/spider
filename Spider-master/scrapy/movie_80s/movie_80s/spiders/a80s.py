import scrapy
from inspect import currentframe, getframeinfo
import pyreBloom


class MoviesSpider(scrapy.Spider):
    name = "movies"
    base_url = 'http://www.80s.tw'
    my_key = '80s_movies'.encode('utf8')
    my_host = '127.0.0.1'.encode('utf8')
    my_passwd = 'poluo123'.encode('utf8')
    filter = pyreBloom.PyreBloom(my_key, 100000, 0.01, host=my_host, password=my_passwd)

    @staticmethod
    def to_bytes(s):
        if isinstance(s, str):
            return s.encode('utf8')
        elif isinstance(s, bytes):
            return s
        else:
            raise TypeError

    def start_requests(self):
        urls = [
            'http://www.80s.tw/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for one_tag in self.parse_tags(response):
            url = one_tag['link']
            yield scrapy.Request(response.urljoin(url), callback=self.parse_overall_info)

    @staticmethod
    def parse_tags(response):

        def get_tag():
            try:
                tag = one.css('a::text')[0].extract()
            except IndexError:
                tag = one.css('a > span::text')[0].extract()
            return tag

        res = []
        row_data = response.css('#nav > ul > li')
        ignored_value = ['/', '/zhuanti', '/top/last_update']
        for one in row_data:
            if one.css('a::attr(href)')[0].extract() not in ignored_value:
                tmp_data = {
                    'link': one.css('a::attr(href)')[0].extract(),
                    'tag': get_tag()
                }
                res.append(tmp_data)
        return res

    def parse_overall_info(self, response):
        info_set = response.css('#block3 > div.clearfix.noborder.block1 > ul.me1.clearfix > li')

        if not info_set:
            info_set = response.css('#block3 > div.clearfix.noborder.block1 > ul.me3.clearfix > li')

        if not info_set:
            info_set = response.css('#block4_in > div.lpelmt2.me2li')

        if not info_set:
            self.logger.info('no valid data')
            self.logger.info(response.url)

        next_page = False
        for one in info_set:
            offset = one.css('a::attr(href)')[0].extract()
            tmp = self.to_bytes(offset)
            if tmp not in self.filter:
            	next_page = True
            	self.filter.add(tmp)
            	yield scrapy.Request(url=''.join(['http://www.80s.tw', offset]), callback=self.parse_detail)

        try:
            if next_page:
            	next_url = response.css('div.pager > a:nth-last-child(2)::attr(href)')[0].extract()
            else:
            	next_url = None
        except IndexError:
            next_url = None

        self.logger.info(next_url)
        if next_url is not None:
            next_url = self.base_url + next_url
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse_overall_info)
        else:
            self.logger.info('last page {}'.format(response.url))

    def parse_detail(self, response):
        tmp_data = {}
        tmp_data['name'] = response.css('#minfo > div.info > h1::text')[0].extract().strip()
        tmp_data['img'] = response.css('#minfo > div.img > img::attr(src)')[0].extract().strip()
        try:
            tmp_data['short_description'] = response.css('#minfo > div.info > '
                                                         'span:nth-child(4)::text')[0].extract().strip()
        except IndexError:
            try:
                tmp_data['short_description'] = response.css('#minfo > div.info > span:nth-child(3)::text')[
                    0].extract().strip()
            except IndexError:

                tmp_data['short_description'] = response.css('#minfo > div.info > span:nth-child(5)::text')[
                    0].extract().strip()
        try:
            tmp_data['long_description'] = response.xpath('//*[@id="movie_content"]/text()')[1].extract().strip()
            tmp = response.css('#minfo > div.info > span > a')
            actors = []
            for one in tmp:
                actors.append(one.xpath('text()')[0].extract())
            if actors:
                tmp_data['actors'] = actors
        except IndexError:
            pass
        info = response.css('#minfo > div.info > div > span.span_block')
        for one in info:
            try:
                tmp = one.css('a::text')[0].extract().strip()
            except IndexError:
                try:
                    tmp = one.xpath('text()')[-1].extract().strip()
                except IndexError:
                    frame_info = getframeinfo(currentframe())
                    self.logger.warning('{} {} {} IndexError'.format(__file__, frame_info.lineno, one))
            try:
                if tmp:
                    tmp_data[one.css('span.font_888::text')[0].extract()] = tmp
            except IndexError:
                pass
        info = response.css('span.xunlei.dlbutton1')
        i = 1
        for one in info:
            tmp_data['download_link{0}'.format(i)] = one.css('a::attr(href)')[0].extract()
            i += 1
        # self.logger.debug(tmp_data)
        yield tmp_data

    def closed(self, reason):
        self.logger.info(reason)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
