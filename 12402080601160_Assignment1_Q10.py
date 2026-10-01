"""
Q10 - Tkinter Assignment Tracker with JSON Persistence and CSV Export

No external packages required.
Data is saved to assignment_data.json.
"""
import csv
import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


DATA_FILE = Path("assignment_data.json")


class AssignmentTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assignment Tracker")
        self.geometry("900x600")
        self.minsize(800, 520)

        self.records = []
        self.load_data()
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        form = ttk.LabelFrame(self, text="Submission Details", padding=10)
        form.pack(fill="x", padx=10, pady=10)

        labels = ["Enrollment", "Name", "Assignment", "Status", "Marks", "Remarks"]
        for col, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=0, column=col, padx=5, pady=5)

        self.enrollment = ttk.Entry(form, width=16)
        self.name = ttk.Entry(form, width=16)
        self.assignment = ttk.Entry(form, width=18)
        self.status = ttk.Combobox(
            form, values=["Pending", "Completed"], state="readonly", width=13
        )
        self.status.set("Pending")
        self.marks = ttk.Entry(form, width=10)
        self.remarks = ttk.Entry(form, width=22)

        widgets = [
            self.enrollment, self.name, self.assignment,
            self.status, self.marks, self.remarks
        ]
        for col, widget in enumerate(widgets):
            widget.grid(row=1, column=col, padx=5, pady=5)

        ttk.Button(form, text="Add / Update", command=self.save_record).grid(
            row=2, column=0, columnspan=2, pady=8
        )
        ttk.Button(form, text="Clear", command=self.clear_form).grid(
            row=2, column=2, pady=8
        )
        ttk.Button(form, text="Export CSV", command=self.export_csv).grid(
            row=2, column=3, columnspan=2, pady=8
        )

        filter_frame = ttk.Frame(self, padding=(10, 0))
        filter_frame.pack(fill="x")
        ttk.Label(filter_frame, text="Filter:").pack(side="left")
        self.filter_var = tk.StringVar(value="All")
        filter_box = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All", "Pending", "Completed"],
            state="readonly",
            width=15,
        )
        filter_box.pack(side="left", padx=8)
        filter_box.bind("<<ComboboxSelected>>", lambda _: self.refresh_table())

        columns = ("enrollment", "name", "assignment", "status", "marks", "remarks")
        self.table = ttk.Treeview(self, columns=columns, show="headings")
        headings = {
            "enrollment": "Enrollment",
            "name": "Name",
            "assignment": "Assignment",
            "status": "Status",
            "marks": "Marks",
            "remarks": "Remarks",
        }
        widths = {
            "enrollment": 100, "name": 130, "assignment": 140,
            "status": 100, "marks": 80, "remarks": 220
        }
        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(col, width=widths[col])

        self.table.pack(fill="both", expand=True, padx=10, pady=10)
        self.table.bind("<<TreeviewSelect>>", self.load_selected)

    def validate(self):
        enrollment = self.enrollment.get().strip()
        name = self.name.get().strip()
        assignment = self.assignment.get().strip()
        status = self.status.get().strip()
        marks_text = self.marks.get().strip()
        remarks = self.remarks.get().strip()

        if not enrollment or not name or not assignment:
            raise ValueError("Enrollment, name and assignment are required.")

        if status not in {"Pending", "Completed"}:
            raise ValueError("Invalid status.")

        if marks_text:
            try:
                marks = float(marks_text)
            except ValueError as exc:
                raise ValueError("Marks must be numeric.") from exc
            if not 0 <= marks <= 100:
                raise ValueError("Marks must be between 0 and 100.")
        else:
            marks = ""

        if status == "Completed" and marks == "":
            raise ValueError("Completed submissions must have marks.")

        return {
            "enrollment": enrollment,
            "name": name,
            "assignment": assignment,
            "status": status,
            "marks": marks,
            "remarks": remarks,
        }

    def save_record(self):
        try:
            record = self.validate()
        except ValueError as exc:
            messagebox.showerror("Validation Error", str(exc))
            return

        # Update matching enrollment + assignment, otherwise add a record.
        for index, existing in enumerate(self.records):
            if (existing["enrollment"] == record["enrollment"]
                    and existing["assignment"] == record["assignment"]):
                self.records[index] = record
                break
        else:
            self.records.append(record)

        self.persist()
        self.refresh_table()
        self.clear_form()

    def clear_form(self):
        for widget in [
            self.enrollment, self.name, self.assignment, self.marks, self.remarks
        ]:
            widget.delete(0, tk.END)
        self.status.set("Pending")
        self.table.selection_remove(self.table.selection())

    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)

        selected_filter = self.filter_var.get()
        for record in self.records:
            if selected_filter != "All" and record["status"] != selected_filter:
                continue

            values = (
                record["enrollment"], record["name"], record["assignment"],
                record["status"], record["marks"], record["remarks"]
            )
            self.table.insert("", tk.END, values=values)

    def load_selected(self, _event=None):
        selection = self.table.selection()
        if not selection:
            return
        values = self.table.item(selection[0], "values")

        self.clear_form()
        self.enrollment.insert(0, values[0])
        self.name.insert(0, values[1])
        self.assignment.insert(0, values[2])
        self.status.set(values[3])
        self.marks.insert(0, values[4])
        self.remarks.insert(0, values[5])

    def load_data(self):
        if not DATA_FILE.exists():
            return
        try:
            with DATA_FILE.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            if not isinstance(data, list):
                raise ValueError("Stored data is not a list.")
            self.records = data
        except (OSError, json.JSONDecodeError, ValueError):
            messagebox.showwarning(
                "Data Warning",
                "Could not read assignment_data.json. Starting with empty data."
            )
            self.records = []

    def persist(self):
        try:
            with DATA_FILE.open("w", encoding="utf-8") as handle:
                json.dump(self.records, handle, indent=2)
        except OSError as exc:
            messagebox.showerror("Save Error", str(exc))

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            title="Export CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return

        fields = ["enrollment", "name", "assignment", "status", "marks", "remarks"]
        try:
            with open(path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(self.records)
            messagebox.showinfo("Export Complete", f"CSV saved to:\n{path}")
        except OSError as exc:
            messagebox.showerror("Export Error", str(exc))


if __name__ == "__main__":
    app = AssignmentTracker()
    app.mainloop()
