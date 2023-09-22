import tkinter as tk
from tkinter import filedialog
import re

def modify_gcode(input_file, output_file):
    try:
        with open(input_file, 'r') as input_file:
            with open(output_file, 'w') as output_file:
                original_content = []
                modified_content = []

                for line in input_file:
                    modified_line = re.sub(r'(G01 X[^ ]+ Y[^ ]+) F(\d+\.\d+)', r'\1 Z0.000 F\2', line)
                    original_content.append(line)
                    modified_content.append(modified_line)
                    output_file.write(modified_line)

                original_text.config(state=tk.NORMAL)
                modified_text.config(state=tk.NORMAL)
                original_text.delete(1.0, tk.END)
                modified_text.delete(1.0, tk.END)
                original_text.insert(tk.END, ''.join(original_content))
                modified_text.insert(tk.END, ''.join(modified_content))
                original_text.config(state=tk.DISABLED)
                modified_text.config(state=tk.DISABLED)

                # Add line numbers to the original and modified_text previews
                add_line_numbers(original_text)
                add_line_numbers(modified_text)

    except FileNotFoundError:
        print(f"Input file '{input_file}' not found.")

def add_line_numbers(text_widget):
    # Insert line numbers at the beginning of each line
    text_widget.config(state=tk.NORMAL)
    line_numbers = "\n".join(f"{i + 1}: {line}" for i, line in enumerate(text_widget.get(1.0, tk.END).splitlines()))
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, line_numbers)
    text_widget.config(state=tk.DISABLED)

def browse_input_file():
    file_path = filedialog.askopenfilename()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

    try:
        with open(file_path, 'r') as selected_file:
            input_content = selected_file.read()
            original_text.config(state=tk.NORMAL)
            original_text.delete(1.0, tk.END)
            original_text.insert(tk.END, input_content)
            original_text.config(state=tk.DISABLED)
            add_line_numbers(original_text)  # Add line numbers

    except FileNotFoundError:
        print(f"Input file '{file_path}' not found.")

def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".nc")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)

def process_gcode():
    input_file = input_entry.get()
    output_file = output_entry.get()
    modify_gcode(input_file, output_file)
    result_label.config(text="G-code modification complete.")

    try:
        with open(output_file, 'r') as modified_file:
            modified_content = modified_file.read()
            modified_text.config(state=tk.NORMAL)
            modified_text.delete(1.0, tk.END)
            modified_text.insert(tk.END, modified_content)
            modified_text.config(state=tk.DISABLED)
            add_line_numbers(modified_text)  # Add line numbers to modified_text

    except FileNotFoundError:
        print(f"Modified file '{output_file}' not found.")

def on_original_scroll(*args):
    original_text.yview_moveto(args[0])
    modified_text.yview_moveto(args[0])

app = tk.Tk()
app.title("G-code Modifier")

input_label = tk.Label(app, text="Input File:")
input_label.pack()
input_entry = tk.Entry(app, width=50)
input_entry.pack()
input_button = tk.Button(app, text="Browse", command=browse_input_file)
input_button.pack()

output_label = tk.Label(app, text="Output File:")
output_label.pack()
output_entry = tk.Entry(app, width=50)
output_entry.pack()
output_button = tk.Button(app, text="Browse", command=browse_output_file)
output_button.pack()

process_button = tk.Button(app, text="Process G-code", command=process_gcode)
process_button.pack()

result_label = tk.Label(app, text="")
result_label.pack()

preview_label = tk.Label(app, text="File Preview")
preview_label.pack()

frame = tk.Frame(app)
frame.pack()

original_text = tk.Text(frame, wrap=tk.WORD, height=20, width=40, state=tk.DISABLED)
original_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

original_scroll = tk.Scrollbar(frame, command=on_original_scroll)
original_scroll.pack(side=tk.RIGHT, fill=tk.Y)
original_text.config(yscrollcommand=original_scroll.set)

modified_text = tk.Text(frame, wrap=tk.WORD, height=20, width=40, state=tk.DISABLED)
modified_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

app.mainloop()
