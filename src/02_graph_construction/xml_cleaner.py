# 파일명: src/02_graph_construction/xml_cleaner.py
import os
import re

# 1. 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

# [입력] 원본 XML이 있는 폴더 (03_raw_xml)
INPUT_DIR = os.path.join(ROOT_DIR, 'data', '03_raw_xml')

# [출력] 청소된 XML을 저장할 폴더 (04_clean_xml)
OUTPUT_DIR = os.path.join(ROOT_DIR, 'data', '04_clean_xml')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def clean_xml_files():
    if not os.path.exists(INPUT_DIR):
        print(f"[오류] 입력 폴더를 찾을 수 없습니다: {INPUT_DIR}")
        return

    xml_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.xml')]
    print(f"[시작] '{INPUT_DIR}' 폴더에서 {len(xml_files)}개의 XML 파일 발견")
    
    for idx, filename in enumerate(xml_files):
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        try:
            # 1. 파일 읽기 (인코딩 에러 무시)
            with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            # 2. 데이터 정제
            # 2-1. XML 금지 제어 문자 제거
            content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', content)

            # 2-2. & 기호 문법 오류 수정
            # & 뒤에 amp;, lt; 등이 없으면 단순 텍스트 &로 간주하고 &amp;로 치환
            content = re.sub(r'&(?!(?:amp|lt|gt|apos|quot|#\d+);)', '&amp;', content)

            # 3. 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f" - [완료] {filename} -> 04_clean_xml 폴더에 저장됨")

        except Exception as e:
            print(f" - [실패] {filename}: {e}")

    print("\n[전체 완료] 모든 파일 청소 끝. 이제 wiki_xml_to_csv.py를 실행하세요.")

if __name__ == "__main__":
    clean_xml_files()