from network import app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("network:app", host="0.0.0.0", port=8011,reload=True)
