import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import sqlite3
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class ProjectManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Manager")

        self.create_menu()

        self.current_project_path = None
        self.current_conn = None
        self.current_cursor = None

        self.create_record_button()
        self.create_pdf_button()
        self.create_records_table()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.create_new_project)
        file_menu.add_command(label="Open Project", command=self.open_project)
        file_menu.add_command(label="Save Project", command=self.save_project)

    def create_new_project(self):
        project_name = tk.simpledialog.askstring("New Project", "Enter project name:")
        if project_name:
            project_path = os.path.join(os.path.expanduser("~"), "Documents", project_name)
            os.makedirs(project_path, exist_ok=True)
            self.current_project_path = project_path

            # Create project-specific database
            self.current_conn = sqlite3.connect(os.path.join(project_path, "project_records.db"))
            self.current_cursor = self.current_conn.cursor()
            self.current_cursor.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, field1 TEXT, field2 TEXT)")
            self.current_conn.commit()

            messagebox.showinfo("Success", f"Project '{project_name}' created at {project_path}")

    def open_project(self):
        project_path = filedialog.askdirectory(title="Open Project")
        if project_path:
            self.current_project_path = project_path
            self.current_conn = sqlite3.connect(os.path.join(project_path, "project_records.db"))
            self.current_cursor = self.current_conn.cursor()
            self.populate_records_table()
            messagebox.showinfo("Success", f"Opened project at {project_path}")

    def save_project(self):
        if self.current_conn:
            self.current_conn.commit()
            messagebox.showinfo("Save Project", "Project saved successfully.")

    def create_record_button(self):
        self.record_button = tk.Button(self.root, text="Add Record", command=self.add_record)
        self.record_button.pack()

    def add_record(self):
        if self.current_cursor:
            field1 = tk.simpledialog.askstring("Add Record", "Enter Field 1:")
            field2 = tk.simpledialog.askstring("Add Record", "Enter Field 2:")
            if field1 and field2:
                self.current_cursor.execute("INSERT INTO records (field1, field2) VALUES (?, ?)", (field1, field2))
                self.current_conn.commit()
                self.populate_records_table()
                messagebox.showinfo("Success", "Record added successfully.")

    def create_records_table(self):
        self.tree = ttk.Treeview(self.root, columns=("Field 1", "Field 2"))
        self.tree.heading("#1", text="Field 1")
        self.tree.heading("#2", text="Field 2")
        self.tree.pack()

        self.populate_records_table()

    def populate_records_table(self):
        if self.current_cursor:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            self.current_cursor.execute("SELECT * FROM records")
            records = self.current_cursor.fetchall()
            for record in records:
                self.tree.insert("", "end", values=(record[1], record[2]))
    
    def create_pdf_button(self):
        self.pdf_button = tk.Button(self.root, text="Create PDF", command=self.create_pdf)
        self.pdf_button.pack()

    def create_pdf(self):
        if self.current_cursor:
            records = self.current_cursor.execute("SELECT * FROM records").fetchall()

            if not records:
                messagebox.showinfo("Info", "No records to create PDF.")
                return

            pdf_file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])

            if pdf_file_path:
                doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
                elements = []

                # Create table for the PDF
                table_data = [["Field 1", "Field 2"]]
                for record in records:
                    table_data.append([record[1], record[2]])

                pdf_table = Table(table_data)
                pdf_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), (0.7, 0.7, 0.7)),
                    ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
                    ('GRID', (0, 0), (-1, -1), 1, (0.5, 0.5, 0.5)),
                ]))

                elements.append(pdf_table)
                doc.build(elements)
                messagebox.showinfo("Success", f"PDF created and saved at: {pdf_file_path}")

    # ... (rest of the code remains the same)


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectManagerApp(root)
    root.mainloop()
