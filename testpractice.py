import sys
import os
from ui_testpractice import * 
from PyQt5.QtWidgets import * 
from persistent import Persistent
from ZODB import FileStorage, DB
import transaction
import shutil

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')
 
class Question(Persistent):
  def __init__(self, question, answer,analysis):
    self.question = question
    self.answer = answer
    self.analysis=analysis
    self.wrong_num =""
    self.isdo=0


class MyZODB(object):

    def __init__(self, path):

        self.storage = FileStorage.FileStorage(path)

        self.db = DB(self.storage)

        self.connection = self.db.open()

        self.dbroot = self.connection.root()

    def close(self):
        self.connection.close()

        self.db.close()

        self.storage.close()


class MyWindow(QtWidgets.QMainWindow,Ui_Form):
    
    def __init__(self):

        super(MyWindow,self).__init__()
        self.isopen=0
        self.local_fname="./Data.fs"
        self.fname=0
        self.numb=0
        self.long=0
        self.que=""
        self.question=""
        self.answer=""
        self.analysis=""
        self.setupUi(self)
    def slot_check(self):
        if self.numb:
            self.answer=self.que.answer
            self.textEdit.setHtml(self.answer)
            self.label_2.setText("答案")
    def slot_read(self):
        if self.numb:
            self.analysis=self.que.analysis
            self.textEdit.setHtml(self.analysis)
            self.label_2.setText("试题解析")
    def slot_back(self):
        self.numb-=1
        
        if self.numb<=0:
            self.textEdit.setText("前面没有题目了")
            self.numb=0
            self.label_3.setText("")
        else:
            self.que=self.dbroot["test"+str(self.numb)]
            self.question=self.que.question
            self.textEdit.setHtml(self.question)
            self.label_2.setText("试题")
            if self.que.isdo:
                self.label_3.setText(self.que.wrong_num)
            else:
                self.label_3.setText("")
    def slot_testnext(self):
        self.numb+=1
        
        if self.numb>self.long:
            self.textEdit.setHtml("没有题目了")
            self.numb=self.long
            self.label_3.setText("")
        else:
            self.que=self.dbroot["test"+str(self.numb)]
            self.question=self.que.question
            self.textEdit.setHtml(self.question)
            self.label_2.setText("试题")
            if self.que.isdo:
                self.label_3.setText(self.que.wrong_num)
            else:
                self.label_3.setText("")
    def slot_yes(self):
        if self.numb:
            self.que.isdo=1
            self.que.wrong_num ="√"
            self.label_3.setText(self.que.wrong_num)
            transaction.commit()
    def slot_no(self):
        if self.numb:
            self.que.isdo=1
            self.que.wrong_num ="×"
            self.label_3.setText(self.que.wrong_num)
            transaction.commit()
    def slot_oldfile(self):
        if self.isopen:
            self.textEdit.setText("题库已经打开了")
        else:
            if os.path.exists(self.local_fname):
                self.db = MyZODB(self.local_fname)
                self.dbroot = self.db.dbroot
                self.long=len(self.dbroot.keys())
                self.textEdit.setText("一共有"+str(self.long)+"道题")
                self.isopen=1
            else:
                self.textEdit.setText("没有上次练习，打开一个新的题库")
                self.slot_fileopen()
    def slot_fileopen(self):
        if self.isopen:
            self.textEdit.setText("题库已经打开了")
        else:
            self.fname,self.ty = QFileDialog.getOpenFileName(self,'open file', GetDesktopPath(),"Fs files(*.fs)")
            shutil.copyfile(self.fname,self.local_fname)
            self.db = MyZODB(self.local_fname)
            self.dbroot = self.db.dbroot
            self.long=len(self.dbroot.keys())
            self.textEdit.setText("一共有"+str(self.long)+"道题")
            self.isopen=1
    def slot_exit(self):
        if self.isopen:
            transaction.commit()
            self.db.close()
            sys.exit()
        else:
            sys.exit()
        



        
if __name__=="__main__":

    app=QtWidgets.QApplication(sys.argv)

    myshow=MyWindow()

    myshow.show()
                
    sys.exit(app.exec_())
