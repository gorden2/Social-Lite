import sqlite3
from flask import *
from contextlib import closing
import os, re,csv,random
# nltk
import nltk
from nltk.tokenize import *
# email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import Encoders
import datetime
#from flask_wtf import Form
#from wtforms import StringField, BooleanField, PasswordField,FileField, RadioField,validators

DATABASE = 'flaskr.db'
DEBUG = True
#WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'


# utils
def handletag(s):
    output = []
    s = word_tokenize(s)
    corpus = nltk.pos_tag(s)
    for item in corpus:
        if item[1] in ["NNPS","NNP"]:
            output.append( item[0] )
    if len(output) > 5:
        output=output[:5]
    return output


def sendemail(email,time,detail,title):
    CRLF = "\r\n"
    login = "sociallite743@gmail.com" #Add the sender email address
    password = "huangbingqing" #Have to add the password for the above email address
    time = str(time)
    print "time: "+time
    time = re.sub(r"(.+)-(.+)-(.+)",r"\1\2\3",time)
    print "time2: "+time
    attendees = [email] #List of attendees

    organizer = "ORGANIZER;CN=organiser:mailto:sociallite743"+CRLF+" @gmail.com" #Email address of the organizer
    fro = "social lite <sociallite743@gmail.com>"  #senders email

    #Below code sets the time of the event Have to change it according to our events
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")


    dtstartt = datetime.datetime.strptime(time+"T100000", "%Y%m%dT%H%M%S")  #start time
    dtendd = datetime.datetime.strptime(time+"T103000", "%Y%m%dT%H%M%S")   #End time
    dtstart = dtstartt.strftime("%Y%m%dT%H%M%S")  #start time
    dtend = dtendd.strftime("%Y%m%dT%H%M%S")

    #Change this event description
    description = "DESCRIPTION: "+detail+CRLF #Add any Description
    attendee = ""
    for att in attendees:
        attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
    ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
    ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
    ical+= "UID:FIXMEUID"+dtstamp+CRLF
    ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
    ical+= "SUMMARY: "+title+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF

    eml_body = "" #Email Body
    eml_body_bin = "This is the email body in binary - two steps"
    msg = MIMEMultipart('mixed')
    msg['Reply-To']=fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Event invite: "+title  #Subject of the Message
    msg['From'] = fro
    msg['To'] = ",".join(attendees)

    part_email = MIMEText(eml_body,"html")
    part_cal = MIMEText(ical,'calendar;method=REQUEST')

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
    ical_atch.set_payload(ical)
    Encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

    eml_atch = MIMEBase('text/plain','')
    Encoders.encode_base64(eml_atch)
    eml_atch.add_header('Content-Transfer-Encoding', "")

    msgAlternative.attach(part_email)
    msgAlternative.attach(part_cal)

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(login, password)
    mailServer.sendmail(fro, attendees, msg.as_string())
    mailServer.close()


def opinion(s):
    print "Now Begin Connotation Lexicon"
    s = word_tokenize(s)

    corpus = []
    with open("connotation.csv",'r') as f:
        csvf = csv.reader(f,delimiter=',')
        for row in csvf:
            if row[1] != "neutral":
                pair = (0,0)
                if row[1] == "positive":
                    pair = (row[0],1)
                if row[1] == "negative":
                    pair =(row[0],-1)
                corpus.append(pair)

    word = set()
    for pair in corpus:
        w = re.sub(r"(.*)_(.*)",r"\1",pair[0])
        word.add(w)
    word2 = []
    for ss in s:
        if ss in word:
            word2.append(ss)
    print "useful words:",
    print word2

    count = 0
    for ww2 in word2:
        flag = True
        for row in corpus:
            w = re.sub(r"(.*)_(.*)",r"\1",row[0])
            if ww2 == w:
                print row
                count+=row[1]
                flag = False
            if flag == False:
                break
    return count


@app.route('/')
def render_index_page():
    return render_template('index.html')


@app.route('/profile')
def render_profile_page():
    return render_template('profile_bq.html')


@app.route('/addNewEvent')
def render_add_new_event_page():
    return render_template('addNewEvent.html')


@app.route('/eventDetail',methods=['GET','POST'])
def gotoEventDetail():
    item = request.data
    global gid
    if len(item) > 0:
        #session['detaileventid'] = item
        gid = item
    return render_template('eventDetail.html')


@app.route('/account_index')
def render_account_index():
    return render_template('account_index.html')



@app.route('/login', methods=["GET", "POST"])
def login():
    item = json.loads(request.data)
    username = item["username"]
    password = item["password"]
    cur = g.db.execute('select username,password from userdata where username=? and password=?',
                       [username,password])
    if len(cur.fetchall()) >0:
        print "Log in"
        session['username'] = username
        global uid
        uid = username
        return "Success"
    else:
        return "Invalid Username or Password!"


@app.route('/logout', methods=["GET", "POST"])
def logout():
    #session.pop('username', None)
    global uid
    uid = ""
    print "log out"
    return "Success"


@app.route('/signup', methods=["GET", "POST"])
def signup():
    item = json.loads(request.data)
    cur = g.db.execute('select username,password from userdata where username=?',[item["username"]])
    if len(cur.fetchall()) != 0:
        return "Wrong Username"
    else:
        g.db.execute('insert into userdata values (?,?)',(item["username"],item["password"]))
        g.db.commit()
        g.db.execute("insert into userinfo(username) values (?)",[item["username"]])
        g.db.commit()
        session['username']=item["username"]
        global uid
        uid = item["username"]
    return "success"


'''
# login and signup
class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired("Username is required!")])
    password = PasswordField('Password', [validators.DataRequired("Password is required!")])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm1(Form):
    username = StringField('Username', [validators.DataRequired("Username is required!")])
    password = PasswordField('Password', [
        validators.DataRequired("Password is required!"),validators.length(min=6),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password',[validators.DataRequired("Password Confirm is required!")])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.json)
    if form.validate_on_submit():
        cur = g.db.execute('select username,password from userdata where username=? and password=?',
                           (form.username.data,form.password.data))
        if len(cur.fetchall()) != 0:
            print "Log in"
            session['username'] = form.username.data
            if form.remember_me.data==True:
                session.permanent = True
            return render_template("index.html")
        else:
            form.errors["invalid"] = ["Invalid Username or Password!"]
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    print "log out"
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm1(request.form)
    if form.validate_on_submit():
        cur = g.db.execute('select username,password from userdata where username=?',([form.username.data]))
        if len(cur.fetchall()) != 0:
            form.errors["repeat"] = ["Username has been used!"]
        else:
            g.db.execute('insert into userdata values (?,?)',(form.username.data,form.password.data))
            g.db.commit()
            session['username']=form.username.data
            return redirect(url_for('profile'))
    return render_template('signup.html', form=form)


# profile
class RegisterForm2(Form):
    email = StringField('Email Address', [validators.DataRequired(), validators.Email()])
    gender= RadioField('Gender',[validators.DataRequired()],choices=[("male","male"),("female","female")])
    photo = FileField('Your photo')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = RegisterForm2(request.form)
    if form.validate_on_submit():

        g.db.execute('insert into userinfo(username,u_gender,u_email) values (?,?)',
                     (session['username'],form.gender.data,))
        g.db.commit()
        print "profile"

        file = request.files['photo']
        filename = session['username']+ "."+file.filename.split(".")[1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print filename
        return redirect(url_for('index'))
    return render_template('profile.html', form=form)
'''


@app.route('/currentUserInfo')
def get_current_user_info():
    '''
    currentUserInfo = {
        'username': "100001userid",
        'password': "test password",
        'displayname': "test user displayname",
        'email': "huangbq.01@gmail.com",
        'address': "college park, MD",
        'city': 'test city',
        'state': 'test state',
        'birth': '1989-12-12',
        'gender': "male",
        'bio': "I'm interested in everything! I'm a test user!",
        'interests': [{
            'name': "Social Media",
            'parent': "Internet & Technology"
        },
        {
            'name': "Interaction Design",
            'parent': "Internet & Technology"
        },
        {
            'name': "Cloud Computing",
            'parent': "Internet & Technology"
        }],

    }
    '''


    currentUserInfo= {}
    try:
        uid
    except NameError:
        return json.dumps(currentUserInfo)
    username = uid
    cur = g.db.execute("select * from userinfo where username= ?", [username])
    for row in cur:
        currentUserInfo["displayname"] = row[1]
        currentUserInfo["gender"] = row[2]
        currentUserInfo["birth"] = row[3]
        currentUserInfo["email"] = row[4]
        currentUserInfo["address"] = row[6]
        currentUserInfo["state"] = row[7]
        currentUserInfo["city"] = row[8]
        if row[9] is not None:
            currentUserInfo["interests"] = row[9].split(",")
        else:
            currentUserInfo["interests"] = row[9]
        currentUserInfo["bio"] =row[10]
    currentUserInfo["username"] = username
    return json.dumps(currentUserInfo)

# fixme date
@app.route('/createNewEvent', methods=['GET', 'POST'])
def create_new_event():
    try:
        uid
    except NameError:
        return "Failed"
    username = uid
    item = json.loads(request.data)
    e_title = item['title']
    e_time = item['date']
    e_address = item['address']
    e_city = item['city']
    e_state = item['state']
    e_detail = item['detail']
    e_tag = ",".join(handletag(e_detail))
    category = ",".join(item['category'])
    g.db.execute("insert into event(e_title,e_time,e_address,e_detail,e_city,e_state,e_tag, category) values (?,?,?,?,?,?,?,?)",
                 (e_title,e_time,e_address,e_detail,e_city,e_state,e_tag,category))
    g.db.commit()
    eid = g.db.execute("select eventid from event where e_title=? order by eventid DESC",[e_title]).fetchone()[0]
    print "Create event"
    print "eventid"+str(eid)
    g.db.execute("insert into event_user(eventid,creator,membercount) values (?,?,?)",(eid,username,0))
    g.db.commit()
    print "Create event_user"
    if eid is not None:
    #    session["detaileventid"] = eid
        global gid
        gid = eid
    return "Success!"


# return one event
@app.route('/getEventDetail', methods=['GET', 'POST'])
def getEventDetail():
    '''
        item = {
        'name': 'test event name',
        'address': 'test location',
        'city': 'test city',
        'state': 'test state',
        'date': 'test date',
        'category': [
            'test cate 1',
            'test cate 2',
            'test cate 3'
        ]
    }
    '''
    try:
        gid
    except NameError:
        return json.dumps([])

    eventid = gid

    output={}
    cur3 = g.db.execute("select * from event,event_user where event.eventid=? and event.eventid=event_user.eventid",[eventid])
    for row in cur3:
        output["eventid"] = row[0]
        output["title"] = row[1]
        output["detail"] = row[2]
        output["date"] = row[3]
        output["address"] = row[4]
        output["city"] = row[5]
        output["state"] = row[6]
        if row[7] is not None:
            output["tag"] = row[7].split(",")
        else:
            output["tag"] = row[7]
        if row[8] is not None:
            output["category"] = row[8].split(",")
        else:
            output["category"] = row[8]
        output["creator"] = row[10]
        if row[11] is not None:
            output["member"] = row[11].split(",")
        else:
            output["member"] = row[11]
        output["member_count"] = row[12]
        output["thumbnail"] = "static/img/"+ str(output["eventid"]) + ".jpg"

    print "get_detail"
    print output
    item = output
    #session["detaileventid"] = "None"

    return json.dumps(item)

@app.route('/getDiscussion', methods=["GET", "POST"])
def get_discussion():
    '''
    item = [{'title': 'This is the title',
             'creator': 'The creator',
             'content': 'the content of the post'}]
             '''
    try:
        gid
    except NameError:
        return json.dumps([])
    eventid = gid
    item=[]
    cur_dis = g.db.execute("select username,discussion,d_title,point,disid from event_discuss where eventid=?",[eventid])
    for row_dis in cur_dis.fetchall():
        print row_dis
        output = {}
        output["creator"] = row_dis[0]
        output["content"] = row_dis[1]
        output["title"] = row_dis[2]
        output["point"] = row_dis[3]
        output["disid"]= row_dis[4]
        item.append(output)
    print "Get discussion",
    print item
    return json.dumps(item)

# discussion
@app.route('/newPost', methods=["GET", "POST"])
def post_new():
    print "Create Discussion"
    try:
        gid
    except NameError:
        return "Failed"
    try:
        uid
    except NameError:
        return "Failed"
    item = json.loads(request.data)
    username = uid
    eventid = gid
    d_title = item["title"]
    discussion = item["content"]
    point1 = opinion(discussion)
    if point1 > 0:
        point = "Positive"
    elif point1 < 0:
        point = "Negative"
    else:
        point = "Neutral"
    g.db.execute("insert into event_discuss(eventid, username,discussion,d_title,point) values (?,?,?,?,?)",
                 [eventid,username,discussion,d_title,point])
    g.db.commit()
    print "Create Discussion Success!"
    return "success"

#recommendation
@app.route('/getReco',methods=['GET', 'POST'])
def get_reco():
    # get the useraddress
    print "Get Recommendation:"
    u_city = "None"
    u_interests = set()
    try:
        uid
    except NameError:
        return json.dumps([])
    username = uid
    cur = g.db.execute("select u_city,u_interests from userinfo where username=?",[username])
    for row in cur.fetchall():
        u_city = row[0]
        u_interests = set(row[1].split(","))
    print "u_city: " + u_city
    print "current u_interests: ",
    print u_interests

    eventid= set()
    cur = g.db.execute("select event.eventid, event.category, event_user.member, event_user.creator from "
                       "event,event_user where event.e_city=? and event.eventid=event_user.eventid order by event_user.membercount DESC",
                        [u_city])
    result=cur.fetchall()
    print "result#: "+ str(len(result))

    # judge whether have 2 more events near user
    if len(result) < 3:
        for row in result:
            eventid.add(row[0])
        print "Too few:"
        print eventid

    # if more than 3, then filter the eventid
    if len(result) >= 3:
        for row in result:
            for i in row[1].split(","):
                if i in u_interests:
                    eventid.add(row[0])
        print "Normal eventid:"
        print eventid

    # if less than 8 event, add parents
    if len(eventid) <= 8:
        parent=set()
        for child in u_interests:
            cur2 = g.db.execute("select parent from parenlist where child=?",[child])
            for row in cur2.fetchall():
                 parent.add(row[0])

        for p in parent:
            cur_p =g.db.execute("select child from parenlist where parent=?",[p])
            for row_p in cur_p:
                u_interests.add(row_p[0])

        print "Have Parent, current u_interests:"
        print u_interests
        eventid=set()
        for row in result:
            for i in row[1].split(","):
                if i in u_interests:
                    eventid.add(row[0])
        print "with parent eventid:",
        print eventid

    # if more than 8 event, cut the rest
    if len(eventid) > 8:
        random.shuffle(eventid)
        eventid = eventid[:8]
        print "Too much, eventid:",
        print "eventid"

    entry = []
    for i in eventid:
        cur3 = g.db.execute("select * from event,event_user where event.eventid=? and event.eventid=event_user.eventid",[i])
        for row in cur3:
            output={}
            output["eventid"] = row[0]
            output["title"] = row[1]
            output["detail"] = row[2]
            output["date"] = row[3]
            output["address"] = row[4]
            output["city"] = row[5]
            output["state"] = row[6]
            if row[7] is not None:
                output["tag"] = row[7].split(",")
            else:
                output["tag"] = row[7]
            if row[8] is not None:
                output["category"] = row[8].split(",")
            else:
                output["category"] = row[8]
            output["creator"] = row[10]
            if row[11] is not None:
                output["member"] = row[11].split(",")
            else:
                output["member"] = row[11]

            output["member_count"] = row[12]
            print output
            entry.append(output)
    print entry
    return json.dumps(entry)



@app.route('/all-interests')
def load_all_interests():
    '''
    all_interests = [{
        'name': "Art",
        'parent': "Arts & Entertainment"
    }, {
        'name': "Fiction",
        'parent': "Arts & Entertainment"
    }]
    '''
    all_interests=[]
    cur_parent = g.db.execute("select * from parenlist")
    result = cur_parent.fetchall()
    print result
    for row in result:
        interest={}
        interest["name"] = row[0]
        interest["parent"] = row[1]
        all_interests.append(interest)
    return json.dumps(all_interests)


@app.route('/all-events')
def load_all_events():
    '''
    all_events = [{
        'eventid': 123,
        'name': "DC wine hangout",
        'thumbnail': "static/img/1.jpg",
        'caption': "The wine Caption"
    }, {
        'eventid': 126,
        'name': "Maryland basketball meetup",
        'thumbnail': "static/img/4.jpg",
        'caption': "GET A DUNK!"
    }]
    '''
    all_events = []
    cur_event = g.db.execute("select * from event,event_user where event.eventid=event_user.eventid")
    for row in cur_event:
        output={}
        output["eventid"] = row[0]
        output["title"] = row[1]
        output["detail"] = row[2]
        output["date"] = row[3]
        output["address"] = row[4]
        output["city"] = row[5]
        output["state"] = row[6]
        if row[7] is not None:
            output["tag"] = row[7].split(",")
        else:
            output["tag"] = row[7]
        if row[8] is not None:
            output["category"] = row[8].split(",")
        else:
            output["category"] = row[8]
        output["creator"] = row[10]
        if row[11] is not None:
            output["member"] = row[11].split(",")
        else:
            output["member"] = row[11]
        output["member_count"] = row[12]
        output["thumbnail"] = "static/img/"+ str(output["eventid"]) + ".jpg"
        all_events.append(output)

    return json.dumps(all_events)

# user
@app.route('/updateCurrentUser', methods=["POST"])
def update_current_user():
    '''
      username text primary key,
      displayname text,
      u_gender text,
      u_birth text,
      u_email text,
      u_image text,
      u_address text,
      u_state text,
      u_city text,
      u_interests text,
      u_bio text,
    :
    '''
    try:
        uid
    except NameError:
        return "Failed"
    item = json.loads(request.data)

    username= uid
    displayname = item["displayname"]
    gender = item["gender"]
    birth = item["birth"]
    email = item["email"]
    bio = item["bio"]

    # file = request.files['photo']
    # filename = username+".png"
    # path = "uploads/"+ filename
    # if os.path.isfile(path):
    #     os.remove(path)
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    address = item["address"]
    state = item["state"]
    city = item["city"]
    interests = ",".join(item["interests"])
    g.db.execute("update userinfo set displayname=?, u_gender=?, u_birth=?, u_email=?, u_address=?, u_state=?, u_city=?, u_interests=?, u_bio=? where username=?",
                 [displayname,gender,birth,email,address,state,city,interests,bio,username])
    g.db.commit()
    print address
    return "Success!"


@app.route('/rsvpEvent', methods=["POST"])
def rsvpEvent():
    try:
        gid
    except NameError:
        return "Failed"
    try:
        uid
    except NameError:
        return "Failed"

    username = uid
    #eventid = session["detaileventid"]
    eventid = gid
    cur = g.db.execute("select member,membercount from event_user where eventid=?",[eventid])
    result = cur.fetchone()
    print result
    output={}
    if result[0] == None:
        output["member"] = username
    else:
        output["member"] = result[0]+","+username
    output["membercount"] = int(result[1]) + 1
    g.db.execute("update event_user set member=?, membercount = ? where eventid = ?",[output["member"],output["membercount"],eventid] )
    g.db.commit()
    cur2= g.db.execute("select e_title, e_detail,e_time from event where eventid=?",[eventid])
    result2 = cur2.fetchall()
    time = "None"
    detail = "None"
    title = "None"
    print "EMAIL FUNCTION"
    if result2 is not None:
        for row in result2:
            print row
            title = row[0]
            detail = row[1]
            time = row[2]
        email="gorden725@gmail.com"
        sendemail(email,time,detail,title)

    return 'Success!'



@app.route('/getRsvpedEvent')
def get_rsvped_event():
    '''
    item = [{
        'title': 'test event name',
        'detail': 'detail description',
        'address': 'test location',
        'city': 'test city',
        'state': 'test state',
        'date': 'test date',
        'thumbnail': 'username.png',
        'category': [
            'test cate 1',
            'test cate 2',
            'test cate 3'
        ],
        'tag': [
            'tag a',
            'tag b'
        ],
        'creator': 'username of creator',
        'member': [
            'attender 1 username',
            'attender 2 username'
        ],
        'member_count': 2
    }, {
        'title': 'test event name 2',
        'detail': 'detail description',
        'address': 'test location',
        'city': 'test city',
        'state': 'test state',
        'date': 'test date',
        'thumbnail': 'username.png',
        'category': [
            'test cate 1',
            'test cate 2',
            'test cate 3'
        ],
        'tag': [
            'tag a',
            'tag b'
        ],
        'creator': 'username of creator',
        'member': [
            'attender 1 username',
            'attender 2 username'
        ],
        'member_count': 3
    }]
    '''
    try:
        uid
    except NameError:
        return json.dumps([])
    username = uid
    cur = g.db.execute("select eventid,member from event_user")
    eventid=[]
    for row in cur.fetchall():
        if row[1] is not None:
            member = row[1].split(",")
            if username in member:
                eventid.append(row[0])
    print "get_rsvp_eventid"
    print eventid


    entry = []
    for i in eventid:
        cur3 = g.db.execute("select * from event,event_user where event.eventid=? and event.eventid=event_user.eventid",[i])
        for row in cur3:
            output = {}
            output["eventid"] = row[0]
            output["title"] = row[1]
            output["detail"] = row[2]
            output["date"] = row[3]
            output["address"] = row[4]
            output["city"] = row[5]
            output["state"] = row[6]
            if row[7] is not None:
                output["tag"] = row[7].split(",")
            else:
                output["tag"] = row[7]
            if row[8] is not None:
                output["category"] = row[8].split(",")
            else:
                output["category"] = row[8]
            output["creator"] = row[10]
            if row[11] is not None:
                output["member"] = row[11].split(",")
            else:
                output["member"] = row[11]
            output["member_count"] = row[12]
            output["thumbnail"] = "static/img/"+ str(output["eventid"]) + ".jpg"
            entry.append(output)
    print entry
    return json.dumps(entry)


#database
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        g.db.close()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('data.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()





if __name__ == '__main__':
    app.run()
