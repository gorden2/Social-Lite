drop table if exists userdata;
create table userdata (
  username text primary key,
  password text not null
);

insert into userdata(username,password) values("admin","admin");

drop table if exists userinfo;
create table userinfo (
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
  foreign key (username) references userdata(username)
);

insert into userinfo(username,u_city,u_interests,displayname,u_gender,u_birth,u_email,u_address,u_state,u_bio)
    values("admin","CP","Football,Games","admin","male","1990-10-10","gorden725@gmail.com","1000 Baltimore Ave.","MD","I love social lite!");


drop table if exists event;
create table event (
  eventid integer primary key autoincrement,
  e_title text,
  e_detail text,
  e_time text,
  e_address text,
  e_city text,
  e_state text,
  e_tag text,
  category text
);

insert into event(eventid,e_title,e_detail,e_time,e_city,e_state,e_tag,category,e_address)
    values (1,"CP Football Match","The 45th Maryland Football Match","2014-12-20","CP","MD","Maryland,Football,Match","Football","2000 Baltimore Ave.");
insert into event(eventid,e_title,e_detail,e_time,e_city,e_state,e_tag,category,e_address)
    values (2,"Baltimore Football Match","The 45th Maryland Football Match","2014-12-20","Baltimore","MD","Maryland,Football,Match","Football","5000 Baltimore Ave.");
insert into event(eventid,e_title,e_detail,e_time,e_city,e_state,e_tag,category,e_address)
    values (3,"Indoor Swimming Pool Party","You can stretch our arms in CPISP","2014-12-22","CP","MD","CPISP","Swimming","2001 Baltimore Ave.");
insert into event(eventid,e_title,e_detail,e_time,e_city,e_state,e_tag,category,e_address)
    values (4,"Sports Day","We will have a sport contest in CP Stadium","2014-12-12","CP","MD","CP,Stadium","Football,Swimming","2005 Baltimore Ave.");

drop table if exists event_user;
create table event_user(
  eventid integer primary key,
  creator text,
  member text,
  membercount integer,
  foreign key (eventid) references event(eventid)
);

insert into event_user(eventid,creator,member,membercount) values(1,"admin","goo,bar,foo,admin",4);
insert into event_user(eventid,creator,member,membercount) values(2,"admin","goo,bar",2);
insert into event_user(eventid,creator,member,membercount) values(3,"admin","bar",1);
insert into event_user(eventid,creator,member,membercount) values(4,"admin","foo",1);


drop table if exists event_discuss;
create table event_discuss(
  disid integer primary key autoincrement,
  eventid integer,
  username text,
  discussion text,
  d_title text,
  point text
);

insert into event_discuss(disid,eventid,username,discussion,d_title,point)
        values (1,1,"admin","This is an awesome event","Event comment","Positive");


drop table if exists parenlist;
create table parenlist(
 child text primary key,
 parent text
);

insert into parenlist(child,parent) values("Nightlife", "Social");
insert into parenlist(child,parent) values("Fun Times", "Social");
insert into parenlist(child,parent) values("Hacking", "Internet & Technology");
insert into parenlist(child,parent) values("Programming", "Internet & Technology");
insert into parenlist(child,parent) values("Java", "Internet & Technology");
insert into parenlist(child,parent) values("Photography", "Internet & Technology");
insert into parenlist(child,parent) values("PHP", "Internet & Technology");
insert into parenlist(child,parent) values("Beer", "Hobbies");
insert into parenlist(child,parent) values("Travel", "Hobbies");
insert into parenlist(child,parent) values("Wine", "Hobbies");
insert into parenlist(child,parent) values("Games", "Hobbies");
insert into parenlist(child,parent) values("Motorcycle Riding", "Hobbies");
insert into parenlist(child,parent) values("Evolution", "Science");
insert into parenlist(child,parent) values("Astronomy", "Science");
insert into parenlist(child,parent) values("Biology", "Science");
insert into parenlist(child,parent) values("Innovation", "Science");
insert into parenlist(child,parent) values("Meditation", "Health & Support");
insert into parenlist(child,parent) values("Yoga", "Health & Support");
insert into parenlist(child,parent) values("Depression", "Health & Support");
insert into parenlist(child,parent) values("Fitness", "Health & Support");
insert into parenlist(child,parent) values("Football","Sport");
insert into parenlist(child,parent) values("Swimming","Sport");
insert into parenlist(child,parent) values("Art","Arts & Entertainment");
insert into parenlist(child,parent) values("Fiction","Arts & Entertainment");
insert into parenlist(child,parent) values("Film","Arts & Entertainment");
insert into parenlist(child,parent) values("Lean Startup","Business & Career");
insert into parenlist(child,parent) values("Marketing","Business & Career");
insert into parenlist(child,parent) values("Investing","Business & Career");
insert into parenlist(child,parent) values("Social Media","Internet & Technology");
insert into parenlist(child,parent) values("Interaction Design","Internet & Technology");
insert into parenlist(child,parent) values("Cloud Computing","Internet & Technology");