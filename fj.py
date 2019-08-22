# -*- coding: utf-8 -*-
'''
problems:
    is legal : 函数待补充，且对移，跳的判断有误
    棋子摆放位置精确度不高,解决方案，将棋盘长宽设为14的倍数
'''
import pygame
import sys
from sys import exit
from pygame.locals import *
#所有pass的地方未完善

debug = 1

#按键设置
key_start = K_a
key_stop = K_s
key_regret = K_r
#

#模式设置
RUN = 1
CHOOSE = 2
MOVE = 3 #表示已选好棋子，等待落子

#一些参数
EPS = 50
FPS = 30
BLACK = (200,101,50)

chosse_image_filename = 'ball.png' #表示棋子被选中的方格
dot_image_filename = 'dot.jpg'
chess_board_size= (14*50,14*30) #为了使棋子的位置精确，两数需为14的倍数
red_score = (50,50)
blue_score = (12*50,50)
chosse_image_size = (50,50) #表示棋子被选中的方格
dot_image_size = (10,10)
ball_image_size = (35,35)
backgroud_filename = 'qipan5.jpg'

def between(a,b,c):
    return a<b and b<c

#可接受的鼠标点击误差
def tolerable(target,pos):
    if abs(pos[0]-target[0])+abs(pos[1]-target[1]) < EPS:
        return True
    return False

def get_txt(num = []):
    #获取用户输入的字符串
    # return value : 表达式的值，表达式非法则返回-1
    
    import tkinter
    # 导入ttk
    from tkinter import ttk
    class App:
        def __init__(self, master,num):
            self.master = master
            self.string = ''
            self.initWidgets(num)
        def initWidgets(self,num):
            num.sort()
            number_available = ''
            for i in num:
                number_available += str(i)+' '
            lb = tkinter.Label(self.master,
                text='请输入一个合法的表达式:\n'+
                '1.表达式仅能包含以下数字  '+number_available+'\n'+
                '2.表达式只能包含以下运算符  +  -  *  /  (  ) \n'+
                '3.使用除法时不得有余数，否则视为非法')
            lb.pack()
            # 创建Entry组件
            self.st = tkinter.StringVar()
            self.entry = ttk.Entry(self.master,
                textvariable=self.st,
                width=44,
                font=('StSong', 14),
                foreground='green')
            self.entry.pack(fill=tkinter.BOTH, expand=tkinter.YES) 
            tkinter.Button(self.master,text='ok',command=self.master.quit).pack()
    root = tkinter.Tk()
    root.title("Entry测试")
    w = App(root,num)
    root.mainloop()
    root.destroy()

    return eval(w.st.get()) #TODO use my own evaluation


#生成棋子像素坐标
def make_coordinate():
    cor = [[0 for i in range(8)] for j in range(8)]
    width,height = chess_board_size[0],chess_board_size[1]
    width /= 14  #x轴单位长度
    height /= 14 #y轴单位长度
    for i in range(8):
        for j in range(8):
            std = coordinate_transform((i,j))
            cor[i][j] = std[1]*width,std[0]*height
    return cor

#加载棋子图片
def load_balls():
    balls = []
    balls.append(Image('0.jpg',ball_image_size))
    for i in range(1,21):
        balls.append(Image(str(i)+'.png',ball_image_size))
    return balls


#从我的坐标系到标准坐标系
def coordinate_transform(coor):
    return coor[0]+coor[1], 7-coor[0]+coor[1]
#从标准坐标系到我的坐标系
def inverse_coordinate_transform(coor):
    return (coor[0]+coor[1]-7)/2,(coor[0]-coor[1]+7)/2

#计算后缀表达式的值
def calculate(expression):
    ret = 0
    stack = []
    for i in expression:
        if i=='+':
            b = stack.pop()
            a = stack.pop()
            stack.append(a+b)
        elif i=='*':
            b = stack.pop()
            a = stack.pop()
            stack.append(a*b)
        elif i=='-':
            b = stack.pop()
            a = stack.pop()
            stack.append(a-b)
        elif i=='/':
            b = stack.pop()
            a = stack.pop()
            #division by zero
            if 0==b :
                return -1
            stack.append(a/b)
        else:
            stack.append(i)
    return stack[0]

#深度优先搜索实现全排列，一旦找到一个解就跳出递归 , 返回表达式
def dfs(cur,cnt,res,pre_num,expression,num,target,visit):
    #递归终点，数字用完且操作符数量足够
    if cur==cnt and res==0:
        return expression if target==calculate(expression) else []
    pos = cur+cnt-1-res
    for i in range(cnt):
        if not visit[i]:
            expression[pos] = num[i]
            visit[i] = 1
            ret = dfs(cur+1,cnt,res,pre_num+1,expression,num,target,visit)
            if ret != []:
                return ret
            visit[i] = 0
    if pre_num>1:
        op = ['+','-','*','/']
        for i in op:
            expression[pos] = i
            ret = dfs(cur,cnt,res-1,pre_num-1,expression,num,target,visit)
            if ret != []:
                return ret
    return []

#TODO 在游戏开始时生成表以判断是否可达，中间值最多为六个，故最多有C(10,6)*10种情况
#判断是否能使用num中每个数字有且仅有一次得到target,采用对后缀表达式全排列的方法实现
def reachable(target,num):
    # 特判：如果num中只有一个元素且与target相等，则也符合条件
    cnt = len(num)
    if cnt==1 and num[0]==target:
        return True
    expression = [0 for i in range(cnt+cnt-1)]
    visit = [0 for i in range(cnt)]
    return dfs(0,cnt,cnt-1,0,expression,num,target,visit)==[]

#注意 用10 表示 0
class Chess_board:

    def __init__(self):
        self.num_row = 8
        self.num_col = 8
        self.empty_flag = 100
        self.board = [ [self.empty_flag for i in range(self.num_row)] for j in range(self.num_col) ] 
        
        #将棋子放在出始位置, 用正负区分不同颜色的棋子
        self.board[0][7] = 10
        self.board[7][0] = -10
        x, y, z = 0, 4, 1
        for i in range(1,10):
            self.board[x][y] = i
            if 1==z: 
                if y==self.num_col-1:
                    x -= 1
                    z = 0
                else :
                    x += 1
                    y += 1
            else:
                if 0==x:
                    y += 1
                    z = 1
                else :
                    x -= 1
                    y -= 1
        x, y, z = 7, 3, 0
        for i in range(1,10):
            self.board[x][y] = -i
            if 1==z: 
                if self.num_row-1==x:
                    y -= 1
                    z = 0
                else :
                    x += 1
                    y += 1
            else:
                if y==0:
                    x += 1
                    z = 1
                else :
                    x -= 1
                    y -= 1
        self.origin_pos = self.board #每个位置的编号，用于后期计算分数
        
    #坐标相加
    def add(self,first,second):
        return (first[0]+second[0],first[1]+second[1])

    def empty(self,position):
        if position[0] < 0 or position[0] > 7:
            return False
        if position[1] < 0 or position[1] > 7:
            return False
        return self.board[position[0]][position[1]]==self.empty_flag

    def in_the_same_row(self,st,ed):
        return st[0] == ed[0]

    def in_the_same_col(self,st,ed):
        return st[1] == ed[1]

    #根据游戏规则，仅考虑右斜对角线
    def in_the_same_diagonal(self,st,ed):
        return st[1]-ed[1] == st[0]-ed[0]

    def in_the_same_line(self,st,ed):
        return self.in_the_same_col(st,ed) or self.in_the_same_diagonal(st,ed) or self.in_the_same_row(st,ed)

    def get_value(self,pos):
        try:
            value = abs(self.board[pos[0]][pos[1]])
        except:
            print (pos,'is not in the board')
            exit()
        return value%10
    
    def get_values_on_the_way(self,start_position,end_position):
        value_on_the_way = [] #获取经过的值
        d = []
        sign = -2
        if self.in_the_same_col(start_position,end_position):
            sign = -1 if end_position[0]-start_position[0]<0 else 1
            d = [sign,0]
        elif self.in_the_same_row(start_position,end_position):
            sign = -1 if end_position[1]-start_position[1]<0 else 1
            d = [0,sign]
        else:
            sign = -1 if end_position[0]-start_position[0]<0 else 1
            d = [sign,sign]
        cur = self.add(start_position,d)
        is_last_empty = 1
        while cur != end_position:
            if not self.empty(cur):
                value_on_the_way.append(self.get_value(cur))
                is_last_empty = 0
            else:
                is_last_empty = 1
            cur = self.add(cur,d)
        #跨的目标地点的前一个没有棋子，则移动非法
        if is_last_empty:
            return False
        return value_on_the_way
    
    def yi(self,start_position,end_position):
        #目标方格非空，非法移动
        if not self.empty(end_position):
            return False
        #没有按格线前进，非法移动
        if not self.in_the_same_line(start_position,end_position):
            return False
        near = [ [0,1], [0,-1], [1,0], [-1,0], [1,1], [-1,-1] ]
        for d in near:
            neighbor = self.add(start_position,d)
            #移
            if  neighbor == end_position:
                return True

        return False


    def tiao(self,start_position,end_position):
        #目标方格非空，非法移动
        if not self.empty(end_position):
            return False
        #没有按格线前进，非法移动
        if not self.in_the_same_line(start_position,end_position):
            return False

        near = [ [0,1], [0,-1], [1,0], [-1,0], [1,1], [-1,-1] ]
        for d in near:
            neighbor = self.add(start_position,d)
            #跳
            if not self.empty(neighbor) and self.empty(self.add(neighbor,d)) and end_position==self.add(neighbor,d):
                return True

        return False


    def is_legal(self,start_position,end_position):
        #目标方格非空，非法移动
        if not self.empty(end_position):
            return False
        #没有按格线前进，非法移动
        if not self.in_the_same_line(start_position,end_position):
            return False

        if self.yi(start_position,end_position) :
            if debug:
                print ('yi')
            return True
        if self.tiao(start_position,end_position) :
            if debug:
                print ('tiao')
            return True

        #跨
        value_on_the_way = self.get_values_on_the_way(start_position,end_position)
        if value_on_the_way == False:
            return False
        value = self.get_value(start_position) #获取要移动的棋子的编号
        if value==get_txt(value_on_the_way):
            if debug:
                print ('kua')
            return True
        return False

    #获取某个位置的分数贡献
    def get_pos_score(self,pos):
        a,b = self.board[pos[0]][pos[1]],self.origin_pos[pos[0]][pos[1]]
        if a*b>0:
            return -1
        a = a if (a!=10 and a!=-10) else 0
        b = b if (b!=10 and b!=-10) else 0
        return abs(a*b)

    #判断能否喊停并计算分数，不能喊停返回-1，-1   不然返回双方分数
    def get_score(self):
        first,second = 0,0
        count_first,count_second = 0,0
        for i in range(self.num_row):
            for j in range(self.num_col):
                if not self.empty([i,j]) and self.origin_pos[i][j]!=self.empty_flag:
                    score = self.get_pos_score((i,j))
                    if score==-1:
                        continue
                    if i<j :
                        first += score
                        count_first += 1
                    else :
                        second += score
                        count_second += 1
        if count_first==10 or count_second==10:
            return first,second
        return -1,-1

    def move(self,From,To):
        if self.empty(From) or not self.empty(To):
            print ('invalid move!')
            return
        self.board[To[0]][To[1]] = self.board[From[0]][From[1]]
        self.board[From[0]][From[1]] = self.empty_flag
        return

    def regret(self):
        pass
         

class Image:
    #图片类，有图片的宽，高，左上角坐标，中心点坐标等信息
    height = 0 
    width = 0
    x_corner = 0
    y_corner = 0
    x_center = 0
    y_center = 0

    #pos参数为图片左上角坐标位置信息，默认为（0，0）
    def __init__(self,filename,Size,pos=(0,0)):
#        self.ima = pygame.image.load(filename).convert()
        try:
            self.ima = pygame.image.load(filename).convert()
        except pygame.error:
            print ('can not load',filename,':')
            exit()
        self.ima = pygame.transform.scale(self.ima,Size)
        self.width = self.ima.get_width()
        self.height = self.ima.get_height()
        self.x_corner, self.y_corner = pos
    
    #已知center坐标求corner
    def to_corner(self):
        self.x_corner = self.x_center - self.width/2
        self.y_corner = self.y_center - self.height/2

    #已知corner坐标求center
    def to_center(self):
        self.x_center = self.x_corner + self.width/2
        self.y_center = self.y_corner + self.height/2

    def in_image(self,pos):
        if between(self.x_corner,pos[0],self.x_corner+self.width) and between(self.y_corner,pos[1],self.y_corner+self.height):
            return True
        return False
    
    def move(self):
        pass

    def set_center(self,pos):
        self.x_center,self.y_center = pos
        self.to_corner()

    def set_corner(self,pos):
        self.x_corner,self.y_corner = pos
        self.to_center()


class FandJ:

    def __init__(self):
        pygame.init()
        self.screen_size = 900,500 #窗口大小
        self.screen = pygame.display.set_mode(self.screen_size,pygame.RESIZABLE,32)  # 显示窗口
        self.background = Image(backgroud_filename,self.screen_size)
        self.chess_board = Chess_board()
        self.coordinate = make_coordinate() #相对于棋盘左上角每个棋子中心点的坐标
        self.balls = load_balls()
        self.mode = CHOOSE
        self.choose_image = Image(chosse_image_filename,chosse_image_size)
        self.choose = 0,0
        self.show_list = [] #需要展示的图片
        self.clock = pygame.time.Clock()
        self.show_score_flag = 0
        pygame.display.set_caption("国际数棋")
#        self.button_start = Image(button_start_filename)
#        self.button_regret = Image(button_regret_filename)
#        self.button_stop = Image(button_stop_filename)

    #根据已经求出的coordinate，和棋盘的现状，给出棋子像素坐标
    #!!!!!!!!!!画屏之前一定要先调用此函数
    def update_balls_position(self):
        #直接修改balls对象(Image类)的坐标值  
        #此函数无返回值
        for i in range(self.chess_board.num_row):
            for j in range(self.chess_board.num_col):
                if self.chess_board.board[i][j] != self.chess_board.empty_flag:
                    self.balls[self.chess_board.board[i][j]].set_center(self.coordinate[i][j])

    def restart(self):
        self.chess_board = Chess_board()
        self.show_score_flag = 0

    def add_image(self,pic):
        self.screen.blit(pic.ima,(pic.x_corner,pic.y_corner))

    def pixel_to_cor(self,pos):
        for i in range(self.chess_board.num_row):
            for j in range(self.chess_board.num_col):
                if self.coordinate[i][j] == pos:
                    return (i,j)
        return (-1,-1)
    
    #处理事件：
    #   鼠标点击
    #   按键
    def deal(self,event):
        if event.type == KEYDOWN:
            if event.key == key_regret:
                self.chess_board.regret()
            elif event.key == key_start:
                self.restart()
            elif event.key == key_stop:
                self.score = self.chess_board.get_score()
                if  self.score == (-1,-1):
                    pass #没有到达终止条件
                else:
                    if debug:
                        print (self.score) 
                    self.show_score_flag = 1
                    pass #达到终止条件,结束游戏，打印分数
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.mode == CHOOSE:
                for ball in self.balls:
                    if ball.in_image(mouse_pos):
                        if debug:
                            print ('ball position',ball.x_corner,ball.y_corner)
                            print ('ball width and height:',(ball.width,ball.height))
                        self.choose_image.set_center((ball.x_center,ball.y_center))
                        self.show_list.append(self.choose_image)
                        self.mode = MOVE
                        self.choose = self.pixel_to_cor((ball.x_center,ball.y_center))
                        break
            elif self.mode == MOVE:
                self.mode = CHOOSE
                self.show_list.remove(self.choose_image)
                row = self.chess_board.num_row
                col = self.chess_board.num_col
                for i in range(row):
                    for j in range(col):
                        if tolerable(self.coordinate[i][j],pygame.mouse.get_pos()):
                            if debug:
                                print ('点击点像素坐标:',self.coordinate[i][j])
                                print ('实际坐标:',self.pixel_to_cor(self.coordinate[i][j]))
                                print ('start position:',self.choose)
                            #TODO 弹窗，用户输入字符串表达式
                            if self.chess_board.is_legal(self.choose,self.pixel_to_cor(self.coordinate[i][j])):
                                self.chess_board.move(self.choose,self.pixel_to_cor(self.coordinate[i][j]))
                            else:
                                print ('illegal move')
                                pass
                                #移动不合法
                            
                            break
        
        elif event.type == MOUSEMOTION:
            pass

    def draw_board(self):
        ''' 画棋盘
        '''
        for i in range(8):
            pygame.draw.line(self.screen,BLACK,self.coordinate[i][0],self.coordinate[i][7])
            pygame.draw.line(self.screen,BLACK,self.coordinate[0][i],self.coordinate[7][i])
            pygame.draw.line(self.screen,BLACK,self.coordinate[0][i],self.coordinate[7-i][7])
            pygame.draw.line(self.screen,BLACK,self.coordinate[i][0],self.coordinate[7][7-i])

    def show_score(self,score):
        red = pygame.font.Font.render(str(self.score[0]))
        blue = pygame.font.Font.render(str(self.score[1]))
        self.screen.blit(red,red_score)
        self.screen.blit(blue,blue_score)

    #游戏运行主函数
    def run(self):
        while True:

            self.clock.tick(FPS)

            self.add_image(self.background)
            self.draw_board()

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                self.deal(event)

            if self.show_score_flag:
                self.show_score()
            
            self.update_balls_position()
            for ball in self.balls:
                self.add_image(ball)
            for ima in self.show_list:
                self.add_image(ima)
            pygame.display.flip()

if __name__ == '__main__':
    game = FandJ()
    game.run()
