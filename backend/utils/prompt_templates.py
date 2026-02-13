"""
LLM 프롬프트 템플릿
"""

def get_root_cause_analysis_prompt(context_data: str) -> str:
    """
    근본 원인 분석을 위한 프롬프트를 생성합니다.
    
    Args:
        context_data: 분석할 컨텍스트 데이터
    
    Returns:
        str: 프롬프트 문자열
    """
    return f"""당신은 제조 라인 KPI 분석 전문가입니다. 
아래 데이터를 분석하여 문제의 근본 원인을 찾아주세요.

{context_data}

**분석 요구사항:**
1. 문제점을 명확히 정의하세요
2. 가능한 근본 원인을 3~5개 제시하세요
3. 각 원인의 가능성을 퍼센트(%)로 표시하세요
4. 각 원인에 대한 증거/근거를 제시하세요

**출력 형식:**
JSON 형식으로 다음과 같이 출력하세요:
{{
    "problem_summary": "문제 요약",
    "root_causes": [
        {{
            "cause": "원인 1",
            "probability": 40,
            "evidence": "근거 설명"
        }},
        ...
    ]
}}
"""


def get_report_writer_prompt(
    problem_summary: str,
    selected_cause: str,
    evidence: str,
    context_data: str
) -> str:
    """
    최종 분석 리포트 작성을 위한 프롬프트를 생성합니다.
    
    Args:
        problem_summary: 문제 요약
        selected_cause: 사용자가 선택한 근본 원인
        evidence: 해당 원인의 근거
        context_data: 분석 컨텍스트
    
    Returns:
        str: 프롬프트 문자열
    """
    return f"""당신은 제조 라인 KPI 분석 리포트 작성 전문가입니다.
아래 정보를 바탕으로 상세한 분석 리포트를 작성해주세요.

## 문제 요약
{problem_summary}

## 확정된 근본 원인
{selected_cause}

## 근거
{evidence}

## 원본 데이터
{context_data}

**리포트 작성 요구사항:**
1. 경영진도 이해할 수 있도록 명확하게 작성
2. 구체적인 수치와 데이터 포함
3. 권장 조치사항 제시
4. 예상 효과 설명

**출력 형식:**
마크다운 형식으로 다음 섹션을 포함하세요:
- # 분석 리포트
- ## 1. 문제 정의
- ## 2. 근본 원인 분석
- ## 3. 영향 분석
- ## 4. 권장 조치사항
- ## 5. 예상 효과
"""


def get_question_answer_prompt(
    question: str,
    similar_reports: list
) -> str:
    """
    과거 리포트 기반 질문 답변을 위한 프롬프트를 생성합니다.
    
    Args:
        question: 사용자 질문
        similar_reports: 유사한 과거 리포트 리스트
    
    Returns:
        str: 프롬프트 문자열
    """
    # 유사 리포트 포맷팅
    reports_text = ""
    for i, report in enumerate(similar_reports, 1):
        reports_text += f"\n### 참고 리포트 {i}\n"
        reports_text += f"**날짜:** {report['metadata'].get('date')}\n"
        reports_text += f"**장비:** {report['metadata'].get('eqp_id')}\n"
        reports_text += f"**KPI:** {report['metadata'].get('kpi')}\n"
        reports_text += f"**내용:**\n{report['document'][:500]}...\n"
    
    return f"""당신은 제조 라인 KPI 분석 전문가입니다.
사용자의 질문에 과거 분석 리포트를 참고하여 답변해주세요.

## 사용자 질문
{question}

## 참고할 과거 리포트
{reports_text if reports_text else "관련된 과거 리포트가 없습니다."}

**답변 요구사항:**
1. 과거 리포트의 내용을 참고하여 답변
2. 구체적인 사례와 수치 포함
3. 명확하고 실용적인 조언 제공
4. 답변 출처 명시 (어떤 리포트 참고했는지)

**답변을 작성해주세요:**
"""