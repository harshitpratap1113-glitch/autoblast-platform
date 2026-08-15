"""
🚀 AUTOBLAST AI - FASTAPI API GATEWAY SERVER
Author: Harshit Pratap & Antigravity AI
"""

import os
import sys
import time
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import marketing_engine

app = FastAPI(
    title="AutoBlast AI - Omnichannel Marketing & Viral Broadcaster Hub",
    version="1.0.0",
    docs_url="/api/docs"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Request Models
class GenerateCopyRequest(BaseModel):
    product_name: str
    target_url: str
    target_audience: Optional[str] = "Video Editors & Creators"
    key_benefit: Optional[str] = "50+ Real Meme Sounds & Hindi AI Voiceover"

class BlastCampaignRequest(BaseModel):
    product_name: str
    platforms: List[str]
    copies: Optional[Dict[str, str]] = {}
    tracking_id: Optional[str] = None

class ConnectAccountRequest(BaseModel):
    platform: str
    credentials: Optional[Dict[str, Any]] = {}

# Endpoints
@app.get("/")
async def serve_dashboard():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return JSONResponse({"status": "error", "message": "index.html not found"})

@app.get("/api/health")
async def health_check():
    db = marketing_engine.load_db()
    return {
        "status": "online",
        "service": "AutoBlast AI Marketing Engine",
        "version": "1.0.0",
        "connected_platforms": len(db["platforms"]),
        "total_delivered": db["analytics"]["total_delivered"],
        "total_clicks": db["analytics"]["total_clicks"]
    }

@app.get("/api/platforms")
async def get_platforms():
    db = marketing_engine.load_db()
    return {"status": "success", "platforms": db.get("platforms", {})}

@app.post("/api/connect")
async def connect_platform_account(req: ConnectAccountRequest):
    db = marketing_engine.load_db()
    p = req.platform.lower().strip()
    if p in db["platforms"]:
        db["platforms"][p]["connected"] = True
        db["platforms"][p]["status"] = "Online"
        marketing_engine.save_db(db)
        return {"status": "success", "message": f"{p.capitalize()} connected successfully!"}
    return JSONResponse(status_code=400, content={"status": "error", "message": "Unknown platform"})

@app.post("/api/generate")
async def api_generate_copy(req: GenerateCopyRequest):
    data = marketing_engine.generate_campaign_copies(
        product_name=req.product_name,
        target_url=req.target_url,
        audience=req.target_audience or "Creators & Editors",
        benefit=req.key_benefit or "Free AI Voices & Meme Sounds"
    )
    return {"status": "success", "tracking_id": data["tracking_id"], "copies": data["copies"]}

@app.post("/api/blast")
async def api_launch_blast(req: BlastCampaignRequest):
    result = marketing_engine.dispatch_omnichannel_blast(req.dict())
    return result

@app.get("/api/analytics")
async def api_get_analytics():
    db = marketing_engine.load_db()
    return {
        "status": "success",
        "analytics": db.get("analytics", {}),
        "recent_campaigns": db.get("campaigns", [])[:10]
    }

@app.get("/t/{tracking_id}")
async def handle_click_tracking(tracking_id: str, src: Optional[str] = "direct"):
    dest = marketing_engine.record_click(tracking_id, src)
    return RedirectResponse(url=dest)

@app.get("/sitemap.xml")
async def serve_sitemap():
    p = os.path.join(BASE_DIR, "sitemap.xml")
    if os.path.exists(p):
        return FileResponse(p, media_type="application/xml")
    return JSONResponse({"status": "error"})

@app.get("/robots.txt")
async def serve_robots():
    p = os.path.join(BASE_DIR, "robots.txt")
    if os.path.exists(p):
        return FileResponse(p, media_type="text/plain")
    return JSONResponse({"status": "error"})

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AutoBlast AI Server on http://127.0.0.1:8001...")
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
