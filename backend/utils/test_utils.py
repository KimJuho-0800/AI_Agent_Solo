"""
유틸리티 함수 테스트
"""

import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.utils.date_utils import (
    parse_datetime,
    get_date_range,
    calculate_duration,
    get_time_window
)

from backend.utils.data_utils import (
    check_alarm_condition,
    calculate_kpi_gap,
    aggregate_lot_states,
    get_downtime_info
)


def test_date_utils():
    """날짜 유틸리티 함수 테스트"""
    
    print("\n" + "=" * 60)
    print("📅 날짜 유틸리티 테스트")
    print("=" * 60 + "\n")
    
    # parse_datetime 테스트
    print("1. parse_datetime() 테스트")
    dt = parse_datetime("2026-01-20")
    print(f"   '2026-01-20' → {dt}")
    
    dt2 = parse_datetime("2026-01-20 14:30")
    print(f"   '2026-01-20 14:30' → {dt2}\n")
    
    # get_date_range 테스트
    print("2. get_date_range() 테스트")
    start, end = get_date_range("2026-01-20", days_before=1, days_after=1)
    print(f"   중심: 2026-01-20, 전후 1일")
    print(f"   결과: {start} ~ {end}\n")
    
    # calculate_duration 테스트
    print("3. calculate_duration() 테스트")
    duration = calculate_duration("2026-01-20 10:00", "2026-01-20 13:30")
    print(f"   10:00 ~ 13:30 = {duration}시간\n")
    
    # get_time_window 테스트
    print("4. get_time_window() 테스트")
    start_time, end_time = get_time_window("2026-01-20 14:00", 4, 4)
    print(f"   중심: 14:00, 전후 4시간")
    print(f"   결과: {start_time} ~ {end_time}\n")
    
    print("✅ 날짜 유틸리티 테스트 완료!\n")


def test_data_utils():
    """데이터 유틸리티 함수 테스트"""
    
    print("=" * 60)
    print("📊 데이터 유틸리티 테스트")
    print("=" * 60 + "\n")
    
    # check_alarm_condition 테스트
    print("1. check_alarm_condition() 테스트")
    alarm, reason = check_alarm_condition("OEE", 70, 53.51)
    print(f"   OEE: 목표 70%, 실제 53.51%")
    print(f"   알람: {alarm}")
    print(f"   사유: {reason}\n")
    
    # calculate_kpi_gap 테스트
    print("2. calculate_kpi_gap() 테스트")
    gap_info = calculate_kpi_gap("OEE", 70, 53.51)
    print(f"   OEE 갭 분석:")
    print(f"   - 절대 차이: {gap_info['gap']:.2f}%")
    print(f"   - 퍼센트 차이: {gap_info['gap_percent']:.2f}%")
    print(f"   - 상태: {gap_info['status']}\n")
    
    # aggregate_lot_states 테스트
    print("3. aggregate_lot_states() 테스트")
    lot_data = [
        {'lot_state': 'RUN', 'in_cnt': 25},
        {'lot_state': 'HOLD', 'in_cnt': 25},
        {'lot_state': 'RUN', 'in_cnt': 25},
        {'lot_state': 'END', 'in_cnt': 25}
    ]
    lot_summary = aggregate_lot_states(lot_data)
    print(f"   총 로트: {lot_summary['total_lots']}개")
    print(f"   상태별: {lot_summary['state_counts']}")
    print(f"   HOLD: {lot_summary['hold_count']}회\n")
    
    # get_downtime_info 테스트
    print("4. get_downtime_info() 테스트")
    eqp_data = [
        {
            'eqp_state': 'DOWN',
            'event_time': '2026-01-20 01:25',
            'end_time': '2026-01-20 04:25'
        },
        {
            'eqp_state': 'DOWN',
            'event_time': '2026-01-20 06:20',
            'end_time': '2026-01-20 09:20'
        }
    ]
    downtime = get_downtime_info(eqp_data)
    print(f"   총 다운타임: {downtime['total_downtime_hours']}시간")
    print(f"   발생 횟수: {downtime['downtime_count']}회\n")
    
    print("✅ 데이터 유틸리티 테스트 완료!\n")


def main():
    """모든 테스트 실행"""
    
    print("\n🧪 유틸리티 함수 테스트 시작\n")
    
    test_date_utils()
    test_data_utils()
    
    print("=" * 60)
    print("🎊 모든 테스트 완료!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()