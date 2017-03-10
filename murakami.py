#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-08 19:39:22
# @Author  : Carlo Villamayor (carlov@volrac.net)
# @Link    : http://github.com/fishisawesome/murakami.py
# @Version : 0.1

from __future__ import division
import os
import bs4
import requests
import re
import nltk
import numpy
import pandas
from pandas import DataFrame

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

    quotes_with_score = []
    for quote in final_quotes:
        quote_with_score = {}
        splitter = nltk.data.load('/Users/V/Documents/simplebox/volrac/punkt/english.pickle')
        tokenizer = nltk.tokenize.TreebankWordTokenizer()

        sentences = splitter.tokenize(quote['quote'].decode('utf-8').strip())
        tokenized_sentences = [tokenizer.tokenize(word) for word in sentences]
        pos = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]

        with open('sentiment/positive.txt') as sentiment:
            content = sentiment.readlines()
        
        positive_words = [x.strip() for x in content]

        with open('sentiment/negative.txt') as sentiment:
            content = sentiment.readlines()
        
        negative_words = [x.strip() for x in content]

        happy_words = []
        sad_words = []

        for p in pos:
            for w in p:
                if w[0] in positive_words:
                    happy_words.append(w[0])
                if w[0] in negative_words:
                    sad_words.append(w[0])

        
        total_words = len(tokenizer.tokenize(quote['quote']))
        percentage_happy = len(happy_words) / total_words
        percentage_sad = len(sad_words) / total_words

        quote['total_words'] = total_words
        quote['percentage_happy'] = percentage_happy
        quote['percentage_sad'] = percentage_sad

        quote['happy_words'] = ', '.join(happy_words)
        quote['sad_words'] = ', '.join(sad_words)

        quote_with_score = quote;
        quotes_with_score.append(quote_with_score)


    df = DataFrame(quotes_with_score)
    files_path = '/Users/V/Documents/simplebox/volrac/quotes.csv'
    df.to_csv(files_path)

    return True

if __name__ == '__main__':
    main()