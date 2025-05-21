from flask import Flask, render_template, request
import fitz  # PyMuPDF
from docx import Document

app = Flask(__name__)

def leer_pdf(archivo):
    doc = fitz.open(stream=archivo.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto


def leer_docx(archivo):
    doc = Document(archivo)
    texto = ""
    for para in doc.paragraphs:
        texto += para.text + "\n"
    return texto


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        archivo = request.files.get("archivo")
        if not archivo:
            return "No se ha subido ningún archivo"

        nombre = archivo.filename.lower()
        texto = ""

        if nombre.endswith(".pdf"):
            texto = leer_pdf(archivo)
        elif nombre.endswith(".docx"):
            texto = leer_docx(archivo)
        else:
            return "Formato no soportado. Solo PDF y DOCX."

        # Estadísticas simples
        num_caracteres = len(texto)
        num_palabras = len(texto.split())
        num_lineas = texto.count('\n') + 1

        return render_template("resultado.html", texto=texto, caracteres=num_caracteres, palabras=num_palabras, lineas=num_lineas)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
