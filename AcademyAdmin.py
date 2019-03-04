import sys;
import pymysql;
from PyQt5.QtWidgets import *;
from PyQt5.QtGui import *;
from datetime import datetime;

class DepartAdminViewstart(QWidget):
    def __init__(self):
        super().__init__();
        self.initUI();

    def initUI(self):
        self.setGeometry(300,30,800,500);
        self.setWindowTitle('奖学金评定学院管理客户端');

        self.Username_label = QLabel('用户名:',self);
        self.Username_label.setGeometry(150,100,100,20);

        self.Pass_label = QLabel('密码:',self);
        self.Pass_label.setGeometry(400,100,100,20);

        self.Dpmt_label = QLabel('学院:',self);
        self.Dpmt_label.setGeometry(150,150,100,20);

        self.Year_label = QLabel('学年:',self);
        self.Year_label.setGeometry(400,150,100,20);

        self.Username_text = QLineEdit(self);
        self.Username_text.setGeometry(200,100,150,20);

        self.Pass_text = QLineEdit(self);
        self.Pass_text.setGeometry(450,100,150,20);
        self.Pass_text.setEchoMode(QLineEdit.Password);

        self.Year_text = QLineEdit(self);
        self.Year_text.setGeometry(450,150,150,20);
        self.Year_text.setText("格式如：20172018");
        self.Year_text.setToolTip("例如:20172018");

        self.Departments = ["计算机学院","电子信息学院","测绘学院","遥感学院","国家网络与安全学院","数学与统计学院","哲学学院","其他（待加入）"];
        self.dbnames = ["CS","EE","Map","RS","NS","MS","Phi","others"];
        self.dpmt_combox = QComboBox(self);
        self.dpmt_combox.addItems(self.Departments);
        self.dpmt_combox.setGeometry(200,150,150,20);

        self.Enter_button = QPushButton('创建数据库',self);
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
        self.Year = self.Year_text.text();
        self.databasename = self.dbname+self.Year;
        self.dbinfo = self.Department+self.Year;

        db = pymysql.connect("localhost",self.Username,self.Password);
        cursor = db.cursor();
        createcmd = "create database if not exists "+self.databasename;
        try:
            cursor.execute(createcmd);
            db.commit();
        except:
            db.rollback();

        Departadminset = DepartAdminViewSet(self.dbinfo,self.Username,self.Password,self.databasename);
        Departadminset.exec_();


    def Aboutus(self):
        Aboutus = AboutUs();
        Aboutus.exec_();


class DepartAdminViewSet(QDialog):
    def __init__(self,dbinfo,Username,Password,databasename):
        super().__init__();
        self.initUI(dbinfo,Username,Password,databasename);

    def initUI(self,dbinfo,Username,Password,databasename):
        self.setGeometry(300,30,800,800);
        self.setWindowTitle('奖学金评定学院管理客户端');

        self.sclsinfo = "奖学金信息："+dbinfo;
        self.sclsinfo_label = QLabel(self.sclsinfo,self);
        self.sclsinfo_label.setGeometry(100,50,400,40);

        self.f1_label = QLabel("第一部分：F1 学生成绩  (注：F1=（必修均分*必修权重+选修均分*选修权重)*总权重）",self);
        self.f1_label.setGeometry(100,100,700,20);

        self.f1cp_label = QLabel("必修均分权重：",self);
        self.f1cp_label.setGeometry(140,130,100,20);

        self.f1se_label = QLabel("选修均分权重：",self);
        self.f1se_label.setGeometry(300,130,100,20);
        
        self.f1cp_text = QLineEdit(self);
        self.f1cp_text.setGeometry(220,130,60,20);

        self.f1se_text = QLineEdit(self);
        self.f1se_text.setGeometry(380,130,60,20);

        self.f1wt_label = QLabel("成绩均分加权：",self);
        self.f1wt_label.setGeometry(520,130,100,20);

        self.f1wt_text = QLineEdit(self);
        self.f1wt_text.setGeometry(610,130,60,20);

        self.f2_label = QLabel("第二部分：F2 校级活动分",self);
        self.f2_label.setGeometry(100,180,300,20);

        self.db_actv = pymysql.connect("localhost",Username,Password,"Activities");
        self.db_scls = pymysql.connect("localhost",Username,Password,databasename);

        self.cursor_actv = self.db_actv.cursor();
        self.cursor_scls = self.db_scls.cursor();

        command = "create table if not exists f1weights(\
        compulsory float not null comment '必修权重',\
        selected float not null comment '选修权重',\
        total float not null comment '总权重')engine=innodb;";
        print(command);
        try:
            self.cursor_scls.execute(command);
            self.db_scls.commit();
        except:
            self.db_scls.rollback();

        command = "select * from f1weights";
        self.cursor_scls.execute(command);
        data_f1weights = self.cursor_scls.fetchall();
        for row in data_f1weights:
            w_cpsr = row[0];
            self.f1cp_text.setText(str(w_cpsr));

            w_slct = row[1];
            self.f1se_text.setText(str(w_slct));

            w_total = row[2];
            self.f1wt_text.setText(str(w_total));


        command = "create table if not exists selectedactv(\
        actvid int(3) not null primary key comment '活动编号',\
        actvname char(20) not null comment '活动名',\
        actvvalue float not null comment '活动分值')engine=innodb;"
        try:
            self.cursor_scls.execute(command);
            self.db_scls.commit();
        except:
            self.db_scls.rollback();

        self.cursor_actv.execute("select count(*) from activitylist");
        actv_num = self.cursor_actv.fetchone()[0];

        self.actv_list = QTableWidget(100,5,self);
        self.actv_list.setHorizontalHeaderLabels(['编号','活动名称','活动日期','主办方','说明']);
        self.actv_list.setGeometry(120,220,500,200);
        self.actv_list.setSelectionBehavior(QAbstractItemView.SelectRows);
        self.actv_list.verticalHeader().setVisible(False);

        self.add_button = QPushButton("添加",self);
        self.add_button.setGeometry(650,310,60,20);
        self.add_button.clicked.connect(lambda:self.add_actv());

        self.slct_label = QLabel("已选活动信息：",self);
        self.slct_label.setGeometry(110,440,100,20);

        self.cursor_scls.execute("select count(*) from selectedactv");
        slct_num = self.cursor_scls.fetchone()[0];

        self.slct_list = QTableWidget(100,3,self);
        self.slct_list.setHorizontalHeaderLabels(['编号','活动名称','活动分分值']);
        self.slct_list.setGeometry(120,480,500,200);
        self.slct_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);
        self.slct_list.verticalHeader().setVisible(False);

        self.updt_button = QPushButton("修改",self);
        self.updt_button.setGeometry(650,555,60,20);
        self.updt_button.clicked.connect(lambda:self.updt_actv());

        self.dlt_button = QPushButton("删除",self);
        self.dlt_button.setGeometry(650,585,60,20);
        self.dlt_button.clicked.connect(lambda:self.dlt_actv());
        
        self.cursor_scls.execute("select * from selectedactv");
        data_slct = self.cursor_scls.fetchall();
        serialnum = 0;
        for row in data_slct:
            idnum = row[0];
            iditem = QTableWidgetItem(str(idnum));
            self.slct_list.setItem(serialnum,0,iditem);

            name = row[1];
            nameitem = QTableWidgetItem(name);
            self.slct_list.setItem(serialnum,1,nameitem);

            value = row[2];
            valueitem = QTableWidgetItem(str(value));
            self.slct_list.setItem(serialnum,2,valueitem);

            serialnum = serialnum + 1;


        self.cursor_actv.execute("select * from activitylist");
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


        self.next_button = QPushButton("确认更新设置-->",self);
        self.next_button.setGeometry(600,700,120,40);
        self.next_button.clicked.connect(lambda:self.next_act(dbinfo,Username,Password,databasename));

        if not self.isVisible():
            self.show();


    def add_actv(self):
        rownum = self.actv_list.currentRow();
        print("%d"%rownum);
        idnum_item = self.actv_list.item(rownum,0);
        name_item = self.actv_list.item(rownum,1);
        idnum_str = idnum_item.text();
        name_str = name_item.text();
        print("%s %s"%(idnum_str,name_str));
        command = "insert into selectedactv(actvid,actvname,actvvalue) values(%d,'%s',0);"%(int(idnum_str),name_str);
        print(command);
        try:
            self.cursor_scls.execute(command);
            self.db_scls.commit();
        except:
            self.db_scls.rollback();

        self.slct_list.clearContents();

        self.cursor_scls.execute("select * from selectedactv");
        data_slct = self.cursor_scls.fetchall();
        serialnum = 0;
        for row in data_slct:
            idnum = row[0];
            iditem = QTableWidgetItem(str(idnum));
            self.slct_list.setItem(serialnum,0,iditem);

            name = row[1];
            nameitem = QTableWidgetItem(name);
            self.slct_list.setItem(serialnum,1,nameitem);

            value = row[2];
            valueitem = QTableWidgetItem(str(value));
            self.slct_list.setItem(serialnum,2,valueitem);
            
            serialnum = serialnum + 1;


    def updt_actv(self):
        rownum = self.slct_list.currentRow();
        actvvalue = float(self.slct_list.item(rownum,2).text());
        actvid = int(self.slct_list.item(rownum,0).text());
        command = "update selectedactv\
        set actvvalue = %f\
        where actvid = %d"%(actvvalue,actvid);
        print(command);
        try:
            self.cursor_scls.execute(command);
            self.db_scls.commit();
        except:
            self.db_scls.rollback();

        self.cursor_scls.execute("select * from selectedactv");
        data_slct = self.cursor_scls.fetchall();
        serialnum = 0;
        for row in data_slct:
            idnum = row[0];
            iditem = QTableWidgetItem(str(idnum));
            self.slct_list.setItem(serialnum,0,iditem);

            name = row[1];
            nameitem = QTableWidgetItem(name);
            self.slct_list.setItem(serialnum,1,nameitem);

            value = row[2];
            valueitem = QTableWidgetItem(str(value));
            self.slct_list.setItem(serialnum,2,valueitem);
            
            serialnum = serialnum + 1;


    def dlt_actv(self):
        rownum = self.slct_list.currentRow();
        actvid = int(self.slct_list.item(rownum,0).text());
        command = "delete from selectedactv where actvid = %d"%(actvid);
        print(command);
        try:
            self.cursor_scls.execute(command);
            self.db_scls.commit();
        except:
            self.db_scls.rollback();

        self.slct_list.clearContents();

        self.cursor_scls.execute("select * from selectedactv");
        data_slct = self.cursor_scls.fetchall();
        serialnum = 0;
        for row in data_slct:
            idnum = row[0];
            iditem = QTableWidgetItem(str(idnum));
            self.slct_list.setItem(serialnum,0,iditem);

            name = row[1];
            nameitem = QTableWidgetItem(name);
            self.slct_list.setItem(serialnum,1,nameitem);

            value = row[2];
            valueitem = QTableWidgetItem(str(value));
            self.slct_list.setItem(serialnum,2,valueitem);
            
            serialnum = serialnum + 1;


    def next_act(self,dbinfo,Username,Password,databasename):
        cpsr_value = float(self.f1cp_text.text());
        slct_value = float(self.f1se_text.text());
        f1_weight = float(self.f1wt_text.text());
        command1 = "delete from f1weights";
        command2 = "insert into f1weights values(%f,%f,%f)"%(cpsr_value,slct_value,f1_weight);
        try:
            self.cursor_scls.execute(command1);
            self.cursor_scls.execute(command2);
            self.db_scls.commit();
        except:
            self.db_scls.rollback();

        try:
            self.cursor_scls.execute("delete from results");
            self.db_scls.commit();
        except:
            self.db_scls.rollback();

        DepartAdminStu = DepartAdminViewStu(dbinfo,Username,Password,databasename);
        DepartAdminStu.exec_();
        

class DepartAdminViewStu(QDialog):
    def __init__(self,dbinfo,Username,Password,databasename):
        super().__init__();
        self.initUI(dbinfo,Username,Password,databasename);

    def initUI(self,dbinfo,Username,Password,databasename):
        self.setGeometry(300,30,800,800);
        self.setWindowTitle('奖学金评定学院管理客户端');

        self.db_scls = pymysql.connect("localhost",Username,Password,databasename);
        self.db_stud = pymysql.connect("localhost",Username,Password,"Students");
        self.db_actv = pymysql.connect("localhost",Username,Password,"activities");

        self.cursor_scls = self.db_scls.cursor();
        self.cursor_stud = self.db_stud.cursor();
        self.cursor_actv = self.db_actv.cursor();

        self.sclsinfo = "奖学金信息："+dbinfo;
        self.sclsinfo_label = QLabel(self.sclsinfo,self);
        self.sclsinfo_label.setGeometry(100,50,400,40);

        self.rslt_label = QLabel("学生综评分排名：",self);
        self.rslt_label.setGeometry(100,100,300,20);

        if databasename[0:2] == "CS":
            major_wanted = "计算机";
        elif databasename[0:2] == "EE":
            major_wanted = "通信工程";
        print(databasename[0:2]);

        command = "select count(*) from studentinfo where major = '%s'"%(major_wanted);
        print(command);
        self.cursor_stud.execute(command);
        studnum = self.cursor_stud.fetchone()[0];
        print(str(studnum));

        self.relt_list = QTableWidget(500,8,self);
        self.relt_list.setGeometry(120,120,500,500);
        self.relt_list.setHorizontalHeaderLabels(['学号','姓名','专业','必修均分加权','选修均分加权','F1','总活动分F2','综评分']);
        self.relt_list.verticalHeader().setVisible(True);

        command = "CREATE TABLE if not exists results(\
        id  char(6) NOT NULL PRIMARY KEY comment '学号',\
        name  char(8) NOT NULL comment '姓名',\
        major  char(10) NULL comment '专业名',\
        cpsrgrade float not null comment '必修均分',\
        slctgrade float not null comment '选修均分',\
        f1 float not null comment 'F1',\
        f2 float not null comment 'F2',\
        total float not null comment '综评分'\
        )ENGINE=innodb;";
        self.cursor_scls.execute(command);

        self.cursor_scls.execute("select * from f1weights");
        data_weight = self.cursor_scls.fetchone();
        self.cpsr_weight = data_weight[0];
        self.slct_weight = data_weight[1];
        self.f1_weight = data_weight[2];

        self.cursor_scls.execute("select count(*) from selectedactv");
        self.actvnum = self.cursor_scls.fetchone()[0];

        command = "select actvid from selectedactv";
        self.cursor_scls.execute(command);
        actvidnums = [];
        data_actvid = self.cursor_scls.fetchall();
        for row in data_actvid:
            actvidnums.append(row[0]);

        self.cursor_stud.execute("select * from studentinfo where major = '%s'"%(major_wanted));
        data_stud = self.cursor_stud.fetchall();
        for row in data_stud:
            id = row[0];
            name = row[1];
            major = row[2];
            cpsr = row[3];
            slct = row[4];

            wd_cpsr = cpsr * self.cpsr_weight;
            wd_slct = slct * self.slct_weight;
            wd_f1 = (wd_cpsr + wd_slct) * self.f1_weight;
            actvcre = 0;

            for i in actvidnums:
                tbname = "actv"+str(i);
                #print("select count(*) from %s where id = '%s'"%(tbname,id));
                self.cursor_actv.execute("select count(*) from %s where id = '%s'"%(tbname,id));
                flagin = self.cursor_actv.fetchone()[0];
                if flagin > 0:
                    self.cursor_scls.execute("select actvvalue from selectedactv where actvid = %d"%i);
                    value = self.cursor_scls.fetchone()[0];
                    actvcre = actvcre + value;

            totalcre = wd_f1 + actvcre;

            command = "insert into results values('%s','%s','%s',%f,%f,%f,%f,%f)"%(id,name,major,wd_cpsr,wd_slct,wd_f1,actvcre,totalcre);
            try:
                self.cursor_scls.execute(command);
                self.db_scls.commit();
            except:
                self.db_scls.rollback();


        self.cursor_scls.execute("select * from results order by total desc");
        data_result = self.cursor_scls.fetchall();
        serialnum = 0;
        for row in data_result:
            id = row[0];
            name = row[1];
            major = row[2];
            wd_cpsr = row[3];
            wd_slct = row[4];
            wd_f1 = row[5];
            actvcre = row[6];
            totalcre = row[7];

            iditem = QTableWidgetItem(id);
            nameitem = QTableWidgetItem(name);
            majoritem = QTableWidgetItem(major);
            cpsritem = QTableWidgetItem(str(wd_cpsr));
            slctitem = QTableWidgetItem(str(wd_slct));
            f1item = QTableWidgetItem(str(wd_f1));
            actvitem = QTableWidgetItem(str(actvcre));
            totalitem = QTableWidgetItem(str(totalcre));

            self.relt_list.setItem(serialnum,0,iditem);
            self.relt_list.setItem(serialnum,1,nameitem);
            self.relt_list.setItem(serialnum,2,majoritem);
            self.relt_list.setItem(serialnum,3,cpsritem);
            self.relt_list.setItem(serialnum,4,slctitem);
            self.relt_list.setItem(serialnum,5,f1item);
            self.relt_list.setItem(serialnum,6,actvitem);
            self.relt_list.setItem(serialnum,7,totalitem);

            serialnum = serialnum + 1;

        if not self.isVisible():
            self.show();       



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

    DepartmentView = DepartAdminViewstart();

    sys.exit(app.exec_());

