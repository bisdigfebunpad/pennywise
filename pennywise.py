import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Tema ----------
CREAM, DARK, MINT, SKY = "#F7F9E1", "#204654", "#CAFFA6", "#A9E0F1"
H, B = "Bookman Old Style", "Palatino Linotype"
KATEGORI = ["Makan", "Transport", "Belanja", "Hiburan", "Tagihan", "Lainnya"]

saldo, rekap = 0, dict.fromkeys(KATEGORI, 0)
rp = lambda n: f"Rp {n:,.0f}".replace(",", ".")


# ---------- Logika ----------
def catat(jenis):
    global saldo
    try:
        nominal = float(entry.get())
        assert nominal > 0
    except (ValueError, AssertionError):
        return messagebox.showerror("Oops", "Masukkan nominal angka yang valid (> 0)")

    if jenis == "in":
        saldo += nominal
        tabel.insert("", 0, values=("Top Up", f"+ {rp(nominal)}"), tags=("in",))
    else:
        if nominal > saldo:
            return messagebox.showwarning("Peringatan", "Saldo tidak mencukupi!")
        kat = kategori.get()
        saldo -= nominal
        rekap[kat] += nominal
        tabel.insert("", 0, values=(kat, f"- {rp(nominal)}"), tags=("out",))

    entry.delete(0, tk.END)
    refresh()


def refresh():
    lbl_saldo.config(text=rp(saldo))
    lbl_warn.config(text="⚠ Saldo menipis, hati-hati ya!" if saldo < 20000 else "")
    for k, val in bars.items():
        val.config(text=rp(rekap[k]))


# ---------- Window & Style ----------
root = tk.Tk()
root.title("PennyWise")
root.geometry("480x740")
root.configure(bg=CREAM)
root.option_add("*TCombobox*Listbox.font", (B, 10))

st = ttk.Style()
st.theme_use("clam")
st.configure("TCombobox", fieldbackground="white", font=(B, 10))
st.configure("Treeview", font=(B, 10), rowheight=26, foreground=DARK, fieldbackground="white")
st.configure("Treeview.Heading", font=(H, 10, "bold"), background=DARK, foreground=CREAM)


def tombol(parent, teks, bg, fg, cmd):
    return tk.Button(parent, text=teks, bg=bg, fg=fg, relief="flat", font=(H, 10, "bold"),
                     activebackground=SKY, cursor="hand2", pady=6, command=cmd)


# ---------- Header ----------
header = tk.Frame(root, bg=DARK)
header.pack(fill="x")
tk.Label(header, text="PennyWise", font=(H, 24, "bold"), bg=DARK, fg=MINT).pack(pady=(18, 0))
tk.Label(header, text="Every Penny, Spent Wisely", font=(B, 10, "italic"), bg=DARK, fg=SKY).pack()
tk.Label(header, text="SALDO SAAT INI", font=(B, 9), bg=DARK, fg=CREAM).pack(pady=(14, 0))
lbl_saldo = tk.Label(header, text=rp(0), font=(H, 22, "bold"), bg=DARK, fg=CREAM)
lbl_saldo.pack(pady=(0, 4))
lbl_warn = tk.Label(header, text="⚠ Saldo menipis, hati-hati ya!", font=(B, 9, "bold"), bg=DARK, fg=MINT)
lbl_warn.pack(pady=(0, 12))

# ---------- Input ----------
form = tk.Frame(root, bg=SKY, padx=16, pady=12)
form.pack(fill="x", padx=18, pady=14)
form.columnconfigure((0, 1), weight=1)

entry = tk.Entry(form, font=(B, 12), relief="flat", justify="center")
entry.grid(row=0, column=0, columnspan=2, sticky="ew", ipady=5, pady=(0, 8))
kategori = ttk.Combobox(form, values=KATEGORI, state="readonly", font=(B, 10))
kategori.set(KATEGORI[0])
kategori.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
tombol(form, "＋ Top Up", MINT, DARK, lambda: catat("in")).grid(row=2, column=0, sticky="ew", padx=(0, 4))
tombol(form, "－ Pengeluaran", DARK, CREAM, lambda: catat("out")).grid(row=2, column=1, sticky="ew", padx=(4, 0))

# ---------- Rekap (progress bar) ----------
tk.Label(root, text="Rekap Pengeluaran", font=(H, 11, "bold"), bg=CREAM, fg=DARK).pack(anchor="w", padx=20)
rekap_frame = tk.Frame(root, bg=CREAM)
rekap_frame.pack(fill="x", padx=20, pady=6)
rekap_frame.columnconfigure(1, weight=1)
bars = {}
for i, k in enumerate(KATEGORI):
    tk.Label(rekap_frame, text=k, font=(B, 10), bg=CREAM, fg=DARK, width=10, anchor="w").grid(row=i, column=0)
    bars[k] = tk.Label(rekap_frame, text=rp(0), font=(B, 10, "bold"), bg=CREAM, fg=DARK, anchor="e")
    bars[k].grid(row=i, column=1, sticky="e", pady=3)

# ---------- Riwayat ----------
tk.Label(root, text="Riwayat Transaksi", font=(H, 11, "bold"), bg=CREAM, fg=DARK).pack(anchor="w", padx=20, pady=(10, 4))
tabel = ttk.Treeview(root, columns=("kat", "nom"), show="headings", height=7)
tabel.heading("kat", text="Kategori")
tabel.heading("nom", text="Nominal")
tabel.column("kat", width=180)
tabel.column("nom", width=220, anchor="e")
tabel.tag_configure("in", background=MINT)
tabel.tag_configure("out", background=SKY)
tabel.pack(fill="x", padx=20)

refresh()
root.mainloop()
