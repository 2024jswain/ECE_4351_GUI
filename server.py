from flask import Flask, render_template, Response, request, jsonify
import cv2

from effects.canny_edge_detection import CannyEdgeDetection
from effects.gaussian_blur import GaussianBlur
from video_processor import VideoProcessor

# Initialize Flask app
app = Flask(__name__)

# Initialize video processor
vp = VideoProcessor()
effects = [CannyEdgeDetection(), GaussianBlur()]  # Add more effects here
effect_map = {effect.__class__.__name__: effect for effect in effects}  # Create a dictionary of effects

effects_data = [
    {
        "name": effect.__class__.__name__,
        "display_name": effect.display_name,
        "parameters": {
            key: {
                "display_name": param.display_name,
                "min": param.min,
                "max": param.max,
                "value": param.value,
                "step": param.step
            } for key, param in effect.get_parameters().items()
        }
    }
    for effect in effects
]

def generate_frames():
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            break

        processed_frame = vp.process_frame(frame)

        _, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html', effects=effects_data)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update_operations', methods=['POST'])
def update_operations():
    operations = request.json.get('operations', [])
    print("Received New Order from Frontend:", operations)  # Debugging

    vp.ordered_operations = [effect_map[op] for op in operations]

    return jsonify({"status": "success", "selected_operations": [op.display_name for op in vp.ordered_operations]})

@app.route('/update_params', methods=['POST'])
def update_params():
    params = request.json

    for effect in vp.ordered_operations:
        for param_name, value in params.items():
            if param_name in effect.get_parameters():
                setattr(effect, param_name, value)

    return jsonify({"status": "success", "updated_params": params})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
