# -*- coding: utf-8 -*-

import jieba

# a = '我在你手机不是很特别重要'
a = '特别报纸不是喜欢手机'
aa = jieba.cut(a)
print aa
print type(aa)
b = []
for i in aa:
	b.append(i)

print b

print '======读入停用词等======='
stopwords = open('stop_words.txt','r')
print type(stopwords)

stop_words = []
for word in stopwords:
	stop_words.extend(word.strip().split(' '))

print stop_words
print type(stop_words[0])

str_stw2 = []
for i in stop_words:
	i = i.decode('gbk')
	str_stw2.extend(i)

# 词语被拆开为单字了
# str_stw = ''.join(stop_words)
# str_stw1 = str_stw.decode('gbk')
# str_stw2 = list(str_stw1)

# 去除停用词，并转成unicode
c = []
for w in b:
	if w in str_stw2:
		continue
	elif w not in str_stw2:
		c.append(w)
print c
str_c = str(c)
print str_c.decode('raw_unicode_escape')

# 不要下列三行代码，c类型已经是unicode
# cwords = ''.join(c)
# cwords = cwords.encode('utf8')
# cwords = list(cwords)

# 读入情感词、否定词、程度副词，并将str转为unicode类型
qgcwords = open('BosonNLP_sentiment_score.txt','r')
qgc_words = []
for word in qgcwords:
	qgc_words.extend(word.strip().split(' '))

#print qgc_words
#奇数列
qgc_keys = qgc_words[::2]

qgc_keys1 = []
for i in qgc_keys:
	i = i.decode('utf8')
	qgc_keys1.append(i)

# qgc_str = ''.join(qgc_keys)
# qgc_str = qgc_str.decode('utf8')
# qgc_keys = list(qgc_str)

#偶数列 
qgc_values = qgc_words[1::2]

# print qg_keys
# print qg_value
qgc = dict(zip(qgc_keys1,qgc_values))


fdcwords = open('notDict.txt','r')
fdc_words = []
for word in fdcwords:
	fdc_words.extend(word.strip().split(' '))

fdc = []
for i in fdc_words:
	i = i.decode('utf8')
	fdc.append(i)

# fdc_str = ''.join(fdc_words)
# fdc_str = fdc_str.decode('utf8')
# fdc_words = list(fdc_str)

#print fdc_words

cdfcwords = open('degreeDict.txt','r')
cdfc_words = []
for word in cdfcwords:
	cdfc_words.extend(word.strip().split(','))

# print cdfc_words

cdfc_keys = cdfc_words[::2]

cdfc_keys1 = []
for i in cdfc_keys:
	i = i.decode('utf8')
	cdfc_keys1.append(i)

# cdfc_str = ''.join(cdfc_keys)
# cdfc_str = cdfc_str.decode('utf8')
# cdfc_keys = list(cdfc_str)

cdfc_values = cdfc_words[1::2]

cdfc = dict(zip(cdfc_keys1,cdfc_values))
# print cdfc_keys
# print cdfc_values

# 将去除停用词的分词划分三种类型，做成三本字典
# (不要)判断分词所属类型，定义情感词为类型1，否定词为类型2，程度副词为类型3, 其于为类型0
# wordfl = []
# for i in c:
# 	if i in qgc_keys1 and i not in fdc_words1 and i not in cdfc_keys1:
# 		wordfl.append(1)
# 	elif i in fdc_words1 and i not in cdfc_keys1:
# 		wordfl.append(2)
# 	elif i in cdfc_keys1:
# 		wordfl.append(3)
# 	else:
# 		wordfl.append(0)
# print wordfl

wordfl = []
wordfl1 = []
wordfl2 = []
wordfl3 = []
wordfl0 = []

worddf = []
worddf1 = []
worddf2 = []
worddf3 = []
worddf0 = []

for i in c:
	if i in qgc.keys() and i not in fdc and i not in cdfc.keys():
		wordfl.append(1)
		worddf.append(qgc[i])

		wordfl1.append(i)
		worddf1.append(qgc[i])
	elif i in fdc and i not in cdfc.keys():
		wordfl.append(2)
		worddf.append(-1)

		wordfl2.append(i)
		worddf2.append(-1)
	elif i in cdfc.keys():
		wordfl.append(3)
		worddf.append(cdfc[i])

		wordfl3.append(i)
		worddf3.append(cdfc[i])
	else:
		wordfl.append(0)
		worddf.append(0)

		wordfl0.append(i)
		worddf0.append(0)

	word1 = dict(zip(wordfl1,worddf1))
	word2 = dict(zip(wordfl2,worddf2))
	word3 = dict(zip(wordfl3,worddf3))
	word0 = dict(zip(wordfl0,worddf0))
	
print wordfl,worddf
print wordfl3,worddf3

# 计算总得分
# finalSentiScore = (-1) ^ (num of notWords) * degreeNum * sentiScore
# finalScore = sum(finalSentiScore)

W = 1
score = 0
wordcount = len(c)

# 存所有词的位置的列表
senLoc = word1.keys()
# print type(senLoc)
notLoc = word2.keys()
degreeLoc = word3.keys()

senloc = -1

# 遍历去除停用词后的分词，i为单词的绝对位置
for i in c:
	# 如果为情感词
	if i in senLoc:
		# loc为情感词位置列表的序号
		senloc += 1
		# 直接添加该情感词分数
		score += W * float(word1[i])
		#print score

	if senloc < len(senLoc) - 1:
		# 判断该情感词与下一个情感词之间是否有否定词或程度副词
		# j为绝对位置
		for j in senLoc[senloc : (senloc + 1)]:
			# 如果有否定词
			if j in notLoc:
				W *= -1
			# 如果有程度副词
			elif j in degreeLoc:
				W *= float(word3[j])
	# i定位至下一个情感词
	if senloc > len(senLoc) - 1:
		i = senLoc[senloc + 1]

print score


#====================先判断有无否定词、情感副词========
sc = 0
sloc = -1
w = 1

# 假设第一个词前的否定词或程度副词，设定初始权重w
for i in c[0:2]:
	if i in notLoc:
		w *= -1
	elif i in degreeLoc:
		w *= float(word3[i])
	elif i in senLoc:
		w *= 1
		break
print w

for i in c:
	if i in senLoc:
		sloc += 1
		sc += w * float(word1[i])

	if sloc < len(senLoc) - 1:
		# 判断该情感词与下一个情感词之间是否有否定词或程度副词
		# j为绝对位置
		for j in senLoc[sloc : (sloc + 1)]:
			# 如果有否定词
			if j in notLoc:
				w *= -1
			# 如果有程度副词
			elif j in degreeLoc:
				w *= float(word3[j])
	# i定位至下一个情感词
	if sloc > len(senLoc) - 1:
		i = senLoc[sloc + 1]

print sc
print sc/len(c)	

# W = 1
# score = 0 
# # 存所有情感词的位置的列表
# senLoc = qgc_keys1
# # print senLoc==qgc_keys1
# notLoc = fdc_words
# degreeLoc = cdfc_keys1

# senloc = -1

# 遍历去除停用词后的分词，记录单词i的绝对位置

# W = 1
# score = 0
# senloc = -1
# # 计算总得分：遍历原分句中所有单词的位置，i为单词的绝对位置
# for i in range(0,len(c)):
# 	# 情感词
# 	if i in qgc_keys1:
# 		# loc为情感词位置列表的序号
# 		senloc += 1
# 		# 直接添加该情感词的分数
# 		score += W * float(qgc[i])

# 		# print 'score = %f' % score
