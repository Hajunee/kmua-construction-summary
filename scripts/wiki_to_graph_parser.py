import re
import os
import pandas as pd
from bs4 import BeautifulSoup

# ==========================================
# 1. 고해상도 관계 매핑 로직 (유지)
# ==========================================
def get_predicate(ontology_tag, text_value, context_hint=""):
    # [1] 인물/조직
    if "Participant" in ontology_tag:
        if any(keyword in context_hint for keyword in ["설계", "건축사", "감독"]): return "kmua:designedBy"
        elif any(keyword in context_hint for keyword in ["시공", "청부", "형무소", "공사"]): return "kmua:constructedBy"
        elif any(keyword in context_hint for keyword in ["설비", "전기", "난방", "위생"]): return "kmua:equippedBy"
        return "cidoc:hasParticipant"

    # [2] 마감재
    if "Covering" in ontology_tag or "Finish" in ontology_tag:
        if any(w in context_hint for w in ["바닥", "깔기", "다다미", "리놀륨"]): return "kmua:hasFloorFinish"
        elif any(w in context_hint for w in ["벽", "징두리", "벽지"]): return "kmua:hasWallFinish"
        elif any(w in context_hint for w in ["천장", "반죽"]): return "kmua:hasCeilingFinish"
        elif any(w in context_hint for w in ["외벽", "화강석", "처마"]): return "kmua:hasExteriorFinish"
        return "kmua:hasFinishDetail"

    # [3] 설비
    if "Heating" in ontology_tag: return "brick:feedsHeatTo"
    if "HVAC" in ontology_tag: return "brick:feedsAirTo"
    if "Plumbing" in ontology_tag: return "brick:providesWaterTo"
    if "Lighting" in ontology_tag: return "brick:hasLighting"
    if "Elevator" in ontology_tag: return "kmua:hasVerticalTransport"
    if "Communication" in ontology_tag: return "brick:hasPoint"

    # [4] 공간/기타
    if "Storey" in ontology_tag: return "bot:hasStorey"
    if "Space" in ontology_tag: return "bot:containsZone"
    if "isLocatedIn" in ontology_tag: return "kmua:isLocatedIn"
    if "hasCost" in ontology_tag or "hasTotalCost" in ontology_tag: return "kmua:hasTotalBudget"

    return "kmua:relatedTo"

# ==========================================
# 2. 파서 (XML 본문 추출 포함)
# ==========================================
def extract_text_from_xml(xml_content):
    try:
        soup = BeautifulSoup(xml_content, "html.parser")
        text_tag = soup.find("text")
        if text_tag:
            return text_tag.get_text()
        else:
            return xml_content
    except Exception as e:
        print(f"⚠️ XML 파싱 경고: {e}")
        return xml_content

def parse_wiki_text(doc_name, wiki_source):
    triples = []
    triples.append({"Subject": doc_name, "Predicate": "rdf:type", "Object": "ModernArchitecture", "Label": "Building"})

    lines = wiki_source.split('\n')
    current_context = "" 

    for line in lines:
        line_soup = BeautifulSoup(line, "html.parser")
        line_text = line_soup.get_text()
        current_context = line_text 
        
        spans = line_soup.find_all("span")
        for span in spans:
            if span.has_attr("title"):
                ontology_tag = span["title"]
                entity_value = span.get_text().strip()
                
                predicate = get_predicate(ontology_tag, entity_value, context_hint=current_context)
                
                label = "Entity"
                if "Participant" in ontology_tag: label = "Actor"
                elif "Storey" in ontology_tag or "Space" in ontology_tag: label = "Space"
                elif "brick" in ontology_tag: label = "Facility"
                elif "Material" in ontology_tag or "Covering" in ontology_tag: label = "Material"
                
                triples.append({
                    "Subject": doc_name,
                    "Predicate": predicate,
                    "Object": entity_value,
                    "Label": label
                })
    return triples

# ==========================================
# 3. 경로 설정 (output_csv 저장용)
# ==========================================

# 현재 스크립트 파일의 위치(scripts 폴더)를 기준으로 경로를 잡습니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
SOURCE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'source_data'))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'output_csv'))

# output_csv 폴더가 없으면 자동으로 생성
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def run_conversion(filename, doc_name):
    # 1. 파일 읽기
    file_path = os.path.join(SOURCE_DIR, filename)
    
    if not os.path.exists(file_path):
        print(f"❌ 오류: source_data 폴더에 파일이 없습니다 -> {filename}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    # 2. XML 처리
    if filename.lower().endswith('.xml'):
        print(f"📂 XML 파일 처리 중: {filename}")
        wiki_text = extract_text_from_xml(raw_content)
    else:
        wiki_text = raw_content
    
    # 3. 파싱 및 데이터프레임 변환
    triples = parse_wiki_text(doc_name, wiki_text)
    df = pd.DataFrame(triples)
    
    # 4. CSV 저장 (output_csv 폴더에만 저장)
    csv_name = f"kmua_{doc_name}.csv"
    output_path = os.path.join(OUTPUT_DIR, csv_name)
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"✅ 변환 완료!")
    print(f"   - 저장 경로: {output_path}")
    print(f"   - 데이터 개수: {len(df)}개")

# ==========================================
# ★ 실행
# ==========================================
if __name__ == "__main__":
    # 선생님 폴더에 있는 파일명 그대로 사용
    target_filename = "07_11_경성재판소.xml"  
    
    run_conversion(target_filename, "Gyeongseong_Court")