import httpx
import time

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "veefy-secret-key"
HEADERS = {"x-api-key": API_KEY}

def test_rate_limit():
    print("Testing Rate Limit on /analyze (Limit: 20/minute)...")
    
    # We hit the endpoint 25 times rapidly
    # Since limits are by remote address and we are local, this acts as one user.
    for i in range(1, 26):
        try:
             # We send a dummy request (invalid ID is fine, we just want to hit the limiter)
            r = httpx.post(
                f"{BASE_URL}/analyze", 
                headers=HEADERS, 
                json={"image_id": "stress-test"}
            )
            if r.status_code == 429:
                print(f"Request {i}: ❌ Rate Limit Triggered! (429 Too Many Requests)")
                print("✅ TEST PASSED: Limiter is working.")
                return
            else:
                print(f"Request {i}: {r.status_code} (OK)")
        except Exception as e:
            print(f"Request {i} Failed: {e}")

    print("⚠️ WARNING: Rate limit was not triggered after 25 requests.")

if __name__ == "__main__":
    test_rate_limit()
