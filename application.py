from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
application = app = Flask(__name__)
import os
import sqlite3
from math import sin, cos, sqrt, atan2, radians
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import datetime
from datetime import timedelta
from datetime import datetime
#conn = sqlite3.connect('database.db')
# print("Opened database successfully")
#conn.execute('drop table earthquake')
#conn.execute('CREATE TABLE Earthquake (time text,latitude real,longitude real,depth real,mag real,magType text,nst real,gap real,dmin real,rms real,net text,id text,updated text,place text,type text,horizontalError real,depthError real,magError real,magNst real,status text,locationSource text,magSource text)')
# print("Table created successfully")
# conn.close()
#port = int(os.getenv("VCAP_APP_PORT"))
port = int(os.getenv("VCAP_APP_PORT",'5000'))

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def upload_csv():
   return render_template('upload.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
       con = sql.connect("database.db")
       csv = request.files['myfile']
       file = pd.read_csv(csv)
       file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
       con.close()
       return render_template("result.html",msg = "Record inserted successfully")

@app.route('/list11')
def list11():
   con = sql.connect("database.db")


   cur = con.cursor()
   cur.execute("select * from Earthquake")

   rows = cur.fetchall();
   con.close()
   return render_template("list.html",rows =len(rows))

@app.route('/magnitude')
def magnitude():
   return render_template('Magnitude.html')



@app.route('/list')
def list():
   con = sql.connect("database.db")
   cur = con.cursor()
   cur.execute("select count(*) from Earthquake")
   counts = cur.fetchall()
   cur.execute("select latitude,longitude,place,min(mag)from Earthquake where mag > 2.0")
   rows = cur.fetchall()
   con.close()
   return render_template("list.html",data1 = counts,data2 = rows)

@app.route('/options' , methods = ['POST', 'GET'])
def options():
   con = sql.connect("database.db")

   print (request.form['1'])
   print (request.form['1'])
   print (request.form['1'])
   mag=request.form['mag']
   cur = con.cursor()
   row = []
   rows_2 = []
   if request.form['1']== 'greater':
       cur.execute("select count(*) from Earthquake")
       rows = cur.fetchall()
       cur.execute("select latitude,longitude,place, min(mag)from Earthquake where mag > 2.0")
       rows = cur.fetchall()
   elif request.form['1']== 'lesser':
       cur.execute("select Count (*) from Earthquake where mag < ?",(request.form['mag'],))
       rows = cur.fetchall()
       cur.execute("select * from Earthquake where mag < ?",(request.form['mag'],))
       rows_2 = cur.fetchall()
   else :
       cur.execute("select Count (*) from Earthquake where mag = ?",(request.form['mag'],))
       rows = cur.fetchall()
       cur.execute("select * from Earthquake where mag = ?",(request.form['mag'],))
       rows_2 = cur.fetchall()
   print(len(rows))
   con.close()
   return render_template("list1.html",rows = [rows,rows_2])

@app.route('/range')
def range():
   return render_template('Range.html')

@app.route('/values',methods = ['POST', 'GET'])
def values():
   con = sql.connect("database.db")
   mag = request.form['mag1']
   mag1 = request.form['mag2']
   inp = request.form['dd']
   # print(inp)
   inps = datetime.strptime(inp,'%Y-%m-%d').date()
   ds = inps + timedelta(7)
   dss = ds.strftime('%Y-%m-%d')
   # print(dss)
   cur = con.cursor()
   cur.execute("select * from Earthquake where mag between "+mag+" and "+mag1+" and date(time) between '"+inp+"' and '"+dss+"'")
   rows = cur.fetchall()
   con.close()
   return render_template("list2.html",rows = rows)

@app.route('/values1',methods = ['POST', 'GET'])
def values1():
   con = sql.connect("database.db")
   mag = request.form['mag1']
   mag1 = request.form['mag2']
   inp = request.form['dd']
   print(inp)
   inps = datetime.strptime(inp,'%Y-%m-%d').date()
   ds = inps + timedelta(30)
   dss = ds.strftime('%Y-%m-%d')
   print(dss)
   cur = con.cursor()
   cur.execute("select * from Earthquake where mag between "+mag+" and "+mag1+" and date(time) between '"+inp+"' and '"+dss+"'")
   rows = cur.fetchall()
   con.close()
   return render_template("list2.html",rows = rows)

@app.route('/values2',methods = ['POST', 'GET'])
def values2():
   con = sql.connect("database.db")
   mag = request.form['mag1']
   mag1 = request.form['mag2']
   inp = request.form['dd']
   inp2 = request.form['dds']
   # print(inp)
   # print(dss)
   cur = con.cursor()
   cur.execute("select * from Earthquake where mag between "+mag+" and "+mag1+" and date(time) between '"+inp+"' and '"+inp2+"'")
   rows = cur.fetchall()
   con.close()
   return render_template("list2.html",rows = rows)


@app.route('/location')
def location():
   return render_template('Location.html')



@app.route('/cluster')
def cluster():
   con = sql.connect("database.db")
   cur = con.cursor()
   cur.execute("select latitude,longitude from Earthquake ")
   #ref:https://mubaris.com/2017/10/01/kmeans-clustering-in-python/
   X = cur.fetchall()
   X = pd.DataFrame(X)
   kmeans = KMeans(n_clusters=3)
   kmeans = kmeans.fit(X)
   labels = kmeans.predict(X)
   centroids = kmeans.cluster_centers_
   print(centroids)
   #colors = ['r', 'g', 'b', 'y', 'c', 'm']
   fig, ax = plt.subplots()
   #for i in range(k):
        #points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
   ax.scatter(X.iloc[:, 0], X.iloc[:, 1])
   ax.scatter(centroids[:, 0], centroids[:, 1], marker='*')
   fig.savefig('static/img.png')
   return render_template('list4.html',centroids = centroids)

@app.route('/night')
def night():
    day = 0
    night = 0
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("select longitude,time from Earthquake where mag > 4  ")
    total = cur.fetchall();
    for row in total:
       diff = row[0] / 15
       x = datetime.strptime(row[1], '%Y-%m-%dT%H:%M:%S.%fZ')
       localtime = x + timedelta(hours=diff)
       if (localtime.hour >= 6 and localtime.hour <= 20):
           day = day + 1
       else:
           night = night + 1
   #cur.execute('select COUNT(*) from (select * from Earthquake where "time" Like "%T20:%" or "time" Like "%T21:%" or "time" Like "%T22:%" or "time" Like "%T23:%" or "time" Like "%T00:%" or "time" Like "%T01:%" or "time" Like "%T02:%" or "time" Like "%T03:%" or "time" Like "%T04:%" or "time" Like "%T05:%") where mag > 4 ')
    if(night > day):
        msg = "Earthquake occurs at Night often"
    else:
       msg = "Earthqaukes occurs at day often"
    con.close()
    return render_template("list5.html",day =day,night=night, msg = msg)

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=port)
