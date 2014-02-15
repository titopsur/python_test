from __future__ import unicode_literals
import feedparser
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
from sklearn.datasets import load_files
from sklearn.linear_model import RidgeClassifier
import sys

def main():
    #buildTrainSet()
    #buildTestSet()
    train = load_files('model/train', encoding='utf-8')
    test = load_files('model/test', encoding='utf-8')
    print train.cc
#    for l in train.target_names:
#        print l
#    for l in train.target:
#        print l
    vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words='english')
    X_train = vectorizer.fit(train)
    X_test = vectorizer.fit_transform(test)
    print X_train.get_feature_names()
#    y_train, y_test = train.target, test.target
#    clf = RidgeClassifier(tol=1e-2, solver="lsqr")
#    clf.fit(X_train, y_train)
#    pred = clf.predict(X_test)
#    score = metrics.f1_score(y_test, pred)
#    print("f1 score: %0.3f" % score)


def buildTrainSet():
    posFolder = 'model/train/bitcoin'
    negFolder = 'model/train/no_bitcoin'
    rss_sources = {
        posFolder : ['https://news.google.com/news/feeds?pz=1&cf=all&ned=us&hl=en&q=bitcoin&output=rss'],
        negFolder : ['http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&output=rss']
    }
    downloadAll(rss_sources)


def buildTestSet():
    posFolder = 'model/test/bitcoin'
    negFolder = 'model/test/no_bitcoin'
    rss_sources = {
        posFolder: ['http://bitcoincharts.com/headlines.rss'],
        negFolder : ['http://feeds.bbci.co.uk/news/rss.xml']
    }
    downloadAll(rss_sources)


def downloadAll(rss_sources):
    for folder, rss_arr in rss_sources.iteritems():
        for rss in rss_arr:
            downloadRssNews(rss, folder)


def downloadRssNews(url, folder):
    print "Starting download {} to {}".format(url, folder)
    d = feedparser.parse(url)
    i = 0
    for e in d.entries:
#        try:
            print "Saving news {}".format(i)
            title = e.title
            desc = BeautifulSoup(e.get('description','')).get_text()
            tosave = "#title#:{}\n#description#:{}".format(title, desc)
            with (open(folder + "/{}".format(i), "w")) as f:
                f.write(tosave.encode("utf-8"))
            i += 1
#        except:
#            print "Error:", sys.exc_info()[0]
    print "Download finished"


if __name__ == "__main__":
    main()
