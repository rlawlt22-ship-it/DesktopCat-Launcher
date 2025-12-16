import tkinter as tk
from tkinter import simpledialog
import random
import time
import webbrowser
import os

class DesktopCat:
    def __init__(self):
        self.window = tk.Tk()

        # --- 1. 윈도우 설정 ---
        self.window.title("Custom Cat Launcher")
        self.window.overrideredirect(True) 
        self.window.attributes('-topmost', True) 
        self.window.attributes('-transparentcolor', 'fuchsia')
        self.window.config(bg='fuchsia')

        self.width = 220
        self.height = 220
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.x = screen_width - 250
        self.y = screen_height - 250
        self.window.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')

        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, 
                                bg='fuchsia', highlightthickness=0)
        self.canvas.pack()

        # --- 2. 데이터 초기화 ---
        self.last_interaction = time.time()
        self.is_sleeping = False
        self.particles = []
        self.anim_state = False # 발 움직임 제어용

        # 즐겨찾기 목록 불러오기 (비어있으면 자동복구 기능 추가)
        self.bookmarks = []
        self.load_bookmarks()

        # 메뉴 미리 만들기
        self.create_menu()

        # --- 3. 고양이 그리기 ---
        self.draw_cat()

        # --- 4. 이벤트 연결 ---
        self.canvas.bind('<Button-1>', self.handle_click)
        self.canvas.bind('<B1-Motion>', self.do_move)
        self.canvas.bind('<Button-3>', self.show_menu) # 우클릭
        self.canvas.bind('<Enter>', self.wake_up)

        self.update_loop()
        self.window.mainloop()

    def load_bookmarks(self):
        self.bookmarks = []
        
        # 1. 파일이 있으면 읽어오기
        if os.path.exists("bookmarks.txt"):
            try:
                with open("bookmarks.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split("|")
                        if len(parts) == 2:
                            self.bookmarks.append({"name": parts[0], "target": parts[1]})
            except:
                pass

        # 2. ★수정됨★: 읽었는데 목록이 텅 비어있으면 기본값 강제 로드
        if not self.bookmarks:
            defaults = [
                "구글|https://www.google.com",
                "유튜브|https://www.youtube.com",
                "계산기|calc",
                "메모장|notepad"
            ]
            for d in defaults:
                parts = d.split("|")
                self.bookmarks.append({"name": parts[0], "target": parts[1]})
            
            # 복구된 내용을 파일에 저장
            self.save_bookmarks_to_file()

    def save_bookmarks_to_file(self):
        with open("bookmarks.txt", "w", encoding="utf-8") as f:
            for bm in self.bookmarks:
                f.write(f"{bm['name']}|{bm['target']}\n")

    def create_menu(self):
        self.menu = tk.Menu(self.window, tearoff=0)
        
        self.menu.add_command(label="★ 내 즐겨찾기", state="disabled")
        for bm in self.bookmarks:
            self.menu.add_command(label=f"🚀 {bm['name']}", command=lambda t=bm['target']: self.run_bookmark(t))
        
        self.menu.add_separator()
        self.menu.add_command(label="➕ 메뉴 추가하기", command=self.add_bookmark)
        self.menu.add_command(label="🗑️ 메뉴 삭제하기", command=self.delete_bookmark_window)
        self.menu.add_separator()
        self.menu.add_command(label="🎨 색깔 바꾸기", command=self.change_color)
        self.menu.add_command(label="❌ 종료", command=self.window.quit)

    def show_menu(self, event):
        self.create_menu()
        try:
            self.menu.post(event.x_root, event.y_root)
        except:
            pass

    def add_bookmark(self):
        name = simpledialog.askstring("설정", "추가할 메뉴 이름을 입력하세요:\n(예: 학교 홈페이지)")
        if not name: return
        target = simpledialog.askstring("설정", "실행할 주소나 명령어를 입력하세요:\n(예: https://... 또는 calc)")
        if not target: return

        self.bookmarks.append({"name": name, "target": target})
        self.save_bookmarks_to_file()
        self.show_message("추가 완료!")

    def delete_bookmark_window(self):
        del_win = tk.Toplevel(self.window)
        del_win.title("메뉴 삭제")
        del_win.geometry("250x300")
        
        lbl = tk.Label(del_win, text="삭제할 메뉴를 선택하세요:")
        lbl.pack(pady=5)

        listbox = tk.Listbox(del_win)
        listbox.pack(expand=True, fill="both", padx=10, pady=5)

        for bm in self.bookmarks:
            listbox.insert(tk.END, bm['name'])

        def delete_selected():
            selection = listbox.curselection()
            if not selection: return
            
            idx = selection[0]
            del self.bookmarks[idx]
            self.save_bookmarks_to_file()
            
            listbox.delete(idx)
            self.show_message("삭제 완료!")

        btn = tk.Button(del_win, text="삭제하기", command=delete_selected, bg="#FF6969", fg="white")
        btn.pack(pady=10)

    def run_bookmark(self, target):
        try:
            if target.startswith("http"):
                webbrowser.open(target)
            else:
                os.startfile(target)
        except:
            self.show_message("실행 실패 ㅠㅠ")

    def draw_cat(self):
        self.color_body = '#FFD700' 
        self.color_outline = '#8B4513'

        self.tail = self.canvas.create_line(120, 110, 160, 70, width=12, fill=self.color_outline, smooth=True, capstyle='round')
        self.tail_inner = self.canvas.create_line(120, 110, 158, 72, width=8, fill=self.color_body, smooth=True, capstyle='round')
        self.leg_l = self.canvas.create_oval(60, 140, 80, 155, fill='white', outline=self.color_outline)
        self.leg_r = self.canvas.create_oval(110, 140, 130, 155, fill='white', outline=self.color_outline)
        self.body = self.canvas.create_oval(50, 70, 140, 150, fill=self.color_body, outline=self.color_outline, width=2)
        self.ear_l = self.canvas.create_polygon(65, 80, 55, 45, 90, 70, fill=self.color_body, outline=self.color_outline, smooth=True)
        self.ear_r = self.canvas.create_polygon(125, 80, 135, 45, 100, 70, fill=self.color_body, outline=self.color_outline, smooth=True)
        
        self.eye_l_bg = self.canvas.create_oval(75, 95, 92, 112, fill='black', outline='')
        self.eye_r_bg = self.canvas.create_oval(108, 95, 125, 112, fill='black', outline='')
        self.eye_l_dot = self.canvas.create_oval(80, 100, 86, 106, fill='white', outline='') 
        self.eye_l_dot_s = self.canvas.create_oval(86, 107, 89, 110, fill='white', outline='') 
        self.eye_r_dot = self.canvas.create_oval(113, 100, 119, 106, fill='white', outline='')
        self.eye_r_dot_s = self.canvas.create_oval(119, 107, 122, 110, fill='white', outline='')

        self.eye_happy_l = self.canvas.create_line(78, 105, 85, 100, 92, 105, width=2, smooth=True, state='hidden', fill=self.color_outline)
        self.eye_happy_r = self.canvas.create_line(111, 105, 118, 100, 125, 105, width=2, smooth=True, state='hidden', fill=self.color_outline)
        self.eye_sleep_l = self.canvas.create_line(78, 108, 92, 108, width=2, state='hidden', fill=self.color_outline)
        self.eye_sleep_r = self.canvas.create_line(111, 108, 125, 108, width=2, state='hidden', fill=self.color_outline)

        self.nose = self.canvas.create_polygon(97, 112, 103, 112, 100, 116, fill='#FFB6C1', outline='')
        self.mouth = self.canvas.create_text(100, 120, text="ω", font=("Arial", 10, "bold"), fill=self.color_outline)
        self.cheek_l = self.canvas.create_oval(65, 110, 75, 120, fill='#FFB6C1', outline='', state='hidden')
        self.cheek_r = self.canvas.create_oval(130, 110, 140, 120, fill='#FFB6C1', outline='', state='hidden')

        self.canvas.create_line(60, 110, 40, 105, width=1, fill=self.color_outline)
        self.canvas.create_line(60, 118, 40, 118, width=1, fill=self.color_outline)
        self.canvas.create_line(140, 110, 160, 105, width=1, fill=self.color_outline)
        self.canvas.create_line(140, 118, 160, 118, width=1, fill=self.color_outline)

        self.bubble_bg = self.canvas.create_rectangle(0,0,0,0, fill="white", outline=self.color_outline, state='hidden')
        self.bubble_text = self.canvas.create_text(100, 40, text="", font=("Malgun Gothic", 9, "bold"), state='hidden')

    def handle_click(self, event):
        self.last_x = event.x
        self.last_y = event.y
        self.wake_up(event)
        for _ in range(4): self.create_effect(event.x, event.y - 30)
        self.set_expression("happy")
        msgs = ["냐옹~", "그릉그릉", "반가워!", "헤헤", "식빵 굽는 중", "기분 좋아!"]
        self.show_message(random.choice(msgs))
        self.window.after(800, lambda: self.set_expression("normal") if not self.is_sleeping else None)

    def do_move(self, event):
        x_diff = event.x - self.last_x
        y_diff = event.y - self.last_y
        self.x += x_diff
        self.y += y_diff
        self.window.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')
        self.last_interaction = time.time()

    def change_color(self):
        colors = ['#FFD700', '#FFFFFF', '#87CEEB', '#FFB6C1', '#98FB98', '#E6E6FA', '#A9A9A9'] 
        new_color = random.choice(colors)
        self.canvas.itemconfig(self.body, fill=new_color)
        self.canvas.itemconfig(self.ear_l, fill=new_color)
        self.canvas.itemconfig(self.ear_r, fill=new_color)
        self.canvas.itemconfig(self.tail_inner, fill=new_color)
        self.show_message("변신!")

    def set_expression(self, exp):
        items = [self.eye_l_bg, self.eye_r_bg, self.eye_l_dot, self.eye_r_dot, self.eye_l_dot_s, self.eye_r_dot_s,
                 self.eye_happy_l, self.eye_happy_r, self.eye_sleep_l, self.eye_sleep_r, self.cheek_l, self.cheek_r]
        for item in items: self.canvas.itemconfig(item, state='hidden')

        if exp == "normal":
            for item in [self.eye_l_bg, self.eye_r_bg, self.eye_l_dot, self.eye_r_dot, self.eye_l_dot_s, self.eye_r_dot_s]:
                self.canvas.itemconfig(item, state='normal')
        elif exp == "happy":
            self.canvas.itemconfig(self.eye_happy_l, state='normal')
            self.canvas.itemconfig(self.eye_happy_r, state='normal')
            self.canvas.itemconfig(self.cheek_l, state='normal')
            self.canvas.itemconfig(self.cheek_r, state='normal')
        elif exp == "sleep":
            self.canvas.itemconfig(self.eye_sleep_l, state='normal')
            self.canvas.itemconfig(self.eye_sleep_r, state='normal')

    def create_effect(self, x, y):
        symbols = ["♪", "★", "✨", "☁️"]
        colors = ['#FFD700', '#87CEEB', '#FF69B4', '#FFA500']
        p = self.canvas.create_text(x + random.randint(-15, 15), y + random.randint(-15, 15), 
                                    text=random.choice(symbols), fill=random.choice(colors), font=("Arial", random.randint(12, 18), "bold"))
        self.particles.append({'id': p, 'life': 20, 'speed': random.randint(3, 5)})

    def show_message(self, text):
        self.canvas.itemconfig(self.bubble_text, text=text, state='normal')
        bbox = self.canvas.bbox(self.bubble_text)
        if bbox:
            self.canvas.coords(self.bubble_bg, bbox[0]-8, bbox[1]-4, bbox[2]+8, bbox[3]+4)
            self.canvas.itemconfig(self.bubble_bg, state='normal')
            self.canvas.tag_raise(self.bubble_text)
        self.last_interaction = time.time()
        self.window.after(2000, lambda: self.canvas.itemconfig(self.bubble_bg, state='hidden') or self.canvas.itemconfig(self.bubble_text, state='hidden'))

    def wake_up(self, event=None):
        if self.is_sleeping:
            self.is_sleeping = False
            self.set_expression("normal")
            self.show_message("오잉?")
        self.last_interaction = time.time()

    def update_loop(self):
        # 1. 파티클(이펙트) 업데이트
        for p in self.particles[:]:
            self.canvas.move(p['id'], 0, -p['speed'])
            p['life'] -= 1
            if p['life'] <= 0:
                self.canvas.delete(p['id'])
                self.particles.remove(p)

        # 2. 졸음 모드 체크
        if not self.is_sleeping and time.time() - self.last_interaction > 15:
            self.is_sleeping = True
            self.set_expression("sleep")
            self.show_message("Zzz...")

        # 3. ★ 발/꼬리 움직임 (Drift 방지 적용됨)
        if not self.is_sleeping:
            should_move = int(time.time() * 5) % 2 == 0
            
            if should_move and not self.anim_state:
                self.canvas.move(self.leg_l, 0, 3)   
                self.canvas.move(self.leg_r, 0, -3)  
                self.canvas.move(self.tail, 2, 0)        
                self.canvas.move(self.tail_inner, 2, 0)
                self.anim_state = True
            
            elif not should_move and self.anim_state:
                self.canvas.move(self.leg_l, 0, -3)  
                self.canvas.move(self.leg_r, 0, 3)   
                self.canvas.move(self.tail, -2, 0)       
                self.canvas.move(self.tail_inner, -2, 0)
                self.anim_state = False
        
        self.window.after(50, self.update_loop)

if __name__ == '__main__':
    DesktopCat()