use activities;
create table if not exists activitylist(
    ActvID int(3) auto_increment not null primary key comment '活动编号',
    ActvName char(20) not null comment '活动名',
    Actvtime date not null comment '活动日期',
    Actvhost char(20) not null comment '主办方',
    Note text null comment '说明'
)engine = innodb

insert into activitylist values('1','活动A','2018-01-01','武汉大学学生会',null);

create table if not exists selectedactv(
    actvid int(3) not null primary key comment '活动编号',
    actvname char(20) not null comment '活动名',
    actvvalue float not null comment '活动分值'
)engine = innodb

create table if not exists f1weights(
    compulsory float not null comment '必修权重',
    selected float not null comment '选修权重',
    total float not null comment '总权重'
)engine = innodb

create database if not exists Students;
use Students;

CREATE TABLE Studentinfo
   ( id  char(6) NOT NULL PRIMARY KEY comment "学号",
     name  char(8) NOT NULL comment "姓名",
     major  char(10) NULL comment "专业名",
     cpsrgrade float not null comment "必修均分",
     slctgrade float not null comment "选修均分"
   ) ENGINE=innodb;

insert into Studentinfo values
('081101','王林','计算机',80,90),
('081102','程明','计算机',75,69),
('081103','王燕','计算机',99,80),
('081104','韦严平','计算机',68,79),
('081106','李方方','计算机',77,95),
('081107','李明','计算机',88,93),
('081108','林一帆','计算机',90,90),
('081109','张强民','计算机',90,63),
('081110','张蔚','计算机',79,68),
('081111','赵琳','计算机',75,90),
('081113','严红','计算机',83,89),
('081201','王敏','通信工程',99,93),
('081202','王林','通信工程',92,78),
('081203','王玉民','通信工程',60,78),
('081204','马琳琳','通信工程',70,86),
('081206','李计','通信工程',86,84),
('081210','李红庆','通信工程',67,89),
('081216','孙祥欣','通信工程',98,65),
('081218','孙研','通信工程',75,88),
('081220','吴薇华','通信工程',67,94),
('081221','刘燕敏','通信工程',82,89),
('081241','罗林琳','通信工程',93,71);