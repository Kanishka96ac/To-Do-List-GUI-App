import tkinter as tk
from tkinter import font, messagebox

class TaskList(tk.Tk):
    def __init__(self):
        super().__init__()

        # === Window Setup ===
        self.title("✨ My Dark To-Do App")
        self.geometry("520x640")
        self.configure(bg="#121212")  # Pure dark background

        # Custom font for consistency
        self.custom_font = font.Font(family="Segoe UI", size=12)

        # To keep track of task frames
        self.tasks = []

        # === Header ===
        header = tk.Label(
            self,
            text="📝 Stay Productive",
            bg="#1F1F1F",
            fg="#FFFFFF",
            font=("Segoe UI", 18, "bold"),
            pady=18
        )
        header.pack(fill=tk.X)

        # === Task Input Field ===
        self.new_task = tk.Text(
            self,
            height=2,
            font=self.custom_font,
            bg="#1E1E1E",               # Dark background for input
            fg="#E0E0E0",               # Light text color
            insertbackground="#E0E0E0", # White cursor
            padx=12,
            pady=8,
            relief=tk.FLAT,
            bd=0
        )
        self.new_task.pack(padx=20, pady=(15, 5), fill=tk.X)
        self.new_task.focus_set()

        # Add task when pressing Enter
        self.bind("<Return>", self.add_task)

        # === Reset Button ===
        self.reset_btn = tk.Button(
            self,
            text="⟳ Clear All Tasks",
            command=self.reset_tasks,
            bg="#333333",              # Button background
            fg="#FFFFFF",              # Button text
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#555555",
            bd=0
        )
        self.reset_btn.pack(pady=10, padx=20, anchor="e")

        # Hover effect for reset button
        self.reset_btn.bind("<Enter>", lambda e: self.reset_btn.config(bg="#555555"))
        self.reset_btn.bind("<Leave>", lambda e: self.reset_btn.config(bg="#333333"))

        # === Scrollable Task List Area ===
        container = tk.Frame(self, bg="#121212")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        self.canvas = tk.Canvas(container, bg="#121212", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Task container inside the canvas
        self.task_frame = tk.Frame(self.canvas, bg="#121212")
        self.task_window = self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")

        # Resize canvas when content or window changes
        self.task_frame.bind("<Configure>", self._update_scrollregion)
        self.canvas.bind("<Configure>", self._frame_width)

        # Scroll using mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    # === Scroll Support Functions ===

    def _frame_width(self, event):
        # Make sure task area stretches to canvas width
        self.canvas.itemconfig(self.task_window, width=event.width)

    def _update_scrollregion(self, event=None):
        # Automatically update scroll area size
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        # Enable scrolling with mouse wheel
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # === Core Logic ===

    def add_task(self, event=None):
        """
        Extract task from input box, clean it, and create new task block.
        """
        task_text = self.new_task.get("1.0", tk.END).strip()
        if not task_text:
            return "break"

        self.new_task.delete("1.0", tk.END)
        self._create_task(task_text)
        return "break"  # Prevent default newline in text box

    def _create_task(self, text):
        """
        Visually create a new task row with label, ✔ and ✖ buttons.
        """
        row = tk.Frame(self.task_frame, bg="#1E1E1E", pady=6)
        row.pack(fill=tk.X, pady=5, padx=2)

        label = tk.Label(
            row,
            text=text,
            font=self.custom_font,
            fg="#E0E0E0",
            bg="#1E1E1E",
            anchor="w",
            wraplength=320,
            justify="left"
        )
        label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        # ✔ Done button
        done_btn = tk.Button(
            row,
            text="✔",
            command=lambda: self.toggle_done(label),
            bg="#2E7D32",  # Green
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=3,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#1B5E20"
        )
        done_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # ✖ Delete button
        del_btn = tk.Button(
            row,
            text="✖",
            command=lambda: self.delete_task(row),
            bg="#C62828",  # Red
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=3,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#8E0000"
        )
        del_btn.pack(side=tk.RIGHT, padx=(5, 5))

        self.tasks.append(row)
        self._update_scrollregion()

    def toggle_done(self, label):
        """
        Cross out a task and dim text if marked as done.
        """
        font_style = label.cget("font")
        if "overstrike" in str(font_style):
            label.config(font=self.custom_font, fg="#E0E0E0")
        else:
            label.config(
                font=(self.custom_font.actual("family"), 12, "overstrike"),
                fg="#777777"
            )

    def delete_task(self, row):
        """
        Remove a task row from the view and memory.
        """
        row.destroy()
        self.tasks.remove(row)
        self._update_scrollregion()

    def reset_tasks(self):
        """
        Clear all tasks after user confirms.
        """
        if messagebox.askyesno("Clear All", "Do you want to delete all tasks?"):
            for row in self.tasks:
                row.destroy()
            self.tasks.clear()
            self._update_scrollregion()


# === Run the Application ===
if __name__ == "__main__":
    app = TaskList()
    app.mainloop()
