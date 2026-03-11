"""
TA Engine Python Backend - PHASE 13.1 Alpha Node Registry
==========================================================
Minimal TA Engine runtime with Alpha Factory module.

API Endpoints:
- GET  /api/health                        - Health check
- GET  /api/system/db-health              - MongoDB health
- GET  /api/alpha-factory/health          - Alpha Factory health
- GET  /api/alpha-factory/nodes           - List all nodes
- GET  /api/alpha-factory/nodes/{id}      - Get node by ID
- POST /api/alpha-factory/nodes           - Create node
- GET  /api/alpha-factory/nodes/types     - Node types breakdown
- GET  /api/alpha-factory/nodes/search    - Search nodes
- GET  /api/alpha-factory/stats           - Registry statistics
"""

import os
import sys
import time
from datetime import datetime, timezone
from contextlib import asynccontextmanager

# Add modules directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize MongoDB connection
try:
    from core.database import get_database, mongo_health_check
    _db = get_database()
    print("[Server] MongoDB connection initialized")
except Exception as e:
    print(f"[Server] MongoDB connection warning: {e}")
    _db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("[Server] TA Engine starting...")
    yield
    print("[Server] TA Engine shutting down...")


app = FastAPI(
    title="TA Engine API",
    description="PHASE 13.1 - Alpha Node Registry",
    version="13.1.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Core Health Endpoints
# ============================================

@app.get("/api/health")
async def health():
    """API health check"""
    return {
        "ok": True,
        "mode": "TA_ENGINE_ALPHA_FACTORY",
        "version": "13.3.0",
        "phase": "PHASE 13.3 - Factor Generator",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/system/db-health")
async def db_health():
    """MongoDB health check endpoint."""
    try:
        return mongo_health_check()
    except Exception as e:
        return {
            "status": "error",
            "connected": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# ============================================
# Register Alpha Factory Router (PHASE 13.1)
# ============================================

try:
    from modules.alpha_factory.alpha_routes import router as alpha_factory_router
    app.include_router(alpha_factory_router)
    print("[Routes] PHASE 13.1 Alpha Factory router registered")
except ImportError as e:
    print(f"[Routes] Alpha Factory router not available: {e}")

# PHASE 13.2 Feature Library Router
try:
    from modules.alpha_factory.feature_library.feature_routes import router as feature_library_router
    app.include_router(feature_library_router)
    print("[Routes] PHASE 13.2 Feature Library router registered")
except ImportError as e:
    print(f"[Routes] Feature Library router not available: {e}")

# PHASE 13.3 Factor Generator Router
try:
    from modules.alpha_factory.factor_generator.factor_routes import router as factor_generator_router
    app.include_router(factor_generator_router)
    print("[Routes] PHASE 13.3 Factor Generator router registered")
except ImportError as e:
    print(f"[Routes] Factor Generator router not available: {e}")


# ============================================
# TA Analysis Endpoints (Minimal)
# ============================================

@app.get("/api/ta/registry")
async def ta_registry():
    """Get TA Engine registry summary"""
    try:
        from modules.alpha_factory.alpha_node_registry import get_alpha_registry
        registry = get_alpha_registry()
        stats = registry.get_stats()
        
        return {
            "status": "ok",
            "phase": "13.1",
            "registry": stats,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


@app.get("/api/ta/patterns")
async def ta_patterns():
    """Get available TA patterns/nodes"""
    try:
        from modules.alpha_factory.alpha_node_registry import get_alpha_registry
        from modules.alpha_factory.alpha_types import NodeType
        
        registry = get_alpha_registry()
        
        # Get nodes by type
        alpha_nodes = registry.get_nodes_by_type(NodeType.ALPHA)
        structure_nodes = registry.get_nodes_by_type(NodeType.STRUCTURE)
        
        return {
            "status": "ok",
            "alpha_patterns": [n.node_id for n in alpha_nodes],
            "structure_patterns": [n.node_id for n in structure_nodes],
            "total_count": len(alpha_nodes) + len(structure_nodes),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


@app.post("/api/ta/analyze")
async def ta_analyze(symbol: str = "BTCUSDT", timeframe: str = "4h"):
    """
    Analyze symbol using registered alpha nodes.
    
    Note: This is a placeholder - full implementation requires 
    market data and indicator computation.
    """
    try:
        from modules.alpha_factory.alpha_node_registry import get_alpha_registry
        
        registry = get_alpha_registry()
        stats = registry.get_stats()
        
        # Mock analysis result
        return {
            "status": "ok",
            "symbol": symbol,
            "timeframe": timeframe,
            "analysis": {
                "nodes_available": stats.get("total_nodes", 0),
                "active_nodes": stats.get("active_nodes", 0),
                "note": "Full analysis requires market data integration"
            },
            "signals": [],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# ============================================
# Root endpoint
# ============================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "TA Engine",
        "version": "13.2.0",
        "phase": "PHASE 13.2 - Alpha Feature Library",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "db_health": "/api/system/db-health",
            "alpha_factory": "/api/alpha-factory/*",
            "feature_library": "/api/alpha-features/*",
            "ta_registry": "/api/ta/registry",
            "ta_patterns": "/api/ta/patterns",
            "ta_analyze": "/api/ta/analyze"
        }
    }
