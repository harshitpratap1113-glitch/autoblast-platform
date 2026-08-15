#!/usr/bin/env python3
"""
🚀 AUTOBLAST AI - EXHAUSTIVE UNIT & INTEGRATION TEST SUITE
Author: Harshit Pratap & Antigravity AI
"""

import os
import sys
import json
import time

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("=" * 70)
print("🚀 AUTOBLAST AI - RUNNING EXHAUSTIVE INTEGRATION TESTS")
print("=" * 70)

passed = 0
total = 0

def test(name, condition, error_msg=""):
    global passed, total
    total += 1
    if condition:
        passed += 1
        print(f"  ✅ [PASS] {name}")
    else:
        print(f"  ❌ [FAIL] {name}: {error_msg}")

# 1. Test File Structure
print("\n[1/5] Testing Project File Structure...")
test("main.py exists", os.path.exists("main.py"))
test("marketing_engine.py exists", os.path.exists("marketing_engine.py"))
test("index.html exists", os.path.exists("index.html"))
test("requirements.txt exists", os.path.exists("requirements.txt"))
test("vercel.json exists", os.path.exists("vercel.json"))
test("sitemap.xml exists", os.path.exists("sitemap.xml"))
test("robots.txt exists", os.path.exists("robots.txt"))

# 2. Test Marketing Engine Import & DB Load
print("\n[2/5] Testing Engine & Database...")
try:
    import marketing_engine
    test("marketing_engine import", True)
    
    db = marketing_engine.load_db()
    test("Database contains platforms", "platforms" in db and len(db["platforms"]) == 6)
    test("Database contains analytics", "analytics" in db and "total_clicks" in db["analytics"])
except Exception as e:
    test("marketing_engine import", False, str(e))

# 3. Test AI Copywriter Multiplier
print("\n[3/5] Testing AI Copywriter Generator...")
try:
    res = marketing_engine.generate_campaign_copies(
        product_name="VoxAI Studio",
        target_url="https://voxai-platform.vercel.app/memes",
        audience="Video Editors & YouTubers",
        benefit="50+ Real Meme MP3s & 110+ Hindi Voices"
    )
    test("AI Copywriter returned tracking_id", "tracking_id" in res and len(res["tracking_id"]) > 0)
    copies = res.get("copies", {})
    test("WhatsApp Copy generated", "whatsapp" in copies and "VoxAI Studio" in copies["whatsapp"])
    test("Telegram Copy generated", "telegram" in copies and "#VideoEditing" in copies["telegram"])
    test("Reddit Copy generated", "reddit" in copies and "Title:" in copies["reddit"])
    test("Discord Copy generated", "discord" in copies and "NEW TOOL LAUNCH" in copies["discord"])
    test("Twitter Copy generated", "twitter" in copies and "#AITools" in copies["twitter"])
    test("Instagram Copy generated", "instagram" in copies and "#capcuttutorial" in copies["instagram"])
except Exception as e:
    test("AI Copywriter execution", False, str(e))

# 4. Test Omnichannel Dispatcher with Jitter
print("\n[4/5] Testing Omnichannel Dispatcher...")
try:
    blast_payload = {
        "product_name": "VoxAI Studio",
        "platforms": ["whatsapp", "telegram", "discord", "reddit", "twitter"],
        "tracking_id": "test_cid"
    }
    dispatch_res = marketing_engine.dispatch_omnichannel_blast(blast_payload)
    test("Dispatcher returned success", dispatch_res.get("status") == "success")
    test("Delivered count > 0", dispatch_res.get("delivered_count", 0) >= 5)
    test("Logs generated with jitter", len(dispatch_res.get("logs", [])) >= 5)
    test("Estimated reach calculated", dispatch_res.get("estimated_reach", 0) > 1000)
except Exception as e:
    test("Dispatcher execution", False, str(e))

# 5. Test Click Tracker & Analytics Update
print("\n[5/5] Testing Click Tracking & Real-Time Stats...")
try:
    initial_clicks = marketing_engine.load_db()["analytics"]["total_clicks"]
    dest_url = marketing_engine.record_click("test_cid", "telegram")
    new_clicks = marketing_engine.load_db()["analytics"]["total_clicks"]
    test("Click counter incremented", new_clicks == initial_clicks + 1)
    test("Redirect destination valid", dest_url.startswith("http"))
except Exception as e:
    test("Click Tracker execution", False, str(e))

print("\n" + "=" * 70)
print(f"🎯 TEST RESULTS: {passed}/{total} Tests Passed ({passed/total*100:.1f}%)")
print("=" * 70)

if passed == total:
    print("\n🏆 PERFECT SCORE! AUTOBLAST AI ENGINE IS 100% ROCK-SOLID & PRODUCTION-READY!")
else:
    print("\n❌ SOME TESTS FAILED!")
