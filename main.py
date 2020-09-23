#!/usr/bin/env python
# -*- coding: utf-8 -*-

from googlesearch import search
from bs4 import BeautifulSoup as bs
import requests as r
import re

import traceback
import constants

from fabulous import text


def error_googler(func):
    def wrapper():
        try:
            func()
        except Exception as e:
            error_googler = ErrorGoogler()
            error_googler.complete_traceback()
            error_googler.automatic_answer(e)
            error_googler.manual_answer()

            pass

    return wrapper()


class TracebackError(object):
    def __init__(self):
        self.traceback = traceback.format_exc()

    def complete_traceback(self):
        print('Work in progress\n\n\n')


class GoogleSearch(object):
    def __init__(self, query):
        self.query = query
        self.search_results = []

    def _search(self):
        for url in search(self.query,
                          tld='com',
                          lang='en',
                          num=10,
                          start=0,
                          stop=10,
                          pause=2.0):
            if self._valid_website(url):
                self.search_results.append(url)

    @staticmethod
    def _valid_website(url):
        if constants.WEBSITE in url:
            return True

    def return_results(self):
        self._search()
        return self.search_results


class WebsiteScraping(object):
    def __init__(self, url):
        self.url = url
        self.text_answer = ''

    @staticmethod
    def remove_html_tags(text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def _scrape_url(self):

        html_page = r.get(self.url).text
        soup = bs(html_page, 'html.parser')

        # For now only first answer of every page
        # Can change find_all in simple find
        answer = soup.find_all("div", class_="answercell post-layout--right")[0]

        tag_list = answer.find_all()
        skip_tags = list()

        for tag in tag_list:

            if tag not in skip_tags:

                # MODIFY LOGIC REMOVE HTML TAGS

                if tag.name in ['p', 'code']:

                    if tag.name == 'p':
                        code_inside_paragraph = tag.find_all('code')

                        # if there is code within the paragraph
                        if len(code_inside_paragraph) > 0:
                            paragraph = self.remove_html_tags(str(tag))
                            self.text_answer += paragraph
                            self.text_answer += '\n'

                            for code_tag in code_inside_paragraph:
                                skip_tags.append(code_tag)

                        else:
                            # double print the code that was in the paragraph
                            self.text_answer += tag.string
                            self.text_answer += '\n'

                    else:
                        # double print the code that was in the paragraph
                        self.text_answer += '\n'
                        self.text_answer += tag.string
                        self.text_answer += '\n'

    def return_text_answer(self):
        self._scrape_url()
        return self.text_answer


class AnswerFinder(object):
    def __init__(self):
        self.current_url = None
        self.current_answer_text = None

    def __repr__(self):
        pass

    def __str__(self):
        l1 = "\n-----------------------------------------------------------------------------------------------------\n"
        l2 = "*****************************************************************************************************\n"
        l3 = "-----------------------------------------------------------------------------------------------------\n"

        l4 = self.current_answer_text

        l5 = "\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n"
        l6 = 'To see more, go to {}\n'.format(self.current_url)
        l7 = "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n"
        return l1+l2+l3+l4+l5+l6+l7

    def _automatic_query(self, e):
        automatic_query = str(type(e)).split()[1].split("'")[1]
        query = self._append_website(automatic_query)
        return query

    def _manual_query(self):
        manual_query = input("Please write what you would like to google: ")
        query = self._append_website(manual_query)
        return query

    @staticmethod
    def _append_website(query):
        return query + ' ' + constants.WEBSITE

    def _want_to_continue(self):
        text1 = "Do you want to continue to the next answer?\n"
        text2 = "Press:\n\t 'y' for YES\n\t 'n' for NO\n\tEnter: "
        while True:
            answer = input(text1+text2)
            if answer in ['y', 'n']:
                break
        return answer == 'y'

    def _submit(self, query):
        google_search = GoogleSearch(query)
        search_results = google_search.return_results()
        print("\n{} RESULTS COMPATIBLE\n".format(len(search_results)))

        for url in search_results:
            self.current_url = url
            website_scraping = WebsiteScraping(self.current_url)
            self.current_answer_text = website_scraping.return_text_answer()
            print(self)

            if not self._want_to_continue():
                return None

    def automatic_answer(self, e):
        query = self._automatic_query(e)
        self._submit(query)

    def manual_answer(self):
        query = self._manual_query()
        self._submit(query)


class ErrorGoogler(object):
    def __init__(self):
        print
        text.Text("Error Googler", color='#0099ff', shadow=True, skew=5)

    def complete_traceback(self):
        traceback_error = TracebackError()
        traceback_error.complete_traceback()

    def automatic_answer(self, e):
        automatic_answer_finder = AnswerFinder()
        automatic_answer_finder.automatic_answer(e)

    def manual_answer(self):
        manual_answer_finder = AnswerFinder()
        manual_answer_finder.manual_answer()


__all__ = ['error_googler']






