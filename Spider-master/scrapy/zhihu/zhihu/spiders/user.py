# -*- coding: utf-8 -*-
import scrapy
import re
import json
from zhihu.items import ZhihuItem


class UserSpider(scrapy.Spider):
    name = "user"
    allowed_domains = ["zhihu.com"]
    count = {}
    get_new_user = True

    def start_requests(self, urls=None):
        if not urls:
            urls = self.settings.getlist('URL')
        for one in urls:
            yield scrapy.Request(url=one, callback=self.parse)

    def parse(self, response):
        text = response.text.replace('&quot;', '"')
        next_url = 'https:' + re.findall('"next":"http://.*desktop=True', text)[0].split(':')[2].replace('amp;', '')
        yield scrapy.Request(url=next_url, meta={'referer': response.url}, callback=self.parse_activities)

    def parse_activities(self, response):
        data = json.loads(response.text)
        name = data['data'][0]['actor']['name']
        if name not in self.count:
            self.count[name] = 0
            if len(self.count) > 1000:
                self.get_new_user = False
                self.logger.info('more than 1000 user')
        else:
            self.count[name] += 1
        # with open('{}_{}.json'.format(name, self.count[name]), 'w') as fobj:
        #     json.dump(data, fobj)

        for one in self.process_data(name, data['data']):
            yield one

        if self.get_new_user:
            urls = self.process_urls(data['data'])
            for one in urls:
                yield scrapy.Request(url=one, callback=self.parse)

        if not data['paging']['is_end']:
            next_url = data['paging']['next'].replace('http', 'https')
            self.logger.info('next_page {}'.format(next_url))
            yield scrapy.Request(url=next_url, meta={'referer': response.url},
                                 callback=self.parse_activities)
        else:
            self.logger.info('Arrived end page')

    def process_urls(self, data):
        urls = set()
        for one in data:
            if one['target']['type'] == 'answer':
                tmp = one['target']['author']['url_token']
                if tmp:
                    tmp = ''.join(['https://www.zhihu.com/people/', tmp, '/activities'])
                    urls.add(tmp)
                tmp = one['target']['question']['author']['url_token']
                if tmp:
                    tmp = ''.join(['https://www.zhihu.com/people/', tmp, '/activities'])
                    urls.add(tmp)
            else:
                if one['target']['type'] == 'question':
                    tmp = one['target']['author']['url_token']
                    if tmp:
                        tmp = ''.join(['https://www.zhihu.com/people/', tmp, '/activities'])
                        urls.add(tmp)
                else:
                    pass
        return urls

    def process_data(self, name, data):
        res_list = []
        for one in data:
            try:
                # 关注了问题
                if one['verb'] == 'QUESTION_FOLLOW':
                    res = {'type': 'QUESTION_FOLLOW', 'created_time': one['created_time'],
                           'questions_id': one['target']['id'],
                           'title': one['target']['title']}
                    # print(res)
                # 回答了问题
                elif one['verb'] == 'ANSWER_CREATE':
                    res = {'type': 'ANSWER_CREATE', 'created_time': one['created_time'],
                           'questions_id': one['target']['id'],
                           'title': one['target']['question']['title']}
                    # print(res)
                # 赞同了回答
                elif one['verb'] == 'ANSWER_VOTE_UP':
                    res = {'type': 'ANSWER_VOTE_UP', 'created_time': one['created_time'],
                           'questions_id': one['target']['question']['id'], 'title': one['target']['question']['title'],
                           'answer_id': one['target']['url']}
                    # print(res)
                # 收藏了回答
                elif one['verb'] == 'MEMBER_COLLECT_ANSWER':
                    res = {'type': 'MEMBER_COLLECT_ANSWER', 'created_time': one['created_time'],
                           'questions_id': one['target']['question']['id'], 'title': one['target']['question']['title'],
                           'answer_id': one['target']['url']}
                    # print(res)
                # 赞了文章
                elif one['verb'] == 'MEMBER_VOTEUP_ARTICLE':
                    res = {'type': 'MEMBER_VOTEUP_ARTICLE', 'created_time': one['created_time'],
                           'title': one['target']['title'],
                           'articles_id': one['target']['url'],
                           'author': one['target']['author']['name']}
                    # print(res)
                    # 关注了圆桌
                elif one['verb'] == 'MEMBER_FOLLOW_ROUNDTABLE':
                    res = {'type': 'MEMBER_FOLLOW_ROUNDTABLE', 'created_time': one['created_time'],
                           'title': one['target']['name'],
                           'url': one['target']['url']}
                    # print(res)
                # 关注了话题
                elif one['verb'] == 'TOPIC_FOLLOW':
                    res = {'type': 'TOPIC_FOLLOW', 'created_time': one['created_time'], 'title': one['target']['name'],
                           'url': one['target']['url']}
                    # print(res)
                # 关注了专栏
                elif one['verb'] == 'MEMBER_FOLLOW_COLUMN':
                    res = {'type': 'MEMBER_FOLLOW_COLUMN', 'created_time': one['created_time'],
                           'title': one['target']['title'],
                           'url': one['target']['url']}
                    # print(res)
                # 收藏了文章
                elif one['verb'] == 'MEMBER_COLLECT_ARTICLE':
                    res = {'type': 'MEMBER_COLLECT_ARTICLE', 'created_time': one['created_time'],
                           'title': one['target']['title'],
                           'articles_id': one['target']['url'],
                           'author': one['target']['author']['name']}
                    # print(res)
                # 赞了分享
                elif one['verb'] == 'MEMBER_CREATE_PIN':
                    res = {'type': 'MEMBER_CREATE_PIN', 'created_time': one['created_time'],
                           'pin_id': one['target']['url'], }
                # 关注了收藏夹
                elif one['verb'] == 'MEMBER_FOLLOW_COLLECTION':
                    res = {'type': 'MEMBER_CREATE_PIN', 'created_time': one['created_time'],
                           'title': one['target']['title'], 'url': one['target']['url']}
                # 参加了live
                elif one['verb'] == 'LIVE_JOIN':
                    res = {'type': 'LIVE_JOIN', 'created_time': one['created_time'],
                           'title': one['target']['subject'], 'id': one['target']['id']}
                else:
                    res = None
                    # self.logger.debug(one)
                res_list.append(ZhihuItem({'name': name, 'action': res}))
            except Exception as e:
                self.logger.info(e)
                self.logger.info(one)
        return res_list


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
