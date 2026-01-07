# Veefy Technical Task - Backend Service

A backend service built with FastAPI that handles image uploads and performs mock skin analysis.

## Features

- **Image Upload**: Upload JPEG/PNG images (max 5MB).
- **Mock Analysis**: Get simulated skin analysis results (Skin Type, Issues, Confidence).
- **Security**: Simple API Key authentication.
- **Rate Limiting**: Defends against abuse (5/min upload, 20/min analyze).
- **Logging**: Request logging middleware.

## Setup & Running Locally

### Prerequisites
- Python 3.9+

### Steps
1. **Clone/Navigate to the repository**
   ```bash
   cd veefy-task
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Create a `.env` file (copy from `.env.example`).
   - Set `VEEFY_API_KEY=veefy-secret-key` (or your preferred key).

4. **Run the Server**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the API**
   - Interactive Docs (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
   - Authenticate by clicking "Authorize" (if configured) or passing header `x-api-key: veefy-secret-key`.

## API Endpoints

### 1. Upload Image
- **URL**: `POST /upload`
- **Header**: `x-api-key: veefy-secret-key`
- **Body**: `multipart/form-data`, key `file`
- **Response**: `{ "image_id": "uuid..." }`

### 2. Analyze Image
- **URL**: `POST /analyze`
- **Header**: `x-api-key: veefy-secret-key`
- **Body**: `{ "image_id": "uuid..." }`
- **Response**:
  ```json
  {
      "image_id": "...",
      "skin_type": "Oily",
      "issues": ["Acne"],
      "confidence": 0.95
  }
  ```

## Assumptions
- Uses local file system (`uploads/`) for storage.
- No database; file existence is checked directly on disk.
- Mock analysis returns randomized data for demonstration.
- No automatic cleanup of old files.

## Future Improvements (Production Readiness)
- **Storage**: Use S3 or Azure Blob Storage for scalability.
- **Database**: Use PostgreSQL/MongoDB to store metadata and analysis history.
- **Async Processing**: Use Celery/Redis for long-running AI tasks.
- **Security**: Use OAuth2/JWT instead of static API Key.
- **Testing**: Add comprehensive unit and integration tests (pytest).

## Docker
Build and run using Docker:
```bash
docker build -t veefy-backend .
docker run -p 8000:8000 veefy-backend
```
