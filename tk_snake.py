import random
import os
from pynput.keyboard import Controller,Key,Listener
from apscheduler.schedulers.background import BackgroundScheduler
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

root = Tk()
root.geometry('400x400')
 
root.title("贪吃蛇")
cv = Canvas(root, bg = 'white', height=400, width=400)

class Sanke:
  def __init__(self, currentHeadOrientation, snakeLeng, width, height):
    lcs = locals()
    lcs.pop('self')
    self.__dict__.update(lcs)
    self.bodyList = [[0]*2]*snakeLeng
    self.snakeLeng = snakeLeng
    # 蛇的爬行方向
    self.orientation = []
    self.width = width
    self.height = height
    self.snakeBody = "*"     # 数组被填充字符串
    self.snakeHead = "@"     # 蛇头填充
    self.snake_cv = None
    self.fruitPoint = [0]*2    # 果实位置
    self.fruitStr = "O"      # 果实填充
    self.fruitCv = None
    self.speed = 3
    

  
  # 蛇向前爬行
  def wriggle(self):
    # if self.currentHeadOrientation == "up":
    #   print("向上爬")
    # if self.currentHeadOrientation == "down":
    #   print("向下爬")
    # if self.currentHeadOrientation == "left":
    #   print("向左爬")
    # if self.currentHeadOrientation == "right":
    #   print("向右爬")
    cv.delete(ALL)
    self.generatesFruit()
    self.addSnakeBody()
    self.draw_snake()
    cv.pack()
  
  def draw_snake(self):
    length = len(self.bodyList)
    for i in range(length):
      if i >= length-1:
        break
      if i == 0:
        cv.create_oval(self.bodyList[i][0],self.bodyList[i][1], self.bodyList[i+1][0] + 1, self.bodyList[i+1][1] + 1, width=5)
      else:
        cv.create_line(self.bodyList[i][0],self.bodyList[i][1], self.bodyList[i+1][0], self.bodyList[i+1][1], width=5)

  # 初始化蛇的位置
  def initSnake(self):
    first_x = random.randint(5, self.width)
    first_y = random.randint(5, self.height)
    self.bodyList[0] = [first_y, first_x-1]
    for i in range(self.snakeLeng-1):
      i = i + 1
      first_x = first_x + 1
      first_y = first_y
      self.bodyList[i] = [first_y, first_x-1]
    self.changeOrientation()

  # 增加蛇身长度
  def addSnakeBody(self):
    snake_copy = self.bodyList.copy()
    for i in range(len(snake_copy)):
      if i == 0:
        if self.currentHeadOrientation == "up":
          self.bodyList[i] = [snake_copy[i][0]-self.speed, snake_copy[i][1]]
        if self.currentHeadOrientation == "down":
          self.bodyList[i] = [snake_copy[i][0]+self.speed, snake_copy[i][1]]
        if self.currentHeadOrientation == "left":
          self.bodyList[i] = [snake_copy[i][0], snake_copy[i][1]-self.speed]
        if self.currentHeadOrientation == "right":
          self.bodyList[i] = [snake_copy[i][0], snake_copy[i][1]+self.speed]
        if self.bodyList[i][0] >= self.fruitPoint[0] and self.bodyList[i][0] <= self.fruitPoint[0] + 5 and self.bodyList[i][1] >= self.fruitPoint[1] and self.bodyList[i][1] <= self.fruitPoint[1] + 5:
          self.bodyList.append(self.bodyList[-1])
          self.fruitPoint = [0]*2
        
        if self.bodyList[i][0] < 0 or self.bodyList[i][0] > width or self.bodyList[i][1] < 0 or self.bodyList[i][1] > height:
          messagebox.showinfo(message="游戏结束, 请重新开始")
          run()
        continue
      self.bodyList[i] = snake_copy[i-1]
    
  # 更换蛇头朝向
  def changeOrientation(self, type = None):
    self.orientation = [0]*3
    first_x = self.bodyList[0][1]
    first_y = self.bodyList[0][0]
    second_x = self.bodyList[1][1]
    second_y = self.bodyList[1][0]
    if first_y == second_y:
      self.orientation[0] = "up"
      self.orientation[1] = "down"
      if first_x > second_x :
        self.orientation[2] = "right"
      else:
        self.orientation[2] = "left"
    
    if first_x == second_x:
      self.orientation[0] = "left"
      self.orientation[1] = "right"
      if first_y > second_y :
        self.orientation[2] = "down"
      else:
        self.orientation[2] = "up"

    # print("当前可操作：", self.orientation)

    if type != None:
      if type in self.orientation:
        self.currentHeadOrientation = type
      else:
        print("此方向爬不动哦")
        return False
    else:
      self.currentHeadOrientation = self.orientation[random.randint(0, len(self.orientation)-1)]
    # print("当前朝向", self.currentHeadOrientation)
    return True
  
  
  # 随机生成果实
  def generatesFruit(self):
    if self.fruitPoint[0] + self.fruitPoint[1]  <= 0:
      pointList = []
      for i in range(self.width-20):
        tmp = []
        for j in range(self.height-20):
          tmp = [i, j]
          if tmp in self.bodyList:
            pass
          else:
            pointList.append(tmp)
      point = random.randint(0, len(pointList)-1)
      self.fruitPoint = pointList[point]
      print("果实位置：", self.fruitPoint)

    self.fruitCv = cv.create_oval(self.fruitPoint[0],self.fruitPoint[1], self.fruitPoint[0] + 5,self.fruitPoint[1] + 5, width=2)
    
  def snake_location(self):
    print(self.bodyList[0])
  
  # 监听释放
  def on_release(self, key):
      keysym = key.keysym.lower()
      if keysym=="up":
        result = self.changeOrientation("left")
        if result == True:
          self.wriggle()
      if keysym=="down":
        result = self.changeOrientation("right")
        if result == True:
          self.wriggle()
      if keysym=="left":
        result = self.changeOrientation("up")
        if result == True:
          self.wriggle()
      if keysym=="right":
        result = self.changeOrientation("down")
        if result == True:
          self.wriggle()
      if keysym==Key.esc:
          # 停止监听
          return False
      

height = 400               # 数组个数
width = 400                # 数组长度
site = ['0']*height       # 场地高度
defaultBody = " "         # 默认数组填充字符串




# 开始监听
def start_listen(snake):
    with Listener(on_release=snake.on_release) as listener:
        listener.join()



def run():
  print("----------------------------------------------------------------------------------------------------------")
  # 创建一条蛇
  snake = Sanke("", 40, width-50, height-50)
  snake.initSnake()
  snake.wriggle()
  # 每0.5秒更新蛇爬行  
  # scheduler = BackgroundScheduler()
  # scheduler.add_job(snake.wriggle, 'interval', seconds=0.8)
  # scheduler.start()

  # 实例化键盘
  # kb=Controller()
  # kb.release("a")
  # # 开始监听,按esc退出监听
  # start_listen(snake)
  # root.after(500, snake.wriggle)

  #给对象绑定按键监听事件<Key>为监听任何按键 <Key-x>监听其它键盘，如大写的A<Key-A>、回车<Key-Return>
  root.bind('<Key>', snake.on_release)

  bt = Button(root, text ="位置", command = snake.snake_location)
  bt.pack()
  #显示窗体
  root.mainloop()
  


if __name__ == "__main__":
  run()