from tkinter import *
from tkinter import messagebox
import sqlite3

class contact_book:
    def __init__(self):
        self.root=Tk()
        self.root.title("Contact Book")
        self.root.geometry("650x600")
        self.root.resizable(False,False)

        self.title=Label(self.root,text="Contact Book",font=("helvetica",30,"bold"))
        self.title.pack(pady=5)

        self.first_name=Label(self.root,text="First_name",font=("arial",15))
        self.first_name.place(x=10,y=60)

        self.entry_1=Entry(self.root,width=16,font=("arial",15))
        self.entry_1.place(x=160,y=60)

        self.last_name=Label(self.root,text="Last_name",font=("arial",15))
        self.last_name.place(x=10,y=100)

        self.entry_2=Entry(self.root,width=16,font=("arial",15))
        self.entry_2.place(x=160,y=100)

        self.pho_no=Label(self.root,text="Phone Number",font=("arial",15))
        self.pho_no.place(x=10,y=140)

        self.entry_3=Entry(self.root,width=16,font=("arial",15))
        self.entry_3.place(x=160,y=140)

        self.email=Label(self.root,text="Email",font=("arial",15))
        self.email.place(x=10,y=180)

        self.entry_4=Entry(self.root,width=16,font=("arial",15))
        self.entry_4.place(x=160,y=180)

        self.address=Label(self.root,text="Address",font=("arial",15))
        self.address.place(x=10,y=220)

        self.entry_5=Text(self.root,width=16,height=10,font=("arial",15))
        self.entry_5.place(x=160,y=220)

        self.add=Button(self.root,text="Add",font=("arial",10),width=3,padx=30,command=self.add)
        self.add.place(x=130,y=500)

        self.update=Button(self.root,text="Update",font=("arial",10),width=3,padx=30,state=DISABLED,command=self.update)
        self.update.place(x=270,y=500)

        self.detele=Button(self.root,text="Delete",font=("arial",10),width=3,padx=30,state=DISABLED,command=self.delete)
        self.detele.place(x=540,y=500)

        self.show_data=Button(self.root,text="Show Data",font=("arial",10),width=3,padx=30,state=DISABLED,command=self.show_data)
        self.show_data.place(x=410,y=500)


        self.frame=Frame(self.root)
        self.scroll_bar=Scrollbar(self.frame,orient=VERTICAL)
        self.listbox=Listbox(self.frame,width=24,height=16,font=("arial",15),yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.listbox.yview)
        self.scroll_bar.pack(side=RIGHT,fill=BOTH)
        self.listbox.pack(side=LEFT,fill=BOTH)
        self.frame.place(x=350,y=60)
        self.listbox.insert(END,"Id"+"  Name"+"  Phone_no")

        

        self.conn=sqlite3.connect("contact_book.db")
        self.c=self.conn.cursor()
        self.c.execute("SELECT oid,* FROM contact")
        data=self.c.fetchall()
        
        for i in data:
            rec=(str(i[0])+' '+i[1]+ " "+str(i[3]))
            self.listbox.insert(END,rec)
        self.conn.commit()
        self.conn.close()

        self.listbox.bind("<ButtonRelease-1>",self.select_record)

        self.root.mainloop()
    def add(self):
        self.conn=sqlite3.connect("contact_book.db")
        self.c=self.conn.cursor()
        self.c.execute("INSERT INTO contact VALUES(:First_name,:Last_name,:Pho_no,:Email,:Address)",
                       {
                         "First_name":self.entry_1.get(),
                         "Last_name":self.entry_2.get(),
                         "Pho_no":self.entry_3.get(),
                         "Email":self.entry_4.get(),
                         "Address":self.entry_5.get(1.0,"end-1c")
                        })
        self.c.execute("SELECT oid,* FROM contact")
        data=self.c.fetchall()
        for i in data:
            if i[1]==self.entry_1.get():
                self.listbox.insert(END,str(i[0])+" "+self.entry_1.get()+" "+self.entry_3.get())
        self.entry_1.delete(0,END)
        self.entry_2.delete(0,END)
        self.entry_3.delete(0,END)
        self.entry_4.delete(0,END)
        self.entry_5.delete("1.0","end")
        

        self.conn.commit()
        self.conn.close()
    def update(self):
        
        self.conn=sqlite3.connect("contact_book.db")
        self.c=self.conn.cursor()
        self.c.execute("""UPDATE contact SET
                First_name = :First_name,
                Last_name=:Last_name,
                Pho_no=:Pho_no,
                Email=:Email,
                Address=:Address
                WHERE oid=:oid 
                """,
                {
                    "First_name":self.entry_1.get(),
                    "Last_name":self.entry_2.get(),
                    "Pho_no":self.entry_3.get(),
                    "Email":self.entry_4.get(),
                    "Address":self.entry_5.get("1.0","end"),
                    "oid":self.listbox.get(ANCHOR)[0]
                })
        
        self.entry_1.delete(0,END)
        self.entry_2.delete(0,END)
        self.entry_3.delete(0,END)
        self.entry_4.delete(0,END)
        self.entry_5.delete("1.0","end")
        
        self.conn.commit()
        self.conn.close()
        
        self.popup()
    def popup(self):
        messagebox.showinfo("Info","Successsfully Updated")
    def show_data(self):
        self.conn=sqlite3.connect("contact_book.db")
        self.c=self.conn.cursor()
        datas=self.c.execute("SELECT oid,* FROM contact")
        for i in datas:
            if str(i[0])==str(self.listbox.get(ANCHOR)[0]):
                messagebox.showinfo("Info","First name: "+i[1]+"\n"+"Last_name: "+i[2]+"\n"+"Phone_no: "+str(i[3])+"\n"+"Email:"+i[4]+"\n"+"Address: "+i[5])
            

        self.conn.commit()
        self.conn.close()
    def delete(self):
        self.entry_1.delete(0,END)
        self.entry_2.delete(0,END)
        self.entry_3.delete(0,END)
        self.entry_4.delete(0,END)
        self.entry_5.delete("1.0","end")
                
        self.conn=sqlite3.connect("contact_book.db")
        self.c=self.conn.cursor()
        contacts=self.listbox.get(ANCHOR)[0]
        self.c.execute("DELETE FROM contact WHERE oid="+contacts)

        self.conn.commit()
        self.conn.close()
        self.listbox.delete(ANCHOR)
    def select_record(self,e):
        self.update.config(state=NORMAL)
        self.show_data.config(state=NORMAL)
        self.detele.config(state=NORMAL)

        self.entry_1.delete(0,END)
        self.entry_2.delete(0,END)
        self.entry_3.delete(0,END)
        self.entry_4.delete(0,END)
        self.entry_5.delete("1.0","end")
        
        self.conn=sqlite3.connect("contact_book.db")
        self.c=self.conn.cursor()
        self.c.execute("select oid,* from contact")
        datas=self.c.fetchall()
        for i in datas:
            if str(i[0])==str(self.listbox.get(ANCHOR)[0]):
                self.entry_1.insert(0,i[1])
                self.entry_2.insert(0,i[2])
                self.entry_3.insert(0,i[3])
                self.entry_4.insert(0,i[4])
                self.entry_5.insert("1.0",i[5])
                


        self.conn.commit()
        self.conn.close()
if __name__=="__main__":
    contact_book()

