import os, sys
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
from app import create_app
app = create_app()

if __name__ == "__main__":
    app.run()