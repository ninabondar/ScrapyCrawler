import scrapy
import re


class EminemSpider(scrapy.Spider):
    name = 'eminem_spider'  # this var is a must

    def handle_error(self, failure):
        f = open('log.txt', 'a')
        f.write(failure.request.url + '\n')
        f.close()
        self.log("Request failed: %s" % failure.request)

    def start_requests(self):  # quoted from docs: "This is the method called by Scrapy when the spider is opened
        # for scraping when no particular URLs are specified."
        urls = [
            'http://www.azlyrics.com/e/eminem.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, errback=self.handle_error)

    def parse(self, response):
        """
        param response is an object storing following data:
            - html text of the document (web page)
            - url of the document
            - http-headers of the http(s)-response from the server
        """
        regexp_pattern_relative = re.compile('<a href="..\/lyrics\/(.)*<\/a>')
        regexp_pattern_absolute = re.compile('<a href="(.)*\/lyrics\/(.)*<\/a>')  # for detecting abs links
        song_list = []  # future lyrics links
        links = response.css("a")  # html tag that we need
        for link in links:
            if regexp_pattern_relative.match(link.css("a").extract_first()):
                # for creating abs links from not
                url = response.url + "/../" + link.css("a::attr(href)").extract_first()
                song_list.append(url)
                yield scrapy.Request(url=url, callback=self.parse_lyrics, errback=self.handle_error)  # def parse_lyrics will take the lyrics out
            elif regexp_pattern_absolute.match(link.css("a").extract_first()):
                url = link.css("a::attr(href)").extract_first()
                song_list.append(url)
                yield scrapy.Request(url=url, callback=self.parse_lyrics, errback=self.handle_error)
        yield {
            'url': response.url,
            'title': response.css("title::text").extract_first(),
            'songs': song_list
        }

    def parse_lyrics(self, response):
        title = response.xpath('//div[contains(@class,"div-share")]/h1/text()').extract_first().replace('" lyrics', '').replace('"', '')
        lyrics_div = response.xpath('//div[contains(@class, "col-xs-12") and contains(@class, "col-lg-8") and contains(@class,"text-center")]')
        lyrics = lyrics_div.xpath('//div')[21].xpath('//div/text()').extract()
        lyrics = "".join(lyrics).replace("Visit www.azlyrics.com for these lyrics.", "").strip()
        album = response.xpath('//div[contains(@class,"panel")  and contains(@class,"album-panel") and contains(@class, "noprint")]/a/text()').extract_first()
        regexp_year = re.compile('\d{4}')
        year = None
        if album:
            year_match = regexp_year.search(album)
            if year_match:
                year = year_match.group(0)  # the first found
        yield {
            'title': title,
            'lyrics': lyrics,
            'album': album,
            'year': year
        }
