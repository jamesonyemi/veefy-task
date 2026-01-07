from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

API_KEY = "veefy-secret-key"
HEADERS = {"x-api-key": API_KEY}

def test_workflow():
    print("--- Starting Verification ---")

    # 1. Test Root
    response = client.get("/")
    print(f"Root: {response.status_code} {response.json()}")
    assert response.status_code == 200

    # 2. Test Upload (No Auth)
    response = client.post("/upload")
    print(f"Upload (No Auth): {response.status_code}")
    assert response.status_code == 403

    # 3. Create dummy image
    with open("test.jpg", "wb") as f:
        f.write(b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01") # minimal jpg header

    # 4. Test Upload (With Auth)
    with open("test.jpg", "rb") as f:
        response = client.post(
            "/upload", 
            files={"file": ("test.jpg", f, "image/jpeg")},
            headers=HEADERS
        )
    print(f"Upload (Auth): {response.status_code} {response.json()}")
    assert response.status_code == 200
    image_id = response.json().get("image_id")
    assert image_id is not None

    # 5. Test Analyze
    response = client.post(
        "/analyze",
        json={"image_id": image_id},
        headers=HEADERS
    )
    print(f"Analyze: {response.status_code} {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["image_id"] == image_id
    assert "skin_type" in data
    assert "issues" in data
    assert "confidence" in data

    # Cleanup
    os.remove("test.jpg")
    print("--- Verification Successful! ---")

if __name__ == "__main__":
    try:
        test_workflow()
    except AssertionError as e:
        print(f"Verification Failed: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
