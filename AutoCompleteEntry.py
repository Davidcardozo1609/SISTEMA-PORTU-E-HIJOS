# AutoCompleteEntry.py
from tkinter import *
import tkinter.font as tkfont

class AutoCompleteEntry(Entry):
    def __init__(self, master, listar, max_suggestions=8, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self._listar = listar
        self.max_suggestions = max_suggestions
        self._trace_active = True


        self.var = StringVar()
        self.config(textvariable=self.var)
        self.var.trace("w", lambda *a: self._on_change())

        self.popup = None
        self.listbox = None
        self.scroll = None

        # Bindings en el Entry
        self.bind("<Down>", self._on_down)
        self.bind("<Escape>", lambda e: self._hide_popup())
        self.bind("<FocusOut>", self._on_focus_out)
        self.bind("<FocusIn>", lambda e: self._on_change())
        self.bind("<Button-1>", lambda e: self.after(1, self._on_change()))
        self.bind("<Return>", self._on_return)


    def _on_change(self):
        if not self._trace_active:
            return
        texto = self.var.get().strip()
        if texto == "":
            self._hide_popup()
            return

        try:
            items = self._listar() or []
        except Exception:
            items = []

        coincidencias = [p for p in items if texto.lower() in p.lower()]
        if not coincidencias:
            self._hide_popup()
            return

        coincidencias = coincidencias[: self.max_suggestions]
        self._show_popup(coincidencias)


    def _show_popup(self, items):
        # crear popup/listbox si no existe
        if self.popup is None or not self.popup.winfo_exists():
            self.popup = Toplevel(self.master)
            self.popup.wm_overrideredirect(True)
            try:
                self.popup.attributes("-topmost", True)
            except Exception:
                pass

            # listbox + scrollbar
            self.listbox = Listbox(self.popup, font=self["font"], activestyle="none")
            self.scroll = Scrollbar(self.popup, command=self.listbox.yview)
            self.listbox.config(yscrollcommand=self.scroll.set)

            self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
            self.scroll.pack(side=RIGHT, fill=Y)

            # Bindings del listbox: NO usamos <<ListboxSelect>>
            self.listbox.bind("<ButtonRelease-1>", self._on_select)   # click del mouse (único release)
            self.listbox.bind("<Double-Button-1>", self._on_double)
            self.listbox.bind("<Return>", self._on_double)           # Enter confirma
            self.listbox.bind("<Up>", self._on_up)                   # Up especial (volver al Entry)
            self.listbox.bind("<Escape>", lambda e: self._hide_popup())
        else:
            self.listbox.delete(0, END)

        # poblar
        for it in items:
            self.listbox.insert(END, it)

        # calcular dimensiones
        # ancho: al menos el ancho del Entry, o el ancho del texto más largo
        f = tkfont.Font(font=self["font"])
        max_text = max(items, key=len) if items else ""
        max_text_w = f.measure(max_text) + 12
        entry_w = self.winfo_width() or 100
        width = max(entry_w, max_text_w)

        # filas visibles
        rows = min(len(items), self.max_suggestions)
        self.listbox.config(height=max(1, rows))

        # forzar actualización y pedir el alto requerido del listbox
        self.popup.update_idletasks()
        height = self.listbox.winfo_reqheight()

        # posicionar justo debajo del Entry
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()

        # evitar que se salga de pantalla (ajuste simple)
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        if x + width > screen_w:
            x = max(0, screen_w - width)
        if y + height > screen_h:
            y = max(0, self.winfo_rooty() - height)  # si no cabe abajo, poner arriba

        self.popup.geometry(f"{int(width)}x{int(height)}+{int(x)}+{int(y)}")
        try:
            self.popup.deiconify()
            self.popup.lift()
        except Exception:
            pass

    def _hide_popup(self, *args):
        if self.popup and self.popup.winfo_exists():
            try:
                self.popup.destroy()
            except Exception:
                pass
        self.popup = None
        self.listbox = None
        self.scroll = None
        
    def funcion_para_enter(self, *args):
        if self.popup and self.popup.winfo_exists():
            try:
                self.popup.destroy()
                self.master.focus()
            except Exception:
                pass
        self.popup = None
        self.listbox = None
        self.scroll = None

    def _on_select(self, event=None):
        # llamado por <ButtonRelease-1> del listbox (click)
        if not self.listbox:
            return
        sel = self.listbox.curselection()
        if sel:
            valor = self.listbox.get(sel[0])
            self.var.set(valor)
            self.icursor(END)
            self._hide_popup()
            self.event_generate("<<AutoCompleteSelected>>")

    def _on_double(self, event=None):
    # usado por double-click y Return
        if self.listbox:
            sel = self.listbox.curselection()
            if sel:
                valor = self.listbox.get(sel[0])
                self.var.set(valor)
                self.icursor(END)
                self.event_generate("<<AutoCompleteSelected>>")
                self.funcion_para_enter()
                


    def _on_down(self, event=None):
        # si hay popup y listbox, y foco está en Entry -> pasar foco al listbox y seleccionar 1er item
        if self.popup and self.listbox and self.listbox.size() > 0:
            if self.focus_get() == self:
                self.listbox.focus_set()
                self.listbox.selection_clear(0, END)
                self.listbox.selection_set(0)
                self.listbox.activate(0)
                return "break"
            # si el foco ya está en el listbox, dejamos que el listbox gestione ↓ por defecto

    def _on_focus_out(self, event=None):
        # esperar un poco para ver si el foco quedó en el listbox (click)
        self.after(120, self._hide_if_focus_out)

    def _hide_if_focus_out(self):
        if not (self.popup and self.popup.winfo_exists()):
            return

        foco = self.focus_get()

        # Mantener abierto si todavía estamos en el Entry o en el Listbox
        if foco == self or (self.listbox and foco == self.listbox):
            return

        # En cualquier otro caso → cerrar
        self._hide_popup()

    def _on_up(self, event=None):
        # manejamos Up dentro del listbox para permitir volver al Entry en el primer elemento
        if not self.listbox:
            return

        # sólo actuar si el foco está en el listbox
        if self.focus_get() == self.listbox:
            sel = self.listbox.curselection()
            if sel:
                index = sel[0]
                if index == 0:
                    # volver al Entry
                    self.focus_set()
                else:
                    # subir dentro del listbox (manejo manual para consistencia)
                    self.listbox.selection_clear(0, END)
                    self.listbox.selection_set(index - 1)
                    self.listbox.activate(index - 1)
            return "break"
        
    def _on_return(self, event=None):
        # Confirmar texto y cerrar popup
        self._trace_active = False  # evita que _on_change muestre el popup de nuevo
        self.icursor(END)
        self._hide_popup()
        self.event_generate("<<AutoCompleteSelected>>")
        # reactivar el trace después de un corto delay
        self.after(100, lambda: setattr(self, "_trace_active", True))
        return "break"

