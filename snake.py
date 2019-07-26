import random
import threading
import time
from pynput.keyboard import Controller,Key,Listener
from apscheduler.schedulers.background import BackgroundScheduler

defaultBody = "-"   # 默认数组填充字符串
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
    self.fruitPoint = [0]*2    # 果实位置
    self.fruitStr = "O"      # 果实填充

  
  # 蛇向前爬行
  def wriggle(self):
    if self.currentHeadOrientation == "up":
      print("向上爬")
    if self.currentHeadOrientation == "down":
      print("向下爬")
    if self.currentHeadOrientation == "left":
      print("向左爬")
    if self.currentHeadOrientation == "right":
      print("向右爬")
    self.generatesFruit()
    self.addSnakeBody()
    self.updateLocation()
    self.updateSite()
  
  # 增加蛇身长度
  def addSnakeBody(self):
    snake_copy = self.bodyList.copy()
    for i in range(len(snake_copy)):
      if i == 0:
        if self.currentHeadOrientation == "up":
          self.bodyList[i] = [snake_copy[i][0]-1, snake_copy[i][1]]
        if self.currentHeadOrientation == "down":
          self.bodyList[i] = [snake_copy[i][0]+1, snake_copy[i][1]]
        if self.currentHeadOrientation == "left":
          self.bodyList[i] = [snake_copy[i][0], snake_copy[i][1]-1]
        if self.currentHeadOrientation == "right":
          self.bodyList[i] = [snake_copy[i][0], snake_copy[i][1]+1]
        if self.bodyList[i] == self.fruitPoint:
          print("*-*-*-**-")
          self.bodyList.append(self.bodyList[-1])
          self.fruitPoint = [0]*2
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

    print("当前可操作：", self.orientation)

    if type != None:
      if type in self.orientation:
        self.currentHeadOrientation = type
      else:
        print("此方向爬不动哦")
        return False
    else:
      self.currentHeadOrientation = self.orientation[random.randint(0, len(self.orientation)-1)]
    print("当前朝向", self.currentHeadOrientation)
    return True
  
  # 更新蛇的位置
  def updateLocation(self):
    for i in range(height):
      site[i] = [0]*width
      for j in range(width):
        site[i][j] = defaultBody
    if self.fruitPoint[0] + self.fruitPoint[1] > 0:
      site[self.fruitPoint[0]][self.fruitPoint[1]] = self.fruitStr

    site[self.bodyList[0][0]][self.bodyList[0][1]] = self.snakeHead
    for i in range(len(self.bodyList)-1):
      i = i + 1
      site[self.bodyList[i][0]][self.bodyList[i][1]] = self.snakeBody

  # 初始化蛇的位置
  def initSnake(self):
    first_x = random.randint(5, self.width-5)
    first_y = random.randint(5, self.height-5)
    self.bodyList[0] = [first_y, first_x-1]
    site[first_y][first_x-1] = self.snakeHead
    for i in range(self.snakeLeng-1):
      i = i + 1
      first_x = first_x + 1
      first_y = first_y
      self.bodyList[i] = [first_y, first_x-1]
      site[first_y][first_x-1] = self.snakeBody
    self.updateSite()
    self.changeOrientation()
  
  # 随机生成果实
  def generatesFruit(self):
    if self.fruitPoint[0] + self.fruitPoint[1]  > 0:
      return
    
    pointList = []
    for i in range(height):
      tmp = []
      for j in range(width):
        tmp = [i, j]
        if tmp in self.bodyList:
          pass
        else:
          pointList.append(tmp)

    point = random.randint(0, len(pointList)-1)
    self.fruitPoint = pointList[point]
    print("果实位置：", self.fruitPoint)
    


  
  # 刷新场地
  def updateSite(self):
    for i in range(height):
      print("".join(site[i]))
    print("当前位置：", self.bodyList)
  
  # 监听释放
  def on_release(self, key):
      if key==Key.up:
        result = self.changeOrientation("up")
        if result == True:
          self.wriggle()
      if key==Key.down:
        result = self.changeOrientation("down")
        if result == True:
          self.wriggle()
      if key==Key.left:
        result = self.changeOrientation("left")
        if result == True:
          self.wriggle()
      if key==Key.right:
        result = self.changeOrientation("right")
        if result == True:
          self.wriggle()
      if key==Key.esc:
          # 停止监听
          return False
      
  


height = 29               # 数组个数
width = 60                # 数组长度
site = ['0']*height


# 初始化场地
def initSite():
  for i in range(height):
    site[i] = [0]*width
    for j in range(width):
      site[i][j] = defaultBody




# 开始监听
def start_listen(snake):
    with Listener(on_release=snake.on_release) as listener:
        listener.join()

def run():
  print("----------------------------------------------------------------------------------------------------------")
  # 创建一条蛇
  snake = Sanke("", 10, width, height)
  
  initSite()
  snake.initSnake()
  # snake.wriggle()
  # 每秒更新蛇爬行
  # time = threading.Timer(2, snake.wriggle)
  # time.start()
  
  scheduler = BackgroundScheduler()
  scheduler.add_job(snake.wriggle, 'interval', seconds=0.5)
  scheduler.start()

  # 实例化键盘
  kb=Controller()
  kb.release("a")
  # 开始监听,按esc退出监听
  start_listen(snake)
  
    

  
    


if __name__ == "__main__":
  run()