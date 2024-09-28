from flask import Flask, jsonify, render_template, request, url_for
import qrcode
import os

app = Flask(__name__)

# Ensure the directory exists within the project folder
qr_code_dir = os.path.join(app.root_path, 'static/generated_qr_codes')
os.makedirs(qr_code_dir, exist_ok=True)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/history')
def history():
    qr_codes = os.listdir('static/generated_qr_codes')
    qr_codes = [url_for('static', filename=f'generated_qr_codes/{filename}') for filename in qr_codes]
    return render_template('history.html', qr_codes=qr_codes)

@app.route('/qr/<filename>')
def display_qr(filename):
    filepath = url_for('static', filename=f'generated_qr_codes/{filename}')
    return render_template('display_qr.html', filepath=filepath , filename=filename)

@app.route('/api/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json.get('data')
    filename = request.json.get('filename')
    if not data or not filename:
        return jsonify({'error': 'Data and filename are required'}), 400

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Save the image to the specified directory
    filepath = os.path.join('static/generated_qr_codes', f'{filename}.png')
    img.save(filepath)

    return jsonify({'message': f'QR code saved as {filename}.png', 'filepath': url_for('static', filename=f'generated_qr_codes/{filename}.png')})

@app.route('/api/delete_qr', methods=['POST'])
def delete_qr():
    filename = request.json.get('filename')
    if not filename:
        return jsonify({'error': 'Filename is required'}), 400

    filepath = os.path.join('static/generated_qr_codes', filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'message': f'{filename} deleted successfully'})
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)