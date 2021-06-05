import TkDraw
import numpy as np
import tkinter
from datetime import datetime as dt

# 格子のサイズ
LATTICE_SIZE = 100

# 辺の長さ＝ゴムの初期長さ
EDGE_SIZE = 8
LATTICE_VEC_SHAPE = (LATTICE_SIZE, LATTICE_SIZE, 2)
LATTICE_SHAPE = (LATTICE_SIZE, LATTICE_SIZE)
pos = np.zeros(LATTICE_VEC_SHAPE)

# ゴムが切れる長さの平均
LIMIT_AVR_H = 12.0
LIMIT_AVR_V = 11.0
# ゴムが切れる長さの偏差値
LIMIT_DEV_H = 1.0
LIMIT_DEV_V = 1.0
# ゴムが切れる長さ
rubber_limit_h = np.random.normal(LIMIT_AVR_H, LIMIT_DEV_H, LATTICE_SHAPE)
rubber_limit_v = np.random.normal(LIMIT_AVR_V, LIMIT_DEV_V, LATTICE_SHAPE)
# ゴムが切れる長さを減らす量
LIMIT_H_SUB = 0.01
LIMIT_V_SUB = 0.01

# ゴムの引っ張りにどれだけ格子点が動かされるか
RUBBER_INTENSITY = 0.1
RUBBER_INTENSITY_ANCHOR = 0.5

# ゴムが切れているフラグ
rubber_cut_h = np.array([[False for i in range(LATTICE_SIZE)] for j in range(LATTICE_SIZE)])
rubber_cut_v = np.array([[False for i in range(LATTICE_SIZE)] for j in range(LATTICE_SIZE)])

# ゴムの長さ
rubber_length_h = np.array([[EDGE_SIZE for i in range(LATTICE_SIZE)] for j in range(LATTICE_SIZE)])
rubber_length_v = np.array([[EDGE_SIZE for i in range(LATTICE_SIZE)] for j in range(LATTICE_SIZE)])

# 張力の作業領域
tension = np.zeros(LATTICE_VEC_SHAPE)

D0 = EDGE_SIZE

# 一回のupdateで回す回数
LOOP_TIMES = 10

# 収束条件
LIMIT_STRESS = 0.1

# GIF出力用
gifimages = []
gifstatus = 0 # 0:最初、1:GIF用画像データ収集中、3:GIF出力すべし

# ImageDraw draw
def update(draw, created_image):
    global rubber_limit_h, rubber_limit_v, rubber_length_h, rubber_length_v, rubber_cut_h, rubber_cut_v, pos, tension

    # ゴムが切れる長さを短くする（ゴムを弱くする）
    rubber_limit_h -= LIMIT_H_SUB
    rubber_limit_v -= LIMIT_V_SUB

    # ステータスの確認
    if gifstatus != 1:
        return
    
    # ゴムが切れているか確認する
    rubber_cut_h |= (rubber_limit_h < rubber_length_h)
    rubber_cut_v |= (rubber_limit_v < rubber_length_v)

    # 繋がり判定用の一時的配列の計算
    rv0 = np.array([[[y, y] for y in x] for x in rubber_cut_v])
    rv1 = np.roll(rv0, 1, axis = 1)
    rh0 = np.array([[[y, y] for y in x] for x in rubber_cut_h])
    rh1 = np.roll(rh0, 1, axis = 0)

    # アンカーの強さに傾斜を設ける場合
    # anchor = [[[0.7*y/LATTICE_SIZE, 0.7*y/LATTICE_SIZE] for y in range(LATTICE_SIZE)] for x in range(LATTICE_SIZE)]

    # 結節点にかかる張力を再計算する
    for count in range(LOOP_TIMES):
        # すべての結節点について張力を計算する
        # 上と繋がっていれば張力を加算する
        tension  = np.where(rv0 == False, np.roll(pos, -1, axis=1) - pos + [0,  D0], 0.0)
        # 下と繋がっていれば張力を加算する
        tension += np.where(rv1 == False, np.roll(pos, +1, axis=1) - pos + [0, -D0], 0.0)
        # 右と繋がっていれば張力を加算する
        tension += np.where(rh0 == False, np.roll(pos, -1, axis=0) - pos + [ D0, 0], 0.0)
        # 左と繋がっていれば張力を加算する
        tension += np.where(rh1 == False, np.roll(pos, +1, axis=0) - pos + [-D0, 0], 0.0)
        # アンカーからの引っ張り
        tension -= pos * RUBBER_INTENSITY_ANCHOR

        tensionNorm = np.array([[np.linalg.norm(y) for y in x] for x in tension])
        if np.amax(tensionNorm) < LIMIT_STRESS:
            break
        # 結節点を張力の方向に移動する
        pos += tension * RUBBER_INTENSITY

        # ゴムの長さの更新
        diff = np.roll(pos, -1, axis=0) - pos + [EDGE_SIZE, 0]
        rubber_length_h = np.array([[np.linalg.norm(y) for y in x] for x in diff])
        diff = np.roll(pos, -1, axis=1) - pos + [0, EDGE_SIZE]
        rubber_length_v = np.array([[np.linalg.norm(y) for y in x] for x in diff])

    # メッシュを描画する
    draw.rectangle((0, 0, LATTICE_SIZE*D0, LATTICE_SIZE*D0), fill=(255, 255, 255, 0))
    for x in range(LATTICE_SIZE):
        for y in range(LATTICE_SIZE):
            p0 = pos[x, y] + [x*D0, y*D0]
            px = pos[(x+1) % LATTICE_SIZE , y] + [(x+1)*D0, y*D0]
            py = pos[x, (y+1) % LATTICE_SIZE] + [x*D0, (y+1)*D0]
            if rubber_cut_h[x, y] == False:
                draw.line(((p0[0], p0[1]), (px[0], px[1])), fill=(0, 0, 128))
            if rubber_cut_v[x, y] == False:
                draw.line(((p0[0], p0[1]), (py[0], py[1])), fill=(0, 0, 128))

    global gifimages
    if gifstatus == 1:
        # GIF用の画像を出力
        gifimages.append(created_image.copy())

def startGif(event):
    global gifimages, gifstatus
    print("start")
    gifstatus = 1
    gifimages = []

def stopGif(event):
    global gifimages, gifstatus
    print("end")
    gifstatus = 2

def writeGif(event):
    now = dt.now()
    nowstr = now.strftime('%Y%m%d%H%M%S')
    # GIF出力
    gifimages[0].save('%s_out.gif' % nowstr, save_all=True, append_images=gifimages)
    # パラメータの出力
    f = open('%s_param.txt' % nowstr, 'w', encoding='utf-8')
    f.write('LATTICE_SIZE = %d' % LATTICE_SIZE + '\n')
    f.write('EDGE_SIZE = %d' % EDGE_SIZE + '\n')
    f.write('LIMIT_AVR_H = %f' % LIMIT_AVR_H + '\n')
    f.write('LIMIT_AVR_V = %f' % LIMIT_AVR_V + '\n')
    f.write('LIMIT_DEV_H = %f' % LIMIT_DEV_H + '\n')
    f.write('LIMIT_DEV_V = %f' % LIMIT_DEV_V + '\n')
    f.write('LIMIT_H_SUB = %f' % LIMIT_H_SUB + '\n')
    f.write('LIMIT_V_SUB = %f' % LIMIT_V_SUB + '\n')
    f.write('RUBBER_INTENSITY = %f' % RUBBER_INTENSITY + '\n')
    f.write('RUBBER_INTENSITY_ANCHOR = %f' % RUBBER_INTENSITY_ANCHOR + '\n')
    f.write('LOOP_TIMES = %d' % LOOP_TIMES + '\n')
    f.write('LIMIT_STRESS = %f' % LIMIT_STRESS + '\n')
    f.close()
    print("出力完了")

root = tkinter.Tk()
wsize = (LATTICE_SIZE*D0, LATTICE_SIZE*D0)
app = TkDraw.Application(update, 'crack', master=root, size=wsize, buttonNames=['start', 'stop', 'write GIF file'], buttonHandlers=[startGif, stopGif, writeGif])
app.mainloop()
