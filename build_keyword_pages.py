# -*- coding: ISO-8859-1 -*-

import csv
from string import punctuation
from operator import itemgetter

# open misspellings document
csvfile = open('inputs/misspellings.csv', encoding='ISO-8859-1')
misspellings = csv.reader(csvfile, delimiter=',')

def main():

    # create dictionary for misspellings
    corrections = {}
    for row in misspellings:
        wrong = row[0]
        right = row[1]
        corrections[wrong] = right

    # open stopwords file & read first line
    stopwords = open('inputs/stopwords.txt', 'r')

    # read in replacement file
    stopwords_list = []
    line = stopwords.readline()
    while line != '':
        line = line.rstrip('\n')
        stopwords_list.append(line)
        line = stopwords.readline()
    
    # create holder for keywords
    keywords = []

    # open file containing the abstracts
    abstracts = open('inputs/abstracts.txt', 'r')

    for i in abstracts:
        # replace noise characters
        abs_words = i.replace(';', ' ').replace(',', ' ').replace(':', ' ').replace('-', ' ').replace('.', ' ') \
            .replace('(', ' ').replace(')', ' ').replace('{', ' ').replace('}', ' ').replace('0', ' ').replace('1', ' ') \
            .replace('2', ' ').replace('3', ' ').replace('4', ' ').replace('5', ' ').replace('6', ' ').replace('7', ' ') \
            .replace('8', ' ').replace('9', ' ').replace("'", ' ').replace('"', ' ').replace(']', ' ').replace('[', ' ') \
            .replace('“', ' ').replace('”', ' ').replace('?', ' ').replace('=', ' ').replace('&', ' ').split()
        for word in abs_words:
            word = word.lower()
            # if word is in misspellings list, replace with correct spelling
            for key in corrections:
                word = word.replace(key, corrections[key])
            # check word is not in stopwords list
            if word not in stopwords_list:
                keywords.append(word)

    # get top keywords
    # from http://stackoverflow.com/questions/4088265/sorted-word-frequency-count-using-python
    words = {}
    N = 35  # number of keywords to display
    for word in keywords:
        words[word] = words.get(word, 0) + 1
    tops = sorted(words.items(), key=itemgetter(1), reverse=True)[:N]

    # keep only the words, not their counts
    top_keywords = []
    for row in tops:
        keys1 = row[0]
        top_keywords.append(keys1)
        
    # Put in descending order alphabetical
    top_keywords = sorted(top_keywords)

    # build HTML list of keywords      
    html_list = []
    for word in top_keywords:
        li = '<li><a href="' + word + '.html">' + word + '</a>'
        html_list.append(li)
    li_list = '\n'.join(map(str, html_list))

    # create list to hold abstract lines
    abstract_list = []

    # read abstracts into individual line items
    abstracts = open('inputs/abstracts.txt', 'r')
    # read in the first line
    aline = abstracts.readline()

    # until reach the end of file
    while aline != '':
        
        # create a (new) blank list for the articles
        article = []
        
        # until reach the newline that's between each article
        while aline != '\n':
            aline = aline.rstrip('\n')
            # append to list called article
            article.append(aline)
            # read the next line
            aline = abstracts.readline()
        
        # Get the whole abstract together
        new_entry = ' '.join(article)
        # append the individual entries to the overall list
        abstract_list.append(new_entry)
        # read in the next line
        aline = abstracts.readline()


    #### Building pages for each keyword
    # take each keyword
    for word in top_keywords:
        indices = []
        count = 0
        
        # compare each keyword to the abstracts
        for listing in abstract_list:
            
            articleholder = []
            # if keyword is in the abstract, append to a list
            # of articles for that keyword
            if (word in str(listing)):
                
                # then split on the " that surround the titles
                articleholder = listing.split('"')
                
                # take the second part of the split (title) and add link
                # use rstrip to remove ending commas
                link = '<a href="article' + str(count) + '.html">' + \
                    str(articleholder[1]).rstrip(',') + '</a>'
                
                # append the first part of the split (author) and second part (title)
                # to create a listing
                # use rstrip to remove ending commas
                key_listing = str(articleholder[0]).rstrip(', ') + '<br>' + link

                # append this to a list for the keyword page
                indices.append(key_listing)
                
                # create page for the abstract with line breaks
                # use rstrip to remove ending commas
                abs_page = '<u> Abstract</u>' + '<br> <br>' + \
                    '<i>' + str(articleholder[0]).rstrip(', ') + '</i>' + '<br>' + \
                    '<b>' + str(articleholder[1]).rstrip(',') + '</b>' + '<br> <br>' + \
                    str(articleholder[2])
                
                # write out HTML for that article
                filename = 'article' + str(count) + '.html'
                keyword_file = open(filename, "w")
                keyword_file.write(abs_page)
                keyword_file.close()
                
            count += 1
        
        # build keyword abstract listing page, 
        # including line breaks between abstracts
        page = '\n \n <br><br> \n'.join(indices)
        
        ### Print out the files
        filename = word + '.html'
        keyword_file = open(filename, "w")
        keyword_file.write(page)
        keyword_file.close()

    # build HTML document
    html_begin = """
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Welcome to the ACM Library</h1>
    <h3>A research, discovery and networking platform</h3>
    <h2>Browse our library by keyword.
    <h3 id="keyword"><h3>Keywords</h3></a>
    <ul>
    """

    html_end = """
    </ul>
    </body>
    </html>"""

    # build HTML doc
    html_str = html_begin + li_list + html_end

    # write out HTML
    html_file = open("index.html", "w")
    html_file.write(html_str)
    html_file.close()

    abstracts.close()


main()



