#! /usr/bin/pthon3
import os
import time
import sys
import mysql.connector

#===================配置信息======================================

m_host='localhost'
m_user='root'
m_passwd=''
m_canNext = "true"

#需要备份的数据库ID区间.(包含NewCenterID)
BeginCenterID = 19
NewCenterID = 20
#要备份的库ID
dbNameList = {"BeginCenterID": BeginCenterID, "NewCenterID": NewCenterID+1}

#==================main()===================================

# 1.创建&&进入目录(该目录用于存放数据库的备份)
if not os.path.exists('backup'):
	os.mkdir('backup')
os.chdir('backup')
time = time.strftime("%Y-%m-%d_%H", time.localtime())
if not os.path.exists(time):
	os.mkdir(time)
os.chdir(time)


# 2.开始备份
mysqlcomm='mysqldump'
sqlfromat="%s -h%s -u%s -p%s %s >%s"

for num in range(dbNameList["BeginCenterID"], dbNameList["NewCenterID"]):
	dbname = "lsj"+str(num)+"world"
	cmd = (sqlfromat%(mysqlcomm, m_host, m_user, m_passwd, dbname, dbname+"_back.sql"))
	print(cmd)
	result = os.popen(cmd)
	if result:
		print("backup completed!")
	else:
		print("I'm sorry!!!,backup failed!")



