import pygame		#pip install pygame
import random		#随机
import math 		#引入数学模块

#------------------------------------------------------------------#初始化界面
pygame.init()
screen = pygame.display.set_mode((800, 600))		#屏幕宽和高
pygame.display.set_caption('飞机大战')				#设置标题
# 引入UFO游戏左上角的游戏图标图片
icon = pygame.image.load('ufo.png')					#外部加载图像
pygame.display.set_icon(icon)						#设置左上角的游戏图标，图标尺寸大小为32*32
# 背景图片
bgImg = pygame.image.load('bg.png')
#------------------------------------------------------------------#初始化界面

#------------------------------------------------------------------#添加音乐音效
#背景音乐
pygame.mixer.music.load('bg.wav')
pygame.mixer.music.play(-1) #单曲循环
#射中音效
bao_sound = pygame.mixer.Sound('exp.wav')
#------------------------------------------------------------------#添加音乐音效

#------------------------------------------------------------------#引入飞机图片
playerImg = pygame.image.load('player.png')
playerX = 400 	#玩家的X坐标
playerY = 500 	#玩家的Y坐标
playerStep = 0 	#玩家移动的速度
#------------------------------------------------------------------#引入飞机图片

#------------------------------------------------------------------#分数
# 初始化分数
score = 0
# 字体	自带的
font = pygame.font.Font('freesansbold.ttf', 32)
#font = pygame.font.SysFont('simsunnsimsun',32) #宋体

# 显示分数
def show_score():
	text = f'Score: {score}'
	# 渲染文本的 Surface 对象
	score_render = font.render(text, True, (255,0,0))
	# 将一个图像（Surface 对象）绘制到另一个图像上
	screen.blit(score_render, (10,10))
#------------------------------------------------------------------#分数

#------------------------------------------------------------------#游戏结束
# 默认是开启游戏的
is_over = False
# 字体
over_font = pygame.font.Font('freesansbold.ttf', 64)
# 判断游戏是否结束
def check_is_over():
	if is_over:
		text = "Game Over"
		# 渲染文本的 Surface 对象
		render = over_font.render(text, True, (255,0,0))
		# 将一个图像（Surface 对象）绘制到另一个图像上
		screen.blit(render, (200,250))
#------------------------------------------------------------------#游戏结束

#------------------------------------------------------------------#两个点之间的距离
def distance(bx, by, ex, ey):
	a = bx - ex
	b = by - ey
	return math.sqrt(a*a + b*b) #开根号
#------------------------------------------------------------------#两个点之间的距

#-----------------------------------------------------------------------------------------------------------#敌人
#初始化敌人的数量
number_of_enemies = 6
#------------------------------------------------------------------#敌人类
class Enemy():
	def __init__(self):
		# 添加敌人
		self.img = pygame.image.load('enemy.png')

		self.x = random.randint(200, 600)
		self.y = random.randint(50, 250)
		# 敌人移动的速度
		self.step = random.randint(2, 6)

	#重置位置：当被射中时，恢复位置
	def reset(self):
		self.x = random.randint(200, 600)
		self.y = random.randint(50, 200)
#------------------------------------------------------------------#敌人类

#保存所有的敌人
enemies = []
for i in range(number_of_enemies):
	enemies.append(Enemy())		#调用敌人类Enemy()

#------------------------------------------------------------------#显示敌人
def show_enemy():
	global is_over
	for e in enemies:
		# 画出敌人
		screen.blit(e.img,(e.x, e.y))
		e.x += e.step
		# 如何敌人碰到左右边界
		if(e.x > 736 or e.x < 0):
			# 改变运行方向
			e.step *= -1
			# 开始向下沉
			e.y += 40
			# 判断游戏是否结束
			if e.y > 450:
				# 显示结束状态	print("游戏结束啦")
				is_over = True
				enemies.clear()
# ------------------------------------------------------------------#显示敌人
#-----------------------------------------------------------------------------------------------------------#敌人

#-----------------------------------------------------------------------------------------------------------#子弹
#------------------------------------------------------------------#子弹类
class Bullet():
	def __init__(self):
		# 画出子弹
		self.img = pygame.image.load('bullet.png')
		self.x = playerX + 16 #(64-32)/2
		self.y = playerY + 10					# 子弹出现在玩家的上方一点点
		# 子弹移动的速度
		self.step = 10

	#判断是否击中敌人
	def hit(self):
		global score
		for e in enemies:
			if(distance(self.x, self.y, e.x, e.y) < 30):		#子弹和敌人位置较近
				#射中啦
				bao_sound.play()		# 射中音效

				bullets.remove(self)	# 移除该子弹
				e.reset()				# 调用重置位置函数reset（）

				#添加分数
				score += 1
#保存现有的子弹
bullets = []
#------------------------------------------------------------------#子弹类

#------------------------------------------------------------------#显示并移动子弹
def show_bullets():
	for b in bullets:
		# 显示图片到什么地方
		screen.blit(b.img, (b.x, b.y))
		# 看看是否击中了敌人：调用hit()函数
		b.hit()
		# 移动子弹：向上
		b.y -= b.step
		#判断子弹是否出了界面，如果出了就移除掉
		if b.y < 0:
			bullets.remove(b)
#------------------------------------------------------------------#显示并移动子弹
#-----------------------------------------------------------------------------------------------------------#子弹



#------------------------------------------------------------------#移动飞机防止飞机出界
def move_player():
	global playerX
	playerX += playerStep
	#防止飞机出界
	if playerX > 736:			#右边
		playerX = 736
	if playerX < 0:				#左边
		playerX = 0
#------------------------------------------------------------------#移动飞机防止飞机出界

#-------------------------------游戏主循环-----------------------------------#
running = True
while running:
	# 画出背景渲染到屏幕
	screen.blit(bgImg,(0,0))					# 导入背景图片
	# 显示分数：调用
	show_score()
	# 返回当前的所有事件
	for event in pygame.event.get():
		if event.type == pygame.QUIT:				# 退出
			running = False

		#通过键盘事件控制飞机的移动
		if event.type == pygame.KEYDOWN: 			# 按下就移动
			if event.key == pygame.K_RIGHT:			# 右键
				playerStep = 5
			elif event.key == pygame.K_LEFT:		# 左键
				playerStep = -5
			elif event.key == pygame.K_SPACE:		# 空格
				#创建一颗子弹
				bullets.append(Bullet())			# 调用子弹Bullet()
		if event.type == pygame.KEYUP:				# 按键之后抬起来就不动
			playerStep = 0

	# 画出飞机
	screen.blit(playerImg, (playerX, playerY))

	# 每帧循环：依次显示
	move_player() 					#移动飞机
	show_enemy() 					#显示敌人
	show_bullets()					#显示子弹
	check_is_over() 				#显示游戏结束字段

	pygame.display.update()			#界面更新
#-------------------------------游戏主循环-----------------------------------#