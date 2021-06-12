import pymysql
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

def get_time():
    now = datetime.now()
    t = ['월', '화', '수', '목', '금', '토', '일']
    daylist = ['월', '화', '수', '목', '금', '토', '일']
    weekday = daylist[datetime.today().weekday()]
    time = now.hour
    minute = now.minute
    return weekday, time, minute

def search_lecture(professor):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='gcf', charset='utf8')
    weekday, time, minute = get_time()
    now_time = time*100 + minute

    loc = None
    lecture = None

    try:
        with conn.cursor() as curs:
            sql = "SELECT NAME, START, END, LOC" + " FROM LECTURE WHERE PROFESSOR=\""+ professor + "\"" + "AND WEEKDAY =\"" + weekday + "\""
            curs.execute(sql)
            rs = curs.fetchall()

            for row in rs:
                if int(row[1]) < now_time and int(row[2]) > now_time:
                    loc = row[3]
                    lecture = row[0]
                for data in row:
                    print(data, end=" ")
                print()

            return loc, lecture
    finally:
        conn.close()

def search_contact(name, way):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='gcf', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = "SELECT " + way + " FROM CONTACT WHERE NAME=\""+name + "\""
            curs.execute(sql)
            rs = curs.fetchall()

            for row in rs:
                for data in row:
                    print(data, end=" ")
                    value = data
                print()

            return value
    finally:
        conn.close()

def search_schedule(sem, name):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='gcf', charset='utf8')
    try:
        with conn.cursor() as curs:
            start = None
            end = None
            sem = sem[0:1]
            sql1 = "SELECT START FROM SCHEDULE WHERE NAME=\""+name + "\" AND SEMESTER=\"" + sem + "\" "
            curs.execute(sql1)
            rs = curs.fetchall()

            for row in rs:
                for data in row:
                    print(data, end=" ")
                    start = data
                print()

            sql2 = "SELECT END FROM SCHEDULE WHERE NAME=\"" + name + "\" AND SEMESTER=\"" + sem + "\" "
            curs.execute(sql2)
            rs = curs.fetchall()

            for row in rs:
                for data in row:
                    print(data, end=" ")
                    end = data
                print()

            return start, end
    finally:
        conn.close()

def grad_url(stdnum):
    if stdnum == "15학번":
        url = "http://ibook.gachon.ac.kr/Viewer/NTBP6619QGB9"
    elif stdnum == "16학번":
        url = "http://ibook.gachon.ac.kr/Viewer/259LCSTNCUDC"
    elif stdnum == "17학번":
        url = "http://ibook.gachon.ac.kr/Viewer/9QX0QSIXOUD9"
    elif stdnum == "18학번":
        url = "http://ibook.gachon.ac.kr/Viewer/Z4SD47VPFNII"
    elif stdnum == "19학번":
        url = "http://ibook.gachon.ac.kr/Viewer/CXZLAWF86T0S"
    elif stdnum == "20학번":
        url = "http://ibook.gachon.ac.kr/Viewer/O9ZLU9JW7KDV"

    return url

def search_grad(major, stdnum):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='gcf', charset='utf8')
    try:
        with conn.cursor() as curs:
            first = None
            second = None
            stdnum = stdnum[0:2]
            sql1 = "SELECT FIRST FROM GRAD WHERE NAME=\""+major + "\" AND STDNUM=\"" + stdnum + "\" "
            curs.execute(sql1)
            rs = curs.fetchall()

            for row in rs:
                for data in row:
                    print(data, end=" ")
                    first = data
                print()

            sql2 = "SELECT SECOND FROM GRAD WHERE NAME=\""+major + "\" AND STDNUM=\"" + stdnum + "\" "
            curs.execute(sql2)
            rs = curs.fetchall()

            for row in rs:
                for data in row:
                    print(data, end=" ")
                    second = data
                print()

            return first, second
    finally:
        conn.close()

def search_FAQ(keyword):
    url = f"https://www.gachon.ac.kr/affairs/info/04.jsp?pageNum=0&pageSize=10&delYn=N&approve=&answer=&secret=&boardType_seq=341&searchopt=title&searchword={keyword}&x=0&y=0"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    total = soup.find(attrs={'class': 'total'}).text.split()[1]

    title_list = []
    content_list = []

    if (total == 0):
        print("There's no result from keyword : " + keyword)
    else:
        print("Total number of answers are : " + total)
        titles = soup.find(attrs={'class': "faq_list"}).find_all('a')
        a = 0
        for title in titles:
            asd = title.text.strip()
            title_list.append(asd)

    if (total == 0):
        print("There's no result from keyword : " + keyword)
    else:
        print("Total number of answers are : " + total)
        titles2 = soup.find(attrs={'class': "faq_list"}).find_all('dd')
        a = 0
        for title2 in titles2:
            asd = title2.text.strip()
            content_list.append(asd)

    return title_list, content_list

def search_study():
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='gcf', charset='utf8')
    weekday, time, minute = get_time()
    now_time = time*100 + minute

    loc = None
    lecture = None

    cafe_list = []
    cafe = None

    if weekday == "토" or weekday == "일":
        weekday = "주말"
    else:
        weekday = "평일"

    try:
        with conn.cursor() as curs:
            sql = "SELECT NAME, START, END, DISTANCE FROM CAFE WHERE DAY=\""+ weekday + "\""
            curs.execute(sql)
            rs = curs.fetchall()

            for row in rs:
                if int(row[1]) < now_time and int(row[2]) > now_time:
                    cafe_list.append([row[0], int(row[3])])

            if len(cafe_list) > 1:
                cafe_list.sort(key=lambda x: x[1])
                cafe = cafe_list[0][0]

            return cafe

    finally:
        conn.close()


@app.route('/')
def hello():
    return "Hello Flask!"

@app.route('/contact', methods=['POST'])
def contact():

    req = request.get_json()
    contactWay = req["action"]["detailParams"]["ContactWay"]["value"]
    who = req["action"]["detailParams"]["Professor"]["value"]

    print("contactWay: "+contactWay+ "   Who: "+who)

    if contactWay == "연락처":
        way = "NUMBER"
        #number = read_excel(who, 3)
        number = search_contact(who, way)
        if number == None:
            text = "연락처가 등록되어있지 않습니다. 죄송합니다."
        else:
            text = who + " 교수님의 사무실 번호는 " + str(number) + " 입니다."
    elif contactWay == "위치":
        #loc = read_excel(who, 4)
        way = "LOC"
        loc = search_contact(who, way)
        if loc == None:
            text = "위치가 등록되어있지 않습니다. 죄송합니다."
        else:
            text = who + " 교수님의 사무실 위치는 " + str(loc) + " 입니다."

        loc, lecture = search_lecture(who)
        if lecture != None and loc != None:
            text = text + " 현재 " + loc + "에서 " + lecture + " 강의 중이십니다."



    elif contactWay == "이메일":
        text = "이메일 기능은 준비 중입니다."
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route('/schedule', methods=['POST'])
def schedule():
    req = request.get_json()

    semester = req["action"]["detailParams"]["학기"]["value"]
    schedule_name = req["action"]["detailParams"]["학사일정"]["value"]
    year = req["action"]["detailParams"]["년도"]["value"]

    print("받은 파라미터: ", semester, schedule_name, year)

    start, end = search_schedule(semester, schedule_name)
    if start == None:
        text = "해당 정보가 존재하지 않습니다."
    elif start != None and end != None:
        text = year + "년 " + semester + " " + schedule_name + " 일정은 " + str(start)[0:10] + "부터 " + str(end)[0:10] + " 까지입니다"
    elif start != None and end == None:
        text = year + "년 " + semester + " " + schedule_name + " 일정은 " + str(start)[0:10] + " 입니다"

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route('/gr', methods=['POST'])
def gradient():
    req = request.get_json()
    std_num = req["action"]["detailParams"]["학번"]["value"]
    major = req["action"]["detailParams"]["Major"]["value"]

    url = grad_url(std_num)
    first, second = search_grad(major, std_num)
    if first == None:
        text = "해당 정보가 존재하지 않습니다."
    elif first != None and second != None:
        text = major + " " + std_num + "학번의 졸업요건은 " + url + " 해당 링크의 " + first + ", " + second + " 페이지에 기재되어있습니다."
    elif first != None and second == None:
        text = major + " " + std_num + "학번의 졸업요건은 " + url + " 해당 링크의 " + first + " 페이지에 기재되어있습니다."
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route('/faq', methods=['POST'])
def faq():
    req = request.get_json()
    keyword = req["action"]["detailParams"]["Keyword"]["value"]

    title, content = search_FAQ(keyword)

    text = [keyword + "관련 FAQ입니다.\n"]

    for i in range(len(title)):
        t = "Q. " + title[i] + "\n" + "A. " + content[i] + "\n\n"
        text.append(t)

    text = "".join(text)
    print(text)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route('/study', methods=['POST'])
def study():

    weekday, time, minute = get_time()

    if weekday != "토" and weekday != "일" and time >= 9 and time <= 17:
        text = "중앙도서관이 현재 운영 중입니다. 도서관에서 공부는 어떠신가요?"
    else:
        cafe_name = search_study()
        if cafe_name != None:
            text = "현재 운영 중인 가장 가까운 카페 " + cafe_name + "에 방문하시는 건 어떠신가요?"
        else:
            text = "너무 한적한 시간이네요. 가벼운 산책은 어떠신가요?"

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    }

    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 3000, debug=True)



