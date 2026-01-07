# Veefy Backend - Demo Script

Use this script to demonstrate the backend capabilities during your presentation.

## Preparation
1. **Clear Data**: Delete the `uploads/` folder contents (optional, to show fresh state).
2. **Start Server**:
   ```bash
   uvicorn app.main:app --reload
   # Keep this terminal visible to show logs!
   ```
3. **Open Postman** and create a new Collection named "Veefy Demo".

---

## Step 1: Show Security (Auth Failure)
*Goal: Demonstrate that the API is secure by default.*

1. **Action**: Create a `POST` request to `http://127.0.0.1:8000/upload`.
2. **Body**: Select `form-data`, add key `file` and select an image.
3. **Send**: Click Send **without** headers.
4. **Outcome**: 
   - Status: `403 Forbidden`
   - Response: `{"detail": "Could not validate credentials"}`
5. **Talking Point**: "As you can see, the API rejects unauthorized requests immediately."

---

## Step 2: Successful Upload
*Goal: Demonstrate file validation and storage.*

1. **Action**: Add Header `x-api-key` with value `veefy-secret-key`.
2. **Send**: Click Send again.
3. **Outcome**:
   - Status: `200 OK`
   - Response: `{"image_id": "8a2...3f1"}`
4. **Verification**:
   - Show the VS Code file explorer.
   - Expand `uploads/` folder to show the new file has appeared.
5. **Talking Point**: "The image is validated (size/type), assigned a unique UUID, and stored locally."

---

## Step 3: Mock AI Analysis
*Goal: Demonstrate the mock AI logic and JSON structure.*

1. **Action**: Copy the `image_id` from the previous step.
2. **Action**: Create a new `POST` request to `http://127.0.0.1:8000/analyze`.
3. **Headers**: Add `x-api-key` : `veefy-secret-key`.
4. **Body**: Select `raw` -> `JSON`.
   ```json
   {
     "image_id": "PASTE_UUID_HERE"
   }
   ```
5. **Send**: Click Request.
6. **Outcome**:
   - Status: `200 OK`
   - Response:
     ```json
     {
         "skin_type": "Oily",
         "issues": ["Acne", "Redness"],
         "confidence": 0.95
     }
     ```
7. **Talking Point**: "The backend simulates processing and returns structured JSON data ready for the mobile app."

---

## Step 4: Show Logging (Bonus)
*Goal: Demonstrate observability.*

1. **Action**: Open the terminal running `uvicorn`.
2. **Outcome**: Point to the logs.
   ```text
   INFO:     POST /upload - 200 - 0.0152s
   INFO:     POST /analyze - 200 - 0.0020s
   ```
3. **Talking Point**: "We have middleware that logs every request with method, status, and processing time for monitoring."
To extend the logging, we can add more details such as the client IP, request body, and response body.Additionally, log into a file for long-term monitoring.

---

## Step 5: Rate Limiting (Bonus)
*Goal: Demonstrate API stability and abuse prevention.*

1.  **Action**: Run the `test_limiter.py` script from the terminal.
    ```bash
    python test_limiter.py
    ```
2.  **Outcome**:
    - Script hits `/analyze` 25 times.
    - Around request 21, it shows: `❌ Rate Limit Triggered! (429 Too Many Requests)`
    - Postman will also obtain `429 Too Many Requests` if you spam "Send".
3.  **Talking Point**: "We implemented rate limiting (20 req/min for analysis) to prevent abuse and manage costs."