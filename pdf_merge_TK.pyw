import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import io

# Function to merge PDFs
def merge_pdfs(pdf1_path, pdf2_path, password1, password2, output_name):
    pdf_writer = PyPDF2.PdfWriter()

    # Process the first PDF
    with open(pdf1_path, 'rb') as pdf1_file:
        pdf1_bytes = io.BytesIO(pdf1_file.read())
        pdf_reader1 = PyPDF2.PdfReader(pdf1_bytes)
        if pdf_reader1.is_encrypted and password1:
            pdf_reader1.decrypt(password1)
        for page_num in range(len(pdf_reader1.pages)):
            page = pdf_reader1.pages[page_num]
            pdf_writer.add_page(page)

    # Process the second PDF
    with open(pdf2_path, 'rb') as pdf2_file:
        pdf2_bytes = io.BytesIO(pdf2_file.read())
        pdf_reader2 = PyPDF2.PdfReader(pdf2_bytes)
        if pdf_reader2.is_encrypted and password2:
            pdf_reader2.decrypt(password2)
        for page_num in range(len(pdf_reader2.pages)):
            page = pdf_reader2.pages[page_num]
            pdf_writer.add_page(page)

    # Write the merged PDF to the desktop
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    output_path = os.path.join(desktop_path, f"{output_name}.pdf")
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    return output_path

# Function to handle the merge button click
def on_merge():
    pdf1_path = entry_pdf1.get()
    pdf2_path = entry_pdf2.get()
    password1 = entry_password1.get()
    password2 = entry_password2.get()
    output_name = entry_output_name.get()

    if not pdf1_path or not pdf2_path or not output_name:
        messagebox.showerror("Error", "Please provide all required inputs.")
        return

    try:
        output_path = merge_pdfs(pdf1_path, pdf2_path, password1, password2, output_name)
        messagebox.showinfo("Success", f"Merged PDF saved as {output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to browse for PDF files
def browse_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

# Tkinter GUI setup
root = tk.Tk()
root.title("PDF Merger")

# PDF 1 selection
label_pdf1 = tk.Label(root, text="Select first PDF:")
label_pdf1.grid(row=0, column=0, padx=10, pady=10, sticky='w')
entry_pdf1 = tk.Entry(root, width=30)
entry_pdf1.grid(row=0, column=1, padx=10, pady=10)
button_browse_pdf1 = tk.Button(root, text="Browse", command=lambda: browse_file(entry_pdf1))
button_browse_pdf1.grid(row=0, column=2, padx=10, pady=10)

# Password for PDF 1
label_password1 = tk.Label(root, text="Password (if any):")
label_password1.grid(row=0, column=3, padx=10, pady=10)
entry_password1 = tk.Entry(root, show='*', width=20)
entry_password1.grid(row=0, column=4, padx=10, pady=10)

# PDF 2 selection
label_pdf2 = tk.Label(root, text="Select second PDF:")
label_pdf2.grid(row=1, column=0, padx=10, pady=10, sticky='w')
entry_pdf2 = tk.Entry(root, width=30)
entry_pdf2.grid(row=1, column=1, padx=10, pady=10)
button_browse_pdf2 = tk.Button(root, text="Browse", command=lambda: browse_file(entry_pdf2))
button_browse_pdf2.grid(row=1, column=2, padx=10, pady=10)

# Password for PDF 2
label_password2 = tk.Label(root, text="Password (if any):")
label_password2.grid(row=1, column=3, padx=10, pady=10)
entry_password2 = tk.Entry(root, show='*', width=20)
entry_password2.grid(row=1, column=4, padx=10, pady=10)

# Output file name
label_output_name = tk.Label(root, text="Output file name (without .pdf):")
label_output_name.grid(row=2, column=0, padx=10, pady=10, sticky='w')
entry_output_name = tk.Entry(root, width=30)
entry_output_name.grid(row=2, column=1, padx=10, pady=10)

# Merge button
button_merge = tk.Button(root, text="Merge PDFs", command=on_merge)
button_merge.grid(row=3, column=1, columnspan=2, pady=20)

root.mainloop()
