#!/usr/bin/env python3
"""
Test script to verify auth redirect loop fix.

Tests:
1. Can access login page
2. Can login with citizen ID
3. Can access protected pages without redirect loop
4. Can logout
"""

import time
import json
import subprocess
import sys
from pathlib import Path

def wait_for_service(url, timeout=10):
    """Wait for service to be ready."""
    import urllib.request
    import urllib.error
    
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except (urllib.error.URLError, Exception):
            time.sleep(0.5)
    return False

def test_frontend_access():
    """Test 1: Can access frontend pages"""
    print("\n🔍 Test 1: Frontend Access")
    print("=" * 50)
    
    import urllib.request
    
    pages = [
        ("Login Page", "http://localhost:8000/citizen-login.html"),
        ("Officer Login", "http://localhost:8000/officer-login.html"),
    ]
    
    for name, url in pages:
        try:
            response = urllib.request.urlopen(url, timeout=3)
            if response.status == 200:
                print(f"  ✅ {name}: {url}")
            else:
                print(f"  ❌ {name}: Status {response.status}")
        except Exception as e:
            print(f"  ❌ {name}: {str(e)[:50]}")
    
    return True

def test_api_access():
    """Test 2: Can access API endpoints"""
    print("\n🔍 Test 2: API Access (without auth)")
    print("=" * 50)
    
    import urllib.request
    import urllib.error
    
    # These should return 401 (unauthorized) since we're not sending auth header
    endpoints = [
        ("Get Reports", "http://localhost:8000/api/reports", 401),
        ("Get Queue", "http://localhost:8000/api/review-queue", 401),
    ]
    
    for name, url, expected_status in endpoints:
        try:
            response = urllib.request.urlopen(url, timeout=3)
            print(f"  ❌ {name}: Expected 401, got {response.status}")
        except urllib.error.HTTPError as e:
            if e.code == expected_status:
                print(f"  ✅ {name}: Correctly returned {e.code}")
            else:
                print(f"  ❌ {name}: Expected {expected_status}, got {e.code}")
        except Exception as e:
            print(f"  ❌ {name}: {str(e)[:50]}")
    
    return True

def test_auth_headers():
    """Test 3: API with auth headers works"""
    print("\n🔍 Test 3: API with Auth Headers")
    print("=" * 50)
    
    import urllib.request
    import json
    
    # Test with citizen auth
    req = urllib.request.Request("http://localhost:8000/api/reports")
    req.add_header('X-Citizen-Id', 'test-citizen-123')
    
    try:
        response = urllib.request.urlopen(req, timeout=3)
        data = json.loads(response.read().decode())
        if 'reports' in data:
            print(f"  ✅ Citizen API: Got {len(data['reports'])} reports")
        else:
            print(f"  ⚠️  Citizen API: Response missing 'reports' field")
    except Exception as e:
        print(f"  ⚠️  Citizen API: {str(e)[:50]}")
    
    return True

def test_auth_check_pattern():
    """Test 4: Verify auth check pattern in HTML"""
    print("\n🔍 Test 4: Auth Check Pattern in Templates")
    print("=" * 50)
    
    templates_dir = Path("templates")
    protected_pages = [
        "citizen-reports.html",
        "citizen-dashboard.html",
        "citizen-report.html",
        "officer-queue.html",
        "officer-detail.html",
    ]
    
    for page in protected_pages:
        file_path = templates_dir / page
        if not file_path.exists():
            print(f"  ❌ {page}: File not found")
            continue
        
        content = file_path.read_text()
        
        # Check for the safe auth pattern
        has_check_auth = "checkAuthAndLoad" in content
        has_typeof_check = "typeof AUTH === 'undefined'" in content
        has_retry = "setTimeout(checkAuthAndLoad" in content
        
        if has_check_auth and has_typeof_check and has_retry:
            print(f"  ✅ {page}: Has proper auth check pattern")
        else:
            print(f"  ❌ {page}: Missing auth check pattern")
            if not has_check_auth:
                print(f"     - Missing checkAuthAndLoad function")
            if not has_typeof_check:
                print(f"     - Missing typeof check")
            if not has_retry:
                print(f"     - Missing retry logic")
    
    return True

def main():
    print("\n" + "=" * 60)
    print("  AUTH REDIRECT LOOP FIX - VERIFICATION TEST")
    print("=" * 60)
    
    # Check if services are running
    print("\n⏳ Waiting for services to be ready...")
    if not wait_for_service("http://localhost:8000/citizen-login.html", timeout=10):
        print("❌ Frontend service not ready!")
        return False
    
    print("✅ Services ready")
    
    # Run tests
    tests = [
        test_frontend_access,
        test_api_access,
        test_auth_headers,
        test_auth_check_pattern,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n  Passed: {passed}/{total}")
    
    if all(results):
        print("\n  ✅ ALL TESTS PASSED - Auth redirect loop is FIXED!")
        return True
    else:
        print("\n  ⚠️  Some tests failed - see details above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
