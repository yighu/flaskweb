import requests
import re
from functools import reduce

#pattern = re.compile("^([0-9]?[A-Za-z][A-Za-z]+[0-9]+:[0-9]+)")

#Biblelines = bibleText.split("\n")
#verses = [line for line in Biblelines if pattern.match(line)]

class Bible:
  pattern = re.compile("^([0-9]?[A-Za-z][A-Za-z]+[0-9]+:[0-9]+)")
  def __init__(self, fileurl) -> None:
    self.fileurl = fileurl
    self.text = self.readInternetFileText()
    self.verses = self.convertTextToVerses()
    self.verse_to_book_map = self.booksinBible()
    self.verseNum_per_book = self.countVersePerBook()

  def findVerseContains(self, word):
    versescontainings= [v for v in self.verses if word.lower() in v.lower()] 
    #Home Work. Change this function to find exact word instead of as a substring
    #for v in versescontainings:
    #  print(v)
    return  versescontainings 

  def findVersesContainsAll_v1(self,words):
    verses = set()
    for word in words:
      versescontains = self.findVerseContains(word)
      if verses != set():
        verses = verses.intersection(set(versescontains))
      else:
        verses = set(versescontains)  

    return  verses
  def findVersesContainsAll(self, words):
    verseses= [self.findVerseContains(word) for word in words]
    head, *tail = verseses
    result = set(head)
    for verse in tail:
      result = result.intersection(set(verse))
    return result


  def findVersesContainsAny(self, words):
    verse = set()
    for word in words:
      verse=verse.union(set(self.findVerseContains(word)))
    return verse  

  def countVersePerBook(self):
    book_versecount={}
    for book, vs in self.verse_to_book_map.items():
      book_versecount[book] = len(vs)
    return book_versecount  

  def printVerseCountPerBook(self):
    for book, count in self.verseNum_per_book.items():
      print(f"{book}\t{count}")

  def convertTextToVerses(self):
    biblelines = self.text.split("\n")
    verses = [line for line in biblelines if pattern.match(line)]
    return verses

  def booksinBible(self):

    verse_to_book = {}
    for v in self.verses: 
        book = v.split(":")[0].rstrip('0123456789')
        #print(f"{v} {book}")
        if book in verse_to_book:
          verse_to_book[book].append(v)
        else:
          verse_to_book[book] = [v]
    return   verse_to_book


  def readInternetFileText(self):
    resp = requests.get(self.fileurl)
    text =resp.text
    return text
  def toString(self):
    return self.text  

  def printFirstLine(self):
    print(self.text)


kjv_url = "https://raw.githubusercontent.com/yighu/python/main/files/kjv.txt"

bible = Bible(kjv_url)
