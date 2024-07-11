from flask import Flask, Response
import os
import requests

app = Flask(__name__)

# Directory where video files are located
video_directory = 'videos'

# List of replica servers
replica_servers = [
    'http://localhost:8081', 'http://localhost:8082', 'http://localhost:8083'
]

@app.route('/')
def home():
    return "Welcome to the Origin Server!"

def replicate_video(video_name):
    video_path = os.path.abspath(os.path.join(video_directory, video_name + '.mp4'))

    if os.path.exists(video_path):
        with open(video_path, 'rb') as video_file:
            video_content = video_file.read()

        for replica_server in replica_servers:
            try:
                # Push video to replica server
                response = requests.post(replica_server + '/replicate', data={'video_name': video_name}, files={'video': video_content})
                if response.status_code == 200:
                    print(f"Video {video_name} replicated to {replica_server}")
            except requests.exceptions.ConnectionError:
                print(f'Error connecting to the replica server: {replica_server}')
            except requests.exceptions.HTTPError:
                print(f'Error replicating video to the replica server: {replica_server}')

    else:
        print(f'Video not found: {video_name}')

    # Return the video from the origin server
    video_path = os.path.abspath(os.path.join(video_directory, f'{video_name}.mp4'))
    if os.path.exists(video_path):
        def generate():
            with open(video_path, 'rb') as video_file:
                while True:
                    video_chunk = video_file.read(1024)
                    if not video_chunk:
                        break
                    yield video_chunk

        return Response(generate(), mimetype='video/mp4')

    return 'Video not found', 404

@app.route('/video1')
def serve_video1():
    return replicate_video('video1')

@app.route('/video2')
def serve_video2():
    return replicate_video('video2')

if __name__ == '__main__':
    # Specify the SSL certificate and private key
    ssl_certificate = 'C:\\Users\\smile\\mydomain.crt'
    ssl_private_key = 'C:\\Users\\smile\\mydomain.key'

    # Run the app with SSL
    app.run(host='localhost', port=8080, ssl_context=(ssl_certificate, ssl_private_key))
