from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, RedirectResponse

from app.core.auth import is_public_enabled
from app.core.logger import logger

router = APIRouter()
STATIC_DIR = Path(__file__).resolve().parents[2] / "static"


def _serve_public_page(page_name: str) -> FileResponse:
    """服务 public 页面，包含错误处理"""
    logger.debug(f"[v0] _serve_public_page called with page_name={page_name}")
    logger.debug(f"[v0] STATIC_DIR={STATIC_DIR}")
    logger.debug(f"[v0] is_public_enabled()={is_public_enabled()}")
    
    if not is_public_enabled():
        logger.debug(f"[v0] public not enabled, returning 404")
        raise HTTPException(status_code=404, detail="Not Found")
    
    file_path = STATIC_DIR / f"public/pages/{page_name}.html"
    logger.debug(f"[v0] file_path={file_path}, exists={file_path.exists()}")
    
    if not file_path.exists():
        logger.error(f"Public page not found: {file_path}")
        raise HTTPException(status_code=404, detail="Page not found")
    
    return FileResponse(file_path)


@router.get("/", include_in_schema=False)
async def root():
    if is_public_enabled():
        return RedirectResponse(url="/login")
    return RedirectResponse(url="/admin/login")


@router.get("/login", include_in_schema=False)
async def public_login():
    return _serve_public_page("login")


@router.get("/imagine", include_in_schema=False)
async def public_imagine():
    return _serve_public_page("imagine")


@router.get("/voice", include_in_schema=False)
async def public_voice():
    return _serve_public_page("voice")


@router.get("/video", include_in_schema=False)
async def public_video():
    return _serve_public_page("video")


@router.get("/chat", include_in_schema=False)
async def public_chat():
    return _serve_public_page("chat")
