import tkinter as tk
from tkinter import filedialog
import time


# ---------- Config ----------
FAKE_BTC_ADDRESS = "1FakeWannaCryLabAddressXXXXXXXXXXXXXXXX"
FAKE_BTC_AMOUNT  = "0.001 BTC"
COUNTDOWN_HOURS  = 3

# Simulation palette
BG        = "#1a0000"      # very dark red-black
PANEL     = "#2a0000"
RED       = "#c8102e"      # Classic alert red
RED_DARK  = "#8b0000"
WHITE     = "#f5f5f5"
YELLOW    = "#ffd700"
GREEN     = "#27ae60"
GREY      = "#888888"
# ----------------------------


class ImpactSimulator:
    def __init__(self, files_count, decrypt_callback):
        self.files_count = files_count
        self.decrypt_callback = decrypt_callback
        self.start = time.time()
        self.total = COUNTDOWN_HOURS * 3600
        self.alive = True  # Flag to stop the timer when window closes
        self.decrypt_window_open = False

        self.root = tk.Tk()
        self.root.title("Ooops! Your files have been encrypted")
        self.root.configure(bg=BG)
        self.root.geometry("820x680")
        self.root.minsize(760, 620)
        self.root.resizable(True, True)
        
        # Handle closing the window directly
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._tick()

    def _on_close(self):
        self.alive = False
        self.root.destroy()

    # ---------- UI construction ----------
    def _build_ui(self):
        # --- Header bar ---
        header = tk.Frame(self.root, bg=RED, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🔒  Ooops, your files have been encrypted!",
            bg=RED, fg=WHITE,
            font=("Helvetica", 20, "bold"),
        ).pack(pady=20)

        # --- LAB banner ---
        tk.Label(
            self.root,
            text="⚠  LAB / EDUCATIONAL SIMULATION — NO REAL PAYMENT  ⚠",
            bg=YELLOW, fg="#000000",
            font=("Helvetica", 11, "bold"),
            pady=6,
        ).pack(fill="x")

        # --- Main body ---
        body = tk.Frame(self.root, bg=BG, padx=30, pady=20)
        body.pack(fill="both", expand=True)

        self._section(body, "❓  What happened to my computer?",
                      "Your important files are encrypted.\n"
                      "Many of your documents, photos, videos, databases\n"
                      "and other files are no longer accessible because\n"
                      "they have been encrypted with a strong cipher.")

        # Files count
        count_frame = tk.Frame(body, bg=PANEL, padx=15, pady=10)
        count_frame.pack(fill="x", pady=(0, 15))
        tk.Label(
            count_frame,
            text=f"📁  Files encrypted in this folder:  {self.files_count}",
            bg=PANEL, fg=WHITE,
            font=("Helvetica", 13, "bold"),
        ).pack(anchor="w")

        # Payment section
        tk.Label(
            body, text="💰  What do I do?",
            bg=BG, fg=RED,
            font=("Helvetica", 15, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(5, 5))

        pay_panel = tk.Frame(body, bg=PANEL, padx=15, pady=12)
        pay_panel.pack(fill="x", pady=(0, 15))

        tk.Label(
            pay_panel,
            text=f"Send  {FAKE_BTC_AMOUNT}  to this address (LAB — DO NOT SEND):",
            bg=PANEL, fg=WHITE,
            font=("Helvetica", 11),
            anchor="w",
        ).pack(fill="x")

        addr_entry = tk.Entry(
            pay_panel,
            font=("Courier", 12, "bold"),
            bg="#111111", fg=YELLOW,
            insertbackground=YELLOW,
            relief="flat", bd=6,
        )
        addr_entry.insert(0, FAKE_BTC_ADDRESS)
        addr_entry.configure(state="readonly", readonlybackground="#111111")
        addr_entry.pack(fill="x", pady=6)

        # Countdown
        timer_panel = tk.Frame(body, bg=RED_DARK, padx=15, pady=12)
        timer_panel.pack(fill="x", pady=(0, 15))

        tk.Label(
            timer_panel,
            text="⏱  Time remaining until the price doubles:",
            bg=RED_DARK, fg=WHITE,
            font=("Helvetica", 11),
            anchor="w",
        ).pack(fill="x")

        self.timer_label = tk.Label(
            timer_panel,
            text="00:00:00",
            bg=RED_DARK, fg=YELLOW,
            font=("Courier", 26, "bold"),
        )
        self.timer_label.pack()

        # --- Buttons ---
        btn_frame = tk.Frame(body, bg=BG)
        btn_frame.pack(fill="x", pady=15)

        self._button(btn_frame, "🔓  Decrypt (private key)", GREEN,
                     self._open_decrypt_dialog).pack(side="left", padx=6)
        self._button(btn_frame, "✖  Quit", "#444444",
                     self._on_close).pack(side="right", padx=6)

    def _section(self, parent, title, text):
        tk.Label(
            parent, text=title,
            bg=BG, fg=RED,
            font=("Helvetica", 15, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 5))
        tk.Label(
            parent, text=text,
            bg=BG, fg=WHITE,
            font=("Helvetica", 11),
            justify="left", anchor="w",
        ).pack(fill="x", pady=(0, 15))

    def _button(self, parent, text, color, command):
        return tk.Button(
            parent, text=text, command=command,
            bg=color, fg=WHITE,
            activebackground=color, activeforeground=WHITE,
            font=("Helvetica", 12, "bold"),
            relief="flat", bd=0,
            padx=18, pady=10,
            cursor="hand2",
        )

    # ---------- Countdown ----------
    def _tick(self):
        if not self.alive:
            return  # Stop updating if the app is closing
            
        remaining = max(0, self.total - int(time.time() - self.start))
        hh = remaining // 3600
        mm = (remaining % 3600) // 60
        ss = remaining % 60
        self.timer_label.config(text=f"{hh:02d}:{mm:02d}:{ss:02d}")
        # turn red when under 1 hour
        self.timer_label.config(fg=(YELLOW if remaining > 3600 else "#ff4444"))
        self.root.after(500, self._tick)

    # ---------- Decrypt dialog ----------
    def _open_decrypt_dialog(self):
        # Prevent opening multiple dialogs at once
        if self.decrypt_window_open:
            return
        self.decrypt_window_open = True

        dlg = tk.Toplevel(self.root)
        dlg.title("Decrypt — Provide private key")
        dlg.configure(bg=BG)
        dlg.geometry("680x520")
        dlg.transient(self.root)
        dlg.grab_set()

        def _on_dlg_close():
            self.decrypt_window_open = False
            dlg.destroy()

        dlg.protocol("WM_DELETE_WINDOW", _on_dlg_close)

        tk.Label(
            dlg, text="🔑  Paste the RSA private key (PEM)",
            bg=BG, fg=YELLOW,
            font=("Helvetica", 13, "bold"),
            pady=10,
        ).pack()

        tk.Label(
            dlg, text="Include -----BEGIN PRIVATE KEY----- and -----END PRIVATE KEY-----",
            bg=BG, fg=GREY,
            font=("Helvetica", 9),
        ).pack()

        txt = tk.Text(
            dlg, height=14, width=70,
            bg="#0a0a0a", fg=WHITE,
            insertbackground=WHITE,
            font=("Courier", 10),
            relief="flat", bd=8,
        )
        txt.pack(padx=15, pady=10, fill="both", expand=True)
        txt.focus_set()

        # --- Paste Fixes ---
        def _right_click_paste(event):
            txt.event_generate("<<Paste>>")
            return "break"
            
        context_menu = tk.Menu(dlg, tearoff=0, bg="#222", fg=WHITE)
        context_menu.add_command(label="Paste", command=lambda: txt.event_generate("<<Paste>>"))
        context_menu.add_command(label="Clear", command=lambda: txt.delete("1.0", "end"))
        
        def _show_menu(event):
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()

        txt.bind("<Button-3>", _show_menu)       # Right click
        txt.bind("<Control-v>", _right_click_paste) # Ctrl+V
        txt.bind("<Control-V>", _right_click_paste) # Ctrl+Shift+V

        # --- Load from File Button ---
        def _load_from_file():
            filepath = filedialog.askopenfilename(
                title="Select Private Key",
                filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
            )
            if filepath:
                try:
                    with open(filepath, "r") as f:
                        content = f.read()
                    txt.delete("1.0", "end")
                    txt.insert("1.0", content)
                except Exception as e:
                    status.config(text=f"❌ Error reading file: {e}", fg="#ff4444")

        status = tk.Label(dlg, text="", bg=BG, fg=WHITE,
                          font=("Helvetica", 10, "bold"))
        status.pack(pady=5)

        def _do_decrypt():
            pem = txt.get("1.0", "end").strip().encode()
            if not pem:
                status.config(text="✖  No key entered.", fg="#ff4444")
                return
            ok, msg = self.decrypt_callback(pem)
            if ok:
                status.config(text=f"✅  {msg}", fg=GREEN)
                # Close dialog after 1.5s, then trigger success screen
                dlg.after(1500, _on_dlg_close)
                self.root.after(1600, self._show_success_and_exit)
            else:
                status.config(text=f"❌  {msg}", fg="#ff4444")

        # Buttons row
        btn_row = tk.Frame(dlg, bg=BG)
        btn_row.pack(pady=8)
        
        self._button(btn_row, "📁 Load from File", "#444444", _load_from_file).pack(side="left", padx=6)
        self._button(btn_row, "Decrypt", GREEN, _do_decrypt).pack(side="left", padx=6)
        self._button(btn_row, "Cancel", "#444444", _on_dlg_close).pack(side="left", padx=6)

    def _show_success_and_exit(self):
        self.alive = False  # Stop timer
        for w in self.root.winfo_children():
            w.destroy()
        tk.Label(
            self.root,
            text="✅  All files have been decrypted successfully.",
            bg=BG, fg=GREEN,
            font=("Helvetica", 18, "bold"),
        ).pack(expand=True)
        # Close the app after 1.8 seconds
        self.root.after(1800, self._on_close)

    # ---------- Run ----------
    def run(self):
        self.root.mainloop()


def run_ransom_note(files_count, decrypt_callback):
    """
    files_count: number of locked files to display
    decrypt_callback(priv_pem_bytes) -> (success, message)
    """
    note = ImpactSimulator(files_count, decrypt_callback)
    note.run()