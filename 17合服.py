#! /usr/bin/pthon3
import os
import time
import sys
import pymysql
import datetime

#==================配置信息=========================================
#  设置数据库的地址和用户名，不设置密码，避免平时手误运行了该脚本
host = "localhost"
user = "root"

# 往zone数据库的合服表中插入此次合服的合服映射id
zoneCenterID = 20

# 数据库里最小的服id 和最大的服id。(作用是为了给所有服的数据添加ServerID)
BeginCenterID = 19
NewCenterID = 20

# 要合拼的数据库id
NeedHeFuID = [19, 20]

# lsjworld库要合并的数据库表，数组有两个参数的是指定合并哪些字段的
LsjWorld_AllTableData = [
	["antiaddict"],
	["friends","PlayerID,PlayerName,PlayerLevel,PlayerVipLevel,FriendsInfo"],
	["guild","Enabled,Data,GuildID,GuildName,GuildLevel,GuildCamp"],
	["guilddungeonfirstpassrecord"],
	["playermail"],
	["playermessageboard","Data,PlayerID"],
	["playerofflinecharge"],
	["players"]
]
#=====================定义类对象=========================================
class mySqlTool:

	mycursor = 0
	mydb = 0

	def __init__(self):
		# 1.数据库连接
		self.mydb = pymysql.connect(host, user, passwd)
		self.mycursor = self.mydb.cursor()
		tmptime = 10
		print("%s秒后开始执行该合服程序..."%tmptime)
		for v in range(tmptime-1,0,-1):
			time.sleep(1)
			print(v)

	def CombineGameData(self, maindbName, subdbName, tableNameAndData):
		tableName = tableNameAndData[0]
		tableData1 = ""
		tableData2 = "*"
		if len(tableNameAndData) ==2:
			tableData1 = "("+tableNameAndData[1]+")"
			tableData2 = tableNameAndData[1]
		cmd = ("insert ignore into %s.%s%s select %s from %s.%s" %(maindbName, tableName, tableData1, tableData2, subdbName, tableName))
		self.Myexecute(cmd)

	def isExistRows(self, dbName, tableName, rowName):
		cmd = (" show columns from %s.`%s` like '%s'" %(dbName, tableName, rowName))
		self.mycursor.execute(cmd)
		mresult = self.mycursor.fetchone()
		if mresult is None:
			print("列：%s 不存在" %(rowName))
			return -1
		else:
			print("列：%s 存在" % (rowName))
			return 1

	def isExistDatabases(self, dbName):
		cmd = ("show databases like '%s' " %(dbName))
		self.mycursor.execute(cmd)
		mresult = self.mycursor.fetchone()
		if mresult is None:
			#print("库：%s 不存在" %dbName)
			return -1
		else:
			print("库：%s 存在" %dbName)
			return 1

	def AddRows(self, dbName, tableName, rowName, rowType, setvalue, Extra):
		# self.m_mycursor.execute("ALTER TABLE "+self.dbName+".`players` ADD COLUMN ServerID int(11) DEFAULT '0' COMMENT 'GameCenterID' AFTER ID")
		cmd = ("ALTER TABLE %s.`%s` ADD COLUMN %s %s DEFAULT '%d' %s" %(dbName, tableName, rowName, rowType, setvalue, Extra))
		self.Myexecute(cmd)

	def Myexecute(self, sqlcmd):
		try:
			self.mycursor.execute(sqlcmd)
			self.mydb.commit()
			print("操作 success %d行，mysql语句:%s" % (self.mycursor.rowcount, sqlcmd))
		except ValueError:
			self.mydb.rollback()
			print("操作 failed，mysql语句:%s\n%s"%(self.mycursor.rowcount,sqlcmd,ValueError))

# ====================main()===========================================
passwd = ""
print("开始合服....，你将要操作合服的数据库为 host:%s, user:%s" %(host, user))
passwd = input("请输入数据库passwd：")

# 1.连接数据库
sqlTool = mySqlTool()
print("连接数据库 完成！")

# 2.为所有服添加serverID
for fuid in range(BeginCenterID, NewCenterID+1):

	dbName ="lsj"+str(fuid)+"world"
	rst = sqlTool.isExistDatabases(dbName)
	if rst > 0 :
		if sqlTool.isExistRows(dbName, "players", "ServerID") < 0:
			sqlTool.AddRows(dbName, "players", "ServerID", "int(11)", fuid, "COMMENT 'GameCenterID' AFTER ID")

		if sqlTool.isExistRows(dbName, "antiaddict", "ServerID") < 0:
			sqlTool.AddRows(dbName, "antiaddict", "ServerID", "int(11)", fuid, "COMMENT 'GameCenterID' AFTER PlayerID")
print("为所有库添加ServerID 完成!")

# 3.开始数据库操作
NeedHeFuID.sort()

# 3.1 zone库更新合服表
zonedbName = "lsj" + str(zoneCenterID) + "zone"
cmd = ("CREATE TABLE if not exists %s.Gm_hefu_list (`Hefuid` int(11) NOT NULL, `Serverid` int(11) NOT NULL, `HefuTime` datetime NOT NULL, PRIMARY KEY (`Hefuid`) ) ENGINE=MyISAM DEFAULT CHARSET=utf8;" % (zonedbName))
sqlTool.Myexecute(cmd)
hefuTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
maindbID = NeedHeFuID[0]
for sid in NeedHeFuID:
	cmd = ("replace into %s.Gm_hefu_list(`Hefuid`, `Serverid`, `HefuTime`) values (%s, %s, '%s')" % (
	zonedbName, sid, maindbID, hefuTime))
	sqlTool.Myexecute(cmd)
print("更新合服表 完成！")

# 3.2 开始合并数据库
maindbName = "lsj"+str(NeedHeFuID[0])+"world"
for fuid in NeedHeFuID:
	subdbName = "lsj"+str(fuid)+"world"

	if maindbName == subdbName:
		print("有一样的%s == %s" %(maindbName, subdbName))
		continue

	for tableData in LsjWorld_AllTableData:
		sqlTool.CombineGameData(maindbName, subdbName, tableData)

print("合并数据库结束！！")