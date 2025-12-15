import tkinter as tk
from tkinter import ttk, messagebox

from src.redesign.controllers.parking_controller import ParkingController
from src.redesign.models.parking_lot import ParkingLot
from src.redesign.strategies.allocation_strategy import RegularFirstStrategy, ElectricOnlyStrategy
from src.redesign.factories.vehicle_factory import create_vehicle, create_electric
import os
from typing import Tuple


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Parking Lot Manager (Redesign)")
        self.suppress_dialogs = bool(os.environ.get("APP_SUPPRESS_DIALOGS"))
        self.controller = ParkingController(
            lot=ParkingLot(level=1, regular_capacity=0, ev_capacity=0),
            allocation_strategy=RegularFirstStrategy(),
        )
        # Use a simpler UI on older Tk (macOS system Python ships 8.5)
        if tk.TkVersion < 8.6:
            self._build_ui_simple()
        else:
            self._build_ui()

    def _build_ui(self) -> None:
        try:
            frm = ttk.Frame(self.root, padding=10)
            frm.grid(sticky="nsew")
            # Expose main container for targeted screenshots
            self.container = frm

            ttk.Label(frm, text="Parking Lot Manager (Redesign)", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=11, sticky="w", pady=(0,6))

            # Lot creation
            ttk.Label(frm, text="Regular Slots").grid(row=1, column=0, sticky="w", padx=(0,4))
            self.regular_var = tk.StringVar(value="10")
            ttk.Entry(frm, textvariable=self.regular_var, width=6).grid(row=1, column=1, padx=(0,8))

            ttk.Label(frm, text="EV Slots").grid(row=1, column=2, sticky="w", padx=(0,4))
            self.ev_var = tk.StringVar(value="4")
            ttk.Entry(frm, textvariable=self.ev_var, width=6).grid(row=1, column=3, padx=(0,8))

            ttk.Label(frm, text="Level").grid(row=1, column=4, sticky="w", padx=(0,4))
            self.level_var = tk.StringVar(value="1")
            ttk.Entry(frm, textvariable=self.level_var, width=4).grid(row=1, column=5, padx=(0,8))

            ttk.Button(frm, text="Create Lot", command=self._create_lot).grid(row=1, column=6, padx=8)

            # Vehicle inputs
            ttk.Label(frm, text="Reg").grid(row=2, column=0, sticky="w", padx=(0,4))
            self.reg_var = tk.StringVar()
            ttk.Entry(frm, textvariable=self.reg_var, width=10).grid(row=2, column=1, padx=(0,8))

            ttk.Label(frm, text="Make").grid(row=2, column=2, sticky="w", padx=(0,4))
            self.make_var = tk.StringVar()
            ttk.Entry(frm, textvariable=self.make_var, width=10).grid(row=2, column=3, padx=(0,8))

            ttk.Label(frm, text="Model").grid(row=2, column=4, sticky="w", padx=(0,4))
            self.model_var = tk.StringVar()
            ttk.Entry(frm, textvariable=self.model_var, width=10).grid(row=2, column=5, padx=(0,8))

            ttk.Label(frm, text="Color").grid(row=2, column=6, sticky="w", padx=(0,4))
            self.color_var = tk.StringVar()
            ttk.Entry(frm, textvariable=self.color_var, width=10).grid(row=2, column=7, padx=(0,8))

            self.is_ev = tk.BooleanVar(value=False)
            ttk.Checkbutton(frm, text="EV", variable=self.is_ev).grid(row=2, column=8, padx=(0,8))
            self.is_bike = tk.BooleanVar(value=False)
            ttk.Checkbutton(frm, text="Motorcycle/Bike", variable=self.is_bike).grid(row=2, column=9, padx=(0,8))

            ttk.Button(frm, text="Park", command=self._park).grid(row=2, column=10, padx=8)

            # Leave section
            ttk.Label(frm, text="Slot #").grid(row=3, column=0, sticky="w", padx=(0,4))
            self.slot_var = tk.StringVar()
            ttk.Entry(frm, textvariable=self.slot_var, width=6).grid(row=3, column=1, padx=(0,8))
            self.leave_ev = tk.BooleanVar(value=False)
            ttk.Checkbutton(frm, text="EV Slot", variable=self.leave_ev).grid(row=3, column=2, padx=(0,8))
            ttk.Button(frm, text="Leave", command=self._leave).grid(row=3, column=3, padx=8)

            # Output
            self.text = tk.Text(frm, width=100, height=20)
            self.text.grid(row=4, column=0, columnspan=11, pady=10, sticky="nsew")
            self.text.insert(tk.END, "Ready. Click 'Create Lot' to begin.\n")

            for i in range(11):
                frm.grid_columnconfigure(i, weight=1)
            for r in range(5):
                frm.grid_rowconfigure(r, weight=0)
            frm.grid_rowconfigure(4, weight=1)
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
        except Exception as e:
            # If anything fails, show a very obvious fallback
            fallback = tk.Frame(self.root)
            fallback.pack(fill="both", expand=True)
            lbl = tk.Label(fallback, text=f"UI failed to load: {e}")
            lbl.pack(pady=20)
            btn = tk.Button(fallback, text="Create Lot", command=self._create_lot)
            btn.pack()

    def _build_ui_simple(self) -> None:
        # Pure-tk, pack-based layout for maximum compatibility on Tk 8.5
        cont = tk.Frame(self.root, padx=10, pady=10)
        cont.pack(fill="both", expand=True)
        # Expose main container for targeted screenshots
        self.container = cont

        title = tk.Label(cont, text="Parking Lot Manager (Redesign)", font=("Arial", 14, "bold"))
        title.pack(anchor="w", pady=(0,8))

        top = tk.Frame(cont)
        top.pack(anchor="w")
        tk.Label(top, text="Regular").grid(row=0, column=0, sticky="w")
        self.regular_var = tk.StringVar(value="10")
        tk.Entry(top, textvariable=self.regular_var, width=6).grid(row=0, column=1)
        tk.Label(top, text="EV").grid(row=0, column=2, sticky="w")
        self.ev_var = tk.StringVar(value="4")
        tk.Entry(top, textvariable=self.ev_var, width=6).grid(row=0, column=3)
        tk.Label(top, text="Level").grid(row=0, column=4, sticky="w")
        self.level_var = tk.StringVar(value="1")
        tk.Entry(top, textvariable=self.level_var, width=4).grid(row=0, column=5)
        tk.Button(top, text="Create Lot", command=self._create_lot).grid(row=0, column=6, padx=6)

        mid = tk.Frame(cont)
        mid.pack(anchor="w", pady=(8,0))
        tk.Label(mid, text="Reg").grid(row=0, column=0, sticky="w")
        self.reg_var = tk.StringVar()
        tk.Entry(mid, textvariable=self.reg_var, width=10).grid(row=0, column=1)
        tk.Label(mid, text="Make").grid(row=0, column=2, sticky="w")
        self.make_var = tk.StringVar()
        tk.Entry(mid, textvariable=self.make_var, width=10).grid(row=0, column=3)
        tk.Label(mid, text="Model").grid(row=0, column=4, sticky="w")
        self.model_var = tk.StringVar()
        tk.Entry(mid, textvariable=self.model_var, width=10).grid(row=0, column=5)
        tk.Label(mid, text="Color").grid(row=0, column=6, sticky="w")
        self.color_var = tk.StringVar()
        tk.Entry(mid, textvariable=self.color_var, width=10).grid(row=0, column=7)
        self.is_ev = tk.BooleanVar(value=False)
        tk.Checkbutton(mid, text="EV", variable=self.is_ev).grid(row=0, column=8)
        self.is_bike = tk.BooleanVar(value=False)
        tk.Checkbutton(mid, text="Motorcycle/Bike", variable=self.is_bike).grid(row=0, column=9)
        tk.Button(mid, text="Park", command=self._park).grid(row=0, column=10, padx=6)

        leave = tk.Frame(cont)
        leave.pack(anchor="w", pady=(8,0))
        tk.Label(leave, text="Slot #", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=(0,5))
        self.slot_var = tk.StringVar()
        slot_entry = tk.Entry(leave, textvariable=self.slot_var, width=10, font=("Arial", 12))
        slot_entry.grid(row=0, column=1, padx=(0,10))
        self.leave_ev = tk.BooleanVar(value=False)
        tk.Checkbutton(leave, text="EV Slot", font=("Arial", 11), variable=self.leave_ev).grid(row=0, column=2, padx=(0,10))
        tk.Button(leave, text="Leave", font=("Arial", 11), command=self._leave).grid(row=0, column=3, padx=6)

        self.text = tk.Text(cont, width=100, height=20)
        self.text.pack(fill="both", expand=True, pady=(10,0))
        self.text.insert(tk.END, "Ready. Click 'Create Lot' to begin.\n")

    def _create_lot(self) -> None:
        try:
            level = int(self.level_var.get())
            reg = int(self.regular_var.get())
            ev = int(self.ev_var.get())
        except Exception:
            # Fallback to sensible defaults if parsing fails
            level, reg, ev = 1, 10, 4
        try:
            self.controller.create_lot(level, reg, ev)
            msg = f"Created lot on level {level} with {reg} regular and {ev} ev slots"
            self._println(msg)
            if not self.suppress_dialogs:
                try:
                    messagebox.showinfo("Create Lot", msg)
                except Exception:
                    pass
        except Exception as e:
            self._println(f"Failed to create lot: {e}")
            if not self.suppress_dialogs:
                try:
                    messagebox.showerror("Create Lot", f"Failed to create lot: {e}")
                except Exception:
                    pass

    def _park(self) -> None:
        reg = (self.reg_var.get().strip() or "ABC123")
        make = (self.make_var.get().strip() or "Toyota")
        model = (self.model_var.get().strip() or "Corolla")
        color = (self.color_var.get().strip() or "Blue")

        if self.is_ev.get():
            veh = create_electric("bike" if self.is_bike.get() else "car", reg, make, model, color)
            # temporarily switch to EV-only strategy for explicit park_ev if needed
            self.controller.allocation_strategy = ElectricOnlyStrategy()
            slot = self.controller.park_ev(veh)
            # switch back to regular-first as default
            self.controller.allocation_strategy = RegularFirstStrategy()
        else:
            veh = create_vehicle("motorcycle" if self.is_bike.get() else "car", reg, make, model, color)
            slot = self.controller.park(veh)

        if slot is None:
            self._println("Sorry, parking is full for that type")
            if not self.suppress_dialogs:
                try:
                    messagebox.showwarning("Park", "Parking is full for that type")
                except Exception:
                    pass
        else:
            msg = f"Allocated slot number: {slot}"
            self._println(msg)
            if not self.suppress_dialogs:
                try:
                    messagebox.showinfo("Park", msg)
                except Exception:
                    pass

    def _leave(self) -> None:
        try:
            slot = int(self.slot_var.get())
        except ValueError:
            self._println("Invalid slot number")
            if not self.suppress_dialogs:
                try:
                    messagebox.showerror("Leave", "Invalid slot number")
                except Exception:
                    pass
            return
        ok = self.controller.leave(slot, is_ev=self.leave_ev.get())
        if ok:
            msg = f"Slot number {slot} is free"
            self._println(msg)
            if not self.suppress_dialogs:
                try:
                    messagebox.showinfo("Leave", msg)
                except Exception:
                    pass
        else:
            msg = f"Unable to remove a vehicle from slot {slot}"
            self._println(msg)
            if not self.suppress_dialogs:
                try:
                    messagebox.showwarning("Leave", msg)
                except Exception:
                    pass

    def _println(self, s: str) -> None:
        self.text.insert(tk.END, s + "\n")
        self.text.see(tk.END)


def run() -> None:
    root = tk.Tk()
    try:
        root.geometry("1100x650")
    except Exception:
        pass
    App(root)
    root.mainloop()


# Helpers for automation/screenshot capture
def create_app() -> Tuple[tk.Tk, App]:
    """Create the Tk root and App without starting mainloop, ready for automation."""
    root = tk.Tk()
    try:
        root.geometry("900x600")
    except Exception:
        pass
    app = App(root)
    try:
        root.update_idletasks()
        root.update()
    except Exception:
        pass
    return root, app


def capture_window(root: tk.Tk, out_path: str) -> bool:
    """Capture the current window to an image file.

    Uses Pillow ImageGrab if available (recommended on macOS). Returns True on success.
    """
    try:
        from PIL import ImageGrab  # type: ignore
    except Exception:
        return False

    try:
        # Ensure window laid out
        root.update_idletasks()
        root.update()
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        w = root.winfo_width()
        h = root.winfo_height()
        if w < 50 or h < 50:
            root.update()
            w = root.winfo_width()
            h = root.winfo_height()
        bbox = (x, y, x + w, y + h)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        img = ImageGrab.grab(bbox=bbox)
        img.save(out_path)
        return True
    except Exception:
        return False


def capture_widget(widget: tk.Misc, out_path: str) -> bool:
    """Capture only the specified widget area to an image file.

    This avoids OS window chrome and captures just the app content area.
    """
    try:
        from PIL import ImageGrab  # type: ignore
    except Exception:
        return False

    try:
        widget.update_idletasks()
        try:
            widget.update()
        except Exception:
            pass
        x = widget.winfo_rootx()
        y = widget.winfo_rooty()
        w = widget.winfo_width()
        h = widget.winfo_height()
        if w < 10 or h < 10:
            # Try a parent update to force layout
            try:
                widget.winfo_toplevel().update()
            except Exception:
                pass
            w = widget.winfo_width()
            h = widget.winfo_height()
        bbox = (x, y, x + w, y + h)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        img = ImageGrab.grab(bbox=bbox)
        img.save(out_path)
        return True
    except Exception:
        return False
