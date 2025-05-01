# Drive-Enumeration-Tool
A Python-based tool for enumerating loaded drivers in Windows systems. This utility helps security analysts, system administrators, and developers gain insights into the kernel-mode drivers running on a machine. It retrieves detailed information such as driver names, image paths, and state, startmode.
# 🛠️ Windows Driver Enumeration Tool (GUI)

A modern, user-friendly Python GUI application for enumerating loaded system drivers on Windows using WMI (Windows Management Instrumentation). This tool displays detailed driver information and offers filtering, exporting, and viewing capabilities — perfect for system diagnostics, security audits, and driver analysis.

---

## 🔍 Features

- ✅ Enumerates all system drivers using `wmi` module
- 🖥️ Clean and responsive Tkinter GUI with dark theme
- 🔎 Real-time search/filter by driver name, state, or type
- 📋 Displays additional details like dependencies, load order group, and error control
- 💾 Save driver information to a timestamped log file
- 🎨 Custom TreeView styling with color-coded status:
  - 🟢 Running → Green
  - 🟡 Paused → Yellow
  - 🔴 Stopped/Error → Red

---

## 🧱 Requirements

- **Windows OS**
- **Python 3.6+**
- Required modules:
  ```bash
  pip install wmi
