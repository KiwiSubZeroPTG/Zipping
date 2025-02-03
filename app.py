from flask import Flask, render_template, jsonify
from monitor import WebsiteObserver
import threading

app = Flask(__name__)

# Global variables for UI updates
observer = WebsiteObserver()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify({
        "prediction": observer.engine.analyze_patterns(observer.last_outcome)["prediction"],
        "confidence": observer.engine.analyze_patterns(observer.last_outcome)["confidence"] * 100,
        "history": observer.engine.history
    })

# Start monitoring in a separate thread
threading.Thread(target=observer.start_monitoring, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)