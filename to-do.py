import tkinter as tk

class TaskList(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__() 
        
        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks
        
        self.title("Task List")
        
        instructions = tk.Label(self, text="Enter items into input field")
        self.tasks.append(instructions)
        
        for task in self.tasks:
            task.pack()
        
        self.new_task = tk.Text(self, height=4)
        self.new_task.pack()
        self.new_task.focus_set()
        
        self.bind("<Return>", self.add_task)
        
        
    def add_task(self, event=None):
        task_text = self.new_task.get(1.0, tk.END).strip()
        
        task_label = tk.Label(self, text=task_text)
        task_label.pack()
        self.tasks.append(task_label)

if __name__ == "__main__":
    task_list = TaskList()
    task_list.mainloop()
    