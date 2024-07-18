from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from label_extractor import extract_and_stitch_frames
from text_extractor import extract_text_from_image
from name_extractor import extract_label_name_from_text
from flask_cors import CORS
import os
import os
import jwt
from functools import wraps
from dotenv import load_dotenv
import shutil  # Import shutil for handling file operations
import base64

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

def jwt_required(f):
    @wraps(f)  # Use wraps here to preserve function metadata
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Missing JWT token'}), 401

        try:
            # Decode the JWT token using the secret key
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            username = request.headers.get('username')
            # Check if the username in the token matches the one in the request
            if payload['username'] == username:
                # Add the decoded payload to the request context
                request.current_user = payload
            else:
                return jsonify({'message': 'Invalid username in JWT token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'JWT token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid JWT token'}), 401

        return f(*args, **kwargs)
    return decorated_function


# Define a folder to store uploaded video files temporarily
UPLOAD_FOLDER = 'uploads'
VIDEO_FOLDER = os.path.join(UPLOAD_FOLDER, 'video')
FRAMES_FOLDER = os.path.join(UPLOAD_FOLDER, 'frames')
STITCHED_IMAGE_FOLDER = os.path.join(UPLOAD_FOLDER, 'stitched_image')

# Create directories if they do not exist
for folder in [UPLOAD_FOLDER, VIDEO_FOLDER, FRAMES_FOLDER, STITCHED_IMAGE_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
app.config['FRAMES_FOLDER'] = FRAMES_FOLDER
app.config['STITCHED_IMAGE_FOLDER'] = STITCHED_IMAGE_FOLDER

def clean_up(directories):
    for directory in directories:
        shutil.rmtree(directory)
        os.makedirs(directory)  # Recreate directory to ensure it's available for the next request

@app.route('/extract-labels', methods=['POST'])
@jwt_required
def extract_labels():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not file.filename.endswith(('.mp4', '.avi', '.mkv')):
        return jsonify({'error': 'Invalid file format'}), 400

    filename = secure_filename(file.filename)
    video_path = os.path.join(app.config['VIDEO_FOLDER'], filename)
    file.save(video_path)

    stitched_image_path, error = extract_and_stitch_frames(video_path, app.config['FRAMES_FOLDER'], app.config['STITCHED_IMAGE_FOLDER'])
    if error:
        clean_up([app.config['VIDEO_FOLDER'], app.config['FRAMES_FOLDER'], app.config['STITCHED_IMAGE_FOLDER']])
        return jsonify({'error': error}), 500
    text = extract_text_from_image(stitched_image_path)
    label_name = extract_label_name_from_text(text)
    
    try:
        with open(stitched_image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        clean_up([app.config['VIDEO_FOLDER'], app.config['FRAMES_FOLDER'], app.config['STITCHED_IMAGE_FOLDER']])
        return jsonify({'error': str(e)}), 500

    # Clean up the temporary files
    clean_up([app.config['VIDEO_FOLDER'], app.config['FRAMES_FOLDER'], app.config['STITCHED_IMAGE_FOLDER']])

    return jsonify({
            'label_name': label_name,
            'image_content': text,
            'image_data': encoded_string
        }), 200

if __name__ == '__main__':
    port = 5002  # Choose the port number you want to use
    app.run(debug=True, port=port)
    print(f"Server is running on port {port}")
