import json
import os
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

APP_TITLE = "선생님 업무 도구함"


class TeacherToolkit(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1040x720")
        self.minsize(860, 600)
        self.configure(bg="#f3f6fb")
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self._style_widgets()
        self.timer_remaining = 0
        self.timer_running = False
        self.timer_end = None
        self.stopwatch_running = False
        self.stopwatch_start = 0.0
        self.stopwatch_elapsed = 0.0
        self.alarms = []
        self.alarm_fired = set()
        self.drawn_names = set()
        self._build_shell()
        self._build_pages()
        self.show_page("홈")
        self._tick()

    def _style_widgets(self):
        self.style.configure("TFrame", background="#f3f6fb")
        self.style.configure("Card.TFrame", background="white")
        self.style.configure("TLabel", background="#f3f6fb", foreground="#172033", font=("Malgun Gothic", 10))
        self.style.configure("Title.TLabel", font=("Malgun Gothic", 22, "bold"), foreground="#172033")
        self.style.configure("Sub.TLabel", font=("Malgun Gothic", 10), foreground="#64748b")
        self.style.configure("CardTitle.TLabel", background="white", font=("Malgun Gothic", 13, "bold"), foreground="#172033")
        self.style.configure("CardText.TLabel", background="white", foreground="#526079")
        self.style.configure("TButton", font=("Malgun Gothic", 10), padding=(12, 8))
        self.style.configure("Accent.TButton", background="#315ee7", foreground="white", font=("Malgun Gothic", 10, "bold"))
        self.style.map("Accent.TButton", background=[("active", "#244bc2")], foreground=[("active", "white")])
        self.style.configure("Nav.TButton", background="#17233b", foreground="#dbe5ff", anchor="w", padding=(16, 11), font=("Malgun Gothic", 10))
        self.style.map("Nav.TButton", background=[("active", "#26385b")], foreground=[("active", "white")])
        self.style.configure("TEntry", padding=9, font=("Malgun Gothic", 10))
        self.style.configure("TCombobox", padding=7)

    def _build_shell(self):
        self.sidebar = tk.Frame(self, bg="#17233b", width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar, text="교실 도구함", bg="#17233b", fg="white", font=("Malgun Gothic", 17, "bold")).pack(anchor="w", padx=20, pady=(26, 2))
        tk.Label(self.sidebar, text="선생님의 하루를 가볍게", bg="#17233b", fg="#9dafd1", font=("Malgun Gothic", 9)).pack(anchor="w", padx=21, pady=(0, 22))
        self.nav_items = ["홈", "QR 코드", "AI 대화", "스톱워치", "타이머", "시계·알람", "학생 뽑기"]
        for name in self.nav_items:
            ttk.Button(self.sidebar, text="  " + name, style="Nav.TButton", command=lambda n=name: self.show_page(n)).pack(fill="x", padx=10, pady=2)
        tk.Label(self.sidebar, text="개인용 도구 · 데이터는 내 PC에", bg="#17233b", fg="#8ea0c3", font=("Malgun Gothic", 8), wraplength=175, justify="left").pack(side="bottom", anchor="w", padx=18, pady=18)
        self.main = ttk.Frame(self, padding=(28, 24))
        self.main.pack(side="left", fill="both", expand=True)
        self.page_area = ttk.Frame(self.main)
        self.page_area.pack(fill="both", expand=True)
        self.pages = {}

    def _build_pages(self):
        self._make_home()
        self._make_qr()
        self._make_ai()
        self._make_stopwatch()
        self._make_timer()
        self._make_clock()
        self._make_picker()

    def _page(self, name, title, subtitle):
        page = ttk.Frame(self.page_area)
        ttk.Label(page, text=title, style="Title.TLabel").pack(anchor="w")
        ttk.Label(page, text=subtitle, style="Sub.TLabel").pack(anchor="w", pady=(4, 20))
        self.pages[name] = page
        return page

    def _card(self, parent, padding=20):
        frame = ttk.Frame(parent, style="Card.TFrame", padding=padding)
        frame.pack(fill="x", pady=(0, 14))
        return frame

    def show_page(self, name):
        for child in self.page_area.winfo_children():
            child.pack_forget()
        self.pages[name].pack(fill="both", expand=True)
        self.current_page = name

    def _make_home(self):
        p = self._page("홈", "안녕하세요, 선생님 👋", "수업 준비와 교실 운영에 자주 쓰는 도구를 한곳에 모았습니다.")
        card = self._card(p, 22)
        ttk.Label(card, text="오늘 바로 쓸 수 있어요", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text="QR 코드를 만들고, 수업 시간을 재고, 학생 순서를 공정하게 정해 보세요.", style="CardText.TLabel").pack(anchor="w", pady=(8, 16))
        grid = ttk.Frame(card, style="Card.TFrame")
        grid.pack(fill="x")
        entries = [("QR 코드", "링크·문구를 QR 이미지로 저장"), ("AI 대화", "수업 자료와 안내문 초안 만들기"), ("타이머", "활동별 남은 시간 확인"), ("학생 뽑기", "발표·모둠 순서 무작위 선정")]
        for i, (name, desc) in enumerate(entries):
            cell = ttk.Frame(grid, style="Card.TFrame", padding=10)
            cell.grid(row=i // 2, column=i % 2, sticky="nsew", padx=5, pady=4)
            ttk.Label(cell, text=name, style="CardTitle.TLabel").pack(anchor="w")
            ttk.Label(cell, text=desc, style="CardText.TLabel").pack(anchor="w", pady=(4, 8))
            ttk.Button(cell, text="열기 →", command=lambda n=name: self.show_page(n)).pack(anchor="w")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        ttk.Label(p, text="도구 사용 안내", style="CardTitle.TLabel").pack(anchor="w", pady=(12, 8))
        ttk.Label(p, text="• AI 대화에는 OpenAI API 키가 필요합니다. 앱에는 키를 저장하지 않습니다.\n• QR 이미지는 PNG 파일로 저장할 수 있습니다.\n• 알람과 타이머는 앱이 실행 중일 때 울립니다.", justify="left").pack(anchor="w")

    def _make_qr(self):
        p = self._page("QR 코드", "QR 코드 만들기", "웹 주소, 설문 링크, 안내 문구를 이미지로 저장합니다.")
        c = self._card(p)
        ttk.Label(c, text="QR에 담을 내용", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))
        self.qr_text = tk.Text(c, height=5, wrap="word", font=("Malgun Gothic", 10), relief="solid", bd=1, padx=8, pady=8)
        self.qr_text.pack(fill="x")
        row = ttk.Frame(c, style="Card.TFrame")
        row.pack(fill="x", pady=(12, 0))
        ttk.Label(row, text="크기").pack(side="left")
        self.qr_size = ttk.Combobox(row, values=["작게", "보통", "크게"], state="readonly", width=10)
        self.qr_size.current(1)
        self.qr_size.pack(side="left", padx=8)
        ttk.Button(row, text="PNG로 저장", style="Accent.TButton", command=self.create_qr).pack(side="right")
        self.qr_preview = ttk.Label(p, text="미리보기는 파일 저장 후 표시됩니다.")
        self.qr_preview.pack(anchor="w", pady=8)

    def create_qr(self):
        content = self.qr_text.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("내용 입력", "QR 코드에 담을 주소나 문구를 입력해 주세요.")
            return
        try:
            import qrcode
            from PIL import ImageTk
            scale = {"작게": 5, "보통": 8, "크게": 12}[self.qr_size.get()]
            qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=scale, border=4)
            qr.add_data(content)
            qr.make(fit=True)
            image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG 이미지", "*.png")], initialfile="수업자료_QR.png")
            if not path:
                return
            image.save(path)
            thumb = image.copy()
            thumb.thumbnail((240, 240))
            self.qr_image_ref = ImageTk.PhotoImage(thumb)
            self.qr_preview.configure(image=self.qr_image_ref, text="")
            messagebox.showinfo("저장 완료", f"QR 이미지를 저장했습니다.\n{path}")
        except Exception as exc:
            messagebox.showerror("QR 생성 오류", f"QR 코드를 만들지 못했습니다.\n{exc}")

    def _make_ai(self):
        p = self._page("AI 대화", "AI 대화", "수업 아이디어, 가정통신문 초안, 활동지 문항을 함께 정리해 보세요.")
        c = self._card(p, 14)
        top = ttk.Frame(c, style="Card.TFrame")
        top.pack(fill="x", pady=(0, 8))
        ttk.Label(top, text="API 키").pack(side="left")
        self.api_key = ttk.Entry(top, show="•", width=42)
        self.api_key.pack(side="left", padx=8)
        self.api_key.insert(0, os.getenv("OPENAI_API_KEY", ""))
        ttk.Label(top, text="모델").pack(side="left", padx=(10, 4))
        self.ai_model = ttk.Entry(top, width=17)
        self.ai_model.insert(0, "gpt-4o-mini")
        self.ai_model.pack(side="left")
        ttk.Label(c, text="대화 내용", style="CardTitle.TLabel").pack(anchor="w", pady=(4, 6))
        self.chat_log = tk.Text(c, height=17, wrap="word", state="disabled", font=("Malgun Gothic", 10), relief="solid", bd=1, padx=10, pady=8)
        self.chat_log.pack(fill="both", expand=True)
        bottom = ttk.Frame(c, style="Card.TFrame")
        bottom.pack(fill="x", pady=(9, 0))
        self.chat_input = ttk.Entry(bottom)
        self.chat_input.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.chat_input.bind("<Return>", lambda _e: self.send_chat())
        self.chat_send = ttk.Button(bottom, text="보내기", style="Accent.TButton", command=self.send_chat)
        self.chat_send.pack(side="right")
        ttk.Label(p, text="API 키는 이번 실행 중에만 입력값으로 사용합니다. OpenAI API 사용량에 따라 별도 비용이 발생할 수 있습니다.", style="Sub.TLabel").pack(anchor="w")
        self.chat_history = []

    def _append_chat(self, who, text):
        self.chat_log.configure(state="normal")
        self.chat_log.insert("end", f"{who}\n{text}\n\n")
        self.chat_log.see("end")
        self.chat_log.configure(state="disabled")

    def send_chat(self):
        key = self.api_key.get().strip()
        prompt = self.chat_input.get().strip()
        model = self.ai_model.get().strip() or "gpt-4o-mini"
        if not key:
            messagebox.showinfo("API 키 필요", "OpenAI API 키를 입력해 주세요. 키는 앱에 저장되지 않습니다.")
            return
        if not prompt:
            return
        self.chat_input.delete(0, "end")
        self._append_chat("선생님", prompt)
        self.chat_history.append({"role": "user", "content": prompt})
        self.chat_send.configure(state="disabled")
        self._append_chat("AI", "답변을 작성하고 있습니다…")

        def request_answer():
            try:
                payload = {"model": model, "messages": [{"role": "system", "content": "당신은 초등학교 교사의 업무를 돕는 한국어 교육 보조자입니다. 학생 개인정보를 요구하지 말고, 수업에 바로 쓸 수 있게 명확하고 연령에 맞게 답하세요."}] + self.chat_history[-12:], "temperature": 0.7}
                request = Request("https://api.openai.com/v1/chat/completions", data=json.dumps(payload).encode("utf-8"), headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, method="POST")
                with urlopen(request, timeout=90) as response:
                    data = json.loads(response.read().decode("utf-8"))
                answer = data["choices"][0]["message"]["content"].strip()
                self.chat_history.append({"role": "assistant", "content": answer})
                self.after(0, lambda: self._finish_chat(answer))
            except HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")[:600]
                error_text = f"요청을 처리하지 못했습니다 (HTTP {exc.code}).\n{detail}"
                self.after(0, lambda message=error_text: self._finish_chat(message))
            except (URLError, TimeoutError) as exc:
                error_text = f"인터넷 연결 또는 서버 응답을 확인해 주세요.\n{exc}"
                self.after(0, lambda message=error_text: self._finish_chat(message))
            except Exception as exc:
                error_text = f"오류가 발생했습니다.\n{exc}"
                self.after(0, lambda message=error_text: self._finish_chat(message))
        threading.Thread(target=request_answer, daemon=True).start()

    def _finish_chat(self, answer):
        self._append_chat("AI", answer)
        self.chat_send.configure(state="normal")

    def _make_stopwatch(self):
        p = self._page("스톱워치", "스톱워치", "발표 시간, 실험 시간, 모둠 활동 시간을 재어 보세요.")
        c = self._card(p, 28)
        self.stopwatch_display = ttk.Label(c, text="00:00.0", style="Title.TLabel", background="white", font=("Malgun Gothic", 52, "bold"))
        self.stopwatch_display.pack(pady=(28, 24))
        row = ttk.Frame(c, style="Card.TFrame")
        row.pack(pady=(0, 24))
        self.stopwatch_toggle = ttk.Button(row, text="시작", style="Accent.TButton", command=self.toggle_stopwatch)
        self.stopwatch_toggle.pack(side="left", padx=5)
        ttk.Button(row, text="초기화", command=self.reset_stopwatch).pack(side="left", padx=5)

    def toggle_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_elapsed += time.perf_counter() - self.stopwatch_start
            self.stopwatch_running = False
            self.stopwatch_toggle.configure(text="시작")
        else:
            self.stopwatch_start = time.perf_counter()
            self.stopwatch_running = True
            self.stopwatch_toggle.configure(text="일시정지")

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0.0
        self.stopwatch_toggle.configure(text="시작")
        self.stopwatch_display.configure(text="00:00.0")

    def _make_timer(self):
        p = self._page("타이머", "수업 타이머", "분과 초를 설정하고 활동 시간을 관리하세요.")
        c = self._card(p, 26)
        row = ttk.Frame(c, style="Card.TFrame")
        row.pack(pady=(14, 8))
        self.timer_minutes = ttk.Entry(row, width=7, justify="center")
        self.timer_minutes.insert(0, "5")
        self.timer_minutes.pack(side="left")
        ttk.Label(row, text="분").pack(side="left", padx=(5, 16))
        self.timer_seconds = ttk.Entry(row, width=7, justify="center")
        self.timer_seconds.insert(0, "0")
        self.timer_seconds.pack(side="left")
        ttk.Label(row, text="초").pack(side="left", padx=5)
        self.timer_display = ttk.Label(c, text="05:00", style="Title.TLabel", background="white", font=("Malgun Gothic", 48, "bold"))
        self.timer_display.pack(pady=18)
        buttons = ttk.Frame(c, style="Card.TFrame")
        buttons.pack(pady=(0, 14))
        ttk.Button(buttons, text="시작", style="Accent.TButton", command=self.start_timer).pack(side="left", padx=5)
        ttk.Button(buttons, text="일시정지", command=self.pause_timer).pack(side="left", padx=5)
        ttk.Button(buttons, text="초기화", command=self.reset_timer).pack(side="left", padx=5)
        self.timer_status = ttk.Label(c, text="활동 시간을 입력한 뒤 시작하세요.", style="CardText.TLabel")
        self.timer_status.pack(pady=(0, 5))

    def start_timer(self):
        if not self.timer_running:
            if self.timer_remaining <= 0:
                try:
                    mins = int(self.timer_minutes.get())
                    secs = int(self.timer_seconds.get())
                    self.timer_remaining = mins * 60 + secs
                except ValueError:
                    messagebox.showinfo("시간 입력", "분과 초를 숫자로 입력해 주세요.")
                    return
            if self.timer_remaining <= 0:
                messagebox.showinfo("시간 입력", "0보다 큰 시간을 입력해 주세요.")
                return
            self.timer_end = time.monotonic() + self.timer_remaining
            self.timer_running = True
            self.timer_status.configure(text="타이머가 실행 중입니다.")

    def pause_timer(self):
        if self.timer_running:
            self.timer_remaining = max(0, int(self.timer_end - time.monotonic() + 0.999))
            self.timer_running = False
            self.timer_status.configure(text="일시정지했습니다.")

    def reset_timer(self):
        self.timer_running = False
        try:
            self.timer_remaining = int(self.timer_minutes.get()) * 60 + int(self.timer_seconds.get())
        except ValueError:
            self.timer_remaining = 0
        self._show_timer(self.timer_remaining)
        self.timer_status.configure(text="초기화했습니다.")

    def _show_timer(self, seconds):
        self.timer_display.configure(text=f"{seconds // 60:02d}:{seconds % 60:02d}")

    def _make_clock(self):
        p = self._page("시계·알람", "시계와 알람", "현재 시각을 확인하고 수업 전환 알람을 설정하세요.")
        c = self._card(p, 24)
        ttk.Label(c, text="현재 시각", style="CardTitle.TLabel").pack(anchor="w")
        self.clock_display = ttk.Label(c, text="00:00:00", style="Title.TLabel", background="white", font=("Malgun Gothic", 38, "bold"))
        self.clock_display.pack(anchor="w", pady=(8, 24))
        ttk.Label(c, text="알람 시각 (24시간제, 시:분)", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))
        row = ttk.Frame(c, style="Card.TFrame")
        row.pack(fill="x")
        self.alarm_time = ttk.Entry(row, width=12)
        self.alarm_time.insert(0, "09:00")
        self.alarm_time.pack(side="left")
        self.alarm_label = ttk.Entry(row, width=30)
        self.alarm_label.insert(0, "수업 준비")
        self.alarm_label.pack(side="left", padx=8)
        ttk.Button(row, text="알람 추가", style="Accent.TButton", command=self.add_alarm).pack(side="left")
        self.alarm_list = tk.Listbox(c, height=7, font=("Malgun Gothic", 10), relief="solid", bd=1)
        self.alarm_list.pack(fill="x", pady=(14, 8))
        ttk.Button(c, text="선택 알람 삭제", command=self.remove_alarm).pack(anchor="w")
        ttk.Label(p, text="알람이 울리려면 앱이 실행 중이어야 합니다.", style="Sub.TLabel").pack(anchor="w")

    def add_alarm(self):
        value = self.alarm_time.get().strip()
        try:
            datetime.strptime(value, "%H:%M")
        except ValueError:
            messagebox.showinfo("시간 형식", "알람 시각을 09:30처럼 입력해 주세요.")
            return
        label = self.alarm_label.get().strip() or "알람"
        self.alarms.append((value, label))
        self.alarm_list.insert("end", f"{value}  ·  {label}")

    def remove_alarm(self):
        selected = self.alarm_list.curselection()
        if selected:
            idx = selected[0]
            self.alarm_list.delete(idx)
            self.alarms.pop(idx)

    def _make_picker(self):
        p = self._page("학생 뽑기", "학생 무작위 뽑기", "이름 목록을 넣으면 중복 없이 한 명씩 뽑습니다.")
        c = self._card(p)
        ttk.Label(c, text="학생 이름 (쉼표 또는 줄바꿈으로 구분)", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))
        self.names_text = tk.Text(c, height=8, wrap="word", font=("Malgun Gothic", 10), relief="solid", bd=1, padx=8, pady=8)
        self.names_text.pack(fill="x")
        row = ttk.Frame(c, style="Card.TFrame")
        row.pack(fill="x", pady=(12, 0))
        ttk.Button(row, text="한 명 뽑기", style="Accent.TButton", command=self.pick_name).pack(side="left")
        ttk.Button(row, text="전체 다시 뽑기", command=self.reset_picker).pack(side="left", padx=8)
        self.picked_name = ttk.Label(c, text="오늘의 발표자는 누구일까요?", style="Title.TLabel", background="white")
        self.picked_name.pack(pady=20)
        self.picker_status = ttk.Label(c, text="", style="CardText.TLabel")
        self.picker_status.pack()

    def pick_name(self):
        import random
        names = [x.strip() for x in self.names_text.get("1.0", "end").replace(",", "\n").splitlines() if x.strip()]
        names = list(dict.fromkeys(names))
        if not names:
            messagebox.showinfo("이름 입력", "먼저 학생 이름을 입력해 주세요.")
            return
        remaining = [n for n in names if n not in self.drawn_names]
        if not remaining:
            self.picked_name.configure(text="모두 한 번씩 뽑혔어요!")
            self.picker_status.configure(text="전체 다시 뽑기를 누르면 새 순서로 시작합니다.")
            return
        chosen = random.choice(remaining)
        self.drawn_names.add(chosen)
        self.picked_name.configure(text=chosen)
        self.picker_status.configure(text=f"남은 학생: {len(remaining) - 1}명")

    def reset_picker(self):
        self.drawn_names.clear()
        self.picked_name.configure(text="다시 시작합니다!")
        self.picker_status.configure(text="아직 뽑지 않았습니다.")

    def _tick(self):
        now = datetime.now()
        if hasattr(self, "clock_display"):
            self.clock_display.configure(text=now.strftime("%H:%M:%S"))
        if self.stopwatch_running and hasattr(self, "stopwatch_display"):
            elapsed = self.stopwatch_elapsed + time.perf_counter() - self.stopwatch_start
            mins, sec = divmod(elapsed, 60)
            self.stopwatch_display.configure(text=f"{int(mins):02d}:{sec:04.1f}")
        if self.timer_running:
            self.timer_remaining = max(0, int(self.timer_end - time.monotonic() + 0.999))
            self._show_timer(self.timer_remaining)
            if self.timer_remaining == 0:
                self.timer_running = False
                self.timer_status.configure(text="시간이 끝났습니다!")
                self.bell()
                messagebox.showinfo("타이머 종료", "설정한 시간이 끝났습니다.")
        minute_key = now.strftime("%Y-%m-%d %H:%M")
        for value, label in self.alarms:
            if now.strftime("%H:%M") == value and minute_key not in self.alarm_fired:
                self.alarm_fired.add(minute_key)
                self.bell()
                messagebox.showinfo("알람", f"{label}\n{value}")
        self.after(100, self._tick)


if __name__ == "__main__":
    TeacherToolkit().mainloop()
