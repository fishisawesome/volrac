#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-08 19:39:22
# @Author  : Carlo Villamayor (carlov@volrac.net)
# @Link    : http://github.com/fishisawesome/murakami.py
# @Version : 0.1

import os
import bs4
import requests
import re

def get_soup(url):
    """
    gets BeautifulSoup object of downloaded url
    """

    # add fake headers to avoid being detected as a bot
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = r.content
    soup = bs4.BeautifulSoup(html,'html.parser')

    return soup

def main():
    final_quotes = []
    quote_source = 'https://www.goodreads.com/author/quotes/3354.Haruki_Murakami'
    soup = get_soup(quote_source)
    quotes = soup.find_all('div',{'class':'quoteText'})
    for quote in quotes:
        final_quote = {}
        quote_text = quote.get_text().strip().encode("utf-8")
        match = re.search(r'“(.*)”',quote_text)
        if match:
            quote_text = match.group(1)
            final_quote['quote'] = quote_text

            span = quote.find('span')
            if span:
                book = span.find('a',{'class':'authorOrTitle'}).get_text().strip()
                final_quote['book'] = book

                final_quotes.append(final_quote)

    for quote in final_quotes:
        print quote['quote'], ' - ', quote['book']
        print '----------\n\n'

    return True

if __name__ == '__main__':
    main()