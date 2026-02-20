"""
간단한 인메모리 캐시
동일한 알람 분석 결과를 캐싱하여 LLM 비용 절감
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json


class SimpleCache:
    """
    간단한 인메모리 캐시
    
    알람 분석 결과를 메모리에 저장하여
    동일한 알람 재분석 시 LLM 호출을 방지합니다.
    """
    
    def __init__(self, ttl_seconds: int = 3600):
        """
        Args:
            ttl_seconds: 캐시 유효 시간 (초, 기본 1시간)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        캐시에서 데이터 조회
        
        Args:
            key: 캐시 키
        
        Returns:
            캐시된 데이터 또는 None
        """
        if key not in self.cache:
            return None
        
        cached_item = self.cache[key]
        
        # TTL 확인
        if datetime.now() > cached_item['expires_at']:
            # 만료된 캐시 삭제
            del self.cache[key]
            return None
        
        print(f"✅ 캐시 히트: {key}")
        return cached_item['data']
    
    def set(self, key: str, data: Dict[str, Any]) -> None:
        """
        캐시에 데이터 저장
        
        Args:
            key: 캐시 키
            data: 저장할 데이터
        """
        expires_at = datetime.now() + timedelta(seconds=self.ttl_seconds)
        
        self.cache[key] = {
            'data': data,
            'expires_at': expires_at,
            'created_at': datetime.now()
        }
        
        print(f"💾 캐시 저장: {key} (만료: {expires_at.strftime('%H:%M:%S')})")
    
    def delete(self, key: str) -> None:
        """
        캐시 삭제
        
        Args:
            key: 캐시 키
        """
        if key in self.cache:
            del self.cache[key]
            print(f"🗑️ 캐시 삭제: {key}")
    
    def clear(self) -> None:
        """모든 캐시 삭제"""
        count = len(self.cache)
        self.cache.clear()
        print(f"🗑️ 전체 캐시 삭제: {count}개")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        캐시 통계
        
        Returns:
            캐시 통계 정보
        """
        # 만료된 항목 정리
        now = datetime.now()
        expired_keys = [
            key for key, item in self.cache.items()
            if now > item['expires_at']
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        return {
            'total_items': len(self.cache),
            'ttl_seconds': self.ttl_seconds,
            'expired_cleaned': len(expired_keys)
        }
    
    def generate_key(self, *args) -> str:
        """
        캐시 키 생성
        
        Args:
            *args: 키를 구성할 값들
        
        Returns:
            생성된 캐시 키
        """
        key_parts = [str(arg) for arg in args]
        return ':'.join(key_parts)


# 전역 캐시 인스턴스
# 알람 분석 결과 캐싱 (1시간 유효)
analysis_cache = SimpleCache(ttl_seconds=3600)

# 질문 답변 캐싱 (30분 유효)
qa_cache = SimpleCache(ttl_seconds=1800)