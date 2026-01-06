# 파일명: src/02_graph_construction/xml_cleaner.py
import os
import html
import re

# ==========================================
# 1. 경로 설정 (자동화)
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

# 입력: 위키 원본 (Raw)
INPUT_DIR = os.path.join(ROOT_DIR, 'data', '03_raw_xml')
# 출력: 정제된 XML (Clean)
OUTPUT_DIR = os.path.join(ROOT_DIR, 'data', '04_clean_xml')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ==========================================
# 2. 청소 로직 (Unescape)
# ==========================================
def clean_xml_content(content):
    # 1. HTML 엔티티 (&lt; -> <) 변환
    # 두 번 해주는 이유: 가끔 &amp;lt; 처럼 이중으로 꼬인 경우가 있어서 안전하게 처리
    cleaned = html.unescape(content)
    cleaned = html.unescape(cleaned) 
    return cleaned

def run_cleaner():
    if not os.path.exists(INPUT_DIR):
        print(f"❌ Error: 입력 폴더가 없습니다 -> {INPUT_DIR}")
        return

    file_list = [f for f in os.listdir(INPUT_DIR) if f.endswith('.xml')]
    print(f"🧹 XML 청소 시작! 총 {len(file_list)}개 파일 처리 중...")

    for filename in file_list:
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        try:
            # 파일 읽기
            with open(input_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()

            # 변환 수행
            clean_content = clean_xml_content(raw_content)

            # 파일 쓰기
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(clean_content)
                
            print(f"  ✨ 변환 완료: {filename}")

        except Exception as e:
            print(f"  ❌ 실패 ({filename}): {e}")

    print(f"\n🎉 모든 작업 완료! 결과는 '{OUTPUT_DIR}' 에서 확인하세요.")

if __name__ == "__main__":
    run_cleaner()