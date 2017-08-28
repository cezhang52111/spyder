# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 19:23:04 2017

@author: Sean Chang
"""

from xml.dom.minidom import parse
import xml.dom.minidom
import jieba
from sklearn.naive_bayes import MultinomialNB
import rankNB
from sklearn.feature_extraction.text import CountVectorizer

stop_words = ["的", "一", "不", "在", "人", "有", "是", "为", "以", "于", "上", "他", "而",
            "后", "之", "来", "及", "了", "因", "下", "可", "到", "由", "这", "与", "也",
            "此", "但", "并", "个", "其", "已", "无", "小", "我", "们", "起", "最", "再",
            "今", "去", "好", "只", "又", "或", "很", "亦", "某", "把", "那", "你", "乃",
            "它","要", "将", "应", "位", "新", "两", "中", "更", "我们", "自己", "没有", "“", "”",
            "，", "（", "）", " ",'[',']',' ','~','。','!']


emo = ['like','fear','disgust','anger','surprise','sadness','happiness']

def readXML(filename):
        # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse(filename)
    collection = DOMTree.documentElement
    
    # 在集合中获取所有电影
    weibos = collection.getElementsByTagName("weibo")
    
    Ncount = 0 #count of all the class
    sen_lst = []
    for weibo in weibos:
       sentence = weibo.getElementsByTagName('sentence')
       for e in sentence:
           lst = []
           if e.getAttribute('opinionated')=='Y':
               lst.append(e.childNodes[0].data)
               emotion1 = e.getAttribute('emotion-1-type')
               Ncount = Ncount + 1
               emotion2 = e.getAttribute('emotion-2-type')
               if emotion2 != 'none':
                   Ncount = Ncount + 1
               lst.append([emotion1,emotion2])
               sen_lst.append(lst)
    
    
    emotionlist = [[],[],[],[],[],[],[]]
    
    for e in sen_lst:
        if 'like' in e[1]:
            emotionlist[0].append(e[0])
        if 'fear' in e[1]:
            emotionlist[1].append(e[0])
        if 'disgust' in e[1]:
            emotionlist[2].append(e[0])
        if 'anger' in e[1]:
            emotionlist[3].append(e[0])
        if 'surprise' in e[1]:
            emotionlist[4].append(e[0])
        if 'sadness' in e[1]:
            emotionlist[5].append(e[0])
        if 'happiness' in e[1]:
            emotionlist[6].append(e[0])
    
    
    return emotionlist,Ncount






def create7Data(emotionlist,Ncount):
    rst = []
    for i in range(7):
        data = []
        label = []
        data = [e for e in emotionlist[i]]
        for j in range(7):
            if j!=i:
                data += [e for e in emotionlist[j]]
        label = [1]*len(emotionlist[i])
        label += [-1]*(Ncount - len(emotionlist[i]))
        rst.append([data,label])
    
    return rst
                
def segmentWord(cont):
    c = []
    for i in cont:
        a = list(jieba.cut(i))
        b = " ".join(a)
        c.append(b)
    return c

def testSentence(rsti,docs):
    vectorizer = CountVectorizer()
    content = segmentWord(rsti[0])
    opinion = rsti[1]
    tfidf = vectorizer.fit_transform(content)  
    clf = MultinomialNB()
    clf.fit(tfidf, opinion)
    new_tfidf = vectorizer.transform(docs)
    predicted = clf.predict(new_tfidf)
    return predicted[0]

if __name__ == "__main__":
    
    emotionlist,Ncount = readXML("NLPCC.xml")
    '''
    likedata,likelabel = createLike(emotionlist,Ncount)
    
    
    emotionlist,Ncount = parseXML.adjustData(emotionlist)
    rst = create7Data(emotionlist,Ncount)
    like_data_feature,word_feature = prepareForTraining(rst[0][0])
    print(testSentence(like_data_feature,word_feature,rst[0][1],"今天真的好开心"))
    '''
    emotionlist,Ncount = rankNB.adjustData(emotionlist)
    rst = create7Data(emotionlist,Ncount)
    docs = [" ".join(list(jieba.cut("好怀念 [泪] 我记得这照片好像是@Christine_HJ 是CC拍的")))]
    print(testSentence(rst[5],docs))
    
    
        
        
            










