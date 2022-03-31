
from enum import unique
from flask import Flask, make_response
import pymongo
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from flask import request
from mongoengine import Document
from mongoengine import DateTimeField,EmbeddedDocument, StringField, ReferenceField, ListField,IntField,EmbeddedDocumentField
import random
import json
import re
import time
from datetime import date



'''cluster=MongoClient('mongodb+srv://Aditya:12345@cluster0.sswhd.mongodb.net/Api?retryWrites=true&w=majority')
db=cluster['Api']
collection=db['Books']  #if i need to use the mongo db and to update ,mongoclient can be used.(this is mongoclient)


class Books(Document):
    bookname = StringField(max_length=60, required=True, unique=True)
    category = StringField(max_length=60, required=True, unique=True)
    authorname =StringField(max_length=60, required=True, unique=True)
    rentperday= IntField(required=True) 
    
    def to_json(self):
        return {"bookname": self.bookname,
                "category":self.category,
                "authorname":self.authorname,
                "rentperday": self.rentperday}     
'''           
app=Flask(__name__)
database_name="Api"
DB_URI='mongodb+srv://Aditya:12345@cluster0.sswhd.mongodb.net/Api?retryWrites=true&w=majority'
app.config["MONGODB_HOST"] =DB_URI
db=MongoEngine()
db.init_app(app)

if __name__=="__main__":
    app.run(debug=False)

class Books(db.Document):
    bookname = db.StringField(max_length=60, required=True,unique=True)
    bookid = db.StringField(max_length=60, required=True, unique=True)   
    category = db.StringField(max_length=60, required=True)
    authorname =db.StringField(max_length=60, required=True)
    rentperday= db.IntField(required=True) 
    
    def to_json(self):
        return {"bookname": self.bookname,
                "bookid":self.bookid,
                "category":self.category,
                "authorname":self.authorname,
                "rentperday": self.rentperday}
            
@app.route('/searchbook/',methods=['GET'])
def searchbook():
    try:    
        args = request.args    
        name=args['name']
        print(name)
        listofsearched=[]
        allbooks=Books.objects()
        if int(name):
            for elem in allbooks:
                if int(name)<=elem['rentperday']:
                    listofsearched.append(elem['bookname'])
        else:
            result=re.sub("[.'!#$%&\'()*+,-./:;<=>?@[\\]^ `{|}~]","",name)
            print(result.lower())
            
            
            print(allbooks)
            
            for element in allbooks:
                print(element)
                if (result in (element['bookname']).lower()) or (result in (element['category']).lower()) or (result in (element['authorname']).lower()):
                    listofsearched.append(element['bookname'])
            
        if len(listofsearched)==0:
            return "oops,try another one ,Not Found!!"  
        else:        
            return str(listofsearched)
    
    except Exception as e:
        return e
        
'''@app.route('/savebook',methods=['POST'])
def savebooks():
    listofbooks=[
        {"title": "A Tale of Two Cities", "author": "Charles Dickens", "year_written": 1865, "edition": "Classics", "price":  12.7},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year_written": 181, "edition": "Classics", "price":  18.2},
        {"title": "Vintage Beloved", "author": "Toni Morrison", "year_written": 1865, "edition": "Classics", "price":  12.7},
        {"title": "Life of Pi", "author": "Yann Martel", "year_written": 1875, "edition": "Action and Adventure", "price":  13.5},
        {"title": "Thre Three Musketeers", "author": "Alexandre Dumas", "year_written": 1925, "edition": "Action and Adventure", "price":  25},
        {"title": "Watchmen", "author": "Alan Moore,Dave Gibbons", "year_written": 1999, "edition": "Comic", "price":  12.35},
        {"title": "The Adventures of Sherlock Holmes", "author": "Sir Arthur Conan Doyle", "year_written": 1865, "edition": "Detective and Mystery", "price":  5.76},
        {"title": "Circe", "author": "Madeline Miller", "year_written": 1870, "edition": "Fantasy", "price":  5.75},
        {"title": "G.P. Putnam's Sons The Help", "author": "Kathryn Stockett", "year_written": 1862, "edition": "Historic", "price":  7.75},
        {"title": "One Hundred Years of Solitude", "author": "Gabriel,Garcia Marquez", "year_written": 1922, "edition": "Historic", "price":  29},
        {"title": "Harry Potter", "author": "J.K. Rowling", "year_written": 2000, "edition": "Contemporary fantasy", "price":  19.95},
        {"title": "Anchor Carrie", "author": "Stephen King", "year_written": 1967, "edition": "Horror", "price":  14.00},
        {"title": "Hamlet, Prince of Denmark", "author": "Shakespeare", "year_written": 1603, "edition": "Signet Classics", "price":  7.95},
        {"title": "Lord of the Rings", "author": "Tolkien, J.R.", "year_written": 1937, "edition": "heroic romance", "price":  27.45},
        {"title": "War and Peace", "author": "Leo Tolstoy ", "year_written": 1865, "edition": "Historical novel", "price":  12.7},
        {"title": "Anna Karenina", "author": "Leo Tolstoy ", "year_written": 1875, "edition": "Realist novel", "price":  13.5},
        {"title": "Mrs. Dalloway", "author": " Virginia Woolf", "year_written": 1925, "edition": "Fictional", "price":  25},
        {"title": "The Hours", "author": " Michael Cunnningham", "year_written": 1999, "edition": "Psychological Drama", "price":  12.35},
        {"title": "Huckleberry Finn", "author": "Mark Twain ", "year_written": 1865, "edition": "satire humour picaresque novel adventure fiction", "price":  5.76},
        {"title": "Bleak House", "author": "Charles Dickens", "year_written": 1870, "edition": "Novel", "price":  5.75}]
    
    testnum=0 
    for elem in listofbooks:
        testnum+=1
        bookelem = Books(bookname= elem["title"],bookid='book'+str(testnum),category=elem["edition"],authorname=elem["author"],rentperday= random.randint(150,1000))
        bookelem.save()
    return make_response('success',200)
'''

@app.route('/displaybooks',methods=['GET'])
def displaybooks():  
    try:  
        take=Books.objects()   
        result=take.to_json()
                
        return make_response(str(result),200)
    except Exception as e:
        return make_response(e,404)




class Transactions(db.Document):
    bookid=db.StringField(max_length=60, required=True)
    userid=db.StringField(max_length=60, required=True)   
    issuedon =db.StringField(max_length=60, required=True)
    returned =db.StringField(max_length=60, required=True)
    totalrent=db.IntField(required=True)
    transactionid=db.StringField(max_length=60, required=True, unique=True) 
    dateoftransaction=db.StringField(max_length=60, required=True, unique=True)
    def to_json(self):
        return {"bookid": self.bookid,
                "userid":self.userid,
                "issuedon":self.issuedon,
                "returned":self.returned,
                "totalrent":self.returned,
                "transactionid":self.transactionid, 
                "dateoftransaction": self.dateoftransaction,}
        
class Userhistory(EmbeddedDocument):
    issuedbookid=StringField(max_length=60, required=True)
    
    
    
           
class Users(db.Document):
    username=db.StringField(max_length=60, required=True)
    userid = db.StringField(max_length=60, required=True)
    userbooks=db.ListField(EmbeddedDocumentField(Userhistory))
    
    
    def to_json(self):
        return {"username": self.username,
                "userid":self.userid,
                "userbooks":self.userbooks}    



def userreg(name,id):
    generateid='bookuser'+str(len(Users.objects())+1)
    instance=Userhistory(issuedbookid=id)
    listsave=[instance]
    saveuser=Users(username=name,userid=generateid,userbooks=listsave)
    saveuser.save()
    return generateid
        
@app.route('/issuebook',methods=["GET"])
def issuebook():
    args =request.args
    bookname=args['bookname']
    username=args['username']
    allbooks=Books.objects()
    regexbook=(re.sub("[.'!#$%&\'()*+,-./:;<=>?@[\\]^ `{|}~]","",bookname)).lower()
    regexuser= (re.sub("[.'!#$%&\'()*+,-./:;<=>?@[\\]^ `{|}~]","",username)).lower()
    allusers=Users.objects()
    useridfunc=''
    bookidfunc=''  
    for el in allbooks:
        if re.sub("[.'!#$%&\'()*+,-./:;<=>?@[\\]^ `{|}~]","",el['bookname']).lower()==regexbook:
            bookidfunc=el['bookid']
    if bookidfunc=='':
        return make_response('No Such Book Exist Here.!!',200)
    else:
        for user in allusers:
            if re.sub("[.'!#$%&\'()*+,-./:;<=>?@[\\]^ `{|}~]","",user['username']).lower()==regexuser:
                useridfunc=user['userid']
                userfind = Users.objects(userid=useridfunc).first()
                userfind.userbooks.append(Userhistory(issuedbookid=bookidfunc))
                userfind.save()
        if useridfunc=='':
            useridfunc=userreg(username,bookidfunc)
        checkbeforeissued=Transactions.objects(bookid=bookidfunc,userid=useridfunc)
        for elem in checkbeforeissued:
            if elem['returned']=='pending':
                return make_response('You cannot issue this book again before returning it.',200)    
        transid='trans'+str(len(Transactions.objects())+1)
        transelem=Transactions(bookid=bookidfunc,userid=useridfunc,issuedon=time.asctime( time.localtime(time.time()) ),returned='pending' ,totalrent=0,transactionid=transid,dateoftransaction=time.asctime( time.localtime(time.time()) ))
        transelem.save()
        return make_response('successfully issued',200)



@app.route('/returnbook',methods=['GET'])
def returnbook():
    try:
        args =request.args
        booknamearg=args['bookname']
        usernamearg=args['username']
        findobject=Books.objects(bookname=booknamearg).first()
        bookidneed=findobject.bookid
        rentoneday=findobject.rentperday
        finduser=Users.objects(username=usernamearg).first()
        useridneed=finduser.userid
       
        elementtransactions=Transactions.objects(bookid=bookidneed,userid=useridneed)
        if len(elementtransactions)<=1:
            dateissued=elementtransactions[0]['issuedon']
            
        listsplitdate=dateissued.split()
       
        a1=int(listsplitdate[4])
        c1=int(listsplitdate[2]) 
        todaydate=time.asctime( time.localtime(time.time()) )
        listtodaytdate=todaydate.split()
        a2=int(listtodaytdate[4])
        c2=int(listtodaytdate[2])
        
        months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
        for i in range(len(months)-1):
            if listsplitdate[1]==months[i]:            
                b1=i+1
            if listtodaytdate[1]==months[i]:
                b2=i+1
        date1 = date(a1,b1 , c1)
        date2 = date(a2, b2, c2)
        
        rentcalc=int(numOfDays(date1, date2))*rentoneday
        if rentcalc==0:
            rentcalc=rentoneday
        #.update_one(set__='Example Post')
        foundornot=False
        for elem in elementtransactions:
            if elem['returned']=='pending':            
                Transactions.objects(bookid=bookidneed,userid=useridneed).update(returned=time.asctime( time.localtime(time.time()) ),totalrent=rentcalc)
                foundornot=True
                break
                
        if foundornot==False:
            return make_response('no such transaction exist',200)
        else:
            return make_response({'Totalrent':rentcalc,'returndate':time.asctime( time.localtime(time.time()))})
    
    except Exception as E:
        return make_response(E,404)
    
    
def numOfDays(date1, date2):
    return (date2-date1).days


    

@app.route('/findusersforbook',methods=["GET"])
def findusersforbook():
    try:
            
        args=request.args
        book=args['book']
        bookfind=Books.objects(bookname=book).first()
        if bookfind==None:
            return make_response('no such Data exists',200)
        
        else:
            print(bookfind)
            bookidtrue=bookfind['bookid']    
            result_list_id=set()
            currently_id=set()
            result_list=set()
            currently=set()
            
            alltransactions=Transactions.objects()
            for el in alltransactions:
                print(el)
                if bookidtrue==el['bookid']:                
                    result_list_id.add(el['userid'])
                    
                if bookidtrue==el['bookid'] and el['returned']=='pending':
                    currently_id.add(el['userid'])
            
            print(currently_id)        
            allusers=Users.objects()
            for data in result_list_id:
                for user in allusers:
                    if user['userid']==data:
                        result_list.add(user['username'])
                        
            
            for item in currently_id:
                for usr in allusers:
                    if usr['userid']==item:
                        currently.add(usr['username'])
                        
            resultshow={
                'Listofusers(issued)':result_list,
                'countofusers':len(result_list),
                'Currentusers':currently,
                'CurrentTotal':len(currently)
                
            }
            return make_response(str(resultshow),200) 
    except Exception as E:
        return make_response(E,404)
                
            
@app.route('/rentgenerated',methods=['GET'])
def rentgenerated():
    try:
            
        args=request.args
        book=args['book']
        bookfind=Books.objects()
        found=False
        totalrent =0
        rentperday=0
        for elem in bookfind:
            if elem['bookname']==book:
                found=True
                bookidtrue=elem['bookid']
                rentperday=elem['rentperday']
            
        if found==False:
            return make_response('No record Found',200)
        
        else:
            alltrans=Transactions.objects()
            for el in alltrans:
                if el['returned']!='pending' and el['bookid']==bookidtrue:
                    totalrent+=rentperday
                    
            return make_response(str(totalrent),200)
    except Exception as E:
        return make_response(E,404)
    
    
@app.route('/userallbook',methods=['GET']) # INPUT - Person’s name ,OUTPUT - List of books issued to that person
def userallbook():
    try:
            
        args=request.args
        username=args['username']
        allusers=Users.objects()
        allbooks=Books.objects()
        for user in allusers:
            if user['username']==username:
                getlist=user['userbooks']
                
        getalldata=set()
        for item in getlist:
            for obj in allbooks:
                if item['issuedbookid']==obj['bookid']:
                    getalldata.add(obj['bookname'])
                    
        return make_response(str(getalldata),200)
    except Exception as E:
        return make_response(E,404)
    
@app.route('/searchdaterange',methods=['GET']) #  INPUT - Date range  OUTPUT - list of books issued in that date range and the person they are issued to
def searchdaterange():
    try:
        args=request.args
        fromdate=args['from'].split('/')
        enddate=args['end'].split('/')
        print(fromdate)
        print(enddate)
        alltrans=Transactions.objects()
        result=[]
        for elem in alltrans:
            checkdate=elem['issuedon'].split()      
            months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
            for i in range(len(months)-1):
                if checkdate[1]==months[i]:            
                    b2=i+1
                    break
                
            d2 = date(int(fromdate[2]),int(fromdate[1]), int(fromdate[0]))
            d1 = date(int(checkdate[4]),int(b2) , int(checkdate[2]))
            d3 = date(int(enddate[2]),int(enddate[1]),int(enddate[0]))
            getalldata={}
            if d2 <= d1 <= d3:
                findbook=Books.objects(bookid=elem['bookid']).first()
                finduser=Users.objects(userid=elem['userid']).first()
                getalldata['bookname']=findbook['bookname']
                getalldata['username']=finduser['username']
                getalldata['transactionid']=elem['transactionid']
                result.append(getalldata)
            
                    
        return make_response(str(result),200)
    
    except Exception as E:
        return make_response(E,404)            
               
                   
 
    