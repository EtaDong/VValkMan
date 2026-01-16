from fastapi import fastapi

app = fastapi(
    title="cosmos-s1",
    description="cosmos-s1",
    version="0.0.1",
    openapi_url="/openapi.json",
    docs_url="/docs",
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

