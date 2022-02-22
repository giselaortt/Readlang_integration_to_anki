# -*- coding: utf-8 -*-
import os
import re
import sys
sys.path.insert(1, "/Users/giortt/Desktop/readlang_to_anki/")
from parsers_deutsch_nouns.parsing_nouns import *
import parsers_deutsch_nouns.parsing_nouns
from readlang_intgration.parsing import removeBold
from googletrans import Translator
from difflib import SequenceMatcher

#abzeichnen (sich)
#dfb (deutscher fußball-bund)
#letzterer, letztere, letzteres
#andere (r, s)
#welch, -e, -er, -es
#final (er, e, es)


def isCognato( word ):
    translator = Translator()
    english = translator.translate(word, src='de', dest='en').text
    if(SequenceMatcher( None, english, word ).ratio() > 0.9):
        return True
        print(word, english)
    else:
        return False


def cleanPonctuation( mystr ):

    return re.sub('[^\w\s]', '', mystr)


def cleanNumbers( card ):

    return re.sub('[0-9]', '', card)


def getFirstField( card ):
    field = separateFieldsWithTab(card)[0]

    return field


def eliminateReflexivePronom( word ):

    return re.sub("\(sich\)", "", word)


def eliminateLegend( word ):

    return re.sub( "\(.*\)", "", word )


def getSuffxes( word ):
    if( "(er, e, es)" in word ):
        answer = ["er", "e", "es"]
    if( "(r, s)" in word ):
        answer = ["r", "s"]
    if( "-e, -er, -es" in word ):
        answer = ["e","er","es"]
    else:
        answer = None

    return answer


def eliminateSufixes( wordField ):
    wordField = re.sub("-e, -er, -es", "", wordField)
    wordField.strip(" ")

    return wordField


def glueSuffixes( word, sufixes ):
    ans = [word]
    for sufix in sufixes:
        ans.append(word+sufix)

    return ans


def getWordsFromFirstField( firstField ):
    words = field.lower().split(" ")

    return words


def separateWords( field ):
    field = re.sub(" ","", field)

    return field.split(",")    


def cleanCard( card ):
    card = cleanNumbers(card)
    card = removeBold(card)
    card = parsers_deutsch_nouns.parsing_nouns.cleanCard(card)
    card = cleanPonctuation(card)

    return card
  

def getWordField( card ):

    return separateFieldsWithTab(card)[1]



def parseFrequentDictionarySecondFild( card ):
    card = card.lower()
    wordField = getWordField( card )
    wordField = eliminateReflexivePronom( wordField )
    wordField = eliminateSufixes( wordField )
    sufixes = getSuffxes( wordField )
    wordField = eliminateLegend( wordField )
    wordField = cleanExtraSpaces( wordField )
    if( sufixes is not None ):
        words = glueSuffixes( wordField, sufixes )
    elif( "," in wordField ):
        words = separateWords( wordField )
    else:
        words = [wordField]

    if(words is None):
        print(card)
    return words


if __name__ == "__main__":
    #sys.path.append('../../')
    current_vocabulary = open('Deutsch__vocabulary.txt',"r")
    wordlist = open("wordlist.txt","w")
    my_vocabulary = set()

    tmp = open("acceptedwords.txt", "w")
    other = open("notaccepted.txt", "w")

    for card in current_vocabulary.readlines():
        card = cleanCard(card)
        field = getFirstField(card)
        words = getWordsFromFirstField(field)
        for word in words:
            my_vocabulary.add(word.lower())

    print(len(my_vocabulary))
    for word in my_vocabulary:
        wordlist.write(word)
        wordlist.write("\n")

    new_deck = open("A Frequency Dictionary of German.txt", "r")
    output_deck = open("neu deutsch wortschatz.txt","w")
    neue_worter = 0
    not_added = 0

    for line in  new_deck.readlines():
        words = parseFrequentDictionarySecondFild( line )
        #bool(test_set & set(test_list))
        #TODO: this if is not working, find out why
        if( bool(my_vocabulary.intersection(set(words))) ):
            not_added = not_added + 1
            other.write(str(words))
        else:
            output_deck.write(line)
            neue_worter = neue_worter + 1
            tmp.write(str(words))

    print(neue_worter, not_added)

    # this is how you apply a function to every element in  place
    # list(map(lambda i:func(a, i), range(0, len(a))))

    #and this is not in  place 
    # map(upper, mylis)
