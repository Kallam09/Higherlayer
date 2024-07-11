from flask import Flask, jsonify, Response
import requests

app = Flask(__name__)

# Define configuration variables for the replica servers
REPLICA_SERVERS = ['http://localhost:8081', 'http://localhost:8082', 'http://localhost:8083']

# Initialize round-robin index for each video
round_robin_index = {'video1': 0, 'video2': 0}

def get_next_replica(video_name):
    global round_robin_index
    replica_count = len(REPLICA_SERVERS)
    if replica_count == 0:
        return None
    selected_replica = REPLICA_SERVERS[round_robin_index[video_name]]
    round_robin_index[video_name] = (round_robin_index[video_name] + 1) % replica_count
    return selected_replica

@app.route('/')
def home():
    return "Welcome to the Video Controller!"

@app.route('/<video_name>')
def get_video(video_name):
    for _ in range(len(REPLICA_SERVERS)):
        selected_replica = get_next_replica(video_name)
        if selected_replica:
            # Extract the port number from the replica server URL
            replica_port = selected_replica.split(':')[-1]
            print(f"Fetching video '{video_name}' from replica server on port {replica_port}")

            # Return the video from the first available replica server
            response = requests.get(selected_replica + f'/{video_name}', stream=True)
            return Response(response.iter_content(chunk_size=1024), content_type='video/mp4')
    # If no replica server has the video available, return an error
    return jsonify({'error': f'{video_name} not available'}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=8084, threaded=True)
