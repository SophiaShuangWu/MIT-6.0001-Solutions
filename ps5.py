# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

from nt import link
#from os import getuid
from typing import Type
from pylab import title
import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        #print(entry.keys())
        #print(hasattr(entry, 'guid'), end='\n\n')
        #attrs = [attr for attr in dir(entry) if not attr.startswith('__')]
        #print(attrs)
        #if not hasattr(entry, 'description'):
        #    print(entry, end='\n\n')
        description = translate_html(entry.get('summary', ''))
        #print(description, end='\n\n')
        pubdate = translate_html(entry.published)

        try:
            #print(pubdate, end='\n')
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            #print(pubdate, end='\n\n')
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            #pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")
            pubdate = datetime.strptime(pubdate, "%Y-%m-%dT%H:%M:%SZ")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        try:
            if not isinstance(guid, str):
                raise TypeError("guid must a string")
            if not isinstance(title, str):
                raise TypeError("title must a string")        
            if not isinstance(description, str):
                raise TypeError("description must a string")
            if not isinstance(link, str):
                raise TypeError("link must a string")
            if not isinstance(pubdate, datetime):
                raise TypeError("pubdate must a datetime")
            self.guid = guid
            self.title = title
            self.description = description
            self.link = link
            self.pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate
        
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        try:
            if not isinstance(phrase, str):
                raise TypeError('phrase must a string, but it is ' + type(phrase).__name__)
            phrase = phrase.lower()
            if phrase == '' or phrase[0] == ' ' or phrase[-1] == ' ' or '  ' in phrase:
                raise ValueError('phrase is not valid')
            for i in phrase:
                if i != ' ' and i not in string.ascii_lowercase:
                    raise ValueError('phrase is not valid')
            self.phrase = phrase
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))
        
    def is_phrase_in(self, text):
        try:
            if not isinstance(text, str):
                raise TypeError("text must a string, but it is " + type(text).__name__)
            text = text.lower()
            clean_text = ''
            for i in text:
                if i not in string.ascii_lowercase:
                    clean_text += ' '
                else:
                    clean_text += i
            while '  ' in clean_text:
                clean_text = clean_text.replace('  ', ' ')
            if clean_text == '' or clean_text == ' ' or self.phrase not in clean_text:
                return False
            word_list = clean_text.split(self.phrase)
            for i in range(len(word_list) - 1):
                if (word_list[i] == '' or word_list[i][-1] == ' ') and (word_list[i+1] == '' or word_list[i+1][0] == ' '):
                    return True
            return False            
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        try:
            if not isinstance(story, NewsStory):
                raise TypeError("story must a NewsStory")
            return self.is_phrase_in(story.get_title())
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))


# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        try:
            if not isinstance(story, NewsStory):
                raise TypeError("story must a NewsStory")
            return self.is_phrase_in(story.get_description())
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time):
        try:
            if not isinstance(time, str):
                raise TypeError("time must a string, but it is " + type(time).__name__)
            self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
            self.time = self.time.replace(tzinfo = pytz.timezone("EST"))
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        try:
            if not isinstance(story, NewsStory):
                raise TypeError("story must a NewsStory")
            return story.get_pubdate() < self.time
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        try:
            #if not isinstance(story, NewsStory):
            #    raise TypeError("story must a NewsStory")
            return story.get_pubdate() > self.time
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        try:
            # There is a TrueTrigger type which seems not a subsclass of Trigger in the py5_test.py
            #if not isinstance(trigger, Trigger):
            #    raise TypeError("trigger must a Trigger, but it is " + type(trigger).__name__)
            self.trigger = trigger
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))
    def evaluate(self, story):
        try:
            if not isinstance(story, NewsStory):
                raise TypeError("story must a NewsStory, but it is " + type(story).__name__)
            return not self.trigger.evaluate(story)
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        try:
            # There is a TrueTrigger type which seems not a subsclass of Trigger in the py5_test.py
            #if not isinstance(trigger1, Trigger):
            #    raise TypeError("trigger1 must a Trigger, but it is " + type(trigger1).__name__)
            #if not isinstance(trigger2, Trigger):
            #    raise TypeError("trigger2 must a Trigger, but it is " + type(trigger2).__name__)
            self.trigger1 = trigger1
            self.trigger2 = trigger2
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        try:
            # There is a TrueTrigger type which seems not a subsclass of Trigger in the py5_test.py
            #if not isinstance(trigger1, Trigger):
            #    raise TypeError("trigger1 must a Trigger, but it is " + type(trigger1).__name__)
            #if not isinstance(trigger2, Trigger):
            #    raise TypeError("trigger2 must a Trigger, but it is " + type(trigger2).__name__)
            self.trigger1 = trigger1
            self.trigger2 = trigger2
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as v:
            print('ValueError: ' + str(v))
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    for i in stories[:]:
        flag = False
        for j in triggerlist:
            if j.evaluate(i):
                flag = True
                break
        if not flag:
            stories.remove(i)
    return stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    #print(lines) # for now, print it so you see what it contains!
    ans = []
    dict_trigger = {}
    for line in lines:
        line = line.split(',')
        if line[0] != 'ADD':
            if line[1] == 'TITLE':
                new_trigger = TitleTrigger(line[2])
            elif line[1] == 'DESCRIPTION':
                new_trigger = DescriptionTrigger(line[2])
            elif line[1] == 'AFTER':
                new_trigger = AfterTrigger(line[2])
            elif line[1] == 'BEFORE':
                new_trigger = BeforeTrigger(line[2])
            elif line[1] == 'NOT':
                new_trigger = NotTrigger(dict_trigger[line[2]])
            elif line[1] == 'AND':
                new_trigger = AndTrigger(dict_trigger[line[2]], dict_trigger[line[3]])
            elif line[1] == 'OR':
                new_trigger = OrTrigger(dict_trigger[line[2]], dict_trigger[line[3]])
            dict_trigger[line[0]] = new_trigger
        else:
            for triggerstr in line[1:]:
                ans.append(dict_trigger[triggerstr])
    return ans    


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        #t1 = TitleTrigger("no problem")
        #t2 = DescriptionTrigger("Trump")
        #t3 = DescriptionTrigger("US")
        #t4 = AndTrigger(t2, t3)
        #triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        #triggerlist = read_trigger_config('triggers.txt')
        triggerlist = read_trigger_config('debate_triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    #print(read_trigger_config('triggers.txt'))
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

