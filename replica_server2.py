from flask import Flask, Response, send_file, request
import os

app = Flask(__name__)

# Directory to store replicated videos
replica_video_directory = 'replicated_videos'

@app.route('/')
def home():
    return "Welcome to Replica Server 2!"

@app.route('/<video_name>')
def serve_replicated_video(video_name):
    video_path = os.path.join(replica_video_directory, f'{video_name}.mp4')

    if os.path.exists(video_path):
        return send_file(video_path, mimetype='video/mp4')

    return 'Video not found', 404

@app.route('/replicate', methods=['POST'])
def replicate_video():
    try:
        video_name = request.form['video_name']
        video_content = request.files['video'].read()

        # Save replicated video
        video_path = os.path.join(replica_video_directory, f'{video_name}.mp4')
        with open(video_path, 'wb') as video_file:
            video_file.write(video_content)

        return 'Video replicated successfully', 200
    except Exception as e:
        print(f'Error replicating video: {str(e)}')
        return 'Internal server error', 500

if __name__ == '__main__':
    app.run(host='localhost', port=8082, threaded=True)
