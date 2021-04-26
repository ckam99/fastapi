import uvicorn
from core import app

if __name__ == '__main__':
    uvicorn.run(app=app)
