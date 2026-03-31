# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import boto3, uuid

# -------------------------------
# AWS S3 CONFIGURATION
# -------------------------------
AWS_ACCESS_KEY_ID = "YOUR_KEY"       # Replace with your AWS access key
AWS_SECRET_ACCESS_KEY = "YOUR_SECRET"  # Replace with your AWS secret key
AWS_REGION = "YOUR_REGION"            # e.g., "ap-south-1"
BUCKET_NAME = "my-devops-images"      # Replace with your S3 bucket name

s3 = boto3.client(
    "s3",
  
    aws_access_key_id="//",
    aws_secret_access_key="//",
    region_name="//"
)

# -------------------------------
# FASTAPI CONFIGURATION
# -------------------------------app = FastAPI(title="S3 Upload App")
app = FastAPI(title="S3 Upload App")
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# API ROUTES FIRST
# -----------------------
@app.get("/api")
def home_api():
    return {"message": "API working"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only images allowed")

    file_name = f"{uuid.uuid4()}_{file.filename}"
    file.file.seek(0)

    try:
        s3.upload_fileobj(
            file.file,
            BUCKET_NAME,
            file_name,
            ExtraArgs={"ContentType": file.content_type or "application/octet-stream"}
        )
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"
        return {"url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# -----------------------
# STATIC FILES LAST
# -----------------------
app.mount("/", StaticFiles(directory="static", html=True), name="static")

