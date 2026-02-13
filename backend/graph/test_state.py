"""
AgentState 테스트
"""

import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.graph.state import (
    AgentState,
    create_initial_state,
    print_state_summary
)


def test_initial_state():
    """초기 State 생성 테스트"""
    
    print("\n" + "=" * 60)
    print("🧪 초기 State 생성 테스트")
    print("=" * 60 + "\n")
    
    # 알람 타입 State 생성
    state = create_initial_state(
        input_type="alarm",
        input_data="EQP01 장비에서 OEE 알람 발생"
    )
    
    print("✅ 알람 타입 State 생성 완료")
    print(f"   - input_type: {state['input_type']}")
    print(f"   - input_data: {state['input_data']}")
    print(f"   - metadata: {state['metadata']}\n")
    
    # 질문 타입 State 생성
    state2 = create_initial_state(
        input_type="question",
        input_data="지난주 EQP01에서 무슨 문제가 있었나요?"
    )
    
    print("✅ 질문 타입 State 생성 완료")
    print(f"   - input_type: {state2['input_type']}")
    print(f"   - input_data: {state2['input_data']}\n")


def test_state_update():
    """State 업데이트 테스트"""
    
    print("=" * 60)
    print("🔄 State 업데이트 테스트")
    print("=" * 60 + "\n")
    
    # 초기 State 생성
    state = create_initial_state("alarm", "알람 발생")
    
    print("1️⃣ 초기 State:")
    print(f"   필드 개수: {len(state)}\n")
    
    # 알람 정보 추가
    state['alarm_date'] = "2026-01-20"
    state['alarm_eqp_id'] = "EQP01"
    state['alarm_kpi'] = "OEE"
    
    print("2️⃣ 알람 정보 추가 후:")
    print(f"   - alarm_date: {state['alarm_date']}")
    print(f"   - alarm_eqp_id: {state['alarm_eqp_id']}")
    print(f"   - alarm_kpi: {state['alarm_kpi']}\n")
    
    # KPI 데이터 추가
    state['kpi_data'] = {
        'date': '2026-01-20',
        'eqp_id': 'EQP01',
        'oee_t': 70,
        'oee_v': 53.51,
        'alarm_flag': 1
    }
    
    print("3️⃣ KPI 데이터 추가 후:")
    print(f"   - kpi_data: {state['kpi_data']}\n")
    
    # 근본 원인 추가
    state['root_causes'] = [
        {
            "cause": "장비 다운타임 증가",
            "probability": 40,
            "evidence": "3시간 다운타임 발생"
        },
        {
            "cause": "복잡한 레시피 사용",
            "probability": 30,
            "evidence": "복잡도 9/10 레시피"
        }
    ]
    
    print("4️⃣ 근본 원인 추가 후:")
    print(f"   - root_causes: {len(state['root_causes'])}개\n")
    
    # 최종 리포트 추가
    state['final_report'] = "# 분석 리포트\n\n문제: OEE 저하..."
    state['report_id'] = "report_20260120_EQP01_OEE"
    
    print("5️⃣ 최종 리포트 추가 후:")
    print(f"   - final_report: 생성 완료")
    print(f"   - report_id: {state['report_id']}\n")


def test_state_summary():
    """State 요약 출력 테스트"""
    
    print("=" * 60)
    print("📊 State 요약 출력 테스트")
    print("=" * 60 + "\n")
    
    # 복잡한 State 생성
    state = create_initial_state("alarm", "EQP01 OEE 알람")
    
    # 다양한 필드 추가
    state['alarm_date'] = "2026-01-20"
    state['alarm_eqp_id'] = "EQP01"
    state['alarm_kpi'] = "OEE"
    state['kpi_data'] = {'oee_v': 53.51, 'oee_t': 70}
    state['lot_data'] = [{'lot_id': 'LOT001'}, {'lot_id': 'LOT002'}]
    state['eqp_data'] = [{'eqp_state': 'DOWN'}]
    state['root_causes'] = [
        {"cause": "원인1", "probability": 40},
        {"cause": "원인2", "probability": 30}
    ]
    state['selected_cause'] = {"cause": "장비 다운타임", "probability": 40}
    state['final_report'] = "# 분석 리포트\n완료"
    state['report_id'] = "report_20260120_EQP01_OEE"
    
    # 요약 출력
    summary = print_state_summary(state)
    print(summary)


def main():
    """모든 테스트 실행"""
    
    print("\n🧪 AgentState 테스트 시작\n")
    
    test_initial_state()
    test_state_update()
    test_state_summary()
    
    print("\n" + "=" * 60)
    print("🎊 모든 테스트 완료!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()