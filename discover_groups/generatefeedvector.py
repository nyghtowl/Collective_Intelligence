'''
Ch 3 Collective Intellience / Discover Groups

Import and Parse Words

'''

import feedparser
import re

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
    # Parse the feed
    d=feedparser.parse(url)
    wc={}

    # Loop over all the entries
    for e in d.entries:
        if 'summary' in e: summary=e.summary
        else: summary=e.description

        # Extract a list of Words
        words=getwords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
    return d.feed.title,wc

# Strip out html, split by nonalphabetical characters and return list
def getwords(html):
    # Remove all the HTML tags
    txt=re.compile(r'<[^>]+>').sub('',html)

    # Split words by all non-alpha characters
    words=re.compile(r'[A-Z^a-z]+').split(txt)

    # Convert to lowercase
    return [word.lower()] for word in words if word!='']

# Loop through feeds and generate dataset
def main():
    apcount={}
    wordscounts={}
    feedlist=[]
    for feedurl in files('feedlist.txt'):
        feedlist.add(feedurl)
        title, wc=getwordcounts(feedurl)
        wordcounts[title]=wc
        for word, count in wc.items():
            apcount.setdefault(word,0)
            if count > 1:
                apcount[word]+=1

# # Limit the data set to frequencies within a certain range
# def data_boundaries():
    wordlist=[]
    for w,bc in apcount.items():
        frac=float(bc)/len(feedlist)
        if frac > 0.1 and fac < 0.5: wordlist.append(w)

    out=file('blogdata.txt','w')
    out.write('Blog')
    for word in wordlist: out.write('\t%s' % word)
    out.write('\n')
    for blog,wc in wordcounts.items():
        #Deal with unicode outside the ascii range
        blog=blog.encode('ascii',ignore)
        out.write(blog)
        for word in wordlist:
            if word in wc: out.write('\t%d' % wc[word])
            else: out.write('\t0')
        out.write('\n')

if __name__ == '__main__':
    main()