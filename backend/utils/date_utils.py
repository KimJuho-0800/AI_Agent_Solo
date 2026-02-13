"""
날짜 및 시간 처리 유틸리티 함수
"""

from datetime import datetime, timedelta
from typing import Tuple, Optional


def parse_datetime(date_str: str, format: str = None) -> datetime:
    """
    문자열을 datetime 객체로 변환합니다.
    
    Args:
        date_str: 날짜 문자열 (예: "2026-01-20" 또는 "2026-01-20 14:30")
        format: 날짜 포맷 (None이면 자동 감지)
    
    Returns:
        datetime: datetime 객체
    
    Examples:
        >>> parse_datetime("2026-01-20")
        datetime(2026, 1, 20, 0, 0)
        
        >>> parse_datetime("2026-01-20 14:30")
        datetime(2026, 1, 20, 14, 30)
    """
    if format:
        # 지정된 포맷으로 파싱
        return datetime.strptime(date_str, format)
    
    # 자동 포맷 감지
    # "2026-01-20" 형식
    if len(date_str) == 10 and date_str.count('-') == 2:
        return datetime.strptime(date_str, '%Y-%m-%d')
    
    # "2026-01-20 14:30" 형식
    elif len(date_str) == 16 and date_str.count(':') == 1:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    
    # "2026-01-20 14:30:00" 형식
    elif len(date_str) == 19 and date_str.count(':') == 2:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    
    else:
        raise ValueError(f"지원하지 않는 날짜 형식입니다: {date_str}")


def get_date_range(
    center_date: str,
    days_before: int = 1,
    days_after: int = 0
) -> Tuple[str, str]:
    """
    중심 날짜를 기준으로 날짜 범위를 계산합니다.
    
    Args:
        center_date: 중심 날짜 (예: "2026-01-20")
        days_before: 이전 며칠 (기본: 1일)
        days_after: 이후 며칠 (기본: 0일)
    
    Returns:
        Tuple[str, str]: (시작날짜, 종료날짜)
    
    Examples:
        >>> get_date_range("2026-01-20", days_before=1, days_after=0)
        ('2026-01-19', '2026-01-20')
    """
    # 중심 날짜를 datetime으로 변환
    center = parse_datetime(center_date)
    
    # 시작/종료 날짜 계산
    start_date = center - timedelta(days=days_before)
    end_date = center + timedelta(days=days_after)
    
    # 문자열로 변환해서 반환
    return (
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )


def format_datetime(
    dt: datetime,
    format: str = '%Y-%m-%d %H:%M:%S'
) -> str:
    """
    datetime 객체를 문자열로 포맷팅합니다.
    
    Args:
        dt: datetime 객체
        format: 출력 포맷 (기본: YYYY-MM-DD HH:MM:SS)
    
    Returns:
        str: 포맷팅된 날짜 문자열
    
    Examples:
        >>> dt = datetime(2026, 1, 20, 14, 30)
        >>> format_datetime(dt)
        '2026-01-20 14:30:00'
    """
    return dt.strftime(format)


def calculate_duration(
    start_time: str,
    end_time: str
) -> float:
    """
    두 시간 사이의 시간차를 시간(hour) 단위로 계산합니다.
    
    Args:
        start_time: 시작 시간 (예: "2026-01-20 10:00")
        end_time: 종료 시간 (예: "2026-01-20 13:30")
    
    Returns:
        float: 시간차 (시간 단위)
    
    Examples:
        >>> calculate_duration("2026-01-20 10:00", "2026-01-20 13:30")
        3.5
    """
    # 문자열을 datetime으로 변환
    start = parse_datetime(start_time)
    end = parse_datetime(end_time)
    
    # 시간차 계산 (timedelta 객체)
    duration = end - start
    
    # 시간 단위로 변환 (초 → 시간)
    hours = duration.total_seconds() / 3600
    
    return hours


def get_time_window(
    center_time: str,
    hours_before: int = 4,
    hours_after: int = 4
) -> Tuple[str, str]:
    """
    중심 시간을 기준으로 시간 윈도우를 계산합니다.
    
    알람 발생 전후의 데이터를 조회할 때 사용합니다.
    
    Args:
        center_time: 중심 시간 (예: "2026-01-20 14:00")
        hours_before: 이전 시간 (기본: 4시간)
        hours_after: 이후 시간 (기본: 4시간)
    
    Returns:
        Tuple[str, str]: (시작시간, 종료시간)
    
    Examples:
        >>> get_time_window("2026-01-20 14:00", 4, 4)
        ('2026-01-20 10:00:00', '2026-01-20 18:00:00')
    """
    # 중심 시간을 datetime으로 변환
    center = parse_datetime(center_time)
    
    # 시작/종료 시간 계산
    start_time = center - timedelta(hours=hours_before)
    end_time = center + timedelta(hours=hours_after)
    
    # 문자열로 변환
    return (
        format_datetime(start_time),
        format_datetime(end_time)
    )