#!pyton3

from flask import *
import pymysql
import pymysql.cursors
from config import *
import pprint

app = Flask(__name__)
app.config.from_object(__name__)

# 连接数据库
def connectdb():
    db = pymysql.connect(host=HOST,
                         user=USER,
                         passwd=PASSWORD,
                         db=DATABASE,
                         port=PORT,
                         charset=CHARSET,
                         cursorclass=pymysql.cursors.DictCursor)
    db.autocommit(True)
    cursor = db.cursor()
    return (db, cursor)

# 关闭数据库
def closedb(db, cursor):
    db.close()
    cursor.close()

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 评分页面
@app.route('/rate')
def rate():
    (db,cursor) = connectdb()
    try:
        cursor.execute("select rate, district, category, showtime, length from movie " + \
                        "where showtime<>'未知' and length<>'-1'")
        movies = cursor.fetchall()
        movies = json.dumps({"movies": movies})
        cursor.execute("select name," + \
                        "group_concat(concat_ws(',', category)) categories," + \
                        "group_concat(concat_ws(',', rate)) rates " + \
                        "from rate " + \
                        "where category<>'未知' " + \
                        "group by name")
        rates = cursor.fetchall()
        temp = {}
        for item in rates:
            temp[item['name']] = {}
            temp[item['name']]['categories'] = item['categories'].split(',')
            temp[item['name']]['rates'] = item['rates'].split(',')
            temp[item['name']]['rates'] = list( map(float, temp[item['name']]['rates']) )
        rates = temp
        rates = json.dumps({"rates": rates})
    finally:
        closedb(db,cursor)
    categories = ['剧情','喜剧','惊悚','爱情','动作','悬疑','犯罪','恐怖','科幻','冒险','奇幻','家庭','动画','战争','历史','古装','传记','音乐','同性','武侠','情色','灾难','运动','歌舞','西部','儿童','黑色电影','鬼怪','荒诞']
    districts = ['United States of America','China','Japan','South Korea','United Kingdom','France','Germany','Spain','Italy','Thailand','Canada','Russia','India','Australia','Ireland','Poland','Finland','Denmark','New Zealand','Czech Republic','Brazil','Sweden','Iran','Argentina','Belgium','Slovakia','Mexico','Norway','Austria','Netherlands','Chile','Hungary','Greece','Indonesia','Turkey','Switzerland','Iceland','Botswana','Malaysia','Israel','Romania','United Arab Emirates','Bulgaria','Myanmar','Bhutan','Armenia','Philippines','Panama','Portugal','Colombia','Luxembourg','Estonia','Uruguay','Slovenia','Georgia','Cuba','Vietnam']
    return render_template('rate.html',movies=movies,categories=categories,districts=districts,rates=rates)

# 搜索页面
@app.route('/search')
def search():
    (db,cursor) = connectdb()
    try:
        cursor.execute("select * from movie order by rate desc limit 10")
        movies = cursor.fetchall()
        for item in movies:
            item['description'] = item['description'].split('/')
    finally:
        closedb(db,cursor)
    return render_template('search.html',movies=movies)

@app.route('/keyword',methods=['POST'])
def keyword():
    data = request.form
    print(data['keyword'])
    (db,cursor) = connectdb()
    try:
        sql = "select * from movie where title like '%%%s%%' order by rate desc"
        cursor.execute(sql % data['keyword'])
        movies = cursor.fetchall()
        for item in movies:
            item['description'] = item['description'].split('/')
    finally:
        closedb(db,cursor)
    return json.dumps({"movies": movies})

if __name__ == '__main__':
    app.run(debug=True)
