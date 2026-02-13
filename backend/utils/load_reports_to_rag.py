"""
PDF 보고서를 ChromaDB에 로드하는 스크립트

사용자가 작성한 과거 알람 PDF 보고서들을 읽어서
ChromaDB Vector Database에 저장합니다.
"""

import sys
from pathlib import Path
import re

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.config.chroma_config import chroma_config

# PDF 텍스트 추출용 (이미 requirements.txt에 있음)
try:
    import pypdf
except ImportError:
    print("⚠️ pypdf 패키지가 필요합니다.")
    print("설치: pip install pypdf")
    sys.exit(1)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    PDF 파일에서 텍스트를 추출합니다.
    
    Args:
        pdf_path: PDF 파일 경로
    
    Returns:
        str: 추출된 텍스트
    """
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text()
        
        return text
    
    except Exception as e:
        print(f"❌ PDF 읽기 실패: {e}")
        return ""


def parse_report_filename(filename: str) -> dict:
    """
    파일명에서 메타데이터를 추출합니다.
    
    Args:
        filename: 파일명 (예: report_20260120_EQP01_OEE.pdf)
    
    Returns:
        dict: {date, eqp_id, kpi}
    """
    # report_20260120_EQP01_OEE.pdf
    pattern = r'report_(\d{8})_(EQP\d+)_([A-Z_]+)\.pdf'
    match = re.match(pattern, filename)
    
    if not match:
        return None
    
    date_str = match.group(1)  # 20260120
    eqp_id = match.group(2)     # EQP01
    kpi = match.group(3)        # OEE
    
    # 날짜 포맷 변환: 20260120 → 2026-01-20
    date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    
    return {
        'date': date,
        'eqp_id': eqp_id,
        'kpi': kpi
    }


def load_reports_to_rag(reports_dir: str = "data/reports"):
    """
    reports 폴더의 모든 PDF를 ChromaDB에 로드합니다.
    
    Args:
        reports_dir: PDF 파일들이 있는 폴더 경로
    """
    
    print("\n" + "=" * 60)
    print("📂 PDF 보고서 → ChromaDB 로드")
    print("=" * 60 + "\n")
    
    # reports 폴더 확인
    reports_path = Path(reports_dir)
    
    if not reports_path.exists():
        print(f"❌ 폴더가 없습니다: {reports_dir}")
        print(f"💡 먼저 폴더를 생성하세요: mkdir -p {reports_dir}")
        return
    
    # PDF 파일 목록 가져오기
    pdf_files = list(reports_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"⚠️ {reports_dir} 폴더에 PDF 파일이 없습니다.")
        print(f"💡 PDF 보고서를 작성해서 저장해주세요.")
        return
    
    print(f"📄 총 {len(pdf_files)}개의 PDF 발견\n")
    
    # 각 PDF 처리
    success_count = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        filename = pdf_file.name
        print(f"[{i}/{len(pdf_files)}] {filename}")
        
        # 1. 파일명에서 메타데이터 추출
        metadata_dict = parse_report_filename(filename)
        
        if not metadata_dict:
            print(f"  ⚠️ 파일명 형식 오류, 스킵\n")
            continue
        
        print(f"  📅 날짜: {metadata_dict['date']}")
        print(f"  🔧 장비: {metadata_dict['eqp_id']}")
        print(f"  📊 KPI: {metadata_dict['kpi']}")
        
        # 2. PDF 텍스트 추출
        text = extract_text_from_pdf(str(pdf_file))
        
        if not text or len(text) < 50:
            print(f"  ⚠️ 텍스트 추출 실패 또는 내용이 너무 짧음, 스킵\n")
            continue
        
        print(f"  📝 텍스트 추출: {len(text)}자")
        
        # 3. ChromaDB에 저장
        report_id = f"report_{metadata_dict['date']}_{metadata_dict['eqp_id']}_{metadata_dict['kpi']}"
        
        metadata = {
            "date": metadata_dict['date'],
            "eqp_id": metadata_dict['eqp_id'],
            "kpi": metadata_dict['kpi'],
            "alarm_flag": 1,
            "source": "pdf_report"
        }
        
        success = chroma_config.add_report(
            report_id=report_id,
            report_text=text,
            metadata=metadata
        )
        
        if success:
            print(f"  ✅ ChromaDB 저장 완료\n")
            success_count += 1
        else:
            print(f"  ❌ ChromaDB 저장 실패\n")
    
    # 최종 결과
    print("=" * 60)
    print(f"🎉 완료! {success_count}/{len(pdf_files)}개 성공")
    print(f"📊 ChromaDB 총 리포트: {chroma_config.count_reports()}개")
    print("=" * 60 + "\n")


def verify_rag_data():
    """
    ChromaDB에 저장된 데이터를 확인합니다.
    """
    
    print("\n" + "=" * 60)
    print("🔍 ChromaDB 저장 데이터 확인")
    print("=" * 60 + "\n")
    
    total = chroma_config.count_reports()
    print(f"총 {total}개의 리포트 저장됨\n")
    
    if total == 0:
        print("⚠️ 저장된 리포트가 없습니다.")
        return
    
    # 테스트 검색
    test_query = "EQP01 장비에서 OEE 문제가 발생했습니다"
    print(f"테스트 검색어: {test_query}\n")
    
    results = chroma_config.search_similar_reports(
        query_text=test_query,
        n_results=3
    )
    
    if results:
        print(f"✅ 유사 리포트 {len(results)}개 발견:\n")
        for i, report in enumerate(results, 1):
            print(f"{i}. ID: {report['id']}")
            print(f"   메타데이터: {report['metadata']}")
            print(f"   유사도: {report['distance']:.4f}")
            print(f"   내용 미리보기: {report['document'][:100]}...")
            print()
    else:
        print("⚠️ 검색 결과 없음")
    
    print("=" * 60 + "\n")


def main():
    """메인 함수"""
    
    print("\n🤖 PDF 보고서 RAG 로더\n")
    
    print("📋 사용 방법:")
    print("1. data/reports/ 폴더에 PDF 파일들을 넣으세요")
    print("2. 파일명 형식: report_YYYYMMDD_EQP번호_KPI.pdf")
    print("3. 이 스크립트를 실행하면 자동으로 ChromaDB에 저장됩니다\n")
    
    user_input = input("계속하시겠습니까? (y/n): ")
    
    if user_input.lower() != 'y':
        print("취소되었습니다.")
        return
    
    # PDF 로드
    load_reports_to_rag()
    
    # 검증
    verify_rag_data()


if __name__ == "__main__":
    main()