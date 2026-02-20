"""
시스템 관리 API 엔드포인트
"""

from fastapi import APIRouter
from backend.utils.cache import analysis_cache, qa_cache

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/cache/stats")
async def get_cache_stats():
    """
    캐시 통계 조회
    
    알람 분석 캐시와 질문 답변 캐시의 상태를 확인합니다.
    """
    
    return {
        "analysis_cache": analysis_cache.get_stats(),
        "qa_cache": qa_cache.get_stats(),
    }


@router.post("/cache/clear")
async def clear_cache(cache_type: str = "all"):
    """
    캐시 초기화
    
    Args:
        cache_type: 'analysis', 'qa', 또는 'all'
    """
    
    if cache_type in ["analysis", "all"]:
        analysis_cache.clear()
    
    if cache_type in ["qa", "all"]:
        qa_cache.clear()
    
    return {
        "success": True,
        "message": f"{cache_type} 캐시가 초기화되었습니다.",
    }