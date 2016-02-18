#!/usr/bin/python

'''
Created on 2015.5.5
@author: Zheng
'''
import redis
import sys

ip = '127.0.0.1'
# ip = '192.168.1.4'
ip = '1338600145584a6e.m.cnbja.kvstore.aliyuncs.com'
r = redis.Redis(host=ip, port=6379, db=0, password='1338600145584a6e:1z34S678')
  


def read_args():
    args = sys.argv
    if len(args)>=2:
        arg = args[1]
    else:
        arg = 0
    return arg


def readRedis_input():
    args = raw_input('Redis SQL: \n========\n')
    if args.upper() == 'EXIT' or args.upper() == 'QUIT':
        sys.exit()
    else:
        keys = r.keys(args)
        keys.sort()
        for k in keys:
            if r.type(k) == 'hash':
                print('%-40s%s' % (k, r.hgetall(k)))
            else:
                print('%-40s%s' % (k, r.get(k)))
                

def readRedis_del_keys():
    args = raw_input('Redis SQL: \n========\n')
    if args.upper() == 'EXIT' or args.upper() == 'QUIT':
        sys.exit()
    else:
        keys = r.keys(args)
        keys.sort()
        for k in keys:
            if r.type(k) == 'hash':
                print('%-40s%s' % (k, r.hgetall(k)))
                
            else:
                print('%-40s%s' % (k, r.get(k)))
                
            r.delete(k)
            
            
if __name__ == '__main__':
    arg = read_args()
    if arg == '-d':
        readRedis_del_keys()
        print(' ======== DONE ======== \n')
        print(' keys deleted successfully. \n')
    elif arg == '-s':
        readRedis_input()
        print(' ======== DONE ======== \n')
        print(' you got the keys. \n')
    else:
        while 1:
            readRedis_input()
            print(' ======== DONE ======== \n')
