import tkinter as tk
from tkinter import messagebox
import sys
from time import sleep
import tkinter.ttk as ttk

class DummyApp(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        master.title("No application registered.")

        btn = tk.Button(master=self,
                text="Back",
                width=5,
                bg = "#00a4e4",
                fg = "#ffffff",
                command=self.master.backToStart)
        btn.pack(anchor=tk.NW)

        lbl = tk.Label(self, text="No application registered here.", height=5, font=("Migu 1M",20))
        lbl.pack()

class AllDeleteApp():
    def __init__(self, master=None, oldmaster=None):
        #tk.Frame.__init__(self, master, oldmaster)
        info_m = messagebox.askyesno('確認', 'すべての商品を削除しますか？')
        if info_m == True:
            info_del = messagebox.showinfo('確認', 'すべての商品を削除しました！！')
            #print(info_del)
            #self.pack_foget()
            #self.master.destroy()
            oldmaster.backToStart()
            oldmaster.pack_foget()
            #master.pack_forget()
            #print('forgot')
            #master.frame = StartPage
            #print('makeFrame')
            #master.frame.pack(expand=True, fill="both")
            #FrameBase.frame.backToStart()
            #print(info_del)
            #self.master.backToStart()#StartPageへ戻る
            #sys.exit()
        else:
            oldmaster.change()

class GoToPay:
    def __init__(self, oldmaster=None, total_price=None):
        msg = messagebox.askokcancel('確認', 'お会計でよろしいでしょうか？')
        if msg ==True:
            msg = messagebox.askokcancel('確認', 'お会計は  {}  でございます。'.format(total_price))
            if msg ==True:
                oldmaster.backToStart()
                oldmaster.pack_foget()
            else:
                oldmaster.change()
        else:
            oldmaster.change()

class SelectDeleteApp:
    def __init__(self,master=None, total_price=None,purchase_history=None,purchase_data=None):
        """一部商品を取り消す"""
        self.window = tk.Tk()
        self.window.title("Select Delete App")
        #self.window.geometry("400x400")
        self.total_price = total_price#買い物かご内の現在の合計金額
        self.purchase_history = purchase_history#現在の買い物かごの内のリスト
        #print('now purchase_history',purchase_history)
        self.spinboxes = []#spinboxの押された情報を入れるリスト
        self.spinbox_values = []
        self.price_list = []#購入されている商品の単価を入れるリスト
        tk.Label(self.window,text='No',font=("Migu 1M",16)).grid(row=0,column=0)
        tk.Label(self.window,text='商品名',font=("Migu 1M",16)).grid(row=0,column=1)
        tk.Label(self.window,text='単価（円）',font=("Migu 1M",16)).grid(row=0,column=2)
        tk.Label(self.window,text='数量（本）',font=("Migu 1M",16)).grid(row=0,column=3)
        tk.Label(self.window,text='金額（円）',font=("Migu 1M",16)).grid(row=0,column=4)
        self.total_price_lbl = tk.Label(self.window,text='合計金額'+str(total_price)+'円',font=("Migu 1M",16))#合計金額ラベル
        self.total_price_lbl.grid(row=5,column=4,sticky=tk.EW)

        for i in range(len(purchase_history)+1):
            idx = purchase_history[i][1][0]#predictラベルを取得
            price = purchase_data[idx][2][0]#商品単価
            self.price_list.append(price)
            lbl1 = tk.Label(self.window,text=purchase_history[i][0][0],font=("Migu 1M",16)).grid(row=1+i,column=0)#No.
            lbl2 = tk.Label(self.window,text=purchase_data[idx][1][0],font=("Migu 1M",16)).grid(row=1+i,column=1)#商品名
            lbl3 = tk.Label(self.window,text=price,font=("Migu 1M",16)).grid(row=1+i,column=2)#単価
            '''
            購入数変更spinboxの配置（押されたら変わる）
            １．spinboxはvaluesで指定した間の値に変更，２．from_=,to=で指定した間の値に変更することができる．
            ただし，fromよりtoの値を小さく設定できない
            現状，↑ボタンを押すことで購入数を減らすプログラムになっている．いい案があれば，どなたかお教えいただきたい
            '''
            val = sorted(tuple(a for a in range(purchase_history[i][2][0]+1)),reverse=True)
            #val = tuple(a for a in range(purchase_history[i][2][0]+1))
            sv = tk.StringVar()
            sp = tk.Spinbox(self.window,values=val,textvariable=sv,
                command=lambda sp_idx=i:self.update_value(sp_idx),font=("Migu 1M",16))
            #val = [a for a in range(purchase_history[i][2][0]+1)]
            #sp = tk.Spinbox(self.window,from_=val[0], to=val[-1],
            #    textvariable=sv,command=lambda sp_idx=i:self.update_value(sp_idx),font=("Migu 1M",16))
            sp.grid(row=1+i, column=3,sticky=tk.EW)
            self.spinbox_values.append(sv)
            self.spinboxes.append(sp)

            val = [a for a in range(purchase_history[i][2][0]+1)]
            sp = tk.Spinbox(self.window,from_ = val[0], to = val[-1],
                increment = val[-1],command=lambda sp_idx=i:self.update_value(sp_idx),font=("Migu 1M",16))

            '''金額ラベル（spinbox内の情報で変わる）'''
            self.price_lbl = tk.Label(self.window,text=purchase_history[i][2][0]*price,font=("Migu 1M",16))
            self.price_lbl.grid(row=1+i,column=4,sticky=tk.EW)

            self.window.rowconfigure(i,weight=1)
            for c in range(4):
                self.window.columnconfigure(c,weight=1)

    def update_value(self,sp_idx):
        '''spinboxを押されたら行うcommand'''
        #print("Update spinbox {}".format(sp_idx))
        num_of_purchase = [int(s.get()) for s in self.spinboxes]#初期の購入個数
        #print('num_of_purchase',num_of_purchase)
        sub_total = [n*p for n,p in zip(num_of_purchase, self.price_list)]#商品ごとの合計金額．
        #print('sub_total',sub_total)
        '''合計金額ラベルの更新'''
        self.total_price = sum(sub_total)#total_price(合計金額）の更新
        self.total_price_lbl = tk.Label(self.window,text='合計金額'+str(self.total_price)+'円',font=("Migu 1M",16))
        self.total_price_lbl.grid(row=5,column=4,sticky=tk.EW)
        '''金額ラベルの更新'''
        for i in range(len(sub_total)):
            self.purchase_history[i][2][0] = sub_total[i]#purchase_historyリストの更新
            #print('new purchase_history',self.purchase_history)
            self.price_lbl = tk.Label(self.window,text=sub_total[i],font=("Migu 1M",16))
            self.price_lbl.grid(row=1+i,column=4,sticky=tk.EW)
            self.window.rowconfigure(i,weight=1)
            for c in range(4):
                self.window.columnconfigure(c,weight=1)

class SelectDeleteApp:
    def __init__(self,master=None,total_price=None,purchase_history=None,purchase_data=None):
        """一部商品を取り消す"""
        self.window = tk.Tk()
        self.window.title("Select Delete App")
        #self.window.geometry("400x400")
        self.master = master
        self.total_price = total_price#買い物かご内の現在の合計金額
        self.purchase_history = purchase_history#現在の買い物かごの内のリスト
        #print('now purchase_history',purchase_history)
        self.spinboxes = []#spinboxの押された情報を入れるリスト
        self.spinbox_values = []
        self.price_list = []#購入されている商品の単価を入れるリスト
        tk.Label(self.window,text='No',font=("Migu 1M",16)).grid(row=0,column=0)
        tk.Label(self.window,text='商品名',font=("Migu 1M",16)).grid(row=0,column=1)
        tk.Label(self.window,text='単価（円）',font=("Migu 1M",16)).grid(row=0,column=2)
        tk.Label(self.window,text='数量（本）',font=("Migu 1M",16)).grid(row=0,column=3)
        tk.Label(self.window,text='金額（円）',font=("Migu 1M",16)).grid(row=0,column=4)
        self.total_price_lbl = tk.Label(self.window,text='合計金額'+str(total_price)+'円',font=("Migu 1M",16))#合計金額ラベル
        self.total_price_lbl.grid(row=5,column=4,sticky=tk.EW)

        for i in range(len(purchase_history)+1):
            idx = purchase_history[i][1][0]#predictラベルを取得
            price = purchase_data[idx][2][0]#商品単価
            self.price_list.append(price)
            lbl1 = tk.Label(self.window,text=purchase_history[i][0][0],font=("Migu 1M",16)).grid(row=1+i,column=0)#No.
            lbl2 = tk.Label(self.window,text=purchase_data[idx][1][0],font=("Migu 1M",16)).grid(row=1+i,column=1)#商品名
            lbl3 = tk.Label(self.window,text=price,font=("Migu 1M",16)).grid(row=1+i,column=2)#単価
            '''購入数変更spinboxの配置（押されたら変わる）
            １．spinboxはvaluesで指定した間の値に変更，２．from_=,to=で指定した間の値に変更することができる．ただし，fromよりtoの値を小さく設定できない
            現状，↑ボタンを押すことで購入数を減らすプログラムになっている．いい案があれば，どなたかお教えいただきたい'''
            val = sorted(tuple(a for a in range(purchase_history[i][2][0]+1)),reverse=True)
            #val = tuple(a for a in range(purchase_history[i][2][0]+1))
            sv = tk.StringVar()
            sp = tk.Spinbox(self.window,values=val,textvariable=sv, command=lambda sp_idx=i:self.update_value(sp_idx),font=("Migu 1M",16))
            #val = [a for a in range(purchase_history[i][2][0]+1)]
            #sp = tk.Spinbox(self.window,from_=val[0], to=val[-1],textvariable=sv,command=lambda sp_idx=i:self.update_value(sp_idx),font=("Migu 1M",16))
            sp.grid(row=1+i, column=3,sticky=tk.EW)
            self.spinbox_values.append(sv)
            self.spinboxes.append(sp)

            val = [a for a in range(purchase_history[i][2][0]+1)]
            sp = tk.Spinbox(self.window,from_ = val[0], to = val[-1], increment = val[-1],command=lambda sp_idx=i:self.update_value(sp_idx),font=("Migu 1M",16))

            '''金額ラベル（spinbox内の情報で変わる）'''
            self.price_lbl = tk.Label(self.window,text=purchase_history[i][2][0]*price,font=("Migu 1M",16))
            self.price_lbl.grid(row=1+i,column=4,sticky=tk.EW)

            self.window.rowconfigure(i,weight=1)
            for c in range(5):
                self.window.columnconfigure(c,weight=1)

    def update_value(self,sp_idx):
        '''spinboxを押されたら行うcommand'''
        #print("Update spinbox {}".format(sp_idx))
        num_of_purchase = [int(s.get()) for s in self.spinboxes]#初期の購入個数
        #print('num_of_purchase',num_of_purchase)
        sub_total = [n*p for n,p in zip(num_of_purchase, self.price_list)]#商品ごとの合計金額．
        #print('sub_total',sub_total)
        '''合計金額ラベルの更新'''
        self.total_price = sum(sub_total)#total_price(合計金額）の更新
        self.total_price_lbl = tk.Label(self.window,text='合計金額'+str(self.total_price)+'円',font=("Migu 1M",16))
        self.total_price_lbl.grid(row=5,column=4,sticky=tk.EW)
        '''OKボタンの作成'''
        tk.Button(self.window, text='OK',bg="#dc143c",fg="#ffffff",command=self.info_message,font=("Migu 1M",16)).grid(row=4,column=5)

        '''金額ラベルの更新'''
        for i in range(len(sub_total)):
            self.purchase_history[i][2][0] = num_of_purchase[i]#purchase_historyリストの更新
            self.price_lbl = tk.Label(self.window,text=sub_total[i],font=("Migu 1M",16))
            self.price_lbl.grid(row=1+i,column=4,sticky=tk.EW)
            self.window.rowconfigure(i,weight=1)
            for c in range(5):
                self.window.columnconfigure(c,weight=1)

    def info_message(self):
        info_m = messagebox.askokcancel('確認', '選択した商品を削除してよろしいですか？', parent=self.window)
        if info_m == True:
            #num_list = [self.purchase_history[i][2][0] for i in range(len(self.purchase_history))]
            #print(num_list)
            """
            while 0 in num_list:
                idx = num_list.index(0)
                print(idx)
                #a.pop(idx)
                #self.master.purchase_history = self.purchase_history.pop(idx)
                self.purchase_history.pop(idx)
                num_list.pop(idx)
                """

            #print('new purchase_history',self.purchase_history)
            self.master.purchase_history = self.purchase_history
            self.master.total_price = self.total_price
            info_del = messagebox.showinfo('確認', '選択した商品を削除しました！')
            self.master.make_history(master=self.master)
            self.window.destroy()
        else:
            pass

'''
class ImgChange(tk.Frame):
    def __init__(self, master=None, **kwargs):
        self.img = tk.PhotoImage(file="./images.png")
        self.img_lbl = tk.Label(master=self, image=self.img)
        self.img_lbl.grid(column=0, row=3, columnspan=6, rowspan=30, padx=3, pady=3, sticky=tk.NSEW)
        self.scan_btn.configure(command=self.img_change2)

    def img_change1(self):
        self.img = tk.PhotoImage(file="./images.png")
        self.img_lbl = tk.Label(master=self, image=self.img)
        self.img_lbl.grid(column=0, row=3, columnspan=6, rowspan=30, padx=3, pady=3, sticky=tk.NSEW)
        self.scan_btn.configure(command=self.img_change2)


    def img_change2(self):
        self.img_lbl.grid_forget()
        #self.img2 = tk.PhotoImage(file="./images2.png")

        #self.img_lbl = tk.Label(master=self, image=self.img2)
        #self.img_lbl.grid(column=0, row=3, columnspan=6, rowspan=30, padx=3, pady=3, sticky=tk.NSEW)
        self.scan_btn.configure(command=self.img_change1)
'''
