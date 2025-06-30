from config import app

@app.route('/')
def index():
    return {"message": "Mkay Events Backend Running!"}

if __name__ == '__main__':
    app.run(port=5555, debug=True)
