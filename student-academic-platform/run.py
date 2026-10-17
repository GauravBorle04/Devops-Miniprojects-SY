import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' is required so Docker/EC2 port forwarding works
    app.run(host="0.0.0.0", port=port, debug=False)
