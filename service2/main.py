import uvicorn

if __name__ == '__main__':
    uvicorn.run('core:app', port=8001,
                reload=True, access_log=False)
