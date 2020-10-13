#! /usr/bin/python
#_*_coding:utf8_*_
import os
#==============================配置区========================
CenterIDArea=[10,32]
StrFormat = "\cp -rf /root/tools/更新_服务端端程序/next/* /root/Stargate/XQ_Z10_G%s/Server"

#===========================代码区=========================
for i in range(FirstCenterID,NewCenterID+1):
    cmd = (StrFormat%i)
    print(cmd)
    os.system((StrFormat%i))
    print(("XQ_Z10_G%s_更新结束"%i))

os.system("\cp -rf /root/tools/更新_服务端端程序/next/* /root/Stargate/备份XQ/Server")
print("备份XQ_更新结束")

os.system("\cp -rf /root/tools/更新_服务端端程序/next/* /root/tools/更新_服务端端程序/last")
print("已备份到last")
os.system("rm -rf /root/tools/更新_服务端端程序/next/*")
print("已清空next")
print("全部更新结束！！！")
