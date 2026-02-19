"""
간단한 워크플로우 테스트
"""

print("=" * 60)
print("테스트 시작")
print("=" * 60)

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("\n1. Import 테스트...")

try:
    print("   - workflow import 시도...")
    from backend.graph.workflow import run_alarm_analysis, run_question_answer
    print("   ✅ workflow import 성공")
except Exception as e:
    print(f"   ❌ workflow import 실패: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n2. 알람 분석 실행...")

try:
    result = run_alarm_analysis(
        alarm_date="2026-01-20",
        alarm_eqp_id="EQP01", 
        alarm_kpi="OEE"
    )
    
    print(f"\n✅ 성공!")
    print(f"   리포트 ID: {result.get('report_id')}")
    print(f"   RAG 저장: {result.get('rag_saved')}")
    
except Exception as e:
    print(f"\n❌ 실행 실패: {e}")
    import traceback
    traceback.print_exc()

print("\n3. 질문 답변 실행...")

try:
    result = run_question_answer("EQP01에서 발생한 OEE 문제의 원인은?")
    
    print(f"\n✅ 성공!")
    print(f"   답변 길이: {len(result.get('final_answer', ''))}자")
    
except Exception as e:
    print(f"\n❌ 실행 실패: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("테스트 완료")
print("=" * 60)