from flask import Flask, render_template, request
import pdfplumber

app = Flask(__name__)

def encontrar_objetivos_y_justificaciones(pdf_path):
    objetivos = []
    justificaciones = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            if i > 5:
                text = page.extract_text()
                parrafos = text.split('\n\n')
                for parrafo in parrafos:
                    if "Objetivos" in parrafo:
                        objetivos.append(parrafo.strip())
                    elif "Justificación" in parrafo:
                        justificaciones.append(parrafo.strip())
    return objetivos, justificaciones

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        objetivos, justificaciones = encontrar_objetivos_y_justificaciones(file)
        return render_template('resultados.html', objetivos=objetivos, justificaciones=justificaciones)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
