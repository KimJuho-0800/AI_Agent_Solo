"""
Node 6: Root Cause Analysis 테스트
"""

import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.nodes.node_1_input_router import node_1_input_router
from backend.nodes.node_2_load_alarm_kpi import node_2_load_alarm_kpi
from backend.nodes.node_3_context_fetch import node_3_context_fetch
from backend.nodes.node_6_root_cause_analysis import node_6_root_cause_analysis


def test_root_cause_analysis():
    """근본 원인 분석 테스트"""
    
    print("\n" + "=" * 60)
    print("🧪 근본 원인 분석 테스트")
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
    
    # Node 6: Root Cause Analysis
    print("4️⃣ Node 6 실행...")
    result6 = node_6_root_cause_analysis(state)
    state.update(result6)
    
    # 검증
    assert 'error' not in state, f"에러 발생: {state.get('error')}"
    assert state.get('root_causes') is not None, "root_causes 없음"
    
    root_causes = state['root_causes']
    
    # 근본 원인 개수 확인 (3~5개)
    assert 3 <= len(root_causes) <= 5, f"근본 원인 개수 이상: {len(root_causes)}"
    
    # 각 원인 검증
    for cause in root_causes:
        assert 'cause' in cause, "cause 필드 없음"
        assert 'probability' in cause, "probability 필드 없음"
        assert 'evidence' in cause, "evidence 필드 없음"
        
        # 확률 범위 확인 (0~100)
        prob = cause['probability']
        assert 0 <= prob <= 100, f"확률 범위 오류: {prob}"
    
    # 확률 합계 확인 (대략 100에 가까워야 함)
    total_prob = sum(c['probability'] for c in root_causes)
    print(f"\n✅ 근본 원인 분석 성공!")
    print(f"   총 {len(root_causes)}개 원인")
    print(f"   확률 합계: {total_prob}%")
    
    # LLM 호출 횟수 확인
    metadata = state.get('metadata', {})
    llm_calls = metadata.get('llm_calls', 0)
    print(f"   LLM 호출 횟수: {llm_calls}회")
    
    print("\n✅ 근본 원인 분석 테스트 통과!\n")


def test_specific_alarm_analysis():
    """특정 알람 분석 테스트 (2026-01-20, EQP01, OEE)"""
    
    print("=" * 60)
    print("🧪 특정 알람 분석 테스트")
    print("=" * 60 + "\n")
    
    # 과거 알람 지정
    state = {
        'alarm_date': '2026-01-20',
        'alarm_eqp_id': 'EQP01',
        'alarm_kpi': 'OEE'
    }
    
    # Node 2, 3 실행
    state.update(node_2_load_alarm_kpi(state))
    state.update(node_3_context_fetch(state))
    
    # Node 6 실행
    result = node_6_root_cause_analysis(state)
    state.update(result)
    
    # 검증
    assert 'error' not in state, f"에러 발생: {state.get('error')}"
    assert state.get('root_causes') is not None, "root_causes 없음"
    
    root_causes = state['root_causes']
    
    print(f"\n✅ 2026-01-20 EQP01 OEE 알람 분석 완료")
    print(f"\n근본 원인 후보:")
    
    for i, cause in enumerate(root_causes, 1):
        print(f"\n{i}. {cause['cause']}")
        print(f"   확률: {cause['probability']}%")
        print(f"   근거: {cause['evidence'][:80]}...")
    
    print("\n✅ 특정 알람 분석 테스트 통과!\n")


def main():
    """모든 테스트 실행"""
    
    print("\n🧪 Node 6: Root Cause Analysis 테스트 시작\n")
    
    try:
        test_root_cause_analysis()
        test_specific_alarm_analysis()
        
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