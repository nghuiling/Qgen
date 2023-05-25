# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:29:55 2023

@author: andya
"""

import nltk
nltk.download('stopwords')
nltk.download('popular')

# =============================================================================
# Summarising text inputs
# =============================================================================
# from summarizer import Summarizer
from summarizer.sbert import SBertSummarizer
from summarizer import TransformerSummarizer

f = open("C:\\Users\\ACER\\Desktop\\Qgen\\cybersecurity.txt","r",encoding="utf8")
full_text = f.read()
full_text_list = [x.replace("\n", " ") for x in full_text.split('\n\n')]

summarized_text_list = []
model = TransformerSummarizer(transformer_type="OpenAIGPT", transformer_model_key="openai-gpt")

for each_para in full_text_list:
    # model = Summarizer()
    # result = model(each_para, min_length=60, ratio = 0.4)
    result = model(each_para, min_length = 60)
    summarized_text = ''.join(result)
    summarized_text_list.append(summarized_text)

summarized_text = ' '.join(summarized_text_list)

# =============================================================================
# Extracting Keywords
# =============================================================================
import pprint
import itertools
import re
import pke
import string
from nltk.corpus import stopwords

def get_nouns_multipartite(text):
    
    # text = ' '.join(full_text_list)
    out=[]
    extractor = pke.unsupervised.MultipartiteRank()
    extractor.load_document(input=text)
    #    not contain punctuation marks or stopwords as candidates.
    pos = {'NOUN', 'PROPN'}
    #pos = {'VERB', 'ADJ', 'NOUN'}
    stoplist = list(string.punctuation)
    stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
    stoplist += stopwords.words('english')
    extractor.candidate_selection(pos=pos)#, stoplist=stoplist)
    # 4. build the Multipartite graph and rank candidates using random walk,
    #    alpha controls the weight adjustment mechanism, see TopicRank for
    #    threshold/method parameters.
    extractor.candidate_weighting(alpha = 1.1,
                                  threshold = 0.75,
                                  method = 'average')
    keyphrases = extractor.get_n_best(n = 100)
        
    for key in keyphrases:
        if key[0] not in stoplist:
            out.append(key[0])
    return out

keywords = get_nouns_multipartite(' '.join(full_text_list)) 
# print(keywords)

filtered_keys=[]
for keyword in keywords:
    if keyword.lower() in summarized_text.lower():
        filtered_keys.append(keyword)
        
# print (filtered_keys)
    

# =============================================================================
# Mapping Keywords to summarised text (sentences)
# =============================================================================
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
def tokenize_sentences(text):
    sentences = [sent_tokenize(text)]
    sentences = [y for x in sentences for y in x]
    # Remove any short sentences less than 20 letters.
    sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20]
    return sentences
def get_sentences_for_keyword(keywords, sentences):
    keyword_processor = KeywordProcessor()
    keyword_sentences = {}
    for word in keywords:
        keyword_sentences[word] = []
        keyword_processor.add_keyword(word)
    for sentence in sentences:
        keywords_found = keyword_processor.extract_keywords(sentence)
        for key in keywords_found:
            keyword_sentences[key].append(sentence)
    for key in keyword_sentences.keys():
            values = keyword_sentences[key]
            values = sorted(values, key=len, reverse=True)
            keyword_sentences[key] = values
    return keyword_sentences

sentences = tokenize_sentences(summarized_text)
keyword_sentence_mapping = get_sentences_for_keyword(filtered_keys, sentences)
keyword_sentence_mapping = {k: v for k, v in keyword_sentence_mapping.items() if v != []} #remove empty sentences

# =============================================================================
# Get Distractors using WordNet
# =============================================================================
import requests
import json
import re
import random
from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk
from nltk.corpus import wordnet as wn

# Distractors from Wordnet
def get_distractors_wordnet(syn, word):
    distractors=[]
    word= word.lower()
    orig_word = word
    if len(word.split())>0:
        word = word.replace(" ","_")
    hypernym = syn.hypernyms()
    
    if len(hypernym) == 0:
        return distractors
    for item in hypernym[0].hyponyms():
        name = item.lemmas()[0].name()
        # print ("name ",name, " word",orig_word)
        if name == orig_word:
            continue
        name = name.replace("_"," ")
        name = " ".join(w.capitalize() for w in name.split())
        if name is not None and name not in distractors:
            distractors.append(name)
    return distractors

def get_wordsense(sent, word):
    
    word= word.lower()
    if len(word.split())>0:
        word = word.replace(" ","_")
    
    synsets = wn.synsets(word,'n')
    
    if synsets:
        wup = max_similarity(sent, word, 'wup', pos='n')
        adapted_lesk_output = adapted_lesk(sent, word, pos='n')
        lowest_index = min(synsets.index(wup), synsets.index(adapted_lesk_output))
        return synsets[lowest_index]
    
    else:
        return None

key_distractor_list = {}

for keyword in keyword_sentence_mapping:
    wordsense = get_wordsense(keyword_sentence_mapping[keyword][0],keyword)
    if wordsense:
        distractors = get_distractors_wordnet(wordsense,keyword)
        if len(distractors) != 0:
            key_distractor_list[keyword] = distractors


# =============================================================================
# Compiling outputs in JSON string
# =============================================================================
import json
json_data = []
for each in key_distractor_list:
    
    sentence = random.choice(keyword_sentence_mapping[each])
    pattern = re.compile(each, re.IGNORECASE)
    output_qns = pattern.sub( " _______ ", sentence)    
    right_answer = each.capitalize()
    wrong_choices = random.sample(key_distractor_list[each], min(len(key_distractor_list[each]), 10))
    
    if len(wrong_choices) >= 3:
        temp_json_data = {}
        temp_json_data['question'] = output_qns
        temp_json_data['answer'] = right_answer
        temp_json_data['distractors'] = wrong_choices
        json_data.append(temp_json_data)