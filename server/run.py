from app import app
import os

root_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(root_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)