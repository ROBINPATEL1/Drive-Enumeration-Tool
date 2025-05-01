import wmi    # Windows Management Instrumentation .
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os   #For directory/file handling.

# Set custom theme style
def setup_styles():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    background="#2d2d30",
                    foreground="white",
                    fieldbackground="#2d2d30",
                    rowheight=25,
                    font=("Segoe UI", 10))
    style.configure("Treeview.Heading",
                    background="#1f1f1f",
                    foreground="white",
                    font=("Segoe UI", 11, "bold"))

    style.configure("TLabel", background="#1f1f1f", foreground="white", font=("Segoe UI", 10))
    style.configure("TButton", background="#444", foreground="white", font=("Segoe UI", 10, "bold"))
    style.map("TButton", background=[('active', '#666')])

    style.configure("TFrame", background="#1f1f1f")

def get_driver_info():
    c = wmi.WMI()
    drivers = c.Win32_SystemDriver()
    driver_list = []

    for driver in drivers:
        info = {
            "Name": getattr(driver, "Name", "N/A"),
            "DisplayName": getattr(driver, "DisplayName", "N/A"),
            "PathName": getattr(driver, "PathName", "N/A"),
            "State": getattr(driver, "State", "N/A"),
            "StartMode": getattr(driver, "StartMode", "N/A"),
            "ServiceType": getattr(driver, "ServiceType", "N/A"),
            "Description": getattr(driver, "Description", "N/A"),
            "ErrorControl": getattr(driver, "ErrorControl", "N/A"),
            "LoadOrderGroup": getattr(driver, "LoadOrderGroup", "N/A"),
            "Dependencies": ', '.join(getattr(driver, "Dependencies", [])) or "None"
        }
        driver_list.append(info)
    
    return driver_list

def save_to_file(data):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"logs/drivers_log_{timestamp}.txt"

    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            for key, value in item.items():
                f.write(f"{key}: {value}\n")
            f.write("-" * 40 + "\n")

    messagebox.showinfo("Success", f"Driver info saved to {file_path}")

class DriverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛠️ Driver Enumeration Tool")
        self.root.geometry("980x600")
        self.driver_data = []

        setup_styles()
        self.setup_ui()

    def setup_ui(self):
        title = ttk.Label(self.root, text="🔍 Windows Driver Enumeration", font=("Segoe UI", 18, "bold"))
        title.pack(pady=15)

        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10)

        self.search_var = tk.StringVar()
        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", self.filter_drivers)

        columns = ("Name", "DisplayName", "PathName", "State", "StartMode", "ServiceType")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=18)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w", width=160 if col != "PathName" else 320, stretch=True)

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.detail_frame = ttk.Frame(self.root)
        self.detail_frame.pack(padx=10, pady=5, fill=tk.X)

        self.detail_labels = {}
        for field in ["Description", "Dependencies", "ErrorControl", "LoadOrderGroup"]:
            label = ttk.Label(self.detail_frame, text=f"{field}: ", anchor="w", font=("Segoe UI", 9, "bold"))
            label.pack(fill=tk.X, pady=2)
            self.detail_labels[field] = label

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=15)

        fetch_btn = ttk.Button(btn_frame, text="📥 Fetch Drivers", command=self.load_drivers)
        fetch_btn.grid(row=0, column=0, padx=15)

        save_btn = ttk.Button(btn_frame, text="💾 Save to File", command=lambda: save_to_file(self.driver_data))
        save_btn.grid(row=0, column=1, padx=15)

        self.tree.tag_configure('running', background='#237a57')
        self.tree.tag_configure('paused', background='#b38f00')
        self.tree.tag_configure('stopped', background='#a12b2b')

    def load_drivers(self):
        self.driver_data = get_driver_info()
        self.display_drivers(self.driver_data)

    def display_drivers(self, drivers):
        self.tree.delete(*self.tree.get_children())

        for driver in drivers:
            state = driver["State"].lower() if driver["State"] else ""
            tag = ""

            if state == "running":
                tag = "running"
            elif state == "paused":
                tag = "paused"
            elif state in ["stopped", "error"]:
                tag = "stopped"

            self.tree.insert('', 'end', values=(
                driver["Name"],
                driver["DisplayName"],
                driver["PathName"],
                driver["State"],
                driver["StartMode"],
                driver["ServiceType"]
            ), tags=(tag,))

    def filter_drivers(self, event=None):
        keyword = self.search_var.get().lower()
        filtered = [
            d for d in self.driver_data
            if keyword in (d["Name"] or "").lower()
            or keyword in (d["State"] or "").lower()
            or keyword in (d["ServiceType"] or "").lower()
        ]
        self.display_drivers(filtered)

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        name = values[0]

        driver_info = next((d for d in self.driver_data if d["Name"] == name), None)
        if driver_info:
            for key in self.detail_labels:
                self.detail_labels[key].config(text=f"{key}: {driver_info.get(key, 'N/A')}")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = DriverApp(root)
    root.mainloop()
