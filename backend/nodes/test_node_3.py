"""
Node 3: Context Fetch 테스트
"""

import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.nodes.node_1_input_router import node_1_input_router
from backend.nodes.node_2_load_alarm_kpi import node_2_load_alarm_kpi
from backend.nodes.node_3_context_fetch import node_3_context_fetch


def test_full_context_fetch():
    """전체 워크플로우 테스트 (Node 1 → 2 → 3)"""
    
    print("\n" + "=" * 60)
    print("🧪 전체 컨텍스트 조회 테스트")
    print("=" * 60 + "\n")
    
    # 초기 State
    state = {'input_type': 'alarm'}
    
    # Node 1: Input Router
    print("1️⃣ Node 1 실행...")
    result1 = node_1_input_router(state)
    state.update(result1)
    
    # Node 2: Load Alarm KPI
    print("2️⃣ Node 2 실행...")
    result2 = node_2_load_alarm_kpi(state)
    state.update(result2)
    
    # Node 3: Context Fetch
    print("3️⃣ Node 3 실행...")
    result3 = node_3_context_fetch(state)
    state.update(result3)
    
    # 검증
    assert 'error' not in state, f"에러 발생: {state.get('error')}"
    assert state.get('lot_data') is not None, "lot_data 없음"
    assert state.get('eqp_data') is not None, "eqp_data 없음"
    assert state.get('rcp_data') is not None, "rcp_data 없음"
    assert state.get('context_text') is not None, "context_text 없음"
    
    # 결과 출력
    print("\n✅ 모든 데이터 조회 성공!")
    print(f"\n📊 최종 State:")
    print(f"   - alarm_date: {state.get('alarm_date')}")
    print(f"   - alarm_eqp_id: {state.get('alarm_eqp_id')}")
    print(f"   - alarm_kpi: {state.get('alarm_kpi')}")
    print(f"   - lot_data: {len(state.get('lot_data', []))}개")
    print(f"   - eqp_data: {len(state.get('eqp_data', []))}개")
    print(f"   - rcp_data: {len(state.get('rcp_data', []))}개")
    print(f"   - context_text: {len(state.get('context_text', ''))}자")
    
    # 컨텍스트 미리보기
    context = state.get('context_text', '')
    print(f"\n📄 컨텍스트 미리보기:")
    print(context[:500] + "...")
    
    print("\n✅ 전체 컨텍스트 조회 테스트 통과!\n")


def test_specific_date_context():
    """특정 날짜 컨텍스트 조회 테스트"""
    
    print("=" * 60)
    print("🧪 특정 날짜 컨텍스트 조회 테스트")
    print("=" * 60 + "\n")
    
    # 과거 알람 (2026-01-20, EQP01, OEE)
    state = {
        'alarm_date': '2026-01-20',
        'alarm_eqp_id': 'EQP01',
        'alarm_kpi': 'OEE'
    }
    
    # Node 2 실행
    result2 = node_2_load_alarm_kpi(state)
    state.update(result2)
    
    # Node 3 실행
    result3 = node_3_context_fetch(state)
    state.update(result3)
    
    # 검증
    assert 'error' not in state, f"에러 발생: {state.get('error')}"
    
    # LOT_STATE 데이터 확인
    lot_data = state.get('lot_data', [])
    print(f"\n📦 로트 데이터:")
    print(f"   총 {len(lot_data)}개 이벤트")
    
    if lot_data:
        # 상태별 집계
        states = {}
        for lot in lot_data:
            state_name = lot.get('lot_state', 'UNKNOWN')
            states[state_name] = states.get(state_name, 0) + 1
        
        print(f"   상태별 분포: {states}")
        
        # HOLD 상태 확인
        hold_count = states.get('HOLD', 0)
        if hold_count > 0:
            print(f"   ⚠️ HOLD 상태 {hold_count}회 발생")
    
    # EQP_STATE 다운타임 확인
    eqp_data = state.get('eqp_data', [])
    print(f"\n🔧 장비 데이터:")
    print(f"   총 {len(eqp_data)}개 이벤트")
    
    if eqp_data:
        downtime_events = [e for e in eqp_data if e.get('eqp_state') == 'DOWN']
        print(f"   다운타임: {len(downtime_events)}회")
    
    # RCP_STATE 복잡도 확인
    rcp_data = state.get('rcp_data', [])
    print(f"\n📋 레시피 데이터:")
    print(f"   총 {len(rcp_data)}개 레시피")
    
    if rcp_data:
        for rcp in rcp_data:
            print(f"   - {rcp.get('rcp_id')}: 복잡도 {rcp.get('complex_level')}/10")
    
    print("\n✅ 특정 날짜 컨텍스트 조회 테스트 통과!\n")


def test_context_text_format():
    """컨텍스트 텍스트 포맷 검증"""
    
    print("=" * 60)
    print("🧪 컨텍스트 텍스트 포맷 검증")
    print("=" * 60 + "\n")
    
    # 최신 알람 조회
    state = {'input_type': 'alarm'}
    
    # Node 1, 2, 3 실행
    state.update(node_1_input_router(state))
    state.update(node_2_load_alarm_kpi(state))
    state.update(node_3_context_fetch(state))
    
    # 컨텍스트 텍스트 검증
    context_text = state.get('context_text', '')
    
    # 필수 섹션 확인
    required_sections = [
        '# 분석 컨텍스트 데이터',
        '## 1. KPI 정보',
        '## 2. KPI 수치',
        '## 3. 로트 상태 요약',
        '## 4. 장비 다운타임',
        '## 5. 레시피 정보'
    ]
    
    print("📄 컨텍스트 구조 검증:")
    for section in required_sections:
        if section in context_text:
            print(f"   ✅ {section}")
        else:
            print(f"   ❌ {section} - 누락!")
            assert False, f"필수 섹션 누락: {section}"
    
    # 데이터 포함 여부 확인
    alarm_date = state.get('alarm_date')
    alarm_eqp_id = state.get('alarm_eqp_id')
    
    assert alarm_date in context_text, "날짜 정보 없음"
    assert alarm_eqp_id in context_text, "장비 ID 정보 없음"
    
    print(f"\n✅ 컨텍스트 텍스트 포맷 검증 통과!\n")


def main():
    """모든 테스트 실행"""
    
    print("\n🧪 Node 3: Context Fetch 테스트 시작\n")
    
    try:
        test_full_context_fetch()
        test_specific_date_context()
        test_context_text_format()
        
        print("=" * 60)
        print("🎊 모든 테스트 통과!")
        print("=" * 60 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ 테스트 실패: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}\n")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()