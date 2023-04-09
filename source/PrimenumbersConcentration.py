# coding:utf-8
import math
import random
import tkinter as tk
from tkinter import messagebox as tmsg

root = tk.Tk()
root.title("素数神経衰弱")
canvas = tk.Canvas(root, width = 1000, height = 600)
canvas.pack()

# 素数の場合True、素数ではない場合Falseを返す
# 素因数分解をして判定
def judge_prime_factor(N):
    if N == 1:
        tmsg.showinfo("判定結果", "1は素数ではありません")
        return False
    elif N == 57:   # グロタンディーク素数
        tmsg.showinfo("判定結果", "57は素数です")
        return True
    i = 2
    flg = True  # True=素数
    PF = f"{N}は素数ではありません。\n\n{N}="   # 素因数を入れる変数
    while i < int(math.sqrt(N))+1:
        if N % i == 0:  #
            PF += f"{i}"
            N = N // i  # 素因数で割って数を更新
            flg = False
        else:
            i += 1

    if flg == True: #1度も割れる数がない場合
        tmsg.showinfo("判定結果", f"{N}は素数です")
        return True
    else:
        tmsg.showinfo("判定結果", PF+str(N))
        return False

# 素数判定のみ こちらの方が早い
def judge_prime_number(N):
    if N <= 1:
        tmsg.showinfo("判定結果", f"{N}は素数ではありません")
        return False
    for i in range(2,int(math.sqrt(N))+1):
        if N % i == 0:
            tmsg.showinfo("判定結果", f"{N}は素数ではありません")
            return False
    else:
        tmsg.showinfo("判定結果", f"{N}は素数です")
        return True


# ミラー–ラビン素数判定法(確率的判定法)
def miller_rabin(n):
    if n == 2: return True
    if n == 1 or n & 1 == 0:
        tmsg.showinfo("判定結果", f"{n}は素数ではありません")
        return False

    d = (n - 1) >> 1
    while d & 1 == 0:
        d >>= 1

    for _ in range(20):
        a = random.randint(1, n - 1)
        t = d
        y = pow(a, t, n)

        while t != n - 1 and y != 1 and y != n - 1:
            y = (y * y) % n
            t <<= 1

        if y != n - 1 and t & 1 == 0:
            tmsg.showinfo("判定結果", f"{n}は素数ではありません")
            return False
    tmsg.showinfo("判定結果", f"{n}は素数です")
    return True


# 山札作成(0文字、1数字、2通常画像、3クリックした時の画像、4裏側の画像)
def make_deck():
    return [(m, n, tk.PhotoImage(file=f"gif/{m}{n}.gif"),tk.PhotoImage(file=f"gif/{m}{n}clicked.gif"),tk.PhotoImage(file=f"gif/z1.gif")) for m in ["c","d","h","s"] for n in range(1,14)]


# 素数に使われたカードをnullに変え、墓地に加える removeしないのはリストの番号がずれてしまうため
def field_to_cemetery():
    for i in clicked:
        card = deck[i]
        cemetery.append(card)
        deck[i] = "null"

# 作ったカードをボタンとして配置する
def make_field():
    for i in range(13*4):
        card = tk.Button(root, image=deck[i][4], command= click_card(deck[i][1],i), )
        card.place(x=(i%13)*77+10, y=(i//13)*105+10)
        cardbuttons.append(card)

# クリックしたカードを文字として後ろから足し、画像を切り替え、クリックできなくして、リストに追加する。
def click_card(e,n):

    def x():
        checked_number_label["text"] += str(e)
        cardbuttons[n]["image"] = deck[n][2]
        cardbuttons[n]["state"] = "disable"
        clicked.append(n)
    return x
    #return lambda: handbutton[e].lower()

# 決定ボタンがクリックされた時の処理
def judge():
    global turn_count
    turn_player = turn_count % number_of_people

    if checked_number_label["text"] != "": # 何も選択されていない場合は何もしない

        if len(checked_number_label["text"]) > 20:
            fanction = miller_rabin         # ※確率的判定法
        # elif len(checked_number_label["text"]) > 10:
        #     fanction = judge_prime_number   # 素数判定のみなのではやい
        else:
            fanction = judge_prime_factor   # 素因数も求める代わりに遅い

        if fanction(int(checked_number_label["text"])):     # 素数の場合の処理
            # 素数に使われたカードを非表示にして、枚数分をプレイヤーに追加
            for i in clicked:
                cardbuttons[i].lower()
                Players[turn_player]["point"] += 1

            Player_Point_Label[turn_player]["text"] = f'{Players[turn_player]["name"]} : {Players[turn_player]["point"]}枚'

            field_to_cemetery()

            # 初期化処理
            checked_number_label["text"] = ""
            clicked.clear()

        else:   # 素数ではない場合の処理
            cancel()

        finish()    # 終了条件をみたしている場合勝者判定して終了する
        turn_count += 1
        Turn_label["text"] = f'{Players[turn_count % number_of_people]["name"]}の番です'    # 手番を更新

# 選択したカードをもとに戻す
def cancel():
    checked_number_label["text"] = ""
    for i in clicked:
        cardbuttons[i]["image"] = deck[i][4]
        cardbuttons[i]["state"] = "normal"
    clicked.clear()

# 1枚のみで素数になる数(2,3,5,7,11,13)がなくなった場合終了する
def finish():
    for i in deck:
        if i[1] == 2 or i[1] == 3 or i[1] == 5 or i[1] == 7 or i[1] == 11 or i[1] == 13:
            return True

    # 枚数を多くとったプレイヤーが勝ち
    if Player1["point"] > Player2["point"]:
        winner = Player1["name"]
        tmsg.showinfo("対戦終了", f"{winner}の勝ちです")
    elif Player1["point"] < Player2["point"]:
        winner = Player2["name"]
        tmsg.showinfo("対戦終了", f"{winner}の勝ちです")
    else:
        tmsg.showinfo("対戦終了", "引き分け")
    exit()


turn_count = 0

# Playerの初期データ 将来使えそうな値も作っておく
Player1 = {"name":"Player1", "point":0, "life":3}
Player2 = {"name":"Player2", "point":0, "life":3}
Player3 = {"name":"Player3", "point":0, "life":3}
Player4 = {"name":"Player4", "point":0, "life":3}

Players = [Player1, Player2, Player3, Player4]

number_of_people = 2

cemetery = []
clicked = []    # 選択しているカードを一時的に保持する
cardbuttons = []    # あとでカードの状態を変えやすいように収納しておくためのリスト

button1 = tk.Button(root, text="決定", font=("",30),command=judge)
button1.place(x=50, y=470)

#button2 = tk.Button(root, text="キャンセル", command=cancel)
#button2.place(x=300, y=550)

# 選択したカード達を表すラベル
checked_number_label = tk.Label(root, text="", font=("",30),foreground="black", background="white",width="50", anchor="w")
checked_number_label.place(x=170,y=480)

# 手番を表すラベル
Turn_label = tk.Label(root, text=f'{Players[0]["name"]}の番です',font=("",20))
Turn_label.place(x=50,y=550)

# プレイヤーの取った枚数を表示するラベル
Player_Point_Label = [tk.Label(root, text=f'{Player1["name"]} : {Player1["point"]}枚',font=("",20))
                      ,tk.Label(root, text=f'{Player2["name"]} : {Player2["point"]}枚',font=("",20))]
Player_Point_Label[0].place(x=250,y=550)
Player_Point_Label[1].place(x=400,y=550)

# カードを作ってシャッフルして場に配置
deck = make_deck()
random.shuffle(deck)
make_field()

root.mainloop()