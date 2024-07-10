
class RecordFile:
    def writeFile(self,filename,text):
        fd=open(filename,"w")
        fd.writelines(text)
        fd.close()

    def insert2File(self,filename,text):
        fd=open(filename,"a")
        fd.writelines(text)
        fd.close()

    def readFile(self,filename):
        fd=open(filename,"r")
        return fd.readlines()
        fd.close()

    def account_founder(self,phone):
        fd=open("accountRecord.txt","r")
        lines=fd.readlines()
        for line in lines:
            list=line.split("|")
            if list[3]==str(phone):
                return True
        return False
        fd.close()

    def register(self,atmNo,phNo,pin):
        if self.account_founder(phNo):
            fd=open("accountRecord.txt","r")
            lines=fd.readlines()
            for line in lines:
                list=line.split("|")
                if list[3]==str(phNo):
                    self.insert2File("userRecord.txt", f"{list[0]}|{atmNo}|{pin}\n")
                    list[5]="yes\n"
                    lines[lines.index(line)]="|".join(list)
            self.writeFile("accountRecord.txt",lines)
            fd.close()
        else:
            return False

    def pinChange(self,atmId,newData):
        fr=open("userRecord.txt","r")
        lines=fr.readlines()
        for line in lines:
            list=line.split("|")
            if list[1]==str(atmId):
                list[2]=str(newData)+"\n"
                lines[lines.index(line)]="|".join(list)
        self.writeFile("userRecord.txt",lines)
        fr.close()

    def withdraw_deposite(self,atmNo,newData):
        f1=open("userRecord.txt","r")
        lines_f1=f1.readlines()
        for line_f1 in lines_f1:
            list_f1=line_f1.split("|")
            if list_f1[1]==str(atmNo):
                f2=open("accountRecord.txt","r")
                lines_f2=f2.readlines()
                for line_f2 in lines_f2:
                    list_f2=line_f2.split("|")
                    if list_f2[0]==list_f1[0]:
                        list_f2[2]=str(newData)
                    lines_f2[lines_f2.index(line_f2)]="|".join(list_f2)
                self.writeFile("accountRecord.txt", lines_f2)
                f1.close()
                f2.close()
    
    def deleteATMAccount(self,atmN,pin):
        if self.passwordMatch(atmN, pin):
            f1=open("userRecord.txt","r")
            f2=open("accountRecord.txt","r")
            lines_f1=f1.readlines()
            lines_f2=f2.readlines()
            for line_f1 in lines_f1:
                list_f1=line_f1.split("|")
                if list_f1[1]==str(atmN):
                    del lines_f1[lines_f1.index(line_f1)]
                    self.writeFile("userRecord.txt",lines_f1)
                    for line2 in lines_f2:
                        list2=line2.split("|")
                        if list_f1[0]==list2[0]:
                            list2[5]="no\n"
                            lines_f2[lines_f2.index(line2)]="|".join(list2)
                            self.writeFile("accountRecord.txt", lines_f2)
                            return True
        return False
        f1.close()
        f2.close()


    def idFounder(self,atmNo):
        fr=open("userRecord.txt","r")
        lines=fr.readlines()
        for line in lines:
            list=line.split("|")
            if list[1]==str(atmNo):
                return True
        return False
        
    def passwordMatch(self,id,passwd):
        fr=open("userRecord.txt","r")
        lines=fr.readlines()
        for line in lines:
            list=line.split("|")
            if list[1]==str(id):
                if list[2].replace("\n","")==str(passwd):
                    return True
        return False
    
    def balanceCheck(self,id):
        if self.idFounder(id):
            f1=open("userRecord.txt","r")
            lines_f1=f1.readlines()
            for line_f1 in lines_f1:
                list_f1=line_f1.split("|")
                if list_f1[1]==str(id):
                    f2=open("accountRecord.txt","r")
                    lines=f2.readlines()
                    for line in lines:
                        list=line.split("|")
                        if list[0]==list_f1[0]:
                            return list[2]
        else: 
            return False

    def nameFounder(self,atmN):
        f1=open("userRecord.txt","r")
        f2=open("accountRecord.txt","r")
        lines_f1=f1.readlines()
        lines_f2=f2.readlines()
        for line_f1 in lines_f1:
            list_f1=line_f1.split("|")
            if list_f1[1]==str(atmN):
                for line2 in lines_f2:
                    list2=line2.split("|")
                    if list_f1[0]==list2[0]:
                        return list2[1]
                f1.close()
                f2.close()
        return "User"


    def admin_create_details_of_atmHolders(self):
        f1=open("userRecord.txt","r")
        f2=open("accountRecord.txt","r")
        f3=open("mergedFile.txt","w")
        lines1=f1.readlines()
        lines2=f2.readlines()
        resultList=[]
        for line1 in lines1:
            list1=line1.split("|")
            for line2 in lines2:
                list2=line2.split("|")
                if list1[0] ==list2[0]:
                    result=list1[0]+"|"+list1[1]+"|"+list2[1]+"|"+list2[3]+"\n"
                    resultList.append(result)
        f3.writelines(resultList)
        f1.close()
        f2.close()
        f3.close()
    
    def display_atmHolders(self):
        self.admin_create_details_of_atmHolders()
        fd=open("mergedFile.txt","r")
        lines=fd.readlines()
        fd.close()
        return lines
    def bool_already_registerd(self,phNo):
        if self.account_founder(phNo):
            fd=open("accountRecord.txt","r")
            lines=fd.readlines()
            for line in lines:
                list=line.split("|")
                if list[3]==str(phNo):
                    if list[5].replace("\n",""):
                        return True
            return False
            fd.close()
        else:
            return False




        
# test=RecordFile()
# print(test.account_founder(1))
# test.register(55556666,1000,5555)
# test.pinChange(55556666, 8666)
# test.withdraw_deposite(55556666,50000)
# print(test.idFounder(55556666))
# print(test.passwordMatch(55556666,7666))
# print(test.balanceCheck(55556666))
# test.admin_show_details()
# print(test.display_atmHolders())
# print(test.bool_already_registerd(9741933493))
# test.deleteATMAccount(222222222222,5555)
# test.nameFounder(123456789012)