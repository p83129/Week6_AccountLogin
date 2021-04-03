from flask import Flask, session
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
import mysql.connector
from urllib.request import urlretrieve

app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)

app.secret_key = b'p83129'

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="qaz4545112",
  database="website"
)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/signup", methods=["POST"])
def signup():
    Name=request.form["txtName"]
    Account=request.form["txtAccount"]
    Password=request.form["txtPassword"]

    #print(Name+"," + Account + "," + Password)

    with mydb.cursor() as cursor:
        # 查詢資料SQL語法
        sql = "Select * From user Where username = '"  + Account + "'"
        # 執行指令
        cursor.execute(sql)
        # 取得所有資料
        result = cursor.fetchall()
        #print(len(result))       

        if len(result) == 0:
            sql = "Insert Into user (name,username,password) Values(%s, %s, %s)" 
            val = (Name, Account, Password)   
            cursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for('index'))
        else:   
            value = "帳號已經被註冊"
            return redirect(url_for('error',message=value))


@app.route("/singin",methods=["POST"])
def singin():
    Account=request.form["txtAccount1"]
    Password=request.form["txtPassword1"]

    with mydb.cursor() as cursor:
        sql = "Select name From user Where username = '"  + Account + "' And password = '" + Password + "'"
        cursor.execute(sql)
        result = cursor.fetchall()   
        for row in result:
            #print ("%s" ,(row[0]))            
            if len(result)==1:
                session['sucess'] = '已登入' 
                return redirect(url_for('member',name=row[0]))
        if(len(result)==0):   
            #return redirect(url_for('error'))
            #name=request.form["txtAccount1"]
            value = "帳號或密碼輸入錯誤"            
            return redirect(url_for('error',message=value))

@app.route("/member/<name>")
def member(name): 
    if session['sucess'] == '已登入':
        return render_template("member.html",name=name)
    else:
        return redirect(url_for('index'))

@app.route("/error")
def error(): 
    errmag = request.args.get("message","帳號已經被註冊")
    if  errmag == "帳號已經被註冊":
        #print("***",name)
        return render_template("error.html",message=errmag)
    else:      
        return render_template("error.html",message=errmag)

@app.route("/signout", methods=["GET"])
def aaa():
    session['sucess'] = '未登入'  
    print(session['sucess'])  
    return redirect(url_for('index'))


app.run(port=3000)    