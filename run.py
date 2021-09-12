import uvicorn


if __name__ == "__main__":
    uvicorn.run("core:app", host='0.0.0.0', port=8000,
                debug=True, reload=True, lifespan='on')
