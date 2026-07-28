from flask import Flask, request, render_template_string, send_file
import qrcode
import io

app = Flask(__name__)

# The HTML Interface
# (Usually kept in a separate templates/ folder, but kept here for simplicity)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QR Code Generator</title>
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            text-align: center;
            background-color: #f4f4f9;
            padding-top: 50px;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            max-width: 500px;
            margin: 0 auto;
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background-color: #0056b3; }
        #qr-result { margin-top: 25px; }
        img { max-width: 100%; height: auto; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>QR Code Generator</h2>
        <form id="qr-form">
            <input type="text" id="url-input" placeholder="Enter URL or text" required>
            <button type="submit">Generate</button>
        </form>
        
        <div id="qr-result">
            <!-- The generated image will be injected here -->
            <img id="qr-image" src="" alt="QR Code" style="display:none; margin: 0 auto;">
        </div>
    </div>

    <script>
        document.getElementById('qr-form').addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent page reload
            
            const url = document.getElementById('url-input').value;
            const img = document.getElementById('qr-image');
            
            // Set the image source to our Python backend endpoint.
            // We add a timestamp (getTime) to prevent the browser from caching old QR codes.
            img.src = '/generate?url=' + encodeURIComponent(url) + '&t=' + new Date().getTime();
            img.style.display = 'block';
        });
    </script>
</body>
</html>
"""

# Route 1: Serve the HTML interface
@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

# Route 2: The API endpoint that generates the QR code
@app.route('/generate')
def generate():
    # Get the URL string from the frontend request
    url = request.args.get('url')
    if not url:
        return "No URL provided", 400

    # Generate the QR code
    img = qrcode.make(url)

    # Save the image to a memory buffer instead of the hard drive
    memory_buffer = io.BytesIO()
    img.save(memory_buffer, 'PNG')
    memory_buffer.seek(0) # Reset the buffer pointer to the beginning

    # Send the image back to the HTML page
    return send_file(memory_buffer, mimetype='image/png')

if __name__ == '__main__':
    # Run the server
    app.run(debug=True, port=5000)