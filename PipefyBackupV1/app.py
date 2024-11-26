from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from PipefyManager import create_backup

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pipe_id = request.form.get('pipe_id')  # Obtener el PIPE ID del formulario
        if not pipe_id:
            flash('Por favor, ingresa el PIPE ID.')
            return redirect(url_for('index'))

        try:
            # Llama a la función de backup
            output_filename = create_backup(pipe_id)
            # Enviar el archivo generado como descarga
            return send_file(output_filename, as_attachment=True)
        except Exception as e:
            flash(f"Ocurrió un error: {e}")
            return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
