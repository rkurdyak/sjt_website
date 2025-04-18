from flask import Flask, request, render_template_string
import qrcode
import io
import base64
import urllib.parse

app = Flask(__name__)

# Inline HTML template
TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>QR Mailto Generator</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 2em auto; }
    label { display: block; margin: 0.5em 0; }
    textarea { width: 100%; height: 100px; }
    img { margin-top: 1em; max-width: 100%; height: auto; }
  </style>
</head>
<body>
  <h1>QR Mailto Generator</h1>
  <form method="post">
    <label>To: <input type="email" name="to" required></label>
    <label>Subject: <input type="text" name="subject"></label>
    <label>Body: <textarea name="body"></textarea></label>
    <button type="submit">Generate QR Code</button>
  </form>
  {% if qr_data %}
    <h2>Generated QR Code</h2>
    <img src="data:image/png;base64,{{ qr_data }}" alt="QR Code">
  {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_data = None
    if request.method == 'POST':
        to = request.form.get('to')
        subject = request.form.get('subject', '')
        body = request.form.get('body', '')

        # Construct mailto URI
        params = {}
        if subject:
            params['subject'] = subject
        if body:
            params['body'] = body
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        mailto = f"mailto:{to}"
        if query:
            mailto += f"?{query}"

        # Generate QR code image
        img = qrcode.make(mailto)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        qr_data = base64.b64encode(buf.getvalue()).decode('ascii')

    return render_template_string(TEMPLATE, qr_data=qr_data)

if __name__ == '__main__':
    # Install dependencies: pip install flask qrcode pillow
    app.run(host='0.0.0.0', port=5000, debug=True)
