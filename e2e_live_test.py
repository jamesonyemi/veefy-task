import httpx
import os
import time

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "veefy-secret-key"
HEADERS = {"x-api-key": API_KEY}

def run_tests():
    print(f"Testing against running server at {BASE_URL}...")
    
    with httpx.Client(base_url=BASE_URL, timeout=10) as client:
        # 1. Health Check
        print("\n[1] Checking Root Endpoint...")
        try:
            r = client.get("/")
            if r.status_code != 200:
                print("Server not reachable or error at /.")
                return False
            print(f"Root OK: {r.json()}")
        except Exception as e:
            print(f"Failed to connect: {e}")
            print("Make sure 'uvicorn app.main:app --reload' is running.")
            return False

        # 2. Auth Check
        print("\n[2] Checking Authentication...")
        r = client.post("/upload")
        if r.status_code == 403:
            print("Auth correctly rejected missing key (403).")
        else:
            print(f"Auth failed: Expected 403, got {r.status_code}")
            return False

        # 3. Create dummy image
        dummy_file = "e2e_test.jpg"
        with open(dummy_file, "wb") as f:
            f.write(b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01")

        # 4. Upload Image
        print("\n[3] Testing Upload...")
        image_id = None
        # Fix: Open file in context manager so it closes automatically
        with open(dummy_file, "rb") as f:
            files = {"file": (dummy_file, f, "image/jpeg")}
            r = client.post("/upload", headers=HEADERS, files=files)
        
        if r.status_code == 200:
            image_id = r.json().get("image_id")
            print(f"Upload successful. Image ID: {image_id}")
        else:
            print(f"Upload failed: {r.status_code} {r.text}")
            return False

        # 5. Analysis
        print("\n[4] Testing Analysis...")
        r = client.post("/analyze", headers=HEADERS, json={"image_id": image_id})
        
        if r.status_code == 200:
            data = r.json()
            print(f"Analysis successful: {data}")
            if data['image_id'] != image_id:
                print("Mismatched Image ID")
                return False
            if not (0.0 <= data['confidence'] <= 1.0):
                 print("Invalid confidence score range")
                 return False
        else:
            print(f"Analysis failed: {r.status_code} {r.text}")
            return False
            
        # 6. Invalid Analysis
        print("\n[5] Testing Analysis (Invalid ID)...")
        r = client.post("/analyze", headers=HEADERS, json={"image_id": "invalid-uuid"})
        if r.status_code == 404:
             print("correctly returned 404 for missing image.")
        else:
             print(f"Expected 404, got {r.status_code}")
             return False

    # Cleanup
    if os.path.exists(dummy_file):
        try:
            os.remove(dummy_file)
        except Exception as e:
             print(f"Warning: Could not remove test file: {e}")
        
    print("\n ALL LIVE TESTS PASSED")
    return True

if __name__ == "__main__":
    run_tests()
