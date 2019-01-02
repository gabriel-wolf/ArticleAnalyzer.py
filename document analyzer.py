# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 20:13:30 2018

@author: Gabriel Wolf
"""

import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.lang.en import English
from spacy import displacy
from spacy.symbols import nsubj, VERB
from IPython.core.display import display, HTML
import webbrowser
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment
from flask import Markup
from urllib.request import urlopen
import io
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from spacy.symbols import nsubj, VERB
import codecs
import sys
from lxml import html
import requests




doc = nlp(u'In 2006 Congress passed the Secure Fence Act, which mandated the construction of multilayer pedestrian fencing along about 600 miles of the U.S.-Mexico border. It passed with big, bipartisan majorities: 283 votes in the House and 80 in the Senate. Some top Democrats who are still in the Senate today supported the fence: Chuck Schumer, Dianne Feinstein, Ron Wyden, Debbie Stabenow, and Sherrod Brown.')


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):


    soup = BeautifulSoup(body, 'html.parser')





    article_soup = [s.get_text(separator="\n", strip=True) for s in soup.find_all( 'div', {'class': 'story-body story-body-2'})]
    text = ''.join(article_soup)
    #print(text)

    texts = soup.findAll(text=True)


    #visible_texts = filter(tag_visible, texts)


    #return u" ".join(t.strip() for t in texts)
    return text



def each_word(words, func):
    for word in words:
        if word.pos_ is "PUNCT":
            continue

        func(word)

def lemma(word):
    return word.lemma_

def fill_occurrences(word):
    word_lemma = lemma(word)
    count = occurrences.get(word_lemma, 0)
    count += 1
    occurrences[word_lemma] = count

def get_score(occurrences, sentence):
    class Totaler:
        def __init__(self):
            self.score = 0
        def __call__(self, word):
            self.score += occurrences.get(lemma(word), 0)
        def total(self):
            # Should the score be divided by total words?
            return self.score

    totaler = Totaler()

    each_word(sentence, totaler)

    return totaler.total()

def get_ranked(sentences, sentence_count, occurrences):
    # Maintain ranked sentences for easy output
    ranked = []

    # Maintain the lowest score for easy removal
    lowest_score = -1
    lowest = 0

    for sent in sentences:
        # Fill ranked if not at capacity
        if len(ranked) < sentence_count:
            score = get_score(occurrences, sent)

            # Maintain lowest score
            if score < lowest_score or lowest_score is -1:
                lowest = len(ranked) + 1
                lowest_score = score

            ranked.append({'sentence': sent, 'score': score})
            continue

        score = get_score(occurrences, sent)
        # Insert if score is greater
        if score > lowest_score:
            # Maintain chronological order
            for i in range(lowest, len(ranked) - 1):
                ranked[i] = ranked[i+1]

            ranked[len(ranked) - 1] = {'sentence': sent, 'score': score}

            # Reset lowest_score
            lowest_score = ranked[0]['score']
            lowest = 0
            for i in range(0, len(ranked)):
                if ranked[i]['score'] < lowest_score:
                    lowest = i
                    lowest_score = ranked[i]['score']

    return ranked



inputtext = input("Enter your text (Enter 0 for default or 1 for url): ")
if (inputtext != "0"):
    if (inputtext == "1"):
        inputtext = input("Enter a url (0 for default): ")
        if (inputtext == "0"):
            html = urllib.request.urlopen('http://www.nytimes.com/2009/12/21/us/21storm.html').read()
            doc = nlp(u'' + text_from_html(html) + '')
            #print(text_from_html(html))

        else:
            html = urllib.request.urlopen(inputtext).read()
            doc = nlp(u'' + text_from_html(html) + '')
            print(text_from_html(html))

    else:
        doc = nlp(u'' + inputtext + '')




print("MAIN TOPICS\n")

for ent in doc.ents:
    print(ent.text, ent.label_)


print("\n\n\n\n")


#
# for token in doc:
#     print(token.text, token.dep_, token.head.text, token.head.pos_,
#           [child for child in token.children])




testdoc = nlp(u"Autonomous cars shift insurance liability toward manufacturers")
for token in testdoc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
          [child for child in token.children])

occurrences = {}


each_word(doc, fill_occurrences)

# print(occurrences)

sentences = [sent.string.strip() for sent in doc.sents]


# 4, 5, 6
ranked = get_ranked(doc.sents, 3, occurrences)

# 7
print(" ".join([x['sentence'].text for x in ranked]))




# verbs = set()
# subheads = set()
# for possible_subject in doc:
#     if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
#         verbs.add(possible_subject.head)
#         subheads.add(possible_subject.dep)
# print(verbs)
# print(subheads)






doc.user_data['title'] = 'Document Analysis Results'
#displacy.serve(doc, style='ent')
html = displacy.render([doc], style='ent', page=True, minify=True)
#print(html)




f = open('exportspacy.html','w', encoding="utf-8")
message = html
f.write(message)
f.close()



sentence_spans = list(doc.sents)

summarytext = (" ".join([x['sentence'].text for x in ranked]))


summaryhtml = """<!DOCTYPE html><html><body style="font-size: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; padding: 4rem 2rem;"><h1>Document Summary</h1><p>""" + summarytext + """</p></body></html>"""
f = open('summaryhtml.html','w', encoding="utf-8")
f.write(summaryhtml)
f.close()




f = open('depexports.html','w', encoding='utf-8')
f.write(displacy.render(sentence_spans, style='dep', minify=True))
f.close()




#webbrowser.open_new_tab('appHTML.html')
