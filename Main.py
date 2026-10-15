
import csv
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from collections import Counter

from models import ArtToy


# =========================================================
# CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "koleksi.csv"

BG = "#0B1020"
SIDEBAR = "#10172A"
PANEL = "#151E33"
PANEL2 = "#1B2740"
BORDER = "#2A3852"

TEXT = "#F1F5F9"
MUTED = "#94A3B8"
PURPLE = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#34D399"
YELLOW = "#FBBF24"
RED = "#FB7185"

FONT = "Segoe UI"


# =========================================================
# CSV FUNCTIONS
# =========================================================

def load_data():
    if not CSV_FILE.exists():
        return []

    items = []

    try:
        with open(CSV_FILE, "r", encoding="utf-8-sig",
                  newline="") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if not row or not any(x.strip() for x in row):
                    continue

                # Jaga agar CSV lama dengan kolom tambahan
                # tidak menyebabkan IndexError.
                row = (row[:4] + [""] * 4)[:4]
                nama, karakter, kelangkaan, kondisi = [
                    x.strip() for x in row
                ]

                if not nama or not karakter or not kelangkaan:
                    continue

                items.append(
                    ArtToy(
                        nama,
                        karakter,
                        kelangkaan,
                        kondisi or "Open Box"
                    )
                )

    except (OSError, csv.Error) as error:
        messagebox.showerror(
            "Kesalahan CSV",
            f"Gagal membaca koleksi.csv:\n{error}"
        )

    return items


def save_data(items):
    try:
        with open(CSV_FILE, "w", encoding="utf-8",
                  newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Nama Seri", "Karakter", "Kelangkaan", "Kondisi"
            ])

            for item in items:
                writer.writerow(item.to_list())

        return True

    except OSError as error:
        messagebox.showerror(
            "Gagal Menyimpan",
            str(error)
        )
        return False


# =========================================================
# APPLICATION
# =========================================================

class ArtToyApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Collector Studio | Art Toy Manager")
        self.geometry("1180x740")
        self.minsize(900, 600)
        self.configure(bg=BG)

        self.items = load_data()
        self.page = "dashboard"
        self.search_text = tk.StringVar()
        self.rarity_filter = tk.StringVar(value="Semua")
        self.form_vars = {}

        self.setup_style()
        self.create_layout()
        self.show_page("dashboard")

    # -----------------------------------------------------
    # STYLES
    # -----------------------------------------------------

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=PANEL,
            foreground=TEXT,
            fieldbackground=PANEL,
            borderwidth=0,
            rowheight=38,
            font=(FONT, 10)
        )

        style.configure(
            "Treeview.Heading",
            background=SIDEBAR,
            foreground=CYAN,
            borderwidth=0,
            padding=(10, 12),
            font=(FONT, 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#433878")],
            foreground=[("selected", "#FFFFFF")]
        )

        style.map(
            "Treeview.Heading",
            background=[("active", PANEL2)]
        )

        style.configure(
            "Vertical.TScrollbar",
            background=PANEL2,
            troughcolor=BG,
            bordercolor=BG,
            arrowcolor=TEXT
        )

    # -----------------------------------------------------
    # REUSABLE WIDGETS
    # -----------------------------------------------------

    def label(self, parent, text, size=11, color=TEXT,
              bold=False, **kwargs):
        return tk.Label(
            parent,
            text=text,
            font=(FONT, size, "bold" if bold else "normal"),
            bg=kwargs.pop("bg", parent.cget("bg")),
            fg=color,
            **kwargs
        )

    def button(self, parent, text, command,
               color=PURPLE, width=16):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="#FFFFFF",
            activebackground="#6D4BC3",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(FONT, 10, "bold"),
            padx=12,
            pady=10,
            width=width
        )

        btn.bind(
            "<Enter>",
            lambda event: btn.configure(bg="#6D4BC3")
            if color == PURPLE else None
        )
        btn.bind(
            "<Leave>",
            lambda event: btn.configure(bg=color)
        )

        return btn

    def card(self, parent, title, value, subtitle, accent):
        frame = tk.Frame(
            parent, bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        tk.Frame(frame, bg=accent, height=4).pack(
            fill="x", side="top"
        )

        self.label(
            frame, title.upper(), 9, MUTED, True
        ).pack(anchor="w", padx=18, pady=(17, 5))

        self.label(
            frame, str(value), 27, TEXT, True
        ).pack(anchor="w", padx=18)

        self.label(
            frame, subtitle, 9, accent
        ).pack(anchor="w", padx=18, pady=(5, 18))

        return frame

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # -----------------------------------------------------
    # MAIN LAYOUT
    # -----------------------------------------------------

    def create_layout(self):
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=225)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Frame(
            self.sidebar, bg=CYAN, height=4
        ).pack(fill="x")

        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=22, pady=(28, 35))

        self.label(
            brand, "✦", 28, CYAN, True
        ).pack(anchor="w")

        self.label(
            brand, "COLLECTOR", 20, TEXT, True
        ).pack(anchor="w")

        self.label(
            brand, "S T U D I O", 10, PURPLE, True
        ).pack(anchor="w", pady=(2, 0))

        self.label(
            self.sidebar, "WORKSPACE", 9, MUTED, True
        ).pack(anchor="w", padx=22, pady=(0, 12))

        self.nav_buttons = {}

        nav_items = [
            ("dashboard", "⌂   Dashboard"),
            ("collection", "▤   Semua Koleksi"),
            ("add", "+   Tambah Koleksi")
        ]

        for page, text in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=lambda p=page: self.show_page(p),
                bg=SIDEBAR,
                fg=MUTED,
                activebackground=PANEL2,
                activeforeground=CYAN,
                anchor="w",
                relief="flat",
                bd=0,
                cursor="hand2",
                font=(FONT, 11, "bold"),
                padx=20,
                pady=14
            )
            btn.pack(fill="x", padx=10, pady=3)
            self.nav_buttons[page] = btn

        tk.Frame(
            self.sidebar, bg=SIDEBAR
        ).pack(fill="both", expand=True)

        tk.Frame(
            self.sidebar, bg=BORDER, height=1
        ).pack(fill="x", padx=18, pady=(0, 15))

        self.label(
            self.sidebar,
            "COLLECTION MANAGER\nPython + Tkinter",
            9, MUTED, bg=SIDEBAR, justify="left"
        ).pack(anchor="w", padx=22, pady=(0, 22))

        # Right content
        self.right = tk.Frame(self, bg=BG)
        self.right.pack(side="left", fill="both", expand=True)

        self.topbar = tk.Frame(self.right, bg=BG)
        self.topbar.pack(fill="x", padx=30, pady=(25, 15))

        self.page_title = self.label(
            self.topbar, "Dashboard", 23, TEXT, True, bg=BG
        )
        self.page_title.pack(side="left")

        self.label(
            self.topbar, "ART TOY COLLECTION", 9, CYAN, True,
            bg=BG
        ).pack(side="right", pady=8)

        self.content = tk.Frame(self.right, bg=BG)
        self.content.pack(
            fill="both", expand=True, padx=30, pady=(5, 25)
        )

    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------

    def show_page(self, page):
        self.page = page
        self.clear_content()

        titles = {
            "dashboard": "Dashboard",
            "collection": "Semua Koleksi",
            "add": "Tambah Koleksi"
        }

        self.page_title.configure(text=titles[page])

        for name, btn in self.nav_buttons.items():
            btn.configure(
                bg="#30264F" if name == page else SIDEBAR,
                fg=CYAN if name == page else MUTED
            )

        if page == "dashboard":
            self.build_dashboard()
        elif page == "collection":
            self.build_collection()
        else:
            self.build_add_form()

    # -----------------------------------------------------
    # DASHBOARD
    # -----------------------------------------------------

    def build_dashboard(self):
        self.label(
            self.content,
            "Your collection, beautifully organized.",
            19, TEXT, True
        ).pack(anchor="w")

        self.label(
            self.content,
            "Kelola dan pantau koleksi art toy & blind box kamu.",
            10, MUTED
        ).pack(anchor="w", pady=(6, 22))

        total = len(self.items)
        series = len({x.nama_seri for x in self.items})
        rare = sum(
            x.kelangkaan.lower() in ("rare", "secret", "super secret")
            for x in self.items
        )
        sealed = sum(
            x.kondisi.lower() in ("sealed", "unopened")
            for x in self.items
        )

        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill="x", pady=(0, 25))

        for i in range(4):
            stats.grid_columnconfigure(i, weight=1, uniform="cards")

        data = [
            ("Total Karakter", total, "Item tersimpan", CYAN),
            ("Total Seri", series, "Seri berbeda", PURPLE),
            ("Rare + Secret", rare, "Item langka", YELLOW),
            ("Sealed Box", sealed, "Belum dibuka", GREEN)
        ]

        for i, values in enumerate(data):
            widget = self.card(stats, *values)
            widget.grid(
                row=0, column=i, sticky="nsew",
                padx=(0 if i == 0 else 6, 6 if i < 3 else 0)
            )

        # Recent items
        recent = tk.Frame(
            self.content, bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        recent.pack(fill="both", expand=True)

        heading = tk.Frame(recent, bg=PANEL)
        heading.pack(fill="x", padx=18, pady=16)

        self.label(
            heading, "Koleksi Terbaru", 14, TEXT, True
        ).pack(side="left")

        self.button(
            heading, "Lihat Semua →",
            lambda: self.show_page("collection"),
            color=PANEL2, width=14
        ).pack(side="right")

        self.create_table(
            recent, self.items[-5:][::-1], height=5
        )

        actions = tk.Frame(self.content, bg=BG)
        actions.pack(fill="x", pady=(18, 0))

        self.button(
            actions, "+ Tambah Koleksi",
            lambda: self.show_page("add")
        ).pack(side="left")

        self.button(
            actions, "↻ Refresh",
            self.refresh_dashboard,
            color=PANEL2
        ).pack(side="left", padx=10)

    # -----------------------------------------------------
    # TABLE
    # -----------------------------------------------------

    def create_table(self, parent, items, height=10):
        frame = tk.Frame(parent, bg=PANEL)
        frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        columns = ("seri", "karakter", "kelangkaan", "kondisi")

        tree = ttk.Treeview(
            frame, columns=columns,
            show="headings", height=height
        )

        definitions = [
            ("seri", "NAMA SERI", 220),
            ("karakter", "KARAKTER", 200),
            ("kelangkaan", "KELANGKAAN", 130),
            ("kondisi", "KONDISI", 130)
        ]

        for col, heading, width in definitions:
            tree.heading(col, text=heading)
            tree.column(col, width=width, minwidth=75, anchor="w")

        tree.tag_configure("even", background=PANEL)
        tree.tag_configure("odd", background="#19243A")

        scrollbar = ttk.Scrollbar(
            frame, orient="vertical",
            command=tree.yview,
            style="Vertical.TScrollbar"
        )
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, item in enumerate(items):
            tree.insert(
                "", "end",
                values=item.to_list(),
                tags=("even" if i % 2 == 0 else "odd",)
            )

        return tree

    # -----------------------------------------------------
    # COLLECTION PAGE
    # -----------------------------------------------------

    def build_collection(self):
        self.label(
            self.content, "All Collectibles", 19, TEXT, True
        ).pack(anchor="w")

        self.label(
            self.content,
            f"Koleksi tersimpan: {len(self.items)} item",
            10, MUTED
        ).pack(anchor="w", pady=(5, 18))

        toolbar = tk.Frame(self.content, bg=BG)
        toolbar.pack(fill="x", pady=(0, 14))

        self.search_text.set("")
        self.rarity_filter.set("Semua")

        search = tk.Entry(
            toolbar,
            textvariable=self.search_text,
            bg=PANEL,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=(FONT, 11),
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=PURPLE
        )
        search.pack(side="left", fill="x", expand=True, ipady=12)

        options = ttk.Combobox(
            toolbar,
            textvariable=self.rarity_filter,
            values=["Semua", "Common", "Rare", "Secret",
                    "Super Secret"],
            state="readonly",
            width=13
        )
        options.pack(side="left", padx=10, ipady=7)

        self.button(
            toolbar, "+ Tambah",
            lambda: self.show_page("add"), width=11
        ).pack(side="left")

        table_panel = tk.Frame(
            self.content, bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        table_panel.pack(fill="both", expand=True)

        self.collection_tree = self.create_table(
            table_panel, [], height=12
        )

        footer = tk.Frame(self.content, bg=BG)
        footer.pack(fill="x", pady=(12, 0))

        self.result_label = self.label(
            footer, "", 9, MUTED
        )
        self.result_label.pack(side="left")

        self.button(
            footer, "Hapus Item",
            self.delete_selected,
            color="#9F3449", width=12
        ).pack(side="right")

        self.button(
            footer, "↻ Refresh",
            self.refresh_collection,
            color=PANEL2, width=11
        ).pack(side="right", padx=8)

        search.bind("<KeyRelease>", lambda event: self.update_table())
        options.bind("<<ComboboxSelected>>",
                     lambda event: self.update_table())

        self.update_table()

    def update_table(self):
        if not hasattr(self, "collection_tree"):
            return

        query = self.search_text.get().strip().lower()
        rarity = self.rarity_filter.get()

        for row in self.collection_tree.get_children():
            self.collection_tree.delete(row)

        filtered = [
            item for item in self.items
            if query in item.nama_seri.lower()
            or query in item.karakter.lower()
        ]

        if rarity != "Semua":
            filtered = [
                item for item in filtered
                if item.kelangkaan.lower() == rarity.lower()
            ]

        for i, item in enumerate(filtered):
            self.collection_tree.insert(
                "", "end",
                values=item.to_list(),
                tags=("even" if i % 2 == 0 else "odd",)
            )

        self.result_label.configure(
            text=f"Menampilkan {len(filtered)} dari {len(self.items)} item"
        )

    def refresh_dashboard(self):
        self.items = load_data()
        self.show_page("dashboard")

    def refresh_collection(self):
        self.items = load_data()
        self.show_page("collection")

    def delete_selected(self):
        selected = self.collection_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Pilih Item", "Pilih item yang ingin dihapus."
            )
            return

        values = list(
            self.collection_tree.item(selected[0], "values")
        )

        if not messagebox.askyesno(
            "Konfirmasi",
            f"Hapus {values[1]} dari koleksi?"
        ):
            return

        index = next(
            (
                i for i, item in enumerate(self.items)
                if item.to_list() == values
            ),
            None
        )

        if index is None:
            messagebox.showerror(
                "Kesalahan", "Item tidak ditemukan."
            )
            return

        removed = self.items.pop(index)

        if save_data(self.items):
            self.refresh_collection()
        else:
            self.items.insert(index, removed)

    # -----------------------------------------------------
    # ADD FORM
    # -----------------------------------------------------

    def build_add_form(self):
        self.label(
            self.content, "Add a New Collectible", 19, TEXT, True
        ).pack(anchor="w")

        self.label(
            self.content,
            "Lengkapi informasi art toy atau blind box kamu.",
            10, MUTED
        ).pack(anchor="w", pady=(5, 20))

        form = tk.Frame(
            self.content, bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        form.pack(fill="x")

        self.label(
            form, "INFORMASI KOLEKSI", 10, CYAN, True
        ).grid(row=0, column=0, columnspan=2,
               sticky="w", padx=25, pady=(25, 20))

        form.grid_columnconfigure((0, 1), weight=1, uniform="form")

        self.form_vars = {}

        self.add_field(
            form, "Nama Seri *", "Contoh: Rafflesia Series",
            1, 0, "nama_seri"
        )
        self.add_field(
            form, "Nama Karakter *", "Contoh: Blossom Raffi",
            1, 1, "karakter"
        )
        self.add_field(
            form, "Kelangkaan *", "",
            2, 0, "kelangkaan",
            ["Common", "Rare", "Secret", "Super Secret"]
        )
        self.add_field(
            form, "Kondisi", "",
            2, 1, "kondisi",
            ["Open Box", "Sealed", "Display", "Damaged"]
        )

        buttons = tk.Frame(form, bg=PANEL)
        buttons.grid(
            row=3, column=0, columnspan=2,
            sticky="w", padx=25, pady=(5, 25)
        )

        self.button(
            buttons, "Simpan Koleksi ✓",
            self.add_collection, width=19
        ).pack(side="left")

        self.button(
            buttons, "Reset Form",
            self.reset_form, color=PANEL2, width=13
        ).pack(side="left", padx=10)

    def add_field(self, parent, title, placeholder,
                  row, col, key, choices=None):
        cell = tk.Frame(parent, bg=PANEL)
        cell.grid(
            row=row, column=col, sticky="ew",
            padx=(25 if col == 0 else 12,
                  12 if col == 0 else 25),
            pady=(0, 20)
        )
        cell.grid_columnconfigure(0, weight=1)

        self.label(
            cell, title, 10, TEXT, True
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        if choices:
            var = tk.StringVar(
                value="Common" if key == "kelangkaan" else "Open Box"
            )
            widget = ttk.Combobox(
                cell, textvariable=var,
                values=choices, state="readonly"
            )
            widget.configure(font=(FONT, 10))
            widget.grid(row=1, column=0, sticky="ew", ipady=7)

        else:
            var = tk.StringVar()
            widget = tk.Entry(
                cell,
                textvariable=var,
                bg="#10172A",
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat",
                font=(FONT, 11),
                highlightthickness=1,
                highlightbackground=BORDER,
                highlightcolor=PURPLE
            )
            widget.grid(row=1, column=0, sticky="ew", ipady=11)

            widget.insert(0, placeholder)
            widget.configure(fg=MUTED)

            def on_focus_in(event):
                if widget.get() == placeholder:
                    widget.delete(0, "end")
                    widget.configure(fg=TEXT)

            def on_focus_out(event):
                if not widget.get():
                    widget.insert(0, placeholder)
                    widget.configure(fg=MUTED)

            widget.bind("<FocusIn>", on_focus_in)
            widget.bind("<FocusOut>", on_focus_out)

            self.form_vars[key] = (var, widget, placeholder)
            return

        self.form_vars[key] = (var, widget, None)

    def reset_form(self):
        for key, (var, widget, placeholder) in self.form_vars.items():
            if placeholder is not None:
                widget.delete(0, "end")
                widget.insert(0, placeholder)
                widget.configure(fg=MUTED)
            elif key == "kelangkaan":
                var.set("Common")
            elif key == "kondisi":
                var.set("Open Box")

    def add_collection(self):
        values = {}

        for key, (var, widget, placeholder) in self.form_vars.items():
            value = var.get().strip()

            if placeholder is not None and value == placeholder:
                value = ""

            values[key] = value

        nama = values["nama_seri"]
        karakter = values["karakter"]
        kelangkaan = values["kelangkaan"]
        kondisi = values["kondisi"] or "Open Box"

        if not nama or not karakter or not kelangkaan:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "Nama seri, karakter, dan kelangkaan wajib diisi."
            )
            return

        item = ArtToy(nama, karakter, kelangkaan, kondisi)
        self.items.append(item)

        if save_data(self.items):
            messagebox.showinfo(
                "Berhasil",
                f"{karakter} berhasil ditambahkan!"
            )
            self.show_page("collection")
        else:
            self.items.pop()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    app = ArtToyApp()
    app.mainloop()
