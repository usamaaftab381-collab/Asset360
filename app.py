from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Asset360</h1>
    <p>Fixed Asset Management System</p>
    <p>QR Tracking | Verification | Audit Logs</p>
    """

@app.route("/asset/<asset_id>")
def asset(asset_id):
    return f"""
    <h2>Asset Details</h2>
    <p>Asset ID: {asset_id}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
