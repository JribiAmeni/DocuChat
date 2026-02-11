import os
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        return text.replace("-\n", "").replace("\n", " ")
    except Exception as e:
        print(f"❌ PDF error ({pdf_path}): {e}")
        return ""

def extract_text_from_txt(txt_path):
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"❌ TXT error ({txt_path}): {e}")
        return ""

def load_documents(folder_path):
    documents = []

    if not os.path.exists(folder_path):
        print("❌ Folder not found")
        return documents

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)

        if file.endswith(".pdf"):
            print(f"📄 Loading PDF: {file}")
            text = extract_text_from_pdf(path)
        elif file.endswith(".txt"):
            print(f"📄 Loading TXT: {file}")
            text = extract_text_from_txt(path)
        else:
            continue

        if text.strip():
            documents.append((file, text))

    return documents
