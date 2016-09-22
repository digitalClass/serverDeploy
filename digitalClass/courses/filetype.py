#! /usr/bin/python
# -*- coding: utf-8 -*- 

import struct
# 支持文件类型 
# 用16进制字符串的目的是可以知道文件头是多少字节 
# 各种文件头的长度不一样，少则2字符，长则8字符 
def typeList(): 
    return { 
        "FFD8FF": "JPEG", 
        "89504E47": "PNG", 
	"255044462D312E": "PDF",
	"68746D6C3E": "HTML",
}
   
# 字节码转16进制字符串 
def bytes2hex(bytes): 
    num = len(bytes) 
    hexstr = u"" 
    for i in range(num): 
        t = u"%x" % bytes[i] 
        if len(t) % 2: 
            hexstr += u"0"
        hexstr += t 
    return hexstr.upper() 
   
# 获取文件类型 
def filetype(filename): 
    print str(type(filename))
    if type(filename) == type('str'):
        binfile = open(filename, 'rb') # 必需二制字读取
    else:
        filename.open('rb')
        binfile = filename
    tl = typeList() 
    ftype = 'unknown'
    for hcode in tl.keys(): 
        numOfBytes = len(hcode) / 2 # 需要读多少字节 
        binfile.seek(0) # 每次读取都要回到文件头，不然会一直往后读取 
        hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes)) # 一个 "B"表示一个字节 
        f_hcode = bytes2hex(hbytes) 
        if f_hcode == hcode: 
            ftype = tl[hcode] 
            break
    binfile.close() 
    return ftype 
   
if __name__ == '__main__': 
    print filetype('./test.jpg')
