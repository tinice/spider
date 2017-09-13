# -*- coding: utf-8 -*-
import scrapy
import re


class PeopleSpider(scrapy.Spider):
    name = "people"
    allowed_domains = ["linkedin.com"]
    first_name = re.compile('"firstName":"(.*?)"')
    last_name = re.compile('"lastName":"(.*?)"')
    summary = re.compile('"summary":"(.*?)"')
    location_name = re.compile('"locationName":"(.*?)"')
    occupation = re.compile('"headline":"(.*?)"')
    educations = re.compile('(\{[^\{]*?profile\.Education"[^\}]*?\})')
    school_name = re.compile('"schoolName":"(.*?)"')
    position = re.compile('(\{[^\{]*?profile\.Position"[^\}]*?\})')
    company_name = re.compile('"companyName":"(.*?)"')
    public_id = re.compile('"publicIdentifier":"[^{}]*",')
    company = re.compile('fs_miniCompany: [\d]*&')
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'Linkedin.middlewares.CrawlMiddleware': 543, },
        'DOWNLOAD_DELAY': 0,
    }

    def start_requests(self):
        return [scrapy.Request(url='http://www.linkedin.com/feed/', callback=self.parse_home)]

    def parse_home(self, response):
        text = response.text.replace('&quot;', '"')
        res = self.public_id.findall(text)
        flag = False

        for one in res[1:]:
            self.logger.info(one)
            flag = True
            one = re.split(':', one.split(',')[0])[1][1:-1]
            yield scrapy.Request(url='http://www.linkedin.com/in/' + one + '/', callback=self.parse_people,)

        if not flag:
            self.logger.warning('No data in feed')

    def parse_people(self, response):
        text = response.text
        content = text.replace('&quot;', '"')
        profile_txt = ' '.join(re.findall('(\{[^\{]*?profile\.Profile"[^\}]*?\})', content))
        res = {}
        first_name = self.first_name.findall(profile_txt)
        last_name = self.last_name.findall(profile_txt)
        if first_name and last_name:
            res['name'] = '{} {}'.format(last_name[0], first_name[0])
            res['url'] = response.url
            summary = self.summary.findall(profile_txt)
            if summary:
                res['summary'] = summary[0].replace('&#92;n', '')
            occupation = self.occupation.findall(profile_txt)
            if occupation:
                res['occupation'] = occupation[0]

            location_name = self.location_name.findall(profile_txt)
            if location_name:
                res['location'] = location_name[0]

            educations = self.educations.findall(content)
            if educations:
                res['education'] = ''
            for one in educations:
                school_name = self.school_name.findall(one)
                res['education'] += school_name[0]

            position = self.position.findall(content)
            if position:
                res['position'] = ''
                for one in position:
                    company_name = self.company_name.findall(one)
                    res['position'] += company_name[0]
            yield res
        else:
            self.logger.warning('No matched')
            self.logger.info(profile_txt)

        company = self.company.findall(content)

        self.logger.info(company)

        res = self.public_id.findall(content)
        for one in res[1:]:
            one = re.split(':', one.split(',')[0])[1][1:-1]
            yield scrapy.Request(url='http://www.linkedin.com/in/' + one + '/', callback=self.parse_people)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
