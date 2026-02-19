"""
LangGraph 워크플로우 정의

두 가지 경로:
1. 알람 분석: 1 → 2 → 3 → 6 → 7 → 8 → 9
2. 질문 답변: 1 → 4 → 5
"""

import sys
from pathlib import Path
from typing import Literal

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from langgraph.graph import StateGraph, END
from backend.graph.state import AgentState

# 각 노드 함수 개별 import
from backend.nodes.node_1_input_router import node_1_input_router
from backend.nodes.node_2_load_alarm_kpi import node_2_load_alarm_kpi
from backend.nodes.node_3_context_fetch import node_3_context_fetch
from backend.nodes.node_4_report_lookup import node_4_report_lookup
from backend.nodes.node_5_rag_answer import node_5_rag_answer
from backend.nodes.node_6_root_cause_analysis import node_6_root_cause_analysis
from backend.nodes.node_7_human_choice import node_7_human_choice
from backend.nodes.node_8_report_writer import node_8_report_writer
from backend.nodes.node_9_persist_report import node_9_persist_report


def route_after_input(state: AgentState) -> Literal["alarm_path", "question_path"]:
    """
    Node 1 이후 경로 결정
    
    Args:
        state: 현재 State
    
    Returns:
        "alarm_path" 또는 "question_path"
    """
    input_type = state.get('input_type')
    
    if input_type == 'alarm':
        return "alarm_path"
    else:
        return "question_path"


def create_workflow() -> StateGraph:
    """
    LangGraph 워크플로우를 생성합니다.
    
    Returns:
        StateGraph: 컴파일된 워크플로우
    """
    
    # StateGraph 생성
    workflow = StateGraph(AgentState)
    
    # ========== 노드 추가 ==========
    
    # 공통 노드
    workflow.add_node("node_1", node_1_input_router)
    
    # 알람 경로 노드
    workflow.add_node("node_2", node_2_load_alarm_kpi)
    workflow.add_node("node_3", node_3_context_fetch)
    workflow.add_node("node_6", node_6_root_cause_analysis)
    workflow.add_node("node_7", node_7_human_choice)
    workflow.add_node("node_8", node_8_report_writer)
    workflow.add_node("node_9", node_9_persist_report)
    
    # 질문 경로 노드
    workflow.add_node("node_4", node_4_report_lookup)
    workflow.add_node("node_5", node_5_rag_answer)
    
    # ========== 엣지 추가 ==========
    
    # 시작점: Node 1
    workflow.set_entry_point("node_1")
    
    # Node 1 이후 조건부 분기
    workflow.add_conditional_edges(
        "node_1",
        route_after_input,
        {
            "alarm_path": "node_2",
            "question_path": "node_4"
        }
    )
    
    # 알람 경로: 2 → 3 → 6 → 7 → 8 → 9 → END
    workflow.add_edge("node_2", "node_3")
    workflow.add_edge("node_3", "node_6")
    workflow.add_edge("node_6", "node_7")
    workflow.add_edge("node_7", "node_8")
    workflow.add_edge("node_8", "node_9")
    workflow.add_edge("node_9", END)
    
    # 질문 경로: 4 → 5 → END
    workflow.add_edge("node_4", "node_5")
    workflow.add_edge("node_5", END)
    
    # 컴파일
    app = workflow.compile()
    
    return app


# 전역 워크플로우 인스턴스 (lazy initialization)
_workflow_app = None


def get_workflow_app():
    """워크플로우 앱을 가져옵니다 (싱글톤 패턴)"""
    global _workflow_app
    if _workflow_app is None:
        _workflow_app = create_workflow()
    return _workflow_app


def run_alarm_analysis(alarm_date: str = None, alarm_eqp_id: str = None, alarm_kpi: str = None) -> AgentState:
    """
    알람 분석 워크플로우를 실행합니다.
    
    Args:
        alarm_date: 알람 날짜 (None이면 최신 알람)
        alarm_eqp_id: 장비 ID (None이면 최신 알람)
        alarm_kpi: KPI (None이면 최신 알람)
    
    Returns:
        AgentState: 최종 State
    
    Examples:
        >>> # 최신 알람 분석
        >>> result = run_alarm_analysis()
        
        >>> # 특정 알람 분석
        >>> result = run_alarm_analysis(
        ...     alarm_date="2026-01-20",
        ...     alarm_eqp_id="EQP01",
        ...     alarm_kpi="OEE"
        ... )
    """
    
    print("\n" + "=" * 60)
    print("🚀 알람 분석 워크플로우 시작")
    print("=" * 60 + "\n")
    
    # 초기 State
    initial_state = {
        'input_type': 'alarm',
        'metadata': {'llm_calls': 0}
    }
    
    # 특정 알람 지정 시
    if alarm_date and alarm_eqp_id and alarm_kpi:
        initial_state['alarm_date'] = alarm_date
        initial_state['alarm_eqp_id'] = alarm_eqp_id
        initial_state['alarm_kpi'] = alarm_kpi
    
    # 워크플로우 실행
    app = get_workflow_app()
    final_state = app.invoke(initial_state)
    
    print("\n" + "=" * 60)
    print("✅ 알람 분석 워크플로우 완료")
    print("=" * 60 + "\n")
    
    return final_state


def run_question_answer(question: str) -> AgentState:
    """
    질문 답변 워크플로우를 실행합니다.
    
    Args:
        question: 사용자 질문
    
    Returns:
        AgentState: 최종 State
    
    Examples:
        >>> result = run_question_answer("EQP01에서 OEE 문제가 발생한 이유는?")
    """
    
    print("\n" + "=" * 60)
    print("🚀 질문 답변 워크플로우 시작")
    print("=" * 60 + "\n")
    
    # 초기 State
    initial_state = {
        'input_type': 'question',
        'input_data': question,
        'metadata': {'llm_calls': 0}
    }
    
    # 워크플로우 실행
    app = get_workflow_app()
    final_state = app.invoke(initial_state)
    
    print("\n" + "=" * 60)
    print("✅ 질문 답변 워크플로우 완료")
    print("=" * 60 + "\n")
    
    return final_state