# -*- coding: utf-8 -*-

import jieba

def sen2words(sentence):
	# 第一步：使用jieba工具切词，返回生成器类型的cutwords
	cutwords = jieba.cut(sentence)

	# 将切开的词语保存为列表类型，且词语类型为unicode
	sumWords = []
	for i in cutwords:
		sumWords.append(i)


	# 第二步：读入停用词，为文件类型f，转存为list类型，并将str转储存为unicode
	stopwords = open('stop_words.txt','r')

	stop_words = []
	for word in stopwords:
		stop_words.extend(word.strip().split(' '))

	stopwords_u = []
	for i in stop_words:
		i = i.decode('gbk')
		stopwords_u.extend(i)

	# 第三步：在sumWords去除停用词
	sumWords_list = []
	for i in sumWords:
		if i in stopwords_u:
			continue
		elif i not in stopwords_u:
			sumWords_list.append(i)
	return sumWords_list




