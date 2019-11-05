import tkinter as tk
#from cleanup import CleanUpRoutine
from gsss_lib_03_03 import DummyApp
from gsss_lib_03_03 import AllDeleteApp
from gsss_lib_03_03 import GoToPay
from gsss_lib_03_03 import SelectDeleteApp
from tkinter import messagebox
import datetime
import sys
from PIL import Image
from time import sleep
from M_system_3 import M2model

from keras.models import load_model
import pickle

#import picamera
from time import sleep
import numpy as np
from keras.preprocessing.image import img_to_array
import random

        #######################
###     Japanese    ###
#######################
applist_ja = {"scan": "次の商品を\nスキャンする",
              "cancel": "取り消す商品を\n選択する",
              "empty": "買い物かごの\n商品を全て削除",
              "pay": "お会計に進む"
              }
items_ja = {"water": "いろはす",
            "tea": "お～いお茶",
            "cola": "コカコーラ",
            "orjuice": "理想のオレンジ",
            "cola0": "コカコーラZERO"
            }
columns_ja = {"no": 'No.',
              "name": '商品名',
              "uprice": '単価(円)',
              "quantity": '数量(本)',
              "price": '金額(円)'
              }
labels_ja = {"title": "無人レジシステム GSSS",
             "msg": "購入する商品を\n置いてください"
             }
confirm_ja = {"confirm": "確認"}
messages_ja = {"unknown": "登録されていない商品です。登録済みの商品を置いてください",
               "confirm": "この商品でよろしいですか？",
               "retry": "もう一度購入したい商品を置いてください"
               }
total_ja = {"total":"合計金額"}

#######################
###     English     ###
#######################
applist_en = {"scan": "Scan",
              "cancel": "Select to cancel",
              "empty": "Empty shopping cart",
              "pay": "Payment"
              }
items_en = {"water": "irohasu",
            "tea": "Oi Ocha",
            "cola": "Coca Cola",
            "orjuice": "Dream Orange",
            "cola0": "Coca Cola ZERO"
            }
columns_en = {"no": 'No.',
              "name": 'Name',
              "uprice": 'Unit Price\n(YEN)',
              "quantity": 'Quantity',
              "price": 'Price\n(YEN)'
              }
labels_en = {"title": "Peopleless Register system GSSS",
             "msg": "Put item you want to buy on the table"
             }
confirm_en = {"confirm": "confirm"}
messages_en = {"unknown": "The item is not registered",
               "confirm": "This is O.K.?",
               "retry": "Retry put the item you want on the table"
               }
total_en = {"total":"total"}

#######################
###     French     ###
#######################
applist_fr = {"scan": "Scan",
              "cancel": "Sélectionnez pour annuler",
              "empty": "Panier vide",
              "pay": "Paiement"
              }
items_fr = {"water": "irohasu",
            "tea": "Oi Ocha",
            "cola": "Coca Cola",
            "orjuice": "Rêve Orange",
            "cola0": "Coca Cola ZERO"
            }
columns_fr = {"no": 'No.',
              "name": 'Nom',
              "uprice": 'Prix ​​unitaire\n(YEN)',
              "quantity": 'Quantité',
              "price": 'Montant\n(YEN)'
              }
labels_fr = {"title": "Peopleless Register system GSSS",
             "msg": "Put item you want to buy on the table"
             }
confirm_fr = {"confirm": "confirm"}
messages_fr = {"unknown": "L'article n'est pas enregistré",
               "confirm": "C'est acceptable.?",
               "retry": "Réessayez de mettre l'article que vous voulez sur la table"
               }
total_fr = {"total":"total"}

# Set language list

ja_list = {"applist": applist_ja,
           "items": items_ja,
           "columns": columns_ja,
           "labels": labels_ja,
           "confirm": confirm_ja,
           "message": messages_ja,
           "total":total_ja
           }

en_list = {"applist": applist_en,
           "items": items_en,
           "columns": columns_en,
           "labels": labels_en,
           "confirm": confirm_en,
           "message": messages_en,
           "total":total_en
           }

fr_list = {"applist": applist_fr,
           "items": items_fr,
           "columns": columns_fr,
           "labels": labels_fr,
           "confirm": confirm_fr,
           "message": messages_fr,
           "total":total_fr
           }

# Make language set

lans = {
    "ja": ja_list,
    "en": en_list,
    "fr": fr_list
}

lan = 'ja'

class RootMaster(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        ww=self.winfo_screenwidth()
        wh=self.winfo_screenheight()
        self.geometry(str(int(ww*0.9))+'x'+str(int(wh*0.9)))
        self.model = M2model()
        self.geometry("800x480")
        self.frame = StartMenu(self, model=self.model)
        self.frame.pack(expand=True, fill="both")
        #self.attributes("-fullscreen", True)

        order = 1

    def change(self, frame):
        self.frame.pack_forget() # delete currrent frame
        self.frame = frame(self, model=self.model)
        self.frame.pack(expand=True, fill="both") # make new frame

    def backToStart(self):
        self.frame.pack_forget()
        self.frame = StartMenu(self, model=self.model)
        self.frame.pack(expand=True, fill="both")

class StartMenu(tk.Frame):
    def __init__(self, master=None, model=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        ja = ['いらっしゃいませ', 'レジに進む']
        en = ['Please Click or Press key below', 'Go to Start']
        fr = []
        lan_list =[ja, en, fr]
        lan = lan_list[0]
        frags = ['./ja.png', './en.png', './fr.png']

        master.title("Start Display")
        self.grid(column=0, row=0, sticky=tk.NSEW)
        self.model = model
        self.Applist = [MainMenu, lan[1]]

        #wc_path = ['./wc_ja.png']
        #self.wcs = []
        #for wc in wc_path:
        #    self.wcs.append(tk.PhotoImage(file=wc))

        lbl = tk.Label(master=self, text =lan[0], font=("Migu 1M",30))
        lbl.grid(column=0,row=0,sticky=tk.N, pady=100)
        btn = tk.Button(
            master = self,
            text="Close",
            width = 5,
            bg = "#dc143c",
            fg = "#ffffff",
            command=self.master.destroy)
        btn.grid(column=2, row=0,sticky=tk.NE)

        start_btn = tk.Button(
            master=self,
            wraplength=200,
            justify=tk.LEFT,
            text=self.Applist[1],
            font=("Migu 1M", 30),
            bg="#e6e6fa",
            command=self.gotoApp(0))
        start_btn.grid(column=0, row=0, padx=200, pady=200, sticky=tk.NSEW)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def gotoApp(self,n):
        return lambda :self.master.change(self.Applist[n])

class MainMenu(tk.Frame):
    def __init__(self, master=None, model=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        master.title("Start Page")

        self.grid(column=0, row=0, sticky=tk.NSEW)
        self.model = model


        #print("test 1: {}".format(languages['en']["columns"]["uprice"]))

        self.lan_list = ['fr', 'en', 'ja']
        #self.lan = self.language()


        self.fs = [30, 20, 15] # フォントサイズ
        self.fd = ["Migu 1M"] # フォントデザイン
        #app_list_lan_en = ["Scan Item", "Select cancel item", "All items cancel", "Finish and Pay"]
        #app_list_lan_fr = []
        #app_list_lan_jp = [lans[lan]["applist"]["scan"], "取り消す商品を\n選択する", "買い物かごの\n商品を全て削除", "お会計に進む"]

        self.Applist = [[self.img_change1, lans[lan]['applist']['scan']], [SelectDeleteApp, lans[lan]['applist']['cancel']],
                        [AllDeleteApp,lans[lan]['applist']['empty']], [GoToPay, lans[lan]['applist']['pay']]]
        self.Lanlist = [[self.change_to_fr, '  Francais'], [self.change_to_en, '  English'], [self.change_to_ja, '  日本語']]
        frag_path = ['./fr.png', './en.png', './ja.png']
        self.frags = []
        for frag in frag_path:
            self.frags.append(tk.PhotoImage(file=frag))

        #self.Ad = [DummyApp, 'Ad']
        ad_path = ['./DIC_logo.png', './DIC_logo.png']
        self.ads = []
        for ad in ad_path:
            self.ads.append(tk.PhotoImage(file=ad))

        self.pad = 3
        n_row = 0
        self.purchase_data = [[[1], [lans[lan]['items']['cola0']], [140]],
                              [[2], [lans[lan]['items']['cola']], [150]],
                              [[3], [lans[lan]['items']['tea']], [120]],
                              [[4], [lans[lan]['items']['water']], [100]],
                              [[5], [lans[lan]['items']['orjuice']], [210]]]
        self.list_columns = [lans[lan]['columns']['no'],
                             lans[lan]['columns']['name'],
                             lans[lan]['columns']['uprice'],
                             lans[lan]['columns']['quantity'],
                             lans[lan]['columns']['price']]
        self.list_colspan = [1, 2, 1, 1, 1]




        '''
        self.purchase_history = [[[1], [0], [1]],
                                 [[2], [1], [1]],
                                 [[3], [2], [3]],
                                 [[4], [3], [5]],
                                 [[5], [4], [2]]]
        '''
        self.purchase_history = []
        self.n_history = 0

        btn = tk.Button(
            master = self,
            text="Close",
            width = 5,
            bg = "#dc143c",
            fg = "#ffffff",
            command=self.master.destroy)
        btn.grid(column=11, row=0,sticky=tk.NE)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        time_lbl = tk.Label(master=self, text =current_time, font=(self.fd[0],self.fs[2]))
        time_lbl.grid(column=10, row=1, columnspan=2, padx=self.pad, pady=self.pad, sticky=tk.E+tk.N+tk.S)

        lbl = tk.Label(master=self, text ="Self Register System  GSSS", font=(self.fd[0],self.fs[0]))
        lbl.grid(column=0, row=2, columnspan=6, rowspan=1, padx=self.pad, pady=self.pad, sticky=tk.NSEW)
        '''
        self.btn_test = tk.Button(master=self, command=self.change_num1)
        test_lbl = tk.Label(master=self.btn_test, image=self.frags[0])
        test_lbl.grid(column=4, row=2, sticky=tk.NSEW)
        test_lbl2 = tk.Label(master=self.btn_test, text='日本語')
        test_lbl2.grid(column=5, row=2, sticky=tk.NSEW)
        self.btn_test.grid(column=4, row=2, columnspan=2, sticky=tk.NSEW)
        self.btn_test.columnconfigure(4, weight=1)
        self.btn_test.columnconfigure(5, weight=1)
        '''
        for c in range(3):
            self.lan_btn = tk.Button(
                    master=self,
                    wraplength=150,
                    justify=tk.LEFT,
                    bg="#e6e6fa",
                    text=self.Lanlist[c][1],
                    image=self.frags[c],
                    font=(self.fd[0],self.fs[2]),
                    compound='left',
                    command=self.Lanlist[c][0])

            #self.lan_img = tk.Label(master=self.lan_btn, image=self.frags[c])
            #self.lan_img.grid(column=c*2+6, row=2, sticky=tk.NSEW)
            #self.lan_txt = tk.Label(master=self.lan_btn, text=self.Lanlist[c][1], font=(self.fd[0],self.fs[2]))
            #self.lan_txt.grid(column=c*2+7, row=2, sticky=tk.NSEW)
            self.lan_btn.grid(column=c*2+6, row=2, columnspan=2, rowspan=1, padx=self.pad, pady=self.pad, sticky=tk.NSEW)
            #self.lan_btn.columnconfigure(c*2+6, weight=1)
            #self.lan_btn.columnconfigure(c*2+7, weight=1)
            #self.lan_btn.rowconfigure(2, weight=1)

        self.img_frame = tk.Frame(master=self, bg='blue', relief='ridge', borderwidth=10)
        self.img_frame.grid(column=0, row=3, columnspan=6, rowspan=28, padx=self.pad, pady=self.pad, sticky=tk.NSEW)
        self.img_frame.columnconfigure(0, weight=1)
        self.img_frame.rowconfigure(0, weight=1)

        #img_lbl = tk.Label(master=img_frame, text=lans[lan]['labels']['msg'], font=(self.fd[0],self.fs[0]))
        #img_lbl.grid(column=0, row=3, columnspan=6, rowspan=28, padx=self.pad, pady=self.pad, sticky=tk.NSEW)
        self.make_word()

        self.list_frame = tk.Frame(master=self, bg='green')
        self.list_frame.grid(column=6, row=3, columnspan=6, rowspan=28, padx=self.pad, pady=self.pad, sticky=tk.NSEW)
        #self.list_frame.columnconfigure(0, weight=1)
        #self.list_frame.rowconfigure(0, weight=1)

        c_span = 0
        r_span = 4

        self.make_history(master=self)

        self.word_lbl = tk.Label(master=self, text ='', font=(self.fd[0],self.fs[0]), relief='ridge')
        self.word_lbl.grid(column=0, row=31, columnspan=6, rowspan=2, padx=self.pad, pady=self.pad, sticky=tk.NSEW)
        '''
        for c in range(2):
            btn = tk.Button(
                    master=self,
                    wraplength=150,
                    justify=tk.LEFT,
                    text=self.Ad[1],
                    font=(self.fd[0],self.fs[2]),
                    bg="#e6e6fa",
                    command=self.gotoadApp(c))
            btn.grid(column=c*3+6, row=33, columnspan=3, rowspan=2, padx=self.pad, pady=self.pad, sticky=tk.NSEW)
        '''
        for c in range(2):
            lbl = tk.Label(master=self, image=self.ads[c])
            lbl.grid(column=c*3+6, row=31, columnspan=3, rowspan=2, padx=self.pad, pady=self.pad, sticky=tk.NSEW)
        '''
        self.scan_btn = tk.Button(master=self, wraplength=150, justify=tk.LEFT,
                                  text=self.Applist[0][1], font=(self.fd[0],self.fs[2]), bg="#e6e6fa", command=self.img_change1)
        self.scan_btn.grid(column=0, row=33, columnspan=3, rowspan=2, padx=self.pad, pady=self.pad, sticky=tk.NSEW)

        for c in range(1, 4):
            if c==0:
                btn = tk.Button(
                        master=self,
                        wraplength=150,
                        justify=tk.LEFT,
                        text=self.Applist[c][1],
                        font=(self.fd[0],self.fs[2]),
                        bg="#e6e6fa",
                        command=self.gotoApp(c))
                btn.grid(column=c*3, row=33, columnspan=3, rowspan=2, padx=self.pad, pady=self.pad, sticky=tk.NSEW)

            else:
                btn = tk.Button(
                        master=self,
                        wraplength=150,
                        justify=tk.LEFT,
                        text=self.Applist[c][1],
                        font=(self.fd[0],self.fs[2]),
                        bg="#e6e6fa",
                        command=self.gotoApp(c))
                btn.grid(column=c*3, row=33, columnspan=3, rowspan=2, padx=self.pad, pady=self.pad, sticky=tk.NSEW)
        '''
        self.make_button()
        max_col = 12
        max_row = 34
        for c in range(max_col):
            self.columnconfigure(c, weight=1, uniform='group1')

        for r in range(max_row):
            self.rowconfigure(r, weight=1)

        #self.master.columnconfigure(0, weight=1)
        #self.master.rowconfigure(0, weight=1)

    def gotoApp(self,c):
        if c==2:
            return lambda :self.master.change(self.Applist[c][0](master=self, oldmaster=self.master))
        elif c==3:
            return lambda :self.master.change(self.Applist[c][0](oldmaster=self.master, total_price=self.total_price))

        elif c==1:
            return lambda :self.master.change(self.Applist[c][0](master=self, total_price=self.total_price,
            purchase_history=self.purchase_history,purchase_data=self.purchase_data))

        else:
            return lambda :self.master.change(self.Applist[c][0])

    #def gotolanApp(self,c):
    #    return lambda :self.master.change(self.Lanlist[c][0])#(lan=self.lan))

    def gotoadApp(self,c):
        return lambda :self.master.change(self.Ad[0])

    def change_to_ja(self):
        lan = 'ja'
        #self.lan = self.language(lan)
        self.make_history()
        self.make_button()

    def change_to_en(self):
        lan = 'en'
        #self.lan = self.language(lan)
        self.make_history()
        self.make_button()

    def change_to_fr(self):
        lan = 'fr'
        #self.lan = self.language(lan)
        self.make_history()
        self.make_button()

    def language(self, lan='en'):
        self.lan = lan
        return self.lan

    def make_word(self):
        img_lbl = tk.Label(master=self.img_frame, text=lans[lan]['labels']['msg'], font=(self.fd[0],self.fs[0]))
        img_lbl.grid(column=0, row=3, columnspan=6, rowspan=28, padx=self.pad, pady=self.pad, sticky=tk.NSEW)

    def make_button(self):
        #self.lan = lan
        #self.lan = self.language(self.lan)
        self.Applist = [[self.img_change1, lans[lan]['applist']['scan']], [SelectDeleteApp, lans[lan]['applist']['cancel']],
                        [AllDeleteApp,lans[lan]['applist']['empty']], [GoToPay, lans[lan]['applist']['pay']]]
        self.scan_btn = tk.Button(master=self, wraplength=150, justify=tk.LEFT,
                                  text=self.Applist[0][1], font=(self.fd[0],self.fs[2]), bg="#e6e6fa", command=self.img_change1)
        self.scan_btn.grid(column=0, row=33, columnspan=3, rowspan=2, padx=self.pad, pady=self.pad, sticky=tk.NSEW)

        for c in range(1, 4):
            if c==0:
                btn = tk.Button(
                        master=self,
                        wraplength=150,
                        justify=tk.LEFT,
                        text=self.Applist[c][1],
                        font=(self.fd[0],self.fs[2]),
                        bg="#e6e6fa",
                        command=self.gotoApp(c))
                btn.grid(column=c*3, row=33, columnspan=3, rowspan=2, padx=self.pad, pady=self.pad, sticky=tk.NSEW)

            else:
                btn = tk.Button(
                        master=self,
                        wraplength=150,
                        justify=tk.LEFT,
                        text=self.Applist[c][1],
                        font=(self.fd[0],self.fs[2]),
                        bg="#e6e6fa",
                        command=self.gotoApp(c))
                btn.grid(column=c*3, row=33, columnspan=3, rowspan=2, padx=self.pad, pady=self.pad, sticky=tk.NSEW)
        #self.master.change(self)

    def img_change1(self):
        '''
        #画像を撮影して，保存する関数
        photo_filename = './photoFile/data.png'
        photofile = open(photo_filename, 'wb')#撮影した画像を書き込み用でopen
        #print(photofile)
        # pi camera 用のライブラリーを使用して、画像を取得
        with picamera.PiCamera() as camera:
            #camera.resolution = (640,480)
            camera.resolution = (300,400)#画像の解像度（適宜変更）
            camera.start_preview()#撮影した画像のプレビュー開始
            sleep(1)#撮影した画像のプレビューを表示する時間（画像をキャプチャするにはsleepが少なくとも2秒は必要）
            camera.capture(photofile)#photofileに撮影した画像を保存
            camera.stop_preview()#公式サイトにはプレビューの後はstopが入ってた．入れる？入れない？試してみる
            #self.img = Image.open(open('./photoFile/data.jpg'))
            #self.img = tk.PhotoImage(file=self.img)
        #self.img = ImageTk.PhotoImage(self.img)
        self.img = tk.PhotoImage(file='./photoFile/data.png')

        pred = self.model.predict(path='./photoFile/data.png')

        self.make_word()
        #self.img_lbl = tk.Label(master=self, image=self.img)
        #self.img_lbl.grid(column=0, row=3, columnspan=6, rowspan=30, padx=3, pady=3, sticky=tk.NSEW)
        #self.Applist[0][0] = self.img_change2
        #self.scan_btn.configure(command=self.img_change2)


        #self.img_lbl.grid_forget()
        #self.img = tk.PhotoImage(file="./images.png")
        '''
        #self.img_lbl = tk.Label(master=self, image=self.img)
        #self.img_lbl.grid(column=0, row=3, columnspan=6, rowspan=30, padx=3, pady=3, sticky=tk.NSEW)

        pred_list = [0, 1, 2, 3, 4, 5]
        pred = random.randint(0, pred_list[-1])

        if pred==0:
            info_msg = messagebox.showinfo('確認', '登録されていない商品です。登録済みの商品を置いてください')
            #self.master.change()
        else:
            pred_name = self.purchase_data[pred-1][1][0]
            pred_price = self.purchase_data[pred-1][2][0]
            self.word_lbl.configure(text='{} : {}'.format(pred_name, pred_price))
            info_msg = messagebox.askyesno('確認', '商品は {} でよろしいですか？'.format(pred_name))
            if info_msg == False:
                info_msg = messagebox.showinfo('確認', 'もう一度購入したい商品を置いてください')

            else:
                if len(self.purchase_history) ==0:
                    self.purchase_history.append([[1], [pred], [1]])
                else:
                    idx_list = [self.purchase_history[i][1][0] for i in range(len(self.purchase_history))]
                    if pred in idx_list:
                        self.purchase_history[idx_list.index(pred)][2][0] += 1

                    else:
                        self.purchase_history.append([[self.purchase_history[-1][0][0]+1], [pred], [1]])
                self.make_history(master=self)

    def img_change2(self):
        self.img_lbl.grid_forget()
        self.scan_btn.configure(command=self.img_change1)

    def make_history(self, master=None):
        self.purchase_data = [[[1], [lans[lan]['items']['cola0']], [140]],
                              [[2], [lans[lan]['items']['cola']], [150]],
                              [[3], [lans[lan]['items']['tea']], [120]],
                              [[4], [lans[lan]['items']['water']], [100]],
                              [[5], [lans[lan]['items']['orjuice']], [210]]]

        self.list_columns = [lans[lan]['columns']['no'],
                             lans[lan]['columns']['name'],
                             lans[lan]['columns']['uprice'],
                             lans[lan]['columns']['quantity'],
                             lans[lan]['columns']['price']]

        self.total_txt = lans[lan]['total']['total']

        fs = [30, 20, 15] # フォントサイズ
        fd = ["Migu 1M"] # フォントデザイン

        #pad=0
        r_span = 4
        c_span = 0
        self.total_price = 0

        for c in range(len(self.list_columns)):
            lbl_name = tk.Label(master=self, text=str(self.list_columns[c]), font=(self.fd[0],self.fs[2]))
            lbl_name.grid(column=6+c_span, row=3, columnspan=self.list_colspan[c], rowspan=r_span,
             padx=self.pad, pady=self.pad, sticky=tk.NSEW)
            c_span += self.list_colspan[c]

        c_span = 0
        r_span = 4

        if len(self.purchase_history)==0:
            pass
        else:
            for r in range(len(self.purchase_history)):
                lbl0 = tk.Label(master=master, text=self.purchase_history[r][0][0], font=(self.fd[0],self.fs[2]))
                lbl0.grid(column=6+c_span, row=7+r*r_span, columnspan=self.list_colspan[0], rowspan=r_span,
                          padx=self.pad, pady=self.pad, sticky=tk.NSEW)
                c_span += self.list_colspan[0]
                lbl1 = tk.Label(master=master, text=self.purchase_data[self.purchase_history[r][1][0]-1][1][0], font=(self.fd[0],self.fs[2]))
                lbl1.grid(column=6+c_span, row=7+r*r_span, columnspan=self.list_colspan[1], rowspan=r_span,
                          padx=self.pad, pady=self.pad, sticky=tk.NSEW)
                c_span += self.list_colspan[1]
                lbl2 = tk.Label(master=master, text=self.purchase_data[self.purchase_history[r][1][0]-1][2][0], font=(self.fd[0],self.fs[2]))
                lbl2.grid(column=6+c_span, row=7+r*r_span, columnspan=self.list_colspan[2], rowspan=r_span,
                          padx=self.pad, pady=self.pad, sticky=tk.NSEW)
                c_span += self.list_colspan[2]
                lbl3 = tk.Label(master=master, text=self.purchase_history[r][2][0], font=(self.fd[0],self.fs[2]))
                lbl3.grid(column=6+c_span, row=7+r*r_span, columnspan=self.list_colspan[3], rowspan=r_span,
                          padx=self.pad, pady=self.pad, sticky=tk.NSEW)
                c_span += self.list_colspan[3]
                sigma = self.purchase_data[self.purchase_history[r][1][0]-1][2][0]*self.purchase_history[r][2][0]
                lbl4 = tk.Label(master=master, text=sigma, font=(self.fd[0],self.fs[2]))
                lbl4.grid(column=6+c_span, row=7+r*r_span, columnspan=self.list_colspan[4], rowspan=r_span,
                          padx=self.pad, pady=self.pad, sticky=tk.NSEW)
                c_span =0
                self.total_price += sigma

        total_lbl = tk.Label(master=master, text=lans[lan]["total"]["total"], font=(self.fd[0],self.fs[2]))
        total_lbl.grid(column=10, row=27, columnspan=1, rowspan=4, padx=self.pad, pady=self.pad, sticky=tk.NSEW)

        total_price_lbl = tk.Label(master=master, text=self.total_price, font=(self.fd[0],self.fs[2]))
        total_price_lbl.grid(column=11, row=27, columnspan=1, rowspan=4, padx=self.pad, pady=self.pad, sticky=tk.NSEW)

    def change_num1(self):
        self.purchase_history[0][2][0] = 9
        self.btn_test.configure(command=self.change_num2)
        max_col = 12
        max_row = 35
        for c in range(max_col):
            self.columnconfigure(c, weight=1)

        for r in range(max_row):
            self.rowconfigure(r, weight=1)

    def change_num2(self):
        self.purchase_history[0][2][0] = 0
        self.btn_test.configure(command=self.change_num1)
        max_col = 12
        max_row = 35
        for c in range(max_col):
            self.columnconfigure(c, weight=1)

        for r in range(max_row):
            self.rowconfigure(r, weight=1)

if __name__=="__main__":
    app=RootMaster()
    app.mainloop()
