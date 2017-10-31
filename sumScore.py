# -*- coding: utf-8 -*-

# 第一步：读入情感词、否定词、程度副词原文件，情感词、程度副词转格式为字典类型，否定词为列表类型

#========情感词==========
# 将情感词txt文件内容转储存为list类型
senwords = open('BosonNLP_sentiment_score.txt','r')
sen_words = []
for word in senwords:
	sen_words.extend(word.strip().split(' '))

# 获取情感词的奇数列，将str类型转存为unicode
sen_keys = sen_words[::2]
sen_keys1 = []
for i in sen_keys:
	i = i.decode('utf8')
	sen_keys1.append(i)

# 获取情感词偶数列
sen_values = sen_words[1::2]

# 建立情感词字典
senDict = dict(zip(sen_keys1,sen_values))

#=======否定词===========
# 读入否定词txt文件类型，转存为list类型，将str转为unicode
notwords = open('notDict.txt','r')
not_words1 = []
for word in notwords:
	not_words1.extend(word.strip().split(' '))

notwords_list = []
for i in not_words1:
	i = i.decode('utf8')
	notwords_list.append(i)

#=======程度副词=========
# 读入程度副词txt文件类型，存为list类型
degreewords = open('degreeDict.txt','r')
degree_words = []
for word in degreewords:
	degree_words.extend(word.strip().split(','))

# 获取程度副词奇数列，将str转存为unicode
degree_keys = degree_words[::2]

degree_keys1 = []
for i in degree_keys:
	i = i.decode('utf8')
	degree_keys1.append(i)

# 获取程度副词偶数列
degree_values = degree_words[1::2]

# 建立程度副词字典
degreeDict = dict(zip(degree_keys1,degree_values))

# 第二步：计算总得分，伪代码如下
# finalSentiScore = (-1) ^ (num of notWords) * degreeNum * sentiScore
# finalScore = sum(finalSentiScore)

def sumscore(wordList):
	# 先将切好的词分类，建立四种类型的字典
	# cf是词语分类，sc为得分，情感词为1，否定词为2，程度副词为3，其它为0
	wordcf1 = []
	wordcf2 = []
	wordcf3 = []
	wordcf0 = []

	wordsc1 = []
	wordsc2 = []
	wordsc3 = []
	wordsc0 = []

	for i in wordList:
		if i in senDict.keys() and i not in notwords_list and i not in degreeDict.keys():
			wordcf1.append(i)
			wordsc1.append(senDict[i])
		elif i in notwords_list and i not in degreeDict.keys():
			wordcf2.append(i)
			wordsc2.append(-1)
		elif i in degreeDict.keys():
			wordcf3.append(i)
			wordsc3.append(degreeDict[i])
		else:
			wordcf0.append(i)
			wordsc0.append(0)

		cwords_senDict = dict(zip(wordcf1,wordsc1))
		cwords_notDict = dict(zip(wordcf2,wordsc2))
		cwords_degreeDict = dict(zip(wordcf3,wordsc3))
		cwords_elseDict = dict(zip(wordcf0,wordsc0))

	#====================先判断有无否定词、情感副词===============
	score = 0  # 初始得分
	senloc = -1 # 情感词初始位置
	w = 1 # 初始权重

	# 存所有切好词的位置列表
	senLoc = cwords_senDict.keys()
	notLoc = cwords_notDict.keys()
	degreeLoc = cwords_degreeDict.keys()

	# 假设第一个词前的否定词或程度副词，设定初始权重w
	for i in wordList[0:2]:
		if i in notLoc:
			w *= -1
		elif i in degreeLoc:
			w *= float(cwords_degreeDict[i])
		elif i in senLoc:
			w *= 1
			break

	for i in wordList:
		if i in senLoc:
			senloc += 1
			score += w * float(cwords_senDict[i])

			if senloc < len(senLoc) - 1:
				# 判断该情感词与下一个情感词之间是否有否定词或程度副词
				# j为绝对位置
				for j in senLoc[senloc : (senloc + 1)]:
					# 如果有否定词
					if j in notLoc:
						w *= -1
					# 如果有程度副词
					elif j in degreeLoc:
						w *= float(cwords_degreeDict[j])
			
			else:
				continue
			# # i定位至下一个情感词
			# if senloc >= len(senLoc) - 1:
			# 	i = senLoc[senloc + 1]

	#return score/len(wordList)
	return score
