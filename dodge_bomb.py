import os
import math
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数 : こうかとんRect or 爆弾Rect
    戻り値 : 判定結果タプル(横方向判定結果, 縦方向判定結果)
    True : 画面内 / False : 画面外
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None: 
    """
    引数：スクリーンSurface
    戻り値：なし
    ゲームオーバー画面を5秒間表示する
    """
    overlay = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(overlay, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    overlay.set_alpha(200)  # 半透明の黒い画面作成

    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)  # 泣きこうかとんの表示
    kk_rct_l = kk_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    kk_rct_r = kk_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))
    overlay.blit(kk_img, kk_rct_l)
    overlay.blit(kk_img, kk_rct_r)

    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))  # 白文字でGame Overの表示
    txt_rct = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    overlay.blit(txt, txt_rct)

    screen.blit(overlay, (0, 0))
    pg.display.update()
    time.sleep(5)  # 5秒間表示させる

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数 : なし
    戻り値：爆弾Surfaceリスト, 加速度リスト
    10段階の爆弾Surfaceリストと加速度リストを返す
    """
    bb_imgs = []
    for r in range(1, 11): # 爆弾Surfaceのリスト
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]  # 加速度のリスト
    return bb_imgs, bb_accs

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    引数：なし
    戻り値：移動量タプル: こうかとんSurface
    移動量タプルをキー、対応するこうかとんSurfaceを値とした辞書を返す
    """
    base_img = pg.image.load("fig/3.png")
    base_img_reverse = pg.transform.flip(base_img, True, False)  # 左向きのこうかとん画像を作成(上下右用)
    kk_dict = {
        (0,   0): pg.transform.rotozoom(base_img,   0, 1.0),  # 静止
        (+5,  0): base_img_reverse,  # 右
        (+5, -5): pg.transform.rotozoom(base_img_reverse,  45, 1.0),  # 右上
        (0,  -5): pg.transform.rotozoom(base_img_reverse,  90, 1.0),  # 上
        (-5, -5): pg.transform.rotozoom(base_img, -45, 1.0),  # 左上
        (-5,  0): base_img,  # 左
        (-5, +5): pg.transform.rotozoom(base_img, 45, 1.0),  # 左下
        (0,  +5): pg.transform.rotozoom(base_img_reverse, -90, 1.0),  # 下
        (+5, +5): pg.transform.rotozoom(base_img_reverse, -45, 1.0),  # 右下
    }
    return kk_dict

def calc_orientation(org: pg.Rect, dst: pg.Rect, current_xy: tuple[float, float],) -> tuple[float, float]:
    """
    引数：org=爆弾Rect, dst=こうかとんRect, current_xy=現在の速度方向
    戻り値：ノルム√50に正規化した(vx, vy)、距離300未満なら慣性でcurrent_xyを返す
    orgからdstへの正規化された方向ベクトルを返す
    """
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery
    norm = math.sqrt(dx ** 2 + dy ** 2)
    if norm < 300:  # 距離300未満なら現在の方向を維持させる
        return current_xy
    scale = math.sqrt(50) / norm
    return dx * scale, dy * scale



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    
    bg_img = pg.image.load("fig/pg_bg.jpg")   

    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()  
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()

    

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen) # ゲームオーバー画面を表示を呼び出す
            return

        screen.blit(bg_img, [0, 0]) 


        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, (dx, dy) in DELTA.items():
             if key_lst[key]:
                  sum_mv[0] += dx
                  sum_mv[1] += dy
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        kk_img = kk_imgs[tuple(sum_mv) if tuple(sum_mv) in kk_imgs else (0, 0)]
        screen.blit(kk_img, kk_rct)

        stage = min(tmr // 500, 9)  # 500フレームごとに段階アップ（最大9）
        bb_img = bb_imgs[stage]

        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))

        acc_vx = vx * bb_accs[stage]  # 加速度を掛けた実際の速度
        acc_vy = vy * bb_accs[stage]

        bb_rct.move_ip(acc_vx, acc_vy)
        bb_rct.width = bb_img.get_rect().width  # Rectサイズを爆弾に合わせて更新
        bb_rct.height = bb_img.get_rect().height
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
