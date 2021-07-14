from flask import Flask, render_template, request
import pymysql  # 置入各种有用的包

app = Flask(__name__)


def get_cursor():  # 从何处取出数据
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': '888888',
        'db': 'text1',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**config)
    conn.autocommit(1)  # conn.autocommit(True)
    return conn.cursor()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')
def index2():
    return render_template("index.html")


@app.route('/register', methods=['get', 'post'])
def register():
    return render_template("注册.html")


@app.route('/enroll', methods=['get', 'post'])
def enroll():
    name = request.form.get("name")
    password = request.form.get("password")
    confirmpassword = request.form.get("confirmpassword")
    print(password)
    print(confirmpassword)
    if password == str(confirmpassword):
        cursor = get_cursor()  # 打开数据库
        cursor.execute("select name from list where name = '{}'".format(name))
        information = cursor.fetchone()
        if name == str(information[0]):
            cursor.execute("select name from manage where name = '{}'".format(name))
            managername = cursor.fetchone()
            if managername is not None and name == str(managername[0]):
                msg = "您已注册过！"
                print(msg)
                return render_template("注册.html", msg=msg)
            else:
                value = (name, password)
                enroll_sql = '''INSERT INTO manage(name, password) values ('{}','{}')'''.format(name, password)
                cursor.execute(enroll_sql)  # 执行sql语句
                msg1 = "注册成功！"
                print(msg1)
                return render_template("index.html", msg=msg1)
        else:
            msg2 = "您不是学生！"
            print(msg2)
            return render_template("注册.html", msg=msg2)
    else:
        msg3 = "密码前后不一致！"
        print(msg3)
        return render_template("注册.html", msg=msg3)


@app.route('/login', methods=['post'])
def login():
    name = request.form.get("name")
    password = request.form.get("password")
    print(name)
    print(password)
    cursor = get_cursor()  # 打开数据库
    row = cursor.execute("select * from manage where name = %s", (name))  # 获取查询到的信息条数
    if row == 2:
        cursor.execute("select password from manage where name = %s", (name))
        message = cursor.fetchone()
        print(message[0])
        print(password)
        if password == str(message[0]):
            cursor.execute("select * from list")
            lists = cursor.fetchall()
            return render_template("manage.html", name=name, lists=lists)
        else:
            msg = "密码错误！"
            return render_template("index.html", msg=msg)
    elif row == 1:
        cursor.execute("select password from manage where name = %s", (name))
        message = cursor.fetchone()
        print(message[0])
        print(password)
        if password == str(message[0]):
            cursor.execute("select * from list")
            lists = cursor.fetchall()
            return render_template("学生网页.html", name=name, lists=lists)
        else:
            msg = "密码错误！"
            return render_template("index.html", msg=msg)
    else:
        msg = "您没有权限！"
        return render_template("index.html", msg=msg)


@app.route('/insert', methods=['post'])
def insert():
    id = request.form.get("id")
    name = request.form.get("name")
    grade = request.form.get("grade")
    nativeplace = request.form.get("nativeplace")
    identity = request.form.get("identity")
    value = (id, name, grade, nativeplace, identity)
    insert_sql = '''INSERT INTO list(id,name,grade,nativepalce,identity) values (%s,%s,%s,%s,%s)'''
    cursor = get_cursor()  # 打开数据库
    cursor.execute(insert_sql, value)
    msg = "添加成功！"
    return msg


@app.route('/delete/<int:id>')  # 这个是网址的后缀，这种直接把id嵌到后缀里去了
def delete(id):
    cursor = get_cursor()  # 打开数据库
    cursor.execute("delete from list where id = %s", (id))  # 删除某一行值
    msg = "删除成功！"
    return msg


@app.route('/update', methods=['post'])
def update():
    id = request.form.get("id")
    name = request.form.get("name")
    grade = request.form.get("grade")
    nativeplace = request.form.get("nativeplace")
    identity = request.form.get("identity")
    value = (name, grade, nativeplace, identity, id)
    cursor = get_cursor()  # 打开数据库
    cursor.execute("update list set name = %s,grade = %s,nativeplace =%s,identity = %s  where id = %s", value)  # 删除某一行值
    msg = "编辑成功！"
    return msg


if __name__ == '__main__':
    app.run()
