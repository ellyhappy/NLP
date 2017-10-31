# -*- coding: UTF-8 -*-

import sen2words
import sumScore
import pymysql

conn = pymysql.connect(host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = '1111',
    db = 'news',
    charset = 'utf8')

# 创建游标，获取数据
cursor = conn.cursor()

sql = 'select URL,正文 from news.搜狐房地产_标题正文;'
cursor.execute(sql)
data = cursor.fetchall()

conn.commit()
cursor.close()
conn.close()

# 将mysql获取的tuple转化为list类型，只要list中每个元组的第二个值，即新闻标题

print '================='
data_list = list(data)
#print data_list[1][1]
#print '==============='

data_newsURL = []
for i in data_list:
	data_newsURL.append(i[0])

data_newstitle = []
for i in data_list:
	data_newstitle.append(i[1])
#print data_newstitle

# 将文本分词，存入wordCut列表中
wordCut = []
for i in data_newstitle:
    words = sen2words.sen2words(''.join(i))
    wordCut.append(words)
# print wordCut

# 计算每一条分词后句子的得分，存入score列表中
sscore = []
for j in wordCut:
    score = sumScore.sumscore(j)
    sscore.append(score)
print sscore

# 存入excel中
import xlwt
f = xlwt.Workbook() # 创建工作薄
sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok = True) # 创建sheet


row_sc = 1
for sc in sscore:
	sheet1.write(row_sc,0,sc) # 表格的第二行第一列开始写得分。
	row_sc += 1

row_url = 1
for u in data_newsURL:
	sheet1.write(row_url,1,u) # 表格的第二行第二列开始得URL。
	row_url += 1

f.save('text.xls')