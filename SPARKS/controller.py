from flask import *   
from random import *
import uuid
from model.model import First  
app = Flask(__name__) #creating the Flask class object  
app.secret_key="gayu"

@app.route('/',methods=["POST","GET"])
def Home():
    if request.method=="GET":
        return render_template('home.html')

@app.route('/customers',methods=["POST","GET"])
def ViewCustomer():
    f=First()
    if request.method=="GET":
        out=f.get_customers()
        return render_template('customer.html',out=out,count=1)

@app.route('/transfer',methods=["POST","GET"])
def MakeTransaction():
    if request.method=="GET":
        return render_template('transfer.html')

@app.route('/money_transfer',methods=["POST","GET"])
def Money_transfer():
    f=First()
    id = uuid.uuid1()
    if request.method=="POST":
        data={
            'id':id.hex,
            'sacc':request.form['sacc'],
            'sname':request.form['sname'],
            'racc':request.form['racc'],        
            'rname':request.form['rname'],    
            'amt':request.form['amt'],
        }
        res=f.transfer_money(data)
        if res==1:
            flash("Amount Transfered")
            return render_template('transfer.html',flag=1)
        else:
            flash("Please check Receiver details")
            return render_template('transfer.html',flag=0)

@app.route('/check_and_transfer',methods=["POST","GET"])
def Check_Transfer():
    f=First()
    id = uuid.uuid1()
    if request.method=="POST":
        data={
        'id':id.hex,
        'sacc':request.form['sacc'],
        'sname':request.form['sname'],
        'racc':request.form['racc'],        
        'rname':request.form['rname'],    
        'amt':request.form['amt'],
        }
        res=f.check_and_transfer(data)
        if res==1:
            flash("Amount Transfered")
            out=f.get_customers()
            return render_template('customer.html',out=out,count=1,flag=1)
        else:
            flash("Please check Receiver details")
            out=f.get_customers()
            return render_template('customer.html',out=out,count=1,flag=0)

@app.route('/transaction',methods=["POST","GET"])
def ViewTransaction():
    f=First()
    if request.method=="GET":
        out=f.get_history()
        return render_template('history.html',out=out,count=1)

@app.route('/contactUs',methods=["POST","GET"])
def Contact():
    if request.method=="POST":
        flash("Message sent!")
        return render_template('home.html')

if __name__ =='__main__':  
    app.run(debug = True) 