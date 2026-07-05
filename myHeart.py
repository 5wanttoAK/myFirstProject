import tkinter as tk, random, time, sys, math

'''
"我喜欢你", "好好爱自己", "好好吃饭", "好想牵你手",
        "我想你了", "顺顺利利", "别熬夜", "我想和你在一起",
        "你笑起来真好看", "你是最可爱的", "想牵你的手", "不许偷偷难过",
        "下雨我来送伞", "累了我的肩给你", "你是我的幸运", "想和你在一起",
        "你无可替代", "你开心我就开心", "想你已成本能", "永远保护你",
        "你是我整个世界", "满眼都是你", "有你就很幸福", "今天也超爱你",
        "你最最重要", "牵了手不放开", "你是我的宝贝", "一想到你就开心",
        "有你的未来真好", "你不许生病", "你是人间值得", "你在我心最高位",
        "永远第一喜欢你", "你值得最好的", "你是我的勇气", "想一直陪着你",
        "你在哪哪是家", "余生都是你", "你是我全部温柔", "星星不如你",
        "只对你心动", "你是我唯一答案", "想和你白头", "你是我的光",
        "照顾好自己", "我永远在", "按时吃饭", "别着凉了",
        "早点休息", "好好睡一觉", "你值得被宠爱", "I love you"
'''

hearts, all_wins = [], []
tips = ['文案']

colors = ["pink", "lightblue", "lightgreen", "lemonchiffon",
          "hotpink", "skyblue"]


def heart_points(n, screen_w, screen_h):
    """生成心形曲线上的 n 个屏幕坐标点"""
    points = []
    for i in range(n):
        t = i / n * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = (13 * math.cos(t) - 5 * math.cos(2*t)
             - 2 * math.cos(3*t) - math.cos(4*t))
        sx = int(screen_w / 2 + x * 24 - 60)
        sy = int(screen_h / 2 - y * 24 - 50)
        sx = max(0, min(sx, screen_w - 150))
        sy = max(0, min(sy, screen_h - 60))
        points.append((sx, sy))
    return points


def create_popup(x, y, tip=None):
    """在指定位置创建一个弹窗"""
    win = tk.Toplevel()
    win.geometry(f"150x60+{x}+{y}")
    win.title("提示")
    win.attributes('-topmost', 1)
    text = tip or random.choice(tips)
    bg = random.choice(colors)
    tk.Label(win, text=text, bg=bg,
             font=("微软雅黑", 14), width=20, height=3).pack()
    win.bind('<space>',
             lambda e: [w.destroy() for w in hearts + all_wins] or sys.exit())
    return win


def main():
    root = tk.Tk()
    root.withdraw()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    # ---- 阶段一：爱心绽放 ----
    # 中间弹窗文案  充实自己
    points = heart_points(120, sw, sh)
    for i, (x, y) in enumerate(points):
        tip = "文案" if i == len(points) - 1 else None
        win = create_popup(x, y, tip)
        hearts.append(win)
        root.update()
        time.sleep(0.02)

    time.sleep(1)
    for w in hearts:
        if isinstance(w, tk.Toplevel) and w.winfo_exists():
            w.destroy()

    # ---- 阶段二：满屏暴击 ----
    count = sw // 150 * sh // 40 + 50
    for _ in range(count):
        x = random.randint(0, sw - 150)
        y = random.randint(0, sh - 60)
        win = create_popup(x, y)
        all_wins.append(win)
        root.update()
        time.sleep(0.005)

    time.sleep(6)

    # ---- 阶段三：优雅关闭 ----
    interval = 1.0 / len(all_wins) if all_wins else 0
    for win in all_wins:
        if isinstance(win, tk.Toplevel) and win.winfo_exists():
            win.destroy()
        root.update()
        time.sleep(interval)

    root.mainloop()


if __name__ == "__main__":
    main()
