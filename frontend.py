from tkinter import messagebox
from tkinter import *
from backend import *

fileHandler=RecordFile()

#this is the main page
class StartScreen:
    def __init__(self, master):
        self.master = master
        master.title("ATM Interface")

        # Create label
        self.label_welcome = Label(master, text="Welcome to MyATM", font=("Arial", 24, "bold"))
        self.label_welcome.pack(pady=20)

        # Create account number entry frame
        self.frame_account = Frame(master)
        self.label_account = Label(self.frame_account, text="ATM Number:", font=("Arial", 16))
        self.label_account.pack(side=LEFT, padx=10)
        self.entry_account = Entry(self.frame_account, font=("Arial", 16))
        self.entry_account.pack(side=LEFT, padx=10)
        self.frame_account.pack(pady=10)

        # Create PIN entry frame
        self.frame_pin = Frame(master)
        self.label_pin = Label(self.frame_pin, text="PIN:", font=("Arial", 16))
        self.label_pin.pack(side=LEFT, padx=10)
        self.entry_pin = Entry(self.frame_pin, show="*", font=("Arial", 16))
        self.entry_pin.pack(side=LEFT, padx=10)
        self.button_pin = Button(self.frame_pin, text="Verify PIN", command=self.verify_pin, font=("Arial", 16))
        self.button_pin.pack(side=LEFT, padx=10)
        self.frame_pin.pack(pady=10)
        
        # forgot passward btn
        self.forgot_pass_frame = Frame(master)
        self.forgot_pass_btn= Button(self.forgot_pass_frame,command=self.show_forgot_pass, text="Forgot password",font=("Arial", 14))
        self.forgot_pass_btn.pack()
        self.forgot_pass_frame.pack(pady=10)

        # admin screen btn frame
        self.admin_screen_frame = Frame(master)
        self.admin_screen_button= Button(self.admin_screen_frame,command=self.show_admin_page, text="Admin",font=("Arial", 14))
        self.admin_screen_button.pack()
        self.admin_screen_frame.pack(pady=10)

        # Create PIN generation btn frame
        self.frame_pin_generation = Frame(master)
        self.button_pin_generation = Button(self.frame_pin_generation, text="Generate PIN", command=self.open_pin_generation_screen, font=("Arial", 16))
        self.button_pin_generation.pack(pady=10)
        self.frame_pin_generation.pack()
    
    def show_admin_page(self):
        self.master.destroy()
        AdminScreen=Admin_page_display()
    
    #show_forgot_password screen 
    def show_forgot_pass(self):
        self.master.destroy()
        AdminScreen=forgot_pass_page_display()
    
    # program to verify the atm number and pin
    def verify_pin(self):
        atm_number = self.entry_account.get()
        pin = self.entry_pin.get()

        #checking the length of the atm number 
        if len(str(atm_number))!=12 :
            messagebox.showwarning("Length error","ATM number should be 12 digit length")
        #checking the length of the pin
        elif len(str(pin))!=4:
            messagebox.showwarning("Length error","PIN must be 4 digit length")
        #everything are ok then continue 
        else:
            if not fileHandler.idFounder(atm_number): #check wether the atm is there or not
                messagebox.showerror("Access Denied","Invalid ATM number or PIN. Access denied!!!")
            else:
            # Code to verify atm number and PIN and allow access to ATM functionality
                if fileHandler.passwordMatch(atm_number, pin):  
                    self.master.destroy()
                    main_screen = MainScreen(atm_number)
                else:
                    messagebox.showerror("Access Denied", "Invalid ATM number or PIN. Access denied!!!")

    def open_pin_generation_screen(self):
        self.master.destroy()
        pin_generation_screen = PinGenerationScreen()


# forgot password screen
class forgot_pass_page_display:
    def __init__(self):
        self.root = Tk()
        self.root.title("ATM Interface - Forgot password")

        # Create heading
        self.label_change_pin = Label(self.root, text="Forgot password", font=("Arial", 26, "bold"))
        self.label_change_pin.pack(pady=20)

        # Create atm numbr entry frame
        self.atmNo_frame = Frame(self.root)
        self.atmNo_label = Label(self.atmNo_frame, text="ATM number", font=("Arial", 16))
        self.atmNo_label.pack(side=LEFT, padx=10)
        self.atmNo_entry = Entry(self.atmNo_frame, font=("Arial", 16))
        self.atmNo_entry.pack(side=LEFT, padx=10)
        self.atmNo_frame.pack(pady=10)

        # Create phone number entry frame
        self.phNO_frame = Frame(self.root)
        self.phNo_label = Label(self.phNO_frame, text="Phone number", font=("Arial", 16))
        self.phNo_label.pack(side=LEFT, padx=10)
        self.phNo_entry = Entry(self.phNO_frame, show="*", font=("Arial", 16))
        self.phNo_entry.pack(side=LEFT, padx=10)
        self.phNO_frame.pack(pady=10)


        # Create verify button
        self.confirm_btn = Button(self.root, text="Verify", command=self.confirm_data_btn, font=("Arial", 16))
        self.confirm_btn.pack(pady=10)

        # Create back button
        self.button_back = Button(self.root, text="Back", command=self.go_back, font=("Arial", 16))
        self.button_back.pack(side=BOTTOM,pady=10)
        self.root.mainloop()

    # function to verify the data 
    def confirm_data_btn(self):
        atmNo = self.atmNo_entry.get()
        phNo= self.phNo_entry.get()
        # these 2 will be checked in the backend logic only
        if fileHandler.account_founder(phNo): #to check the atm account is there or not
            if fileHandler.idFounder(atmNo): #to check the atmno is present or not
                #entry for new pin
                self.pin_frame = Frame(self.root)
                self.pin_label = Label(self.pin_frame, text="New PIN", font=("Arial", 16))
                self.pin_label.pack(side=LEFT, padx=10)
                self.pin_entry = Entry(self.pin_frame,show="*", font=("Arial", 16))
                self.pin_entry.pack(side=LEFT, padx=10)
                self.pin_frame.pack(pady=10)

                #btn to change the pin
                self.pin_change_btn = Button(self.root, text="Change PIN",command=lambda:self.change_forgot_pin(atmNo,self.pin_entry.get()), font=("Arial", 16))
                self.pin_change_btn.pack(pady=10)
            else:
                self.handle_error_forgot_pass("Invalid credential")
        else:
            self.handle_error_forgot_pass("Invalid credential")
    
    # funtionb to change the pin
    def change_forgot_pin(self,atmNo,newPin):
        #chcking the length of the pin
        if len(str(newPin)) !=4:
            messagebox.showwarning()("PIN","PIN must be 4 digit length ")
        else:
            fileHandler.pinChange(atmNo,newPin) #changing the pin
            messagebox.showinfo("PIN change","PIN changed successfully")
            self.go_back()

    # showing error field
    def handle_error_forgot_pass(self,msg):
        error_frame = Frame(self.root)
        error_label = Label(error_frame, text=msg, font=("Arial", 16))
        error_label.pack(side=LEFT, padx=10)
        error_frame.pack(pady=10)

    # to go back to the previous screen       
    def go_back(self):
        self.root.destroy()
        # main_screen = start_screen(self.account_number)
        start_screen = StartScreen(Tk())


#admin login screen
class Admin_page_display:
    def __init__(self):
        self.root = Tk()
        self.root.title("ATM Interface - PIN Change")

        # Create label
        self.label_change_pin = Label(self.root, text="Admin Page", font=("Arial", 26, "bold"))
        self.label_change_pin.pack(pady=20)

        # Create admin username entry frame
        self.frame_admin_uname = Frame(self.root)
        self.label_admin_uname = Label(self.frame_admin_uname, text="Admin UserName", font=("Arial", 16))
        self.label_admin_uname.pack(side=LEFT, padx=10)
        self.entry_admin_uname = Entry(self.frame_admin_uname, font=("Arial", 16))
        self.entry_admin_uname.pack(side=LEFT, padx=10)
        self.frame_admin_uname.pack(pady=10)

        # Create admin passwd entry frame
        self.frame_admin_paswd = Frame(self.root)
        self.label_admin_paswd = Label(self.frame_admin_paswd, text="Password", font=("Arial", 16))
        self.label_admin_paswd.pack(side=LEFT, padx=10)
        self.entry_admin_paswd = Entry(self.frame_admin_paswd, show="*", font=("Arial", 16))
        self.entry_admin_paswd.pack(side=LEFT, padx=10)
        self.frame_admin_paswd.pack(pady=10)


        # login button
        self.button_login = Button(self.root, text="Login", command=self.login, font=("Arial", 16))
        self.button_login.pack  (pady=10)

        # Create back button
        self.button_back = Button(self.root, text="Back", command=self.go_back, font=("Arial", 16))
        self.button_back.pack(pady=10)
        self.root.mainloop()


    def login(self):
        username = self.entry_admin_uname.get()
        password= self.entry_admin_paswd.get()

        # Code to verify username and password
        if username=="admin" and password=="pass":
            self.root.destroy()
            testScreen=admin_home_screen()
        else:
            messagebox.showerror("Login Fail","Invalid credential")
        
    # gott previous screen
    def go_back(self):
        self.root.destroy()
        start_screen = StartScreen(Tk())

# admin home screen
class admin_home_screen:
    def __init__(self):
        self.root = Tk()
        self.root.title("ATM Interface - PIN Change")
        self.root.geometry("700x500")

        # Create label
        self.label_change_pin = Label(self.root, text="Admin Home Page", font=("Arial", 26, "bold"))
        self.label_change_pin.pack(pady=20)

        # Create list of account details
        records=fileHandler.display_atmHolders()

        # Display account details
        account_label = Label(self.root, text=f"AccountNumber \tATMNumber \tName\t phone\n", font=("Arial", 12), width=int(self.root.winfo_screenwidth() * 0.9))
        account_label.pack()
        for line in records:
            list=line.split("|") #to create array
            account_label = Label(self.root, text=f"{list[0]}\t{list[1]}\t{list[2]}\t"+str(list[3].replace("\n", "")), font=("Arial", 12), width=int(self.root.winfo_screenwidth() * 0.9))
            account_label.pack(pady=20)

        # Create back button
        self.button_back = Button(self.root, text="Back", command=self.go_back, font=("Arial", 16))
        self.button_back.pack(pady=10)

        self.root.mainloop()

    #togo previous screen
    def go_back(self):
        self.root.destroy()
        start_screen = StartScreen(Tk())


# to generate new pin
class PinGenerationScreen:
    def __init__(self):
        self.root = Tk()
        self.root.title("ATM Interface - PIN Generation")

        # Create label
        self.label_generate_pin = Label(self.root, text="Generate New PIN", font=("Arial", 24, "bold"))
        self.label_generate_pin.pack(pady=20)

        # Create account number entry frame
        self.frame_account = Frame(self.root)
        self.label_account = Label(self.frame_account, text="Enter New ATM Number:", font=("Arial", 16))
        self.label_account.pack(side=LEFT, padx=10)
        self.entry_account = Entry(self.frame_account, font=("Arial", 16))
        self.entry_account.pack(side=LEFT, padx=10)
        self.frame_account.pack(pady=10)

        # Create phone number entry frame
        self.frame_account_phone = Frame(self.root)
        self.label_account_phone = Label(self.frame_account_phone, text="Enter Phone number:", font=("Arial", 16))
        self.label_account_phone.pack(side=LEFT, padx=10)
        self.entry_account_phone = Entry(self.frame_account_phone, font=("Arial", 16))
        self.entry_account_phone.pack(side=LEFT, padx=10)
        self.frame_account_phone.pack(pady=10)

        # Create PIN entry frame
        self.frame_pin = Frame(self.root)
        self.label_pin = Label(self.frame_pin, text="Enter New PIN:", font=("Arial", 16))
        self.label_pin.pack(side=LEFT, padx=10)
        self.entry_pin = Entry(self.frame_pin, show="*", font=("Arial", 16))
        self.entry_pin.pack(side=LEFT, padx=10)
        self.frame_pin.pack(pady=10)

        # Create generate PIN button
        self.button_generate_pin = Button(self.root, text="Generate PIN", command=self.generate_pin, font=("Arial", 16))
        self.button_generate_pin.pack(pady=10)

        # Create back button
        self.button_back = Button(self.root, text="Back", command=self.go_back, font=("Arial", 16))
        self.button_back.pack(pady=10)

        self.root.mainloop()

    # to generate pin
    def generate_pin(self):
        atm_number = self.entry_account.get()
        account_phone_number=self.entry_account_phone.get()
        pin = self.entry_pin.get()

        #to check the pin length
        if len(pin)!=4:
            messagebox.showerror("PIN error : ","PIN must be equal to 4 characters")
        #to check the lenght if atm number and phone number
        elif len(str(atm_number))!=12 or len(str(account_phone_number))!=10:
            messagebox.showerror("Input Error : ","Invalid ATM number or phone number")
        #to chekc wether the atm number already present or not 
        elif fileHandler.idFounder(atm_number):
            messagebox.showwarning("Account Found","This ATM number already has an account proceed through forgot pass")
        else:
            #create a atm account
            fileHandler.register(atm_number,account_phone_number,pin)
            messagebox.showinfo("New PIN : ", f"Generated PIN for {atm_number}")
            self.go_back()

    # to go previous screen
    def go_back(self):
        self.root.destroy()
        start_screen = StartScreen(Tk())


# main home screen
class MainScreen:
    def __init__(self, account_number):
        self.root = Tk()
        self.root.title("ATM Interface")

        self.account_number = account_number

        self.label_generate_pin = Label(self.root, text="Welcome "+str(fileHandler.nameFounder(self.account_number)), font=("Arial", 24, "bold"))
        self.label_generate_pin.pack(pady=20)

        

        # Create withdraw frame
        self.frame_withdraw = Frame(self.root)
        self.label_withdraw = Label(self.frame_withdraw, text="Withdraw amount:", font=("Arial", 14))
        self.label_withdraw.pack(side=LEFT, padx=10)
        self.entry_withdraw = Entry(self.frame_withdraw, font=("Arial", 14))
        self.entry_withdraw.pack(side=LEFT, padx=10)
        self.button_withdraw = Button(self.frame_withdraw, text="Withdraw", command=self.withdraw, font=("Arial", 14))
        self.button_withdraw.pack(side=LEFT, padx=10)
        self.frame_withdraw.pack(pady=10)

        # Create deposit frame
        self.frame_deposit = Frame(self.root)
        self.label_deposit = Label(self.frame_deposit, text="Deposit amount:", font=("Arial", 14))
        self.label_deposit.pack(side=LEFT, padx=10)
        self.entry_deposit = Entry(self.frame_deposit, font=("Arial", 14))
        self.entry_deposit.pack(side=LEFT, padx=10)
        self.button_deposit = Button(self.frame_deposit, text="Deposit", command=self.deposit, font=("Arial", 14))
        self.button_deposit.pack(side=LEFT, padx=10)
        self.frame_deposit.pack(pady=10)

        # Create balance check frame
        self.frame_check_balance = Frame(self.root)
        self.button_check_balance = Button(self.frame_check_balance, text="Check Balance", command=self.check_balance,
                                           font=("Arial", 14))
        self.button_check_balance.pack()
        self.frame_check_balance.pack(pady=10)

        # Create PIN change frame
        self.frame_pin_change = Frame(self.root)
        self.button_pin_change = Button(self.frame_pin_change, text="Change PIN", command=self.open_pin_change_screen,font=("Arial", 14))
        self.button_pin_change.pack()
        self.frame_pin_change.pack(pady=10)


        # Create account_delete_btn frame
        self.frame_atm_delete = Frame(self.root)
        self.button_atm_delete = Button(self.frame_atm_delete, text="Delete account", command=self.open_atm_delete_screen,font=("Arial", 14))
        self.button_atm_delete.pack()
        self.frame_atm_delete.pack(pady=10)



        # Create back button
        self.button_back = Button(self.root, text="Back", command=self.go_back, font=("Arial", 14))
        self.button_back.pack(pady=10)

        self.root.mainloop()


    # function to withdraw the money
    def withdraw(self):
        amount = int(self.entry_withdraw.get())
        actualAmount=int(fileHandler.balanceCheck(self.account_number))
        if amount>actualAmount: #if withdraw amount grater than his amount in account
            messagebox.showwarning("Withdraw Warning", "Insufficient amount to withraw ")
        else:
            fileHandler.withdraw_deposite(self.account_number,(actualAmount-amount))
            messagebox.showinfo("Withdraw", f"Withdrawn amount: ${amount}. Please collect your cash and ATM card")
            self.entry_withdraw.delete(0,END)

    #function to deposite the money
    def deposit(self):
        amount = int(self.entry_deposit.get())
        actualAmount=int(fileHandler.balanceCheck(self.account_number))
        fileHandler.withdraw_deposite(self.account_number,(actualAmount+amount))
        messagebox.showinfo("Deposit", f"Deposited amount: ${amount}. Collect your card")
        self.entry_deposit.delete(0,END)

    #function to check the balance
    def check_balance(self):
        # Code to retrieve and display account balance
        self.label_account_number = Label(self.root, text=f"Balance:"+str(fileHandler.balanceCheck(self.account_number)), font=("Arial", 16))
        self.label_account_number.pack(pady=10)
        self.balance_close=Button(self.root,text="hide",command=self.hidebalance)
        self.balance_close.pack(pady=10)
        
        # to hide the balance
    def hidebalance(self):
        self.label_account_number.destroy()
        self.balance_close.destroy()
        
        
    def open_pin_change_screen(self):
        self.root.destroy()
        pin_change_screen = PinChangeScreen(self.account_number)

    def open_atm_delete_screen(self):
        self.root.destroy()
        delete_screen=Delete_screen(self.account_number)

    #to go previous screen
    def go_back(self):
        self.root.destroy()
        start_screen = StartScreen(Tk())


# screen to change pin
class PinChangeScreen:
    def __init__(self,account_number):
        self.root = Tk()
        self.root.title("ATM Interface - PIN Change")

        self.account_number = account_number

        # Create label
        self.label_change_pin = Label(self.root, text="Change PIN", font=("Arial", 24, "bold"))
        self.label_change_pin.pack(pady=20)

        # Create account number label
        self.label_account_number = Label(self.root, text=f"ATM Number: {self.account_number}", font=("Arial", 16))
        self.label_account_number.pack(pady=10)

        # Create current PIN entry frame
        self.frame_current_pin = Frame(self.root)
        self.label_current_pin = Label(self.frame_current_pin, text="Current PIN:", font=("Arial", 16))
        self.label_current_pin.pack(side=LEFT, padx=10)
        self.entry_current_pin = Entry(self.frame_current_pin, show="*", font=("Arial", 16))
        self.entry_current_pin.pack(side=LEFT, padx=10)
        self.frame_current_pin.pack(pady=10)

        # Create new PIN entry frame
        self.frame_new_pin = Frame(self.root)
        self.label_new_pin = Label(self.frame_new_pin, text="New PIN:", font=("Arial", 16))
        self.label_new_pin.pack(side=LEFT, padx=10)
        self.entry_new_pin = Entry(self.frame_new_pin, show="*", font=("Arial", 16))
        self.entry_new_pin.pack(side=LEFT, padx=10)
        self.frame_new_pin.pack(pady=10)

        # Create confirm PIN entry frame
        self.frame_confirm_pin = Frame(self.root)
        self.label_confirm_pin = Label(self.frame_confirm_pin, text="Confirm New PIN:", font=("Arial", 16))
        self.label_confirm_pin.pack(side=LEFT, padx=10)
        self.entry_confirm_pin = Entry(self.frame_confirm_pin, show="*", font=("Arial", 16))
        self.entry_confirm_pin.pack(side=LEFT, padx=10)
        self.frame_confirm_pin.pack(pady=10)

        # Create change PIN button
        self.button_change_pin = Button(self.root, text="Change PIN", command=self.change_pin, font=("Arial", 16))
        self.button_change_pin.pack(pady=10)

        # Create back button
        self.button_back = Button(self.root, text="Back", command=self.go_back, font=("Arial", 16))
        self.button_back.pack(pady=10)
        self.root.mainloop()

    # function to change pin
    def change_pin(self):
        current_pin = self.entry_current_pin.get()
        new_pin = self.entry_new_pin.get()
        confirm_pin = self.entry_confirm_pin.get()

        # Code to verify the current PIN and change it to the new PIN
        if not fileHandler.passwordMatch(self.account_number, current_pin):
            messagebox.showwarning("PIN not match","your current pin is wrong")
        elif len(str(new_pin))!=4:
            messagebox.showwarning("PIN ERROR","Invalid pin lenght")
        elif not new_pin==confirm_pin:
            messagebox.showwarning("PIN not match","PIN are not macthing!")
        else:
            fileHandler.pinChange(self.account_number,new_pin)
            messagebox.showinfo("PIN Change", "PIN successfully changed!")
            self.go_back()
    # to go previous screen
    def go_back(self):
        self.root.destroy()
        main_screen = MainScreen(self.account_number)

# delete account screen
class Delete_screen:
    def __init__(self,atmNumber_home):
        self.atmNumber_home=atmNumber_home
        self.root = Tk()
        self.root.title("ATM Interface - ATM delete")

        # Create label
        self.label_change_pin = Label(self.root, text="Deactivate your ATM", font=("Arial", 24, "bold"))
        self.label_change_pin.pack(pady=20)

        # Create current atm number entry frame
        self.frame_current_atmNumber = Frame(self.root)
        self.label_current_atmNumber = Label(self.frame_current_atmNumber, text="ATM number:", font=("Arial", 16))
        self.label_current_atmNumber.pack(side=LEFT, padx=10)
        self.entry_current_atmNumber = Entry(self.frame_current_atmNumber, show="*", font=("Arial", 16))
        self.entry_current_atmNumber.pack(side=LEFT, padx=10)
        self.frame_current_atmNumber.pack(pady=10)

        # Create current PIN entry frame
        self.frame_current_pin = Frame(self.root)
        self.label_current_pin = Label(self.frame_current_pin, text="Current PIN:", font=("Arial", 16))
        self.label_current_pin.pack(side=LEFT, padx=10)
        self.entry_current_pin = Entry(self.frame_current_pin, show="*", font=("Arial", 16))
        self.entry_current_pin.pack(side=LEFT, padx=10)
        self.frame_current_pin.pack(pady=10)

        # Create delete account button
        self.button_delete_account = Button(self.root, text="Deactivate account", command=self.delete_atm, font=("Arial", 16))
        self.button_delete_account.pack(pady=10)

        # Create back button
        self.button_back = Button(self.root, text="Back", command=self.go_back, font=("Arial", 16))
        self.button_back.pack(pady=10)
        self.root.mainloop()

    # funtion to delete the account 
    def delete_atm(self):
        self.atmNumber = self.entry_current_atmNumber.get()
        self.pin = self.entry_current_pin.get()
        if fileHandler.deleteATMAccount(self.atmNumber,self.pin):
            messagebox.showerror("Success","Account deactivated sucessfully")
            self.go_back()
        else:
            messagebox.showerror("PIN Error","Wrong PIN")

    # to go previous screen    
    def go_back(self):
        self.root.destroy()
        main_screen = MainScreen(self.atmNumber_home)



root = Tk()
start_screen = StartScreen(root)
root.mainloop()
