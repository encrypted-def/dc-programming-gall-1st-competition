import random
from PIL import Image, ImageDraw, ImageFont
import time
ALIVE = 0
ELIMINATE = 1
DIE_TODAY = 2
DIE = 3

# 이번 턴에 공격당한 서버 : 빨간색
# 이번 턴에 작은 클러스터에 속해 무력화된 덩어리 : 파란색
# 살아있는 서버 : 하얀색
# 죽은 서버 : 검정색

COLORS = [(255,255,255), (255,0,0), (0,0,255), (0,0,0)]
IMAGE_SIZE = 600
TXT_SIZE = 60
dx = [1,0,-1,0]
dy = [0,1,0,-1]

def OOB(x, y, A):
  return x < 0 or x >= A or y < 0 or y >= A

# print board in stdout
def printBoard(board, A):
  for i in range(A):
    for j in range(A):
      print(board[i][j], end=' ')
    print()

def board2img(board, A, info):
  img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE+TXT_SIZE),COLORS[0])
  PIXEL_SIZE = IMAGE_SIZE // A
  for i in range(A):
    for j in range(A):
      for x in range(i * PIXEL_SIZE, i * PIXEL_SIZE + PIXEL_SIZE):
        for y in range(j * PIXEL_SIZE, j * PIXEL_SIZE + PIXEL_SIZE):
          img.putpixel((x, y), COLORS[board[i][j]])
  d = ImageDraw.Draw(img)
  fnt = ImageFont.truetype(r"C:\WINDOWS\FONTS\ARIAL.TTF", 30)
  d.text((180,IMAGE_SIZE + TXT_SIZE // 2 - 15), text = info, font=fnt, fill=(0,0,0) )
  return img

def die_transition(board, A):
  for i in range(A):
    for j in range(A):
      if board[i][j] in [DIE_TODAY, ELIMINATE]: board[i][j] = DIE  

def simulation(board, A, B):
  die_transition(board, A)  
  alive_list = [(i,j) for i in range(A) for j in range(A) if board[i][j] == ALIVE]
  eliminate_set = set()
  while len(eliminate_set) < B:
    eliminate_set.add(random.choice(alive_list))
  for elim in eliminate_set:
    board[elim[0]][elim[1]] = ELIMINATE
  visit = [[False]*A for j in range(A)]
  cluster = []
  cluster_elem = {}

  for i in range(A):
    for j in range(A):
      if visit[i][j] or board[i][j] != ALIVE: continue
      cluster_size = 0
      visit[i][j] = True
      cluster_elem[(i,j)] = []
      S = [(i,j)] # DFS를 위한 list
      while S:
        cur = S.pop()
        cluster_size += 1
        cluster_elem[(i,j)].append(cur)
        for dir in range(4):
          nx, ny = cur[0] + dx[dir], cur[1] + dy[dir]
          if OOB(nx, ny, A) or visit[nx][ny] or board[nx][ny] != ALIVE: continue
          visit[nx][ny] = True
          S.append((nx,ny))
      cluster.append((cluster_size, (i, j)))

  if len(cluster) > 1:
    cluster.sort(reverse=True)
    same_size_idx = 0
    while same_size_idx != len(cluster) and cluster[same_size_idx][0] == cluster[0][0]:
      same_size_idx += 1
    idx = random.randrange(0, same_size_idx)
    for i in range(len(cluster)):
      if i == idx: continue
      for dead_elem in cluster_elem[cluster[i][1]]:
        board[dead_elem[0]][dead_elem[1]] = DIE_TODAY
      
  alive_num = sum(1 if board[i][j] == ALIVE else 0 for i in range(A) for j in range(A))
  return alive_num

def run_and_save(A, B, filename):
  imgs = []

  board = [[ALIVE]*A for i in range(A)]
  day = 0
  info = f"Day {day}, {A*A}/{A*A}"
  imgs.append(board2img(board, A, info))
  while True:
    day += 1  
    alive_num = simulation(board, A, B)  
    info = f"Day {day}, {alive_num}/{A*A}"
    imgs.append(board2img(board, A, info))
    if alive_num < A * A * 4 // 10:
      break

  die_transition(board, A)
  info = f"Day {day}, {alive_num}/{A*A}"
  imgs.append(board2img(board, A, info))
  imgs[0].save(filename, save_all = True, append_images = imgs[1:], optimize = False, duration = 250, loop = 1)
  return day

# Given parameter
As = [5, 10, 100, 200]
Bs = [1, 5, 100, 400]

for i in range(len(As)):
  print(f"****** A {As[i]} B {Bs[i]} ******")
  for cnt in range(10):
    day = run_and_save(As[i], Bs[i], f"results/{As[i]}-{Bs[i]}-{cnt}.gif")
    print(f"Case #{cnt}: Day {day}")
