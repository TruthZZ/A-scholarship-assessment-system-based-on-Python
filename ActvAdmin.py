import sys;
import pymysql;
from PyQt5.QtWidgets import *;
from PyQt5.QtGui import *;
from datetime import datetime;

class ActvAdminViewstart(QWidget):
    def __init__(self):
        super().__init__();
        self.initUI();

    def initUI(self):
        self.setGeometry(300,30,800,500);
        self.setWindowTitle('奖学金评定活动管理客户端');

        self.Username_label = QLabel('用户名:',self);
        self.Username_label.setGeometry(150,100,100,20);

        self.Pass_label = QLabel('密码:',self);
        self.Pass_label.setGeometry(400,100,100,20);

        self.Dpmt_label = QLabel('组织:',self);
        self.Dpmt_label.setGeometry(150,150,100,20);

        self.Username_text = QLineEdit(self);
        self.Username_text.setGeometry(200,100,150,20);

        self.Pass_text = QLineEdit(self);
        self.Pass_text.setGeometry(450,100,150,20);
        self.Pass_text.setEchoMode(QLineEdit.Password);

        self.Departments = ["武汉大学学生会","计算机学院学生会","测绘学院学生会","电子信息学院学生会","其他（待加入）"];
        self.dbnames = ["WHUSTU","CSSTU","MapSTU","EESTU","others"];
        self.dpmt_combox = QComboBox(self);
        self.dpmt_combox.addItems(self.Departments);
        self.dpmt_combox.setGeometry(200,150,150,20);

        self.Enter_button = QPushButton('查看我的活动',self);
        self.Enter_button.setGeometry(650,400,100,50);
        self.Enter_button.clicked.connect(lambda:self.Enterdb());

        self.au_button = QPushButton("关于我们",self);
        self.au_button.setGeometry(100,400,100,50);
        self.au_button.clicked.connect(lambda:self.Aboutus());

        self.show();

    def Enterdb(self):
        self.Username = self.Username_text.text();
        self.Password = self.Pass_text.text();
        self.Department = self.dpmt_combox.currentText();
        print(self.Department);
        dindex = self.Departments.index(self.Department);
        print("%d"%(dindex));
        self.dbname = self.dbnames[dindex];

        ActvCheckView = ActvAdminCheck(self.Department,self.Username,self.Password);
        ActvCheckView.exec_();

    def Aboutus(self):
        Aboutus = AboutUs();
        Aboutus.exec_();


class ActvAdminCheck(QDialog):
    def __init__(self,dbname,Username,Password):
        super().__init__();
        self.initUI(dbname,Username,Password);

    def initUI(self,dbname,Username,Password):
        self.setGeometry(300,30,800,800);
        self.setWindowTitle('奖学金评定活动管理客户端');

        self.db_actv = pymysql.connect("localhost",Username,Password,"activities");
        self.cursor_actv = self.db_actv.cursor();

        self.actv_label = QLabel("我的活动：",self);
        self.actv_label.setGeometry(100,50,300,20);

        self.actv_list = QTableWidget(50,5,self);
        self.actv_list.setGeometry(120,120,560,500);
        self.actv_list.setHorizontalHeaderLabels(['活动号','活动名','活动时间','主办方','备注']);
        self.actv_list.verticalHeader().setVisible(False);
        self.actv_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);
        self.actv_list.setSelectionBehavior(QAbstractItemView.SelectRows);

        command = "select * from activitylist where actvhost = '%s'"%(dbname);
        print(command);
        self.cursor_actv.execute(command);
        data_actv = self.cursor_actv.fetchall();
        serialnum = 0;
        for row in data_actv:
            idnum = row[0];
            iditem = QTableWidgetItem(str(idnum));
            self.actv_list.setItem(serialnum,0,iditem);

            name = row[1];
            nameitem = QTableWidgetItem(name);
            self.actv_list.setItem(serialnum,1,nameitem);

            time = row[2];
            timestr = time.strftime('%Y-%m-%d');
            timeitem = QTableWidgetItem(timestr);
            self.actv_list.setItem(serialnum,2,timeitem);

            host = row[3];
            hostitem = QTableWidgetItem(host);
            self.actv_list.setItem(serialnum,3,hostitem);

            note = row[4];
            noteitem = QTableWidgetItem(note);
            self.actv_list.setItem(serialnum,4,noteitem);

            serialnum = serialnum + 1;


        self.add_button = QPushButton("创建新活动",self);
        self.add_button.setGeometry(600,700,120,40);
        self.add_button.clicked.connect(lambda:self.addnew_act(dbname,Username,Password));
        
        self.change_button = QPushButton("修改此活动参与情况",self);
        self.change_button.setGeometry(400,700,120,40);
        self.change_button.clicked.connect(lambda:self.change_act(dbname,Username,Password));

        self.updt_button = QPushButton("刷新",self);
        self.updt_button.setGeometry(220,700,100,40);
        self.updt_button.clicked.connect(lambda:self.updt_act(dbname));

        self.dlt_button = QPushButton("删除",self);
        self.dlt_button.setGeometry(100,700,100,40)
        self.dlt_button.clicked.connect(lambda:self.dlt_act(dbname));

        if not self.isVisible():
            self.show();


    def dlt_act(self,dbname):
        rownum = self.actv_list.currentRow();
        actvid = int(self.actv_list.item(rownum,0).text());

        command = "delete from activitylist where actvid = %d"%actvid;
        tbname = "actv"+str(actvid);
        try:
            self.cursor_actv.execute(command);
            self.cursor_actv.execute("drop table %s"%(tbname));
            self.db_actv.commit();
        except:
            self.db_actv.rollback();

        self.actv_list.clearContents();
        command = "select * from activitylist where actvhost = '%s'"%(dbname);
        print(command);
        self.cursor_actv.execute(command);
        data_actv = self.cursor_actv.fetchall();
        serialnum = 0;
        for row in data_actv:
            idnum = row[0];
            iditem = QTableWidgetItem(str(idnum));
            self.actv_list.setItem(serialnum,0,iditem);

            name = row[1];
            nameitem = QTableWidgetItem(name);
            self.actv_list.setItem(serialnum,1,nameitem);

            time = row[2];
            timestr = time.strftime('%Y-%m-%d');
            timeitem = QTableWidgetItem(timestr);
            self.actv_list.setItem(serialnum,2,timeitem);

            host = row[3];
            hostitem = QTableWidgetItem(host);
            self.actv_list.setItem(serialnum,3,hostitem);

            note = row[4];
            noteitem = QTableWidgetItem(note);
            self.actv_list.setItem(serialnum,4,noteitem);

            serialnum = serialnum + 1;


    def addnew_act(self,dbname,Username,Password):
        ActvAddView = ActvAdminAdd(dbname,Username,Password);
        ActvAddView.exec_();


    def change_act(self,dbname,Username,Password):
        rownum = self.actv_list.currentRow();
        actvid = int(self.actv_list.item(rownum,0).text());
        print("%d"%actvid);

        ActvChangeView = ActvAdminChange(dbname,Username,Password,actvid);
        ActvChangeView.exec_();


    def updt_act(self,dbname):
        self.actv_list.clearContents();
        command = "select * from activitylist where actvhost = '%s'"%(dbname);
        print(command);
        self.cursor_actv.execute(command);
        data_actv = self.cursor_actv.fetchall();
        serialnum = 0;
        for row in data_actv:
            idnum = row[0];
            iditem = QTableWidgetItem(str(idnum));
            self.actv_list.setItem(serialnum,0,iditem);

            name = row[1];
            nameitem = QTableWidgetItem(name);
            self.actv_list.setItem(serialnum,1,nameitem);

            time = row[2];
            timestr = time.strftime('%Y-%m-%d');
            timeitem = QTableWidgetItem(timestr);
            self.actv_list.setItem(serialnum,2,timeitem);

            host = row[3];
            hostitem = QTableWidgetItem(host);
            self.actv_list.setItem(serialnum,3,hostitem);

            note = row[4];
            noteitem = QTableWidgetItem(note);
            self.actv_list.setItem(serialnum,4,noteitem);

            serialnum = serialnum + 1;
        



class ActvAdminAdd(QDialog):
    def __init__(self,dbname,Username,Password):
        super().__init__();
        self.initUI(dbname,Username,Password);

    def initUI(self,dbname,Username,Password):
        self.setGeometry(300,30,800,500);
        self.setWindowTitle('奖学金评定活动管理客户端');

        self.db_actv = pymysql.connect("localhost",Username,Password,"activities");
        self.cursor_actv = self.db_actv.cursor();

        self.cursor_actv.execute("select count(*) from activitylist");
        self.actvid = self.cursor_actv.fetchone()[0] + 1;

        self.actvinfo_label = QLabel("活动基本信息",self);
        self.actvinfo_label.setGeometry(100,50,200,20);

        self.actvname_label = QLabel("活动名称：",self);
        self.actvname_label.setGeometry(120,100,100,20);

        self.time_label = QLabel("活动时间：",self);
        self.time_label.setGeometry(320,100,100,20);

        self.host_label = QLabel("主办方：",self);
        self.host_label.setGeometry(120,150,100,20);

        self.note_label = QLabel("备注：",self);
        self.note_label.setGeometry(320,150,100,20);

        self.name_text = QLineEdit(self);
        self.name_text.setGeometry(200,100,100,20);

        self.time_text = QLineEdit(self);
        self.time_text.setGeometry(400,100,100,20);

        self.host_text = QLineEdit(self);
        self.host_text.setGeometry(200,150,100,20);
        self.host_text.setText(dbname);

        self.note_text = QLineEdit(self);
        self.note_text.setGeometry(400,150,100,20);

        self.add_button = QPushButton("确认活动信息",self);
        self.add_button.setGeometry(650,125,100,20);
        self.add_button.clicked.connect(lambda:self.confirm());

        if not self.isVisible():
            self.show();


    def confirm(self):
        name = self.name_text.text();
        date = self.time_text.text();
        host = self.host_text.text();
        note = self.note_text.text();

        command = "insert into activitylist values(%d,'%s','%s','%s','%s');"%(self.actvid,name,date,host,note);
        tbname = "actv"+str(self.actvid);
        command2 = "create table if not exists %s(\
        id char(6) not null primary key comment '学号',\
        name char(8) not null comment '姓名'\
        )engine=innodb;"%(tbname);
        print(command2);
        print(command);
        self.cursor_actv.execute(command);
        self.cursor_actv.execute(command2);
        self.db_actv.commit();


class ActvAdminChange(QDialog):
    def __init__(self,dbname,Username,Password,actvid):
        super().__init__();
        self.initUI(dbname,Username,Password,actvid);

    def initUI(self,dbname,Username,Password,actvid):
        self.setGeometry(300,30,800,800);
        self.setWindowTitle('奖学金评定活动管理客户端');

        self.tbname = "actv"+str(actvid);
        self.db_actv = pymysql.connect("localhost",Username,Password,"activities");
        self.cursor_actv = self.db_actv.cursor();

        command = "select actvname from activitylist where actvid = %d"%(actvid);
        self.cursor_actv.execute(command);
        actvname = self.cursor_actv.fetchone()[0];

        self.actvname_label = QLabel(actvname,self);
        self.actvname_label.setGeometry(100,50,200,20);

        self.add_label = QLabel("添加新成员：",self);
        self.add_label.setGeometry(100,100,100,20);

        self.name_label = QLabel("姓名：",self);
        self.name_label.setGeometry(120,150,100,20);

        self.id_label = QLabel("学号：",self);
        self.id_label.setGeometry(320,150,100,20);

        self.name_text = QLineEdit(self);
        self.name_text.setGeometry(200,150,100,20);

        self.id_text = QLineEdit(self);
        self.id_text.setGeometry(400,150,100,20);

        self.add_button = QPushButton("添加",self);
        self.add_button.setGeometry(650,150,80,20);
        self.add_button.clicked.connect(lambda:self.add_act());

        self.ptcp_label = QLabel("参与人员信息：",self);
        self.ptcp_label.setGeometry(100,210,150,20);

        self.ptcp_list = QTableWidget(100,2,self); 
        self.ptcp_list.setGeometry(120,270,500,400);
        self.ptcp_list.setHorizontalHeaderLabels(['学号','姓名']);
        self.ptcp_list.verticalHeader().setVisible(False);
        self.ptcp_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);
        self.ptcp_list.setSelectionBehavior(QAbstractItemView.SelectRows);

        self.dlt_button = QPushButton("删除",self);
        self.dlt_button.setGeometry(650,460,80,20);
        self.dlt_button.clicked.connect(lambda:self.dlt_act());

        command = "select * from %s"%(self.tbname);
        self.cursor_actv.execute(command);
        data_ptcp = self.cursor_actv.fetchall();
        serialnum = 0;
        for row in data_ptcp:
            stuid = row[0];
            name = row[1];

            iditem = QTableWidgetItem(stuid);
            nameitem = QTableWidgetItem(name);

            self.ptcp_list.setItem(serialnum,0,iditem);
            self.ptcp_list.setItem(serialnum,1,nameitem);

            serialnum = serialnum + 1;


        if not self.isVisible():
            self.show();


    def add_act(self):
        stuid = self.id_text.text();
        name = self.name_text.text();

        command = "insert into %s values('%s','%s');"%(self.tbname,stuid,name);
        try:
            self.cursor_actv.execute(command);
            self.db_actv.commit();
        except:
            self.db_actv.rollback();

        self.ptcp_list.clearContents();
        command = "select * from %s"%(self.tbname);
        self.cursor_actv.execute(command);
        data_ptcp = self.cursor_actv.fetchall();
        serialnum = 0;
        for row in data_ptcp:
            stuid = row[0];
            name = row[1];

            iditem = QTableWidgetItem(stuid);
            nameitem = QTableWidgetItem(name);

            self.ptcp_list.setItem(serialnum,0,iditem);
            self.ptcp_list.setItem(serialnum,1,nameitem);

            serialnum = serialnum + 1;


    def dlt_act(self):
        rownum = self.ptcp_list.currentRow();
        stuid = self.ptcp_list.item(rownum,0).text();
        name = self.ptcp_list.item(rownum,1).text();

        command = "delete from %s where id = '%s'"%(self.tbname,stuid);
        print(command);
        try:
            self.cursor_actv.execute(command);
            self.db_actv.commit();
        except:
            self.db_actv.rollback();

        self.ptcp_list.clearContents();
        print("clear");
        command = "select * from %s"%(self.tbname);
        self.cursor_actv.execute(command);
        data_ptcp = self.cursor_actv.fetchall();
        serialnum = 0;
        for row in data_ptcp:
            stuid = row[0];
            name = row[1];

            iditem = QTableWidgetItem(stuid);
            nameitem = QTableWidgetItem(name);

            self.ptcp_list.setItem(serialnum,0,iditem);
            self.ptcp_list.setItem(serialnum,1,nameitem);

            serialnum = serialnum + 1;


class AboutUs(QDialog):
    def __init__(self):
        super().__init__();
        self.initUI();

    def initUI(self):
        self.setGeometry(300,30,800,600);
        self.setWindowTitle('关于我们');

        self.label1 = QLabel("周桢礼    2016301200276",self);
        self.label2 = QLabel("1259179722@qq.com",self);
        self.label3 = QLabel("13760468455",self);

        self.label1.setGeometry(100,50,200,20);
        self.label2.setGeometry(100,100,200,20);
        self.label3.setGeometry(100,150,200,20);

        self.label4 = QLabel("徐文逸    2017301610018",self);
        self.label5 = QLabel("15571001331",self);

        self.label4.setGeometry(100,250,200,20);
        self.label5.setGeometry(100,300,200,20);

        self.label6 = QLabel("刘奥楠    2017301610013",self);
        self.label7 = QLabel("17396155189",self);

        self.label6.setGeometry(100,400,200,20);
        self.label7.setGeometry(100,450,200,20);
        

        if not self.isVisible():
            self.show();




if __name__ == '__main__':
    app = QApplication(sys.argv)

    ActvAdmin = ActvAdminViewstart();

    sys.exit(app.exec_());
