import os
import random
import sys
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
    pg.time.wait(5000)  # 5秒間表示させる

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    
    bg_img = pg.image.load("fig/pg_bg.jpg")   

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
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

        
        bb_rct.move_ip(vx, vy)
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
