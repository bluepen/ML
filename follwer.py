import requests,json,time
from other import getUser_Agent,getIpList
import threading,logging
import pymysql
import re

header = getUser_Agent.getUser_Agent()
proxies = getIpList.getProxy()

def getInfo(url):
    url = url
    reps = requests.get(url=url,headers=header,proxies=proxies)
    data = json.loads(reps.content.decode("utf-8"))
    for i in data['data']:
        print(i)

#返回用户所关注的用户信息列表
def getUrlTokensDetails(url):

    url_tokens_list = []
    page = 0
    s_url = url.format(str(page*20))
    print(s_url)
    reps = requests.get(url=s_url,headers=header)
    data = json.loads(reps.content.decode("utf-8"))
    #类似do
    for da in data['data']:
        # print(da)
        url_tokens_dict = {}
        url_tokens_dict["url_token"] = da['url_token']
        url_tokens_dict["headline"] = da["headline"]
        url_tokens_dict["name"] = da["name"]
        url_tokens_dict["follower_count"] = da["follower_count"]
        url_tokens_dict["articles_count"] = da["articles_count"]
        url_tokens_dict["answer_count"] = da["answer_count"]
        if len(da["badge"]):
            url_tokens_dict["description"] = da["badge"][0]['description']
        else:
            url_tokens_dict["description"] = "无"

        url_tokens_list.append(url_tokens_dict)

    is_end = str(data["paging"]["is_end"])
    print(is_end)

    while (is_end.lower() == "false"):
        print(data)
        page = int(page) + 1
        s_url = url.format(str(page * 20))
        print(s_url)
        reps = requests.get(url=s_url, headers=header)
        data = json.loads(reps.content.decode("utf-8"))
        is_end = str(data["paging"]["is_end"])
        for da in data['data']:
            # print(da)
            url_tokens_dict = {}
            url_tokens_dict["url_token"] = changeStr(da['url_token'])
            url_tokens_dict["headline"] = changeStr(da["headline"])
            url_tokens_dict["name"] = changeStr(da["name"])
            url_tokens_dict["follower_count"] = da["follower_count"]
            url_tokens_dict["articles_count"] = da["articles_count"]
            url_tokens_dict["answer_count"] = da["answer_count"]
            if len(da["badge"]):
                url_tokens_dict["description"] = da["badge"][0]['description']
            else:
                url_tokens_dict["description"] = "无"

            url_tokens_list.append(url_tokens_dict)

        print("sleeping...1.5seconds")
        time.sleep(1.5)

    print(str(url.split("/")[6]) + "关注了：" + str(len(url_tokens_list)))

    return url_tokens_list



#一次插入一条语句  将具体数据插入到数据库中
def insertIntoMysql(info_dict,tablename):

    # config = {
    #     "host":"localhost",
    #     "user":"root",
    #     "password":"root",
    #     "database":"test",
    #     "charset":"utf8",
    #     "port":"3306"
    # }
    # mysqlDB = pymysql.connect(**config)
    mysqlDB = pymysql.connect("localhost", "root", "root", "test", 3306, charset="utf8mb4")
    cursor = mysqlDB.cursor()
    sql = "INSERT INTO " + tablename + " (name,headline,url_token,answer_count,follower_count,articles_count,description) VALUES(\'{0}\',\'{1}\',\'{2}\',{3},{4},{5},\'{6}\')"

    sqlline = sql.format (str(info_dict['name']),str(info_dict['headline']),str(info_dict['url_token']),info_dict['answer_count'],info_dict['follower_count'],info_dict['articles_count'],info_dict['description'])
    print(sqlline)
    #检测table是否存在    不存在就创建
    try:
        cursor.execute("select * from {0}".format(tablename))
    except pymysql.err.ProgrammingError as e:
        logging.error(e)
        createMysqlTable(tablename)
        print(tablename + "创建完毕。")
    try:
        cursor.execute(sqlline)
        mysqlDB.commit()
    except KeyError as e:
        logging.error(e)
        pass
    finally:
        cursor.close()
        mysqlDB.close()

#创建一个数据表
def createMysqlTable(tablename):
    # config = {
    #     "host":"localhost",
    #     "user":"root",
    #     "password":"root",
    #     "database":"test",
    #     "charset": "utf-8",
    #     "port":"3306"
    # }
    mysqlDB = pymysql.connect("localhost","root","root","test",3306,charset="utf8mb4")
    # mysqlDB = pymysql.connect(**config)
    cursor = mysqlDB.cursor()

    sql = "select * from {0}".format(tablename)
    print(sql)
    try:
        data = cursor.execute(sql)
        print(tablename + "已经创建。")
    except pymysql.err.ProgrammingError as e:
        logging.error(e)#捕获异常   如果没有数据表就创建该数据表
        _sql = "create table " + tablename + "(id int(11) auto_increment not null primary key," \
                                            "url_token char(100)," \
                                            "name char(100)," \
                                            "headline longtext," \
                                            "answer_count int(20)," \
                                            "follower_count int(20)," \
                                            "articles_count int(20)," \
                                            "description longtext);"
        print(_sql)
        cursor.execute(_sql)

        print(tablename + "数据表创建完毕")
    # mysqlDB.commit()
    finally:
        cursor.close()
        mysqlDB.close()

#查询数据表中的数据条数 返回一个值
def getTableColumes(tablename):
    mysqlDB = pymysql.connect("localhost", "root", "root", "test", 3306, charset="utf8mb4")
    cursor = mysqlDB.cursor()
    try:
        columes = cursor.execute("select * from {}".format(tablename))
    except pymysql.err.ProgrammingError as e:
        logging.error(e)
        return 0
    return columes


#层次爬取  每一个用户的关注的用户表为一层
def levelCraw(url_token_list):
    time = 0 #控制次数

    for di in url_token_list:
        #在字典中找到新的url_token  用来进行递归循环
        url_token = di["url_token"]
        url = "https://www.zhihu.com/api/v4/members/"#合成一个新的URL
        url = url + str(url_token) + "/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={0}&limit=20"

        _url_tokens_list = getUrlTokensDetails(url)
        tablename = changeStr(url_token) + "_" + "followee"
        table_columes = getTableColumes(tablename)
        followee_length = len(_url_tokens_list)
        try:
            if len(_url_tokens_list):
                createMysqlTable(tablename)
        except Exception as e:
            logging.error(e)
        for di,i in zip(_url_tokens_list,range(followee_length)):
            if followee_length == table_columes:#数据已经下载过了   不再下载
                print("数据已经下载过了，跳过")
                break
            elif followee_length > table_columes and table_columes != 0:#下载了一半   在终端出继续下载
                print(tablename + "该数据表已经下载了一部分数据，从中断处开始下载，终端索引：" + str(i))
                if i >= table_columes:
                    insertIntoMysql(di,tablename)
                else:
                    pass
            else:#没有下载过的数据
                insertIntoMysql(di,tablename)



def changeStr(str_):
    s = ""
    #先判断
    if "." in str_:
        lis = str_.split(".")
        for li in lis:
            s = s + li

    elif "-" in str_:
        lis = str_.split("-")
        for li in lis:
            s = s + li
    elif "'" in str_:
        lis = str_.split("'")
        for li in lis:
            s = s + li
    else:
        return str_
    return s

#先放着   之后用递归实现
def digui(num):

    if num == 1:
        return 1
    else:
        return num * digui(num-1)



if __name__ == '__main__':
    '''
    需要抓取的字段
    headline 签名
    name 名字
    answer_count 回答问题的次数
    url_token 用户名
    follower_count 关注他的人数
    articles_count 文章数量
    description 所属部门
    '''
    # url_tokens = []
    #https://www.zhihu.com/api/v4/members/zhu-hong-gen/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=20&limit=20
    #https://www.zhihu.com/api/v4/members/zhu-hong-gen/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=40&limit=20

    #该用户的关注者 URL
    follower_url = "https://www.zhihu.com/api/v4/members/niu-ke-wang-53/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={0}&limit=20"

    #我的知乎首页
    url = "https://www.zhihu.com/api/v4/members/zhu-hong-gen/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={0}&limit=20"
    # print(url.split('/')[6])


    # di = {'url_token': 'sgai', 'headline': '喜欢用数据讲故事，微信公众号：一个程序员的日常，合作请加微信：904727147', 'name': '路人甲', 'follower_count': 274276, 'articles_count': 163, 'answer_count': 343, 'description': '无'}
    # insertIntoMysql(di,"zhihu")



    #存放我关注的知乎用户的信息
    url_tokens_list = []
    try:
        url_tokens_list = getUrlTokensDetails(url)
    except Exception as e:
        logging.error(e)

    #开始遍历抓取我的关注列表
    levelCraw(url_tokens_list)


    # print(getTableColumes("zhuhonggenfollowee_"))
    # #存储我的关注
    # for di in url_tokens_list:
    #     insertIntoMysql(di,"zhuhonggenfollowee")
    #进行层次爬取和存储


    # name = "-ke-wang-53"
    # na = changeName(name)
    # print(na)
    # createMysqlTable("nihao")


    # #显示我关注的知乎用户
    # # print("我关注的所有用户总数：" + str(len(url_tokens_list)))
    # # for di in url_tokens_list:
    # #     print(di["url_token"] + "-----" + di['name'])
    #


