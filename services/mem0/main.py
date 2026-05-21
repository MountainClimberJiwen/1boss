"""
mem0 API server - lightweight FastAPI wrapper around mem0 Memory.

Env vars:
  OPENAI_API_KEY   required for LLM + embeddings
  OPENAI_BASE_URL  optional API proxy (e.g. local LLM)
  MEM0_PORT        listen port (default 8000)
  MEM0_DATA_DIR    data root (default /opt/mem0/data)
"""

import os
import sys
import json
import logging
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Configuration from env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
MEM0_PORT = int(os.getenv("MEM0_PORT", "8000"))
MEM0_DATA_DIR = os.getenv("MEM0_DATA_DIR", "/opt/mem0/data")
MEM0_QDRANT_PATH = os.path.join(MEM0_DATA_DIR, "qdrant")
MEM0_HISTORY_DB = os.path.join(MEM0_DATA_DIR, "history.db")

# Ensure data directories exist
os.makedirs(MEM0_DATA_DIR, exist_ok=True)

memory_instance: Any = None
init_error: Optional[str] = None


def _build_memory():
    from mem0 import Memory
    from mem0.configs.base import MemoryConfig

    llm_config = {"provider": "openai", "config": {}}
    embedder_config = {"provider": "openai", "config": {}}

    if OPENAI_API_KEY:
        llm_config["config"]["api_key"] = OPENAI_API_KEY
        embedder_config["config"]["api_key"] = OPENAI_API_KEY
    if OPENAI_BASE_URL:
        llm_config["config"]["base_url"] = OPENAI_BASE_URL
        embedder_config["config"]["base_url"] = OPENAI_BASE_URL

    return Memory(config=MemoryConfig(
        vector_store={"provider": "qdrant", "config": {"path": MEM0_QDRANT_PATH}},
        llm=llm_config,
        embedder=embedder_config,
        history_db_path=MEM0_HISTORY_DB,
    ))


@asynccontextmanager
async def lifespan(app: FastAPI):
    global memory_instance, init_error
    try:
        memory_instance = _build_memory()
        logger.info("mem0 Memory initialized successfully")
    except Exception as exc:
        init_error = str(exc)
        logger.error("mem0 Memory init failed: %s", exc)
    yield
    logger.info("mem0 server shutting down")


app = FastAPI(title="mem0 Server", version="1.0.0", lifespan=lifespan)


def _require_memory():
    if memory_instance is None:
        detail = f"mem0 not initialized: {init_error}" if init_error else "mem0 not initialized"
        raise HTTPException(status_code=503, detail=detail)
    return memory_instance


class AddMemoryRequest(BaseModel):
    messages: str = Field(..., description="Message or memory content to store")
    user_id: Optional[str] = Field(None, description="User identifier")
    agent_id: Optional[str] = Field(None, description="Agent identifier")
    run_id: Optional[str] = Field(None, description="Run/session identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")
    filters: Optional[Dict[str, Any]] = Field(None, description="Optional filters")


class SearchMemoryRequest(BaseModel):
    query: str = Field(..., description="Search query")
    user_id: Optional[str] = Field(None, description="User identifier")
    agent_id: Optional[str] = Field(None, description="Agent identifier")
    run_id: Optional[str] = Field(None, description="Run/session identifier")
    filters: Optional[Dict[str, Any]] = Field(None, description="Optional filters")
    limit: int = Field(10, ge=1, le=100, description="Max results")


class DeleteMemoryRequest(BaseModel):
    memory_id: str = Field(..., description="Memory ID to delete")


class BulkDeleteRequest(BaseModel):
    memory_ids: List[str] = Field(..., description="List of memory IDs to delete")


@app.get("/health")
def health():
    return {
        "status": "ok" if memory_instance else "degraded",
        "init_error": init_error,
        "openai_configured": bool(OPENAI_API_KEY),
        "data_dir": MEM0_DATA_DIR,
    }


@app.post("/v1/memories")
def add_memory(req: AddMemoryRequest):
    mem = _require_memory()
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY not configured")
    try:
        result = mem.add(
            req.messages,
            user_id=req.user_id,
            agent_id=req.agent_id,
            run_id=req.run_id,
            metadata=req.metadata,
            filters=req.filters,
        )
        return {"success": True, "data": result}
    except Exception as exc:
        logger.exception("add_memory failed")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/v1/memories")
def get_memories(
    user_id: Optional[str] = Query(None),
    agent_id: Optional[str] = Query(None),
    run_id: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
):
    mem = _require_memory()
    try:
        result = mem.get_all(
            user_id=user_id,
            agent_id=agent_id,
            run_id=run_id,
            limit=limit,
        )
        return {"success": True, "data": result}
    except Exception as exc:
        logger.exception("get_memories failed")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/v1/memories/search")
def search_memories(req: SearchMemoryRequest):
    mem = _require_memory()
    try:
        result = mem.search(
            req.query,
            user_id=req.user_id,
            agent_id=req.agent_id,
            run_id=req.run_id,
            filters=req.filters,
            limit=req.limit,
        )
        return {"success": True, "data": result}
    except Exception as exc:
        logger.exception("search_memories failed")
        raise HTTPException(status_code=500, detail=str(exc))


@app.delete("/v1/memories/{memory_id}")
def delete_memory(memory_id: str):
    mem = _require_memory()
    try:
        result = mem.delete(memory_id)
        return {"success": True, "data": result}
    except Exception as exc:
        logger.exception("delete_memory failed")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/v1/memories/delete")
def bulk_delete(req: BulkDeleteRequest):
    mem = _require_memory()
    errors = []
    for mid in req.memory_ids:
        try:
            mem.delete(mid)
        except Exception as exc:
            logger.warning("delete %s failed: %s", mid, exc)
            errors.append({"id": mid, "error": str(exc)})
    return {"success": len(errors) == 0, "deleted": len(req.memory_ids) - len(errors), "errors": errors}


@app.get("/")
def root():
    return {"service": "mem0-server", "docs": "/docs", "health": "/health"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=MEM0_PORT)
