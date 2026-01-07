# 파일명: src/02_graph_construction/wiki_xml_to_csv.py
import xml.etree.ElementTree as ET
import pandas as pd
import re
import os
import uuid

# 1. 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

# [입력] 청소된 XML이 있는 폴더 (04_clean_xml)
INPUT_DIR = os.path.join(ROOT_DIR, 'data', '04_clean_xml')

# [출력] 최종 CSV 저장 경로 (05_graph_csv)
OUTPUT_DIR = os.path.join(ROOT_DIR, 'data', '05_graph_csv')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 2. 파싱 엔진
def parse_wiki_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except Exception as e:
        print(f"[오류] 파싱 실패 ({os.path.basename(xml_file)}): {e}")
        return []

    data = []
    
    for page in root.findall('.//{*}page'):
        # 건물명
        title_node = page.find('.//{*}title')
        if title_node is None: continue
        building_name = title_node.text
        
        # 본문 텍스트
        revision = page.find('.//{*}revision')
        if revision is None: continue
        text_node = revision.find('.//{*}text')
        if text_node is None or not text_node.text: continue
        text = text_node.text
        
        # 태그 데이터 추출
        pattern = r'<span[^>]+title="([^"]+)"[^>]*>(.*?)</span>'
        matches = re.findall(pattern, text)
        
        for class_field, value in matches:
            clean_val = re.sub(r'<[^>]+>', '', value).strip()
            
            row = {
                'id': str(uuid.uuid4())[:8],
                'building_name': building_name,
                'class_field': class_field,
                'name': clean_val,
                'korname': clean_val
            }
            data.append(row)
            
    return data

# 3. 실행
def run_converter():
    if not os.path.exists(INPUT_DIR):
        print(f"[오류] 입력 폴더가 없습니다: {INPUT_DIR}")
        print("먼저 xml_cleaner.py를 실행하여 04_clean_xml 폴더를 채워주세요.")
        return

    xml_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.xml')]
    print(f"[시작] '{INPUT_DIR}' 폴더에서 {len(xml_files)}개의 XML 파일 발견")
    
    all_data = []
    
    for idx, filename in enumerate(xml_files):
        file_path = os.path.join(INPUT_DIR, filename)
        file_data = parse_wiki_xml(file_path)
        all_data.extend(file_data)
        
        if (idx + 1) % 10 == 0:
            print(f" - 진행 중: {idx + 1}/{len(xml_files)} 완료")

    if all_data:
        df = pd.DataFrame(all_data)
        cols = ['id', 'building_name', 'class_field', 'name', 'korname']
        
        output_csv = os.path.join(OUTPUT_DIR, 'wiki_graph_data.csv')
        df[cols].to_csv(output_csv, index=False, encoding='utf-8-sig')
        
        print(f"\n[완료] 변환 성공. 총 {len(df)}개의 데이터 추출됨.")
        print(f"[저장] {output_csv}")
    else:
        print("\n[경고] 데이터가 추출되지 않았습니다.")

if __name__ == "__main__":
    run_converter()