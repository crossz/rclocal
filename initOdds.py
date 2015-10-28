# -*- coding: utf-8 -*-
"""
Created on Tue Sep 02 14:25:46 2014
@author: zhengxin
"""

"""
todo: to combine the 2 parts(tks, mainV2)

v1.2 combine ticket info with splited levels in one table.
v1.3 download extra columns from Mysql
v1.4 bug fix for 1st row selection; remove l*_sports
v1.41 bug fix for sp column type: code
v1.5 cancel and sgl tickets handling
v2.0 split tickets into rows, while not cols

"""
# %% system level subfunctions:
import os, re, itertools, datetime


class TheInfo():

    def __init__(self):
        pass

    # ## tweak ip

    if os.name == 'nt':
        ip = '192.168.1.5'
    else:
        try:
    	    import ConfigParser
    	    conf=ConfigParser.ConfigParser()
    	    conf.read('ops.conf')    
    	    ipaddress = conf.get('ip','ipaddr')

	    ip = ipaddress
        except:
            import socket, fcntl, struct
            def get_ip_address(ifname,socket, fcntl, struct):
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', ifname[:15])
                    )[20:24])

            ip = get_ip_address('eth0',socket, fcntl, struct)


    ECS_ip = ip
    RDS_ip = ip


    # ## sqlite: default configuration
    n_once = 10000  # 1w
    # n_once = 100

    # etr = 737431742 # existing total row / initial No in the main Mysql
    etr = 756764567 # from 1st Monday of Aug
    ftr = 808166690 # end of 1st weekc

    sqlitePath = os.getcwd() + '\\' + 'ytd_spV2.1_1231.sqlite'
    tableName = 'tx'
    YtdTableName = 'Source_FB'
    TicketsTableName = 'cp_tickets_levels'

    # ## db driver
    db = 'sqlite'
    db = 'mysql'

    ## Excel path
    #excelPath =  '/opt/sbc'
    excelPath = os.path.dirname(os.path.realpath(__file__))

    ##
    sport_type = {1:'football',2:'basketball'}

    ## config maps
    keys_cn = [u'周一', u'周二', u'周三', u'周四', u'周五', u'周六', u'周日']
    vals_cn = ['1', '2', '3', '4', '5', '6', '7']
    WeekMap_cn = dict(zip(keys_cn, vals_cn))

    keys_en = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    vals_en = ['1', '2', '3', '4', '5', '6', '7']
    WeekMap_en = dict(zip(keys_en, vals_en))

    ProdKeys = ('Code', 'HAD', 'HHAD', 'HAFU', 'TTG', 'CRS')
    MarginKeys = (float('nan'), 1.125, 1.125, 1.30, 1.30, 1.50)

    # %% mn types
    mn = {'FSGL':[1],\
          '2X1':[2],\
          '3X1':[3],'3X3':[2],'3X4':[2,3],\
          '4X1':[4],'4X4':[3],'4X5':[3,4],'4X6':[2],'4X11':[2,3,4],\
          '5X1':[5],'5X5':[4],'5X6':[4,5],'5X10':[2],'5X16':[3,4,5],'5X20':[2,3],'5X26':[2,3,4,5],\
          '6X1':[6],'6X6':[5],'6X7':[5,6],'6X15':[2],'6X20':[3],'6X22':[4,5,6],'6X35':[2,3],'6X42':[3,4,5,6],'6X50':[2,3,4],'6X57':[2,3,4,5,6],\
          '7X1':[7],'7X7':[6],'7X8':[6,7],'7X21':[2],'7X35':[3],'7X120':[2,3,4,5,6,7],\
          '8X1':[8],'8X8':[7],'8X9':[7,8],'8X28':[2],'8X56':[3],'8X70':[4],'8X247':[2,3,4,5,6,7,8]}

    ## mysql with redis:
    import optparse
    parser = optparse.OptionParser()
    parser.add_option("-s", "--split", dest="split", action="store_true", help="Split and process synchronized data.")

    parser.add_option("-m", "--mn", dest="mnSplit", action="store_true", help="multiple and M*N spliting.")
    parser.add_option("-t", "--proc", dest="tk_proc", action="store_true", help="process N*1 tickets into N rows.")

    parser.add_option("-i", "--importMatchInfo", dest="importMatchInfo", action="store_true", help="Import YTD excel files into Mysql match_info.")
    parser.add_option("-o", "--importMatchOdds", dest="importMatchOdds", action="store_true", help="Import Odds excel files into Mysql match_odds.")
    parser.add_option("-p", "--initMatchProduct", dest="initMatchProduct", action="store_true", help="Init Mysql match_product.")
    parser.add_option('', "--redis_mi_SomeKeys", dest="redis_mi_SomeKeys", action="store_true", help="init redis some keys for match status.")
    parser.add_option('', "--redis_mo_current_price", dest="redis_mo_current_price", action="store_true", help="sync redis local odds from mysql match_odds.")
    parser.add_option('', "--redis_mo_position_limit", dest="redis_mo_position_limit", action="store_true", help="sync redis position_limit from mysql match_prodcut.")
    parser.add_option('', "--redis_mp_pool_state", dest="redis_mp_pool_state", action="store_true", help="sync redis pool_state from mysql match_prodcut.")
    parser.add_option('', "--redis_mp_pool_result", dest="redis_mp_pool_result", action="store_true", help="sync redis pool_result from mysql match_prodcut.")
    parser.add_option('', "--redis_dictionary_table", dest="redis_dictionary_table", action="store_true", help="sync redis dictionary from mysql dictionary_table.")
    parser.add_option('', "--redis_position_limit_all", dest="redis_position_limit_all", action="store_true", help="sync redis dictionary from mysql position_limit_all.")
    parser.add_option('', "--redis_big_small_invest", dest="redis_big_small_invest", action="store_true", help="sync redis dictionary from mysql big_small_invest.")
    parser.add_option('', "--redis_risk_limit_warning_percent", dest="redis_risk_limit_warning_percent", action="store_true", help="sync redis dictionary from mysql risk_limit_warning_percent.")
    parser.add_option('', "--redis_position_singlecallpmsort", dest="redis_position_singlecallpmsort", action="store_true", help="sync redis dictionary from mysql position_singlecallpmsort.")
    parser.add_option('', "--hadoop_hdfs_rm", dest="hadoop_hdfs_rm", action="store_true", help="clean hdfs directories.")
    parser.add_option('', "--redis_order_ticket", dest="redis_order_ticket", action="store_true", help="sync redis tid from order_ticket.")




    parser.add_option('', "--flushdb", dest="flushdb", action="store_true", help="redis-cli, flushdb.")
    parser.add_option('', "--all", dest="runAll", action="store_true", help="run all init scripts.")
    parser.add_option('', "--test", dest="isatest", action="store_true", help="just a test.")

    (options, args) = parser.parse_args()


def main():
    global infos,cu,cu_r    # have to announce global here due to outter var could be re-assigned in this scope.


    # ## __init__
    sqlitePath = infos.sqlitePath
    db_diver = infos.db
    RDS_ip = infos.RDS_ip
    ECS_ip = infos.ECS_ip

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    import redis
    cu_r = redis.Redis(host=ECS_ip, port=6379, db = 0)







    # ====switches====
    opts=infos.options

    if opts.split: # -s
        tk_split()

    if opts.importMatchInfo: # -i
        ReadAndUpdate_match_info()
    if opts.importMatchOdds: # -o
        ReadAndUpdate_match_odds()
    if opts.initMatchProduct: # -p
        InitAndUpdate_match_product()
    if opts.redis_mo_current_price: # --
        redis_mo_current_price()
    if opts.redis_mo_position_limit: # --
        redis_mo_position_limit()
    if opts.redis_mp_pool_state: # --
        redis_mp_pool_state()
    if opts.redis_mp_pool_result: # --
        redis_mp_pool_result()
    if opts.redis_dictionary_table: # --
        redis_dictionary_table()
    if opts.redis_position_limit_all: # --
        redis_position_limit_all()
    if opts.redis_big_small_invest: # --
        redis_big_small_invest()
    if opts.redis_risk_limit_warning_percent: # --
        redis_risk_limit_warning_percent()
    if opts.redis_position_singlecallpmsort: # --
        redis_position_singlecallpmsort()
    if opts.hadoop_hdfs_rm: # --
        hadoop_hdfs_rm()
    if opts.redis_order_ticket: # --
        redis_order_ticket()

    if opts.redis_mi_SomeKeys: # --
        redis_mi_SomeKeys()

    if opts.flushdb: # --
        redis_flushdb()

    if opts.runAll:
        runAll()
    if opts.isatest: # --test
        isatest()



    #%% test part =================
#     str_test='ALUP 3X4 FB CRS FRI 7 * (2:0)@8.5 + (2:1)@7.5 / FB HAD FRI 9 * [Troyes] 2@2.26 / FB CRS FRI 10 * (2:0)@8.5 + (3:0)@17'
#     str_test = b'4000001,2014-12-26 22:26:21,2,2,01,88109,1,HAD,ALUP 3X1 FB HAD FRI 6 * [Liverpool] 2@1.52 / FB HAD FRI 8 * [Everton] 1@1.65 / FB HAD FRI 9 * [Tottenham] 2@1.92\r\n'
#     str_test='ALUP 2X1 FB HAD WED 1 * [FC Seoul] 2@2 / FB HAD WED 2 * [Cerezo Osaka] 1@1.98'

    mstr = 'ALUP 6X22 FB HAD THU 8 * [Burnley] 2@4.7 / FB HAD THU 7 * X@6.25 + [Sunderland] 2@13 / FB HAD THU 6 * X@4.5 + [Leicester] 2@7.5 / FB HAD THU 3 * X@3.3 + [Manchester Utd] 2@1.75 / FB HAD THU 2 * [Dundee] 2@4.15 / FB HAD WED 1 * [Wellington Phoenix] 2@5.25'
    #mstr='ALUP 3X4 FB CRS FRI 7 * (2:0)@8.5 + (2:1)@7.5 / FB HAD FRI 9 * [Troyes] 2@2.26 / FB CRS FRI 10 * (2:0)@8.5 + (3:0)@17'

    str_test = 'ALUP 3X1 FB HAD FRI 6 * [Liverpool] 2@1.52 / FB HAD FRI 8 * [Everton] 1@1.65 / FB HAD FRI 9 * [Tottenham] 2@1.92\r\n'
    str_test.replace('\r\n','')

    if opts.mnSplit: # -m
        a=multi_mn_split(mstr)
        print(len(a))
        print(a)
    if opts.tk_proc: # -str_test
        b=tk_proc(str_test)
        print(b)


    # ## __clear__
    cu.close()
    conn.close()


# %% sub-functions ====================
def findnames(string):
    NameAndOpt = []
    ind = string.find(' ')
    if ind>0:
        ind_sym = string.find(']')
        name_str = string[1:ind_sym]
        opt_str = string[ind_sym+2:]
        NameAndOpt.append(name_str)
        NameAndOpt.append(opt_str)
    else:
        NameAndOpt.append('')
        NameAndOpt.append(string)

    return NameAndOpt

def findindices(string, sub, offset=0):
    listindex=[]
    i = string.find(sub, offset)
    while i >= 0:
        listindex.append(i)
        i = string.find(sub, i + 1)
    return listindex

def tk_proc(t):
    ind_space = findindices(t, ' ')
    t_cap = t.upper()
    FOSornot = t_cap.find('ALUP')

    if FOSornot != -1:
    #    tk_type = t[0:ind_space[1]]
        tk_detail = t[ind_space[1]+1:len(t)]
    else:
    #    tk_type = 'FOS'
        tk_detail = t


    tks = tk_detail.split(' / ')
    tks_rows = []
    for tk in tks:
        tks_cols = []
        ind_space = findindices(tk, ' ')
        # level_sports = tk[0:ind_space[0]]
        # tks_cols.append(level_sports)

        level_prod = tk[ind_space[0]+1:ind_space[1]]
        tks_cols.append(level_prod)

        ind_ster = tk.find('*')
        level_code = tk[ind_space[1]+1:ind_ster-1]
        tks_cols.append(level_code)

        ind_at = tk.find('@')
        NameAndOpt = findnames(tk[ind_ster+2:ind_at])
        level_name = NameAndOpt[0]
        level_opt = NameAndOpt[1]
        tks_cols.append(level_name)
        tks_cols.append(level_opt)

        level_odds = tk[ind_at+1:]
        tks_cols.append(level_odds)

        tks_rows.append(tks_cols)

    #print(tks_rows)
    return tks_rows

#: create MX1 and remove duplicated combinations
def comb_filter(combs):
    combi = list()
    for c in combs:
        #c = list(c)
        #c.sort()
        m = len(c)
        comb = c[0]
        for i in range(1,m):
            #if i!=m: #not the last one
            comb = comb + ' / ' +c[i]
        combi.append(comb)
    combi=list(set(combi))
    return combi




def multi_mn_split(str_test):
    mn = infos.mn

    #%% test
    #str='ALUP 3X4 FB CRS FRI 7 * (2:0)@8.5 + (2:1)@7.5 / FB HAD FRI 9 * [Troyes] 2@2.26 / FB CRS FRI 10 * (2:0)@8.5 + (3:0)@17'
    #str='ALUP FSGL FB HAFU THU 3 * (X-1)@7.5 + (X-X)@4.8 + (X-2)@4.2'


    str_test = str_test.replace('\r','')

    #r1=re.compile('(^ALUP \dX\d{1,2}|FSGL) (.*)')
    r1=re.compile('(^ALUP (\dX\d{1,3}|SGL|FSGL)) (.*)') # \d means [0-9], \d{1,2} means 'double digits', (...) Matches whatever regular expression is inside the parentheses, and indicates the start and end of a group
    r2=re.compile('[^/]+') # split strings by some charactors, i.e. [^X] means not the X; equivlent to "rs = re.split('./.',n)" in the following for loop.
    r3=re.compile('[^+]+')

    # %% splitting
    sp1 = r1.match(str)
    option1 = sp1.group(1)
    # option1: 'ALUP 3X4'
    match1 = sp1.group(3)
    # match1: 'FB CRS FRI 7 * (2:0)@8.5 + (2:1)@7.5 / FB HAD FRI 9 * [Troyes] 2@2.26 / FB CRS FRI 10 * (2:0)@8.5 + (3:0)@17'
    match2 = r2.findall(match1)
    # match2: 3 parts
    match3 = list()
    for m in match2:
        mm = r3.findall(m)
        match3.append(mm)

    # %% "+" processing
    match_sp = list()

    for row in match3:
        row1 = row[0]
        sterInd = row1.find('*')
        gameStr = row1[:sterInd]
        gameStr = gameStr.strip()

        match_temp = list()
        for col in row:
            if col.find('*') == -1:
                match_temp.append(gameStr + ' * ' + col.strip())
            else:
                match_temp.append(col.strip())

        match_sp.append(match_temp)


    # %% split multiple into M*1 or M*N: input:: match_sp
    mxns = multi_sp(match_sp)

    # %% M*N combination:
    combs = list()

    #mn_type = '3X4'
    mn_type = option1[option1.find(' ')+1:]
    m_option = mn[mn_type]

    # levels
    if 1 in m_option:
        combs = mxns;
    else:
        for level in range(2,9):
            if level in m_option:
                for mxn in mxns:
                    iter_var = itertools.combinations(mxn,level)
                    a = list(iter_var)
                    for aa in a:
                        combs.append(aa)



    # comb_all=list()
    comb_all = comb_filter(combs)
    return comb_all


def multi_sp(match_sp):
    """
    split multiple into 1 M*N
    """
    mns = list()
    mn = list(match_sp[0])
    for mx1_temp in mn:
        list_temp = list()
        list_temp.append(mx1_temp)
        mns.append(list_temp)

    for i in range(1,len(match_sp)):
        # mx1: a list of all existing combinations for i-1 levels
        level_i = match_sp[i]
        level_i_n = len(level_i)

        for n in range(len(mns)):
            mn = mns[n]
            for j in range(1,level_i_n):
                mx1_new = list(mn)
                mx1_new.append(level_i[j])
                mns.append(mx1_new)
            mn.append(level_i[0])

    return mns


# %% ==== main API ====
def tk_split():
    """
    import
    all data from csv files in a batch
    """
    import csv
    tableName=infos.tableName
    n_once=infos.n_once
    sqlitePath = infos.sqlitePath

    db_diver = infos.db
    RDS_ip = infos.RDS_ip

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",port=3306,charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)


    cu = conn.cursor()

    fn='fb20141231.csv\\fb20141231.csv'

    i = 0
    sid = 0
    #while True:    

    with open(fn) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for b in spamreader:

            if not b:
                break

            #print(b)
            i += 1


            c1 = b[0] # tid
            c2 = b[1] # SellingTime
            c3 = b[2] # UnitInvestment
            c4 = b[3] # TotalInvestment
            c5 = b[4] # ProviceCentre
            c6 = b[5] # TerminalNo
            # b[6]
            c8 = b[7] # betting type
            c = b[8] # ticket detail

            if c.find('FSGL')!=-1:
                c7 = 1
                n = 1
            elif c[c.find(' ')+2] == 'X':
                c7 = float(c[c.find('X')-1])
                n = float(c[c.find('X')+1])

            c_upper = c.upper()

            try:
                if  c_upper.find('CANCEL') != -1:
                    insert_sql_err = 'insert into ' + tableName + '_errlog' + ' values(?,?,?,?,?,?,?,?,?);'
                    insert_args_err = b
                    cu.execute(insert_sql_err, insert_args_err)
                else:
                    #if c_upper.find('SGL') != -1:
                        #insert_sql_plus = 'insert into ' + tableName + '_sgl' + ' values(?,?,?,?,?,?,?,?,?);'
                        #insert_args_plus = b
                        #cu.execute(insert_sql_plus, insert_args_plus)
                    #elif c_upper.find('+') != -1:
                        #insert_sql_plus = 'insert into ' + tableName + '_plus' + ' values(?,?,?,?,?,?,?,?,?);'
                        #insert_args_plus = b
                        #cu.execute(insert_sql_plus, insert_args_plus)

    # %% into _info
                    if db_diver == 'mysql':
                        insert_sql_info = 'insert into ' + tableName + '_info' + ' values(%s,%s,%s,%s,%s,%s,%s,%s);'
                    else:
                        insert_sql_info = 'insert into ' + tableName + '_info' + ' values(?,?,?,?,?,?,?,?);'

                    #insert_args_info = [c1,datetime.datetime.strptime(c2,'%Y-%m-%d %H:%M:%S'),c3,c4,c5,c6,c7,c8]
                    insert_args_info = [c1,c2,c3,c4,c5,c6,c7,c8]
                    cu.execute(insert_sql_info, insert_args_info)

    # %% into _mx1
                    if c_upper.find('+') != -1 or n != 1: # multiple or m*n
                        d=multi_mn_split(c)
                    else:
                        d=[c]

                    c_inv_allup = float(c4)/len(d)

                    for x1 in d:
                        sid += 1
                        if db_diver == 'mysql':
                            insert_sql_mx1 = 'insert into ' + tableName + '_mx1' + ' values(%s,%s,%s);'
                        else:
                            insert_sql_mx1 = 'insert into ' + tableName + '_mx1' + ' values(?,?,?);'
                        insert_args_mx1 = [sid,c1,c_inv_allup]
                        cu.execute(insert_sql_mx1, insert_args_mx1)

                        # ## prepare for insert into _matches
                        tk_level_rows = tk_proc(x1)
                        # tk_level_rows.extend(tk_level_row)

    # %% into _matches
                        # ## insert splited tickets
                        c_inv_match = float(c4)/len(tk_level_rows)

                        for g in tk_level_rows:
                            if db_diver == 'mysql':
                                insert_sql = 'insert into ' + tableName + '_matches' + ' values(%s,%s,%s,%s,%s,%s,%s);'
                            else:
                                insert_sql = 'insert into ' + tableName + '_matches' + ' values(?,?,?,?,?,?,?);'

                            insert_args = [sid,c_inv_match] + g
                            cu.execute(insert_sql, insert_args)

            except Exception as e:
                print('current No is: {0}'.format(c1))
                print(e)
                if db_diver == 'mysql':
                    insert_sql_err = 'insert into ' + tableName + '_errlog' + ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s);'
                else:
                    insert_sql_err = 'insert into ' + tableName + '_errlog' + ' values(?,?,?,?,?,?,?,?,?);'
                insert_args_err = b
                cu.execute(insert_sql_err, insert_args_err)
                break

            if i>=n_once:
                i = 0
                conn.commit() # key factor for performance
                print('{0}: {1} :: {2} '.format(c1, c2, c))

    if i: # to commit those insert action after n*n_once
        conn.commit() # key factor for performance
        print('==== end of the day is: '+str(i))
        print('{0}: {1} :: {2} '.format(c1, c2, c))

    print(':: Split all tickets successfully.')
    print('============ split line ============')

    cu.close()
    conn.close()


# %% main functions    
def ReadAndUpdate_match_info():
    """
    to import and init
    table: match_info
    """
    import xlrd

    target_table = 'match_info'

    sqlitePath = infos.sqlitePath

    mc_map = infos.WeekMap_cn

    db_diver = infos.db
    RDS_ip = infos.RDS_ip

    excelName='2014full.xlsx'

    sheetName = 'Source_FB'
    startRow = 8


    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    # ==== clear table ====
    cu.execute('delete from ' + target_table + ';')
    print(':: All the tables got cleared.')


    # ==== import into db ====
    curRow = startRow

    os.chdir(infos.excelPath)
    bk = xlrd.open_workbook(excelName)
    sh = bk.sheet_by_name(sheetName)
    totalRows = sh.nrows

    print('Available rows/area is: %s' %totalRows)

    j = 0
    for i in xrange(curRow, totalRows):
        j+=1

        rowi = sh.row_values(i)    # the index starts from 0, so no need curRow+1

        #### columns in sqlite   
        bi = [j] #mid
        #bi.append(rowi[1]) #match_date
        bi.append(datetime.datetime(*xlrd.xldate_as_tuple(rowi[1], bk.datemode))) # "*" can unpack tuple into several var as input only (can not save as a var)

        #bi.append(rowi[2]) #match_code
        bi.append(mc_map.get(rowi[2][0:2])+rowi[2][2:])

        bi.append(0) #st_id
        bi.append(rowi[3]) #match_league
        bi.append(rowi[6]) #
        bi.append(rowi[7]) #
        bi.append(rowi[8])
        bi.append(rowi[10])
        bi.append(rowi[11])
        bi.append(rowi[13])
        bi.append(0) # state
        bi.append(datetime.datetime.now()) # create_time
        bi.append(0) # auto_stop
        bi.append(0) # hold
        bi.append('') #week_id

        print(bi)
        if db_diver == 'mysql':
            insert_sql_info = 'insert into ' + target_table + ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        else:
            insert_sql_info = 'insert into ' + target_table + ' values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'

        insert_args_info = bi
        cu.execute(insert_sql_info, insert_args_info)

    conn.commit()
    print(':: import finished.')

    cu.close()
    conn.close()

    print(':: Updated to latest fixture successfully.')
    print('============ split line ============')


def ReadAndUpdate_match_odds():
    """
    to import and init
    table: match_odds
    """
    import xlrd

    target_table = 'match_odds'

    sqlitePath = infos.sqlitePath

    mc_map = infos.WeekMap_cn

    db_diver = infos.db
    RDS_ip = infos.RDS_ip

    excelName='HKPrice BET.xlsm'

    sheetName = 'Pool'
    startRow = 4


    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    # ==== clear table ====
    cu.execute('delete from ' + target_table + ';')
    print(':: All the tables got cleared.')


    # ==== import into db ====
    curRow = startRow

    os.chdir(infos.excelPath)
    bk = xlrd.open_workbook(excelName)
    sh = bk.sheet_by_name(sheetName)
    totalRows = sh.nrows

    options = ['1','X','2']
    col_weekNum = 46
    col_home_odds = 32
    col_home_h_odds = 43
    col_matchcode = 48
    col_hhad_line = 38

    print('Available rows/area is: %s' %totalRows)

    # %% mid(match_info中的主键)去关联 match_odds中的mid
    cu.execute('select match_code,mid from match_info;')
    mysql_table=cu.fetchall()

    keys = list()
    for itm in mysql_table:
        key = str(itm[0])
        keys.append(key)

    vals = list()
    for itm in mysql_table:
        key = str(itm[1])
        vals.append(key)

    mdict = dict(zip(keys, vals))

    # %% global initial position_limit
    cu.execute('select dictionary_value from dictionary_table where dictionary_name = "initPositionLimit";')
    mysql_table_positionLimit=cu.fetchall()
    position_limit = mysql_table_positionLimit[0][0]


    # %% insert into db
    j = 0
    for i in xrange(curRow, totalRows):
        rowi = sh.row_values(i)    # the index starts from 0, so no need curRow+1
        #print(rowi[col_matchcode])
        #mid = mdict.get(str(int(rowi[col_weekNum]))+mc_map.get(rowi[col_matchcode][0:2])+rowi[col_matchcode][2:])
        mid = mdict.get(mc_map.get(rowi[col_matchcode][0:2])+rowi[col_matchcode][2:])

        #### columns in db
        for i in range(3):
            if not rowi[col_matchcode]:
                break

            j+=1
            #col: odd_id
            bi = [None]
            #col: mid
            # print(rowi[143]) # match_code
            bi.append(mid)
            #col: betting_product(play_type)
            bi.append('HAD')
            #col: opt (result):: l_opt(1x2)
            bi.append(options[i])
            #col: handicap (concede_points):: hhad line 
            bi.append('')
            #col: opening_price
            opening_price = rowi[col_home_odds+i]
            if opening_price == '':
                opening_price = 0
            bi.append(opening_price)
            #col: last_price
            bi.append(opening_price)
            #col: current_price
            bi.append(opening_price)
            #col: unconfirm_price
            bi.append(0)
            #col: position_limit
            bi.append(position_limit)
            #col: update_time
            bi.append(datetime.datetime.now())
            #col: last_update_time
            bi.append(datetime.datetime.now())

            if db_diver == 'mysql':
                insert_sql_info = 'insert into ' + target_table + ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            else:
                insert_sql_info = 'insert into ' + target_table + ' values(?,?,?,?,?,?,?,?,?,?,?,?);'

            insert_args_info = bi
            print(bi)
            cu.execute(insert_sql_info, insert_args_info)


        for i in range(3):
            if not rowi[col_matchcode]:
                break

            j+=1
            #col: odd_id
            bi = [None]
            #col: mid
            # print(rowi[143]) # match_code
            bi.append(mid)
            #col: betting_product(play_type)
            bi.append('HHAD')
            #col: opt (result):: l_opt(1x2)
            if i != 2:
                bi.append(options[i]+'['+str(int(rowi[col_hhad_line]))+']')
            else:
                bi.append(options[i]+'['+str(0-int(rowi[col_hhad_line]))+']')
            #col: handicap (concede_points):: hhad line
            if i !=2:
                bi.append(int(rowi[col_hhad_line]))
            else:
                bi.append(0-int(rowi[col_hhad_line]))
            #col: opening_price
            opening_price = rowi[col_home_h_odds+i]
            if opening_price == '':
                opening_price = 0
            bi.append(opening_price)
            #col: last_price
            bi.append(opening_price)
            #col: current_price
            bi.append(opening_price)
            #col: unconfirm_price
            bi.append(0)
            #col: position_limit
            bi.append(position_limit)
            #col: update_time
            bi.append(datetime.datetime.now())
            #col: last_update_time
            bi.append(datetime.datetime.now())

            if db_diver == 'mysql':
                insert_sql_info = 'insert into ' + target_table + ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            else:
                insert_sql_info = 'insert into ' + target_table + ' values(?,?,?,?,?,?,?,?,?,?,?,?);'

            insert_args_info = bi
            cu.execute(insert_sql_info, insert_args_info)



    conn.commit()
    print(':: import finished.')

    cu.close()
    conn.close()

    print(':: Import local odds successfully.')
    print('============ split line ============')

    ReadAndUpdate_match_opening_odds()


def ReadAndUpdate_match_opening_odds():
    """
    to import and init
    table: match_opening_odds
    """
    import xlrd

    target_table = 'match_opening_odds'

    sqlitePath = infos.sqlitePath

    mc_map = infos.WeekMap_cn

    db_diver = infos.db
    RDS_ip = infos.RDS_ip

    excelName='HKPrice BET.xlsm'

    sheetName = 'Pool'
    startRow = 4


    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    # ==== clear table ====
    cu.execute('delete from ' + target_table + ';')
    print(':: All the tables got cleared.')


    # ==== import into db ====
    curRow = startRow

    os.chdir(infos.excelPath)
    bk = xlrd.open_workbook(excelName)
    sh = bk.sheet_by_name(sheetName)
    totalRows = sh.nrows

    options = ['1','X','2']
    col_weekNum = 46
    col_home_odds = 28
    col_home_h_odds = 39
    col_matchcode = 48
    col_hhad_line = 38

    print('Available rows/area is: %s' %totalRows)

    # %% mid(match_info中的主键)去关联 match_odds中的mid
    cu.execute('select match_code,mid from match_info;')
    mysql_table=cu.fetchall()

    keys = list()
    for itm in mysql_table:
        key = str(itm[0])
        keys.append(key)

    vals = list()
    for itm in mysql_table:
        key = str(itm[1])
        vals.append(key)

    mdict = dict(zip(keys, vals))

    # %% global initial position_limit
    cu.execute('select dictionary_value from dictionary_table where dictionary_name = "initPositionLimit";')
    mysql_table_positionLimit=cu.fetchall()
    position_limit = mysql_table_positionLimit[0][0]


    # %% insert into db
    j = 0
    for i in xrange(curRow, totalRows):
        rowi = sh.row_values(i)    # the index starts from 0, so no need curRow+1
        #print(rowi[col_matchcode])
        # mid = mdict.get(str(int(rowi[col_weekNum]))+mc_map.get(rowi[col_matchcode][0:2])+rowi[col_matchcode][2:])
        mid = mdict.get(mc_map.get(rowi[col_matchcode][0:2])+rowi[col_matchcode][2:])

        #### columns in db
        for i in range(3):
            if not rowi[col_matchcode]:
                break

            j+=1
            #col: odd_id
            bi = [None]
            #col: mid
            # print(rowi[143]) # match_code
            bi.append(mid)
            #col: betting_product(play_type)
            bi.append('HAD')
            #col: opt (result):: l_opt(1x2)
            bi.append(options[i])
            #col: handicap (concede_points):: hhad line
            bi.append('')
            #col: opening_price
            opening_price = rowi[col_home_odds+i]
            if opening_price == '':
                opening_price = 0
            bi.append(opening_price)
            #col: last_price
            bi.append(opening_price)
            #col: current_price
            bi.append(opening_price)
            #col: unconfirm_price
            bi.append(0)
            #col: position_limit
            bi.append(position_limit)
            #col: update_time
            bi.append(datetime.datetime.now())
            #col: last_update_time
            bi.append(datetime.datetime.now())

            if db_diver == 'mysql':
                insert_sql_info = 'insert into ' + target_table + ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            else:
                insert_sql_info = 'insert into ' + target_table + ' values(?,?,?,?,?,?,?,?,?,?,?,?);'

            insert_args_info = bi
            print(bi)
            cu.execute(insert_sql_info, insert_args_info)


        for i in range(3):
            if not rowi[col_matchcode]:
                break

            j+=1
            #col: odd_id
            bi = [None]
            #col: mid
            # print(rowi[143]) # match_code
            bi.append(mid)
            #col: betting_product(play_type)
            bi.append('HHAD')
            #col: opt (result):: l_opt(1x2)
            if i != 2:
                bi.append(options[i]+'['+str(int(rowi[col_hhad_line]))+']')
            else:
                bi.append(options[i]+'['+str(0-int(rowi[col_hhad_line]))+']')
            #col: handicap (concede_points):: hhad line
            if i !=2:
                bi.append(int(rowi[col_hhad_line]))
            else:
                bi.append(0-int(rowi[col_hhad_line]))
            #col: opening_price
            opening_price = rowi[col_home_h_odds+i]
            if opening_price == '':
                opening_price = 0
            bi.append(opening_price)
            #col: last_price
            bi.append(opening_price)
            #col: current_price
            bi.append(opening_price)
            #col: unconfirm_price
            bi.append(0)
            #col: position_limit
            bi.append(position_limit)
            #col: update_time
            bi.append(datetime.datetime.now())
            #col: last_update_time
            bi.append(datetime.datetime.now())

            if db_diver == 'mysql':
                insert_sql_info = 'insert into ' + target_table + ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            else:
                insert_sql_info = 'insert into ' + target_table + ' values(?,?,?,?,?,?,?,?,?,?,?,?);'

            insert_args_info = bi
            cu.execute(insert_sql_info, insert_args_info)



    conn.commit()
    print(':: import finished.')

    cu.close()
    conn.close()

    print(':: Import opening odds successfully.')
    print('============ split line ============')






def InitAndUpdate_match_product():
    """
    to init
    table: match_product
    """
    target_table = 'match_product'

    sqlitePath = infos.sqlitePath

    db_diver = infos.db
    RDS_ip = infos.RDS_ip

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    # ==== clear table ====
    cu.execute('delete from ' + target_table + ';')
    print(':: All the tables got cleared.')


    #%% init a new table from 2 joined tables
    ## raw mysql:
    # select 1 'pid', mo.mid, mo.betting_product, mo.update_time selling_time, mi.create_time, mo.handicap_line, 0 'single_enable', 0 'all_up_enbale', 0 'pool_state',  null 'pool_result', 0 'max_netloss'
    # from match_info mi join match_odds mo on mi.mid = mo.mid
    # where LEFT(mo.opt,1) = '1';
    cu.execute('select mo.mid, mo.betting_product, mo.update_time selling_time, mi.create_time, mo.handicap_line\
    from match_info mi join match_odds mo on mi.mid = mo.mid where LEFT(mo.opt,1) = "1";')
    mysql_table=cu.fetchall()

    #%% insert into db
    for rowi in mysql_table:
        #col: pid
        bi = [None]
        #col: mid
        bi.append( rowi[0])
        #col: betting_product(play_type)
        bi.append(rowi[1])
        #col: selling_time
        bi.append(rowi[2])
        #col: create_time
        bi.append(rowi[3])
        #col: handicap_line
        bi.append(rowi[4])
        #col: single_enable
        bi.append(0)
        #col: all_up_enable
        bi.append(0)
        #col: pool_state
        bi.append(0)
        #col: pool_result
        bi.append('')
        #col: pool_result
        bi.append(0)

        if db_diver == 'mysql':
            insert_sql_info = 'insert into ' + target_table + ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        else:
            insert_sql_info = 'insert into ' + target_table + ' values(?,?,?,?,?,?,?,?,?,?,?);'

        insert_args_info = bi
        print(bi)
        cu.execute(insert_sql_info, insert_args_info)





    conn.commit()
    print(':: import finished.')

    cu.close()
    conn.close()

    print(':: Initialize HAD/HHAD pools successfully.')
    print('============ split line ============')








def redis_mo_current_price():
    '''
    to sync
    table: match_odds.current_price 
    redis
    '''

    sqlitePath = infos.sqlitePath
    db_diver = infos.db
    RDS_ip = infos.RDS_ip
    ECS_ip = infos.ECS_ip

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    import redis
    cu_r = redis.Redis(host=ECS_ip, port=6379, db = 0)

    #%% mid(match_info中的主键)去关联 match_odds中的mid
    cu.execute('select week_id,match_code,mo.betting_product,opt,current_price\
                from match_info mi join match_odds mo on mi.mid=mo.mid;')
    mysql_table = cu.fetchall()

    # clear existing local odds
    wild_keys = '*' +'currentFixedPrize'+ '*'
    existing_keys = cu_r.keys(wild_keys)
    for existing_key in existing_keys:
        cu_r.delete(existing_key)

    # import into redis
    for rowi in mysql_table:
        week_id = str(rowi[0])
        match_code = str(rowi[1])
        betting_product = rowi[2]
        opt = str(rowi[3])
        key = match_code+betting_product+'currentFixedPrize'+opt
        val = rowi[4]
        print('Redis Key and Val: %s, %s' % (key, val))
        cu_r.set(key, val)

    cu.close()
    conn.close()



def redis_mp_pool_state():
    '''
    to sync
    table: mysql_product.pool_state 
    redis
    '''

    sqlitePath = infos.sqlitePath
    db_diver = infos.db
    RDS_ip = infos.RDS_ip
    ECS_ip = infos.ECS_ip

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    import redis
    cu_r = redis.Redis(host=ECS_ip, port=6379, db = 0)

    #%% mid(match_info中的主键)去关联 match_odds中的mid
    cu.execute('select mi.week_id, mi.match_code, mp.betting_product, mp.pool_state \
                from match_info mi join match_product mp on mi.mid = mp.mid;')
    mysql_table = cu.fetchall()

    # clear existing local odds
    wild_keys = '*' +'HADpoolState'+ '*'
    existing_keys = cu_r.keys(wild_keys)
    for existing_key in existing_keys:
        cu_r.delete(existing_key)

    # import into redis
    for rowi in mysql_table:
        week_id = str(rowi[0])
        match_code = str(rowi[1])
        betting_product = rowi[2]

        key = match_code+betting_product+'poolState'
        val = rowi[3]
        print('Redis Key and Val: %s, %s' % (key, val))
        cu_r.set(key, val)

    cu.close()
    conn.close()




def redis_mp_pool_result():
    '''
    to sync
    table: mysql_product.pool_state
    redis
    '''

    sqlitePath = infos.sqlitePath
    db_diver = infos.db
    RDS_ip = infos.RDS_ip
    ECS_ip = infos.ECS_ip

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    import redis
    cu_r = redis.Redis(host=ECS_ip, port=6379, db = 0)

    #%% mid(match_info中的主键)去关联 match_odds中的mid
    cu.execute('select mi.week_id, mi.match_code, mp.betting_product, mp.pool_result \
                from match_info mi join match_product mp on mi.mid = mp.mid;')
    mysql_table = cu.fetchall()

    # clear existing local odds
    wild_keys = '*' +'HADresult'+ '*'
    existing_keys = cu_r.keys(wild_keys)
    for existing_key in existing_keys:
        cu_r.delete(existing_key)

    # import into redis
    for rowi in mysql_table:
        week_id = str(rowi[0])
        match_code = str(rowi[1])
        betting_product = rowi[2]

        key = match_code+betting_product+'result'
        val = rowi[3]
        print('Redis Key and Val: %s, %s' % (key, val))
        cu_r.set(key, val)

    cu.close()
    conn.close()


def redis_mo_position_limit():
    '''
    to sync
    table: mysql_odds.postion_limit
    redis
    '''
    sqlitePath = infos.sqlitePath
    db_diver = infos.db
    RDS_ip = infos.RDS_ip
    ECS_ip = infos.ECS_ip

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    import redis
    cu_r = redis.Redis(host=ECS_ip, port=6379, db = 0)

    #%% mid(match_info中的主键)去关联 match_odds中的mid
    cu.execute('select mi.week_id, mi.match_code, mo.betting_product, mo.opt , mo.position_limit\
                from match_info mi join match_odds mo on mi.mid = mo.mid;')
    mysql_table = cu.fetchall()

    # clear existing local odds
    wild_keys = '*' + 'PositionLimit' + '*'
    existing_keys = cu_r.keys(wild_keys)
    for existing_key in existing_keys:
        cu_r.delete(existing_key)

    # import into redis
    for rowi in mysql_table:
        week_id = str(rowi[0])
        match_code = str(rowi[1])
        betting_product = rowi[2]
        opt = str(rowi[3])
        key = match_code+betting_product+'PositionLimit'+opt
        val = rowi[4]
        print('Redis Key and Val: %s, %s' % (key, val))
        cu_r.set(key, val)

    # %% for allUpPositionLimit+玩法+关数 如：allUpPositionLimitHHAD3
    cu.execute('select * from position_limit;')
    mysql_table = cu.fetchall()

    # clear existing local odds
    wild_keys = '*' + 'allUpPositionLimit' + '*'
    existing_keys = cu_r.keys(wild_keys)
    for existing_key in existing_keys:
        cu_r.delete(existing_key)

    # import into redis
    for rowi in mysql_table:
        j = 1
        product = rowi[1]

        # j =+1 # 2
        # leveln = str(j)
        # key = 'allUpPositionLimit' + product + leveln
        # val = rowi[j]
        # print('Redis Key and Val: %s, %s' % (key, val))
        # cu_r.set(key, val)

        for j in range(2,9):
            leveln = str(j)
            key = 'allUpPositionLimit' + product + leveln
            val = rowi[j]
            print('Redis Key and Val: %s, %s' % (key, val))
            cu_r.set(key, val)

    cu.close()
    conn.close()




def redis_dictionary_table():
    '''
    to sync
    table: dictionary_table
    redis
    '''

    sqlitePath = infos.sqlitePath
    db_diver = infos.db
    RDS_ip = infos.RDS_ip
    ECS_ip = infos.ECS_ip

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    import redis
    cu_r = redis.Redis(host=ECS_ip, port=6379, db = 0)



    #%% mid(match_info中的主键)去关联 match_odds中的mid
    cu.execute('select dictionary_name,dictionary_value \
                from dictionary_table;')
    mysql_table = cu.fetchall()

    # # clear existing local odds
    # wild_keys = '*' +'HADpoolState'+ '*'
    # existing_keys = cu_r.keys(wild_keys)
    # for existing_key in existing_keys:
    #     cu_r.delete(existing_key)

    # import into redis
    for rowi in mysql_table:
        key = rowi[0]

        val = rowi[1]
        print('Redis Key and Val: %s, %s' % (key, val))
        cu_r.set(key, val)

    cu.close()
    conn.close()




def redis_position_limit_all():
    '''
    to sync
    table: position_limit_all
    redis
    '''

    sqlitePath = infos.sqlitePath
    db_diver = infos.db
    RDS_ip = infos.RDS_ip
    ECS_ip = infos.ECS_ip

    st = infos.sport_type

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    import redis
    cu_r = redis.Redis(host=ECS_ip, port=6379, db = 0)


    #%% Mysql table reading
    st_id = 1
    sport_type = st[st_id]

    cu.execute('select type, position_type,' + sport_type + ' from position_limit_all;')
    mysql_table = cu.fetchall()

    map_pos_type = {1:'PositionPercentLimit',2:'PositionLimitMax'}

    #%% import into redis
    for rowi in mysql_table:
        key = rowi[1] + str(st_id) + map_pos_type[rowi[0]]
        val = rowi[2]
        print('Redis Key and Val: %s, %s' % (key, val))
        cu_r.set(key, val)

    cu.close()
    conn.close()



def redis_big_small_invest():
    '''
    to sync
    table: big_small_invest
    redis
    '''

    sqlitePath = infos.sqlitePath
    db_diver = infos.db
    RDS_ip = infos.RDS_ip
    ECS_ip = infos.ECS_ip

    st = infos.sport_type

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    import redis
    cu_r = redis.Redis(host=ECS_ip, port=6379, db = 0)


    #%% Mysql table reading
    st_id = 1
    sport_type = st[st_id]

    cu.execute('select type, position_type,' + sport_type + ' from big_small_invest;')
    mysql_table = cu.fetchall()

    map_pos_type = {1:'allSmallInvest',2:'allBigInvest'}


    # allSmallInvestHHADFOOTBALL, allBigInvestHHADFOOTBALL
    #%% import into redis
    for rowi in mysql_table:
        key = map_pos_type[rowi[0]] + rowi[1] + str(st_id)
        val = rowi[2]
        print('Redis Key and Val: %s, %s' % (key, val))
        cu_r.set(key, val)

    cu.close()
    conn.close()



def redis_risk_limit_warning_percent():
    '''
    to sync
    table: risk_limit_warning_percent
    redis
    '''

    sqlitePath = infos.sqlitePath
    db_diver = infos.db
    RDS_ip = infos.RDS_ip
    ECS_ip = infos.ECS_ip

    st = infos.sport_type

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    import redis
    cu_r = redis.Redis(host=ECS_ip, port=6379, db = 0)


    #%% Mysql table reading
    st_id = 1
    sport_type = st[st_id]

    for i in range(2,9):
        initial = 'xn' + str(i) + '_initial'
        incremental = 'xn' + str(i) + '_incremental'
        bounceback = 'xn' + str(i) + '_bounceback'

        cu.execute('select type, pool, '+ initial + ',' + incremental + ',' + bounceback + ' from risk_limit_warning_percent;')
        mysql_table = cu.fetchall()

        ## import into redis
        initial = 'XN' + str(i) + ':INITIAL'
        incremental = 'XN' + str(i) + ':INCREMENTAL'
        bounceback = 'XN' + str(i) + ':BOUNCEBACK'

        for rowi in mysql_table:
            key = str(rowi[0]) + ':' + rowi[1].upper() + ':' + initial
            val = rowi[2]
            print('Redis Key and Val: %s, %s' % (key, val))
            cu_r.set(key, val)

            key = str(rowi[0]) + ':' + rowi[1].upper() + ':' + incremental
            val = rowi[3]
            print('Redis Key and Val: %s, %s' % (key, val))
            cu_r.set(key, val)

            key = str(rowi[0]) + ':' + rowi[1].upper() + ':' + bounceback
            val = rowi[4]
            print('Redis Key and Val: %s, %s' % (key, val))
            cu_r.set(key, val)

    cu.close()
    conn.close()



def redis_position_singlecallpmsort():
    '''
    to sync
    table: position_singlecallpmsort
    redis
    '''

    sqlitePath = infos.sqlitePath
    db_diver = infos.db
    RDS_ip = infos.RDS_ip
    ECS_ip = infos.ECS_ip

    st = infos.sport_type

    # ====connect and reset db====
    if db_diver == 'mysql':
        import MySQLdb
        conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters

        #import pymysql
        #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    else:
        import sqlite3
        conn=sqlite3.connect(sqlitePath)

    cu = conn.cursor()

    import redis
    cu_r = redis.Redis(host=ECS_ip, port=6379, db = 0)


    #%% Mysql table reading
    st_id = 1
    sport_type = st[st_id]

    for i in range(1,4):
        min_position = 'min_position' + str(i)
        max_position = 'max_position' + str(i)

        cu.execute('select type, betting_product, '+ min_position + ',' + max_position + ' from position_singlecallpmsort;')
        mysql_table = cu.fetchall()

        ## import into redis
        min_position = 'singleMinPosition' + str(i)
        max_position = 'singleMaxNetloss' + str(i)

        for rowi in mysql_table:
            key = min_position + rowi[1] + str(st_id)
            val = rowi[2]
            print('Redis Key and Val: %s, %s' % (key, val))
            cu_r.set(key, val)

            key = max_position + rowi[1] + str(st_id)
            val = rowi[3]
            print('Redis Key and Val: %s, %s' % (key, val))
            cu_r.set(key, val)

    cu.close()
    conn.close()


def redis_order_ticket():
    '''
    to sync
    table: order_ticket:tid
    redis
    '''

    #%% Mysql table reading
    cu.execute('select tid from order_ticket;')
    mysql_table = cu.fetchall()

    # allSmallInvestHHADFOOTBALL, allBigInvestHHADFOOTBALL
    #%% import into redis
    for rowi in mysql_table:
        key = str(rowi[0]) + 'saleresult'
        val = 1
        print('Redis Key and Val: %s, %s' % (key, val))
        cu_r.set(key, val)

def hadoop_hdfs_rm():
    '''
    to clean
    hdfs dfs -rm -r /[0-9]
    hdfs
    '''

    from subprocess import Popen, PIPE

    # cmd = '/opt/hadoop-2.7.0/bin/hdfs dfs -ls /'
    cmd = 'sudo /opt/hadoop-2.7.0/bin/hdfs dfs -rm -r hdfs:///*'

    p_cmd = Popen(cmd.split(), stdin=PIPE, stdout=PIPE)
    p_cmd.communicate()
    if p_cmd.returncode:
        print("## ERROR: HDFS clean failed!")
        exit(2)









def redis_mi_SomeKeys():
    '''
    to sync
    table: match_info.match_code
    redis
    '''

    #%% mid(match_info中的主键)去关联 match_odds中的mid
    cu.execute('select mi.match_code \
                from match_info mi;')
    mysql_table = cu.fetchall()

    # import into redis
    for rowi in mysql_table:
        key1 = str(rowi[0]) + 'InplayMark'
        val1 = 0
        print('Redis Key and Val: %s, %s' % (key1, val1))
        cu_r.set(key1, val1)

        key2 = str(rowi[0]) + 'Statistics'
        val2 = '0000-0000-0000-0000-0000-0000-0000'
        print('Redis Key and Val: %s, %s' % (key2, val2))
        cu_r.set(key2, val2)


def redis_flushdb():
    '''
    to sync
    flushdb
    redis
    '''

    RDS_ip = infos.RDS_ip
    ECS_ip = infos.ECS_ip

    import redis
    cu_r = redis.Redis(host=ECS_ip, port=6379, db=0)
    cu_r.flushdb()


def runAll():
    redis_mo_current_price()
    redis_mo_position_limit()
    redis_mp_pool_state()
    redis_mp_pool_result()
    redis_dictionary_table()
    redis_position_limit_all()
    redis_big_small_invest()
    redis_risk_limit_warning_percent()
    redis_position_singlecallpmsort()
    redis_mi_SomeKeys()
    redis_order_ticket()

    hadoop_hdfs_rm()



def isatest():
    print('ip: ' + infos.ip)

## ============================================
if __name__ == "__main__":
    infos = TheInfo()

    # # ====connect and reset db====
    # sqlitePath = infos.sqlitePath
    # db_diver = infos.db
    # RDS_ip = infos.RDS_ip
    # ECS_ip = infos.ECS_ip
    #
    # if db_diver == 'mysql':
    #     import MySQLdb
    #     conn = MySQLdb.connect(host=RDS_ip,user="caiex",passwd="12345678",db="caiex",charset="utf8") # ,conv=type_converters
    #
    #     #import pymysql
    #     #conn=pymysql.connect(host=RDS_ip,user='caiex',passwd='12345678',db='caiex',port=3306,charset='utf8')
    # else:
    #     import sqlite3
    #     conn=sqlite3.connect(sqlitePath)
    #
    # import redis
    # cu_r = redis.Redis(host=ECS_ip, port=6379, db = 0)


    # pySqliteReCreate()
    starttime=datetime.datetime.now()
    main()
    endtime=datetime.datetime.now()
    print(endtime-starttime)
