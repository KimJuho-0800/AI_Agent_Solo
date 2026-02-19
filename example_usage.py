"""
AI Agent 사용 예제
"""

from backend.graph.workflow import run_alarm_analysis, run_question_answer

print("=" * 60)
print("🤖 AI Agent KPI Monitor 사용 예제")
print("=" * 60)

# 예제 1: 최신 알람 분석
print("\n📊 예제 1: 최신 알람 분석")
print("-" * 60)

result = run_alarm_analysis()

print(f"\n결과:")
print(f"  📅 날짜: {result['alarm_date']}")
print(f"  🔧 장비: {result['alarm_eqp_id']}")
print(f"  📈 KPI: {result['alarm_kpi']}")
print(f"  🔍 근본 원인: {result['selected_cause']['cause']}")
print(f"  📝 리포트 ID: {result['report_id']}")
print(f"  💾 RAG 저장: {'✅' if result['rag_saved'] else '❌'}")

# 예제 2: 질문 답변
print("\n" + "=" * 60)
print("💬 예제 2: 질문 답변")
print("-" * 60)

question = "EQP01 장비에서 OEE 문제가 발생한 원인을 설명해주세요"
result = run_question_answer(question)

print(f"\n질문: {question}")
print(f"\n답변:")
print("-" * 60)
print(result['final_answer'][:300] + "...")
print("-" * 60)
print(f"\n참고 리포트: {len(result['similar_reports'])}개")

print("\n" + "=" * 60)
print("✨ 완료!")
print("=" * 60)