# ---------------------------------------------
# CODTECH TEXT SUMMARIZATION TOOL (Sumy + Tkinter GUI)
# Using LexRank Summarizer
# ---------------------------------------------

# Install dependencies:
# pip install sumy

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer  # <-- Changed here

def summarize_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            input_text = f.read()
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_path}' not found.")
        return ""

    if len(input_text.split('.')) < 3:
        messagebox.showwarning("Warning", "Please use a longer text with at least 3 sentences.")
        return ""

    parser = PlaintextParser.from_string(input_text, Tokenizer("english"))
    summarizer = LexRankSummarizer()  # <-- Using LexRank instead of LSA

    summary = summarizer(parser.document, 3)  # Fewer sentences for more compression

    result = '\n'.join(str(sentence) for sentence in summary)

    # Save summary to file
    with open("output_summary.txt", 'w', encoding='utf-8') as f:
        f.write(result)

    return result

def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")],
        title="Select Input Text File"
    )
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def generate_summary():
    file_path = entry_file.get().strip()
    if not file_path:
        messagebox.showwarning("Warning", "Please select an input file.")
        return

    summary = summarize_text(file_path)

    if summary:
        text_summary.delete('1.0', tk.END)
        text_summary.insert(tk.END, summary)
        messagebox.showinfo("Success", "Summary generated and saved to 'output_summary.txt'.")

# -------------------------------
# Create the GUI Window
# -------------------------------

root = tk.Tk()
root.title("CODTECH Text Summarization Tool (LexRank)")
root.geometry("700x500")
root.resizable(False, False)

label_title = tk.Label(root, text="CODTECH TEXT SUMMARIZATION TOOL", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

frame_file = tk.Frame(root)
frame_file.pack(pady=5)

entry_file = tk.Entry(frame_file, width=50)
entry_file.pack(side=tk.LEFT, padx=5)

btn_browse = tk.Button(frame_file, text="Browse", command=browse_file)
btn_browse.pack(side=tk.LEFT)

btn_summarize = tk.Button(root, text="Generate Summary", command=generate_summary, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
btn_summarize.pack(pady=10)

label_output = tk.Label(root, text="Generated Summary:", font=("Arial", 12, "bold"))
label_output.pack()

text_summary = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
text_summary.pack(padx=10, pady=10)

root.mainloop()
