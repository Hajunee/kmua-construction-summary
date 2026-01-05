# 파일명: src/02_graph_construction/wiki_parser.py
import os
import pandas as pd
from bs4 import BeautifulSoup

# ==========================================
# 1. 경로 설정 (자동화)
# ==========================================
# 현재 파일 위치: kmua.../src/02_graph_construction/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

# 입력: 위키 XML 파일들이 모여있는 폴더
SOURCE_DIR = os.path.join(ROOT_DIR, 'data', '03_raw_xml')
# 출력: 변환된 CSV가 저장될 폴더
OUTPUT_DIR = os.path.join(ROOT_DIR, 'data', '04_graph_csv')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ==========================================
# 2. 고해상도 관계 매핑 (Ontology Logic)
# ==========================================
def get_predicate(ontology_tag, text_value, context_hint=""):
    """
    태그와 문맥을 분석하여 최적의 관계명(Predicate)을 도출
    """
    # [1] 인물/조직 (Role Inference)
    if "Participant" in ontology_tag:
        if any(k in context_hint for k in ["설계", "건축사", "기사"]): return "kmua:designedBy"
        elif any(k in context_hint for k in ["시공", "청부", "공사", "조"]): return "kmua:constructedBy"
        elif any(k in context_hint for k in ["설비", "전기", "난방", "위생"]): return "kmua:equippedBy"
        return "cidoc:hasParticipant"

    # [2] 마감재 (Finish Detail)
    if "Covering" in ontology_tag or "Finish" in ontology_tag:
        if any(w in context_hint for w in ["바닥", "깔기", "다다미", "마루"]): return "kmua:hasFloorFinish"
        elif any(w in context_hint for w in ["벽", "징두리", "벽지", "타일"]): return "kmua:hasWallFinish"
        elif any(w in context_hint for w in ["천장", "반죽", "몰탈"]): return "kmua:hasCeilingFinish"
        elif any(w in context_hint for w in ["외벽", "화강석", "벽돌"]): return "kmua:hasExteriorFinish"
        return "kmua:hasFinishDetail"

    # [3] 설비 시스템 (Technical System)
    if "Heating" in ontology_tag: return "brick:feedsHeatTo"
    if "Plumbing" in ontology_tag: return "brick:providesWaterTo"
    if "Lighting" in ontology_tag: return "brick:hasLighting"
    if "Elevator" in ontology_tag: return "kmua:hasVerticalTransport"

    # [4] 수치/단위 정밀 매핑 (Unit Inference)
    # 예산/비용
    if "hasCost" in ontology_tag or any(c in text_value for c in ["원", "엔"]):
        return "kmua:hasTotalBudget"
    # 면적
    if any(unit in text_value for unit in ["평", "홉", "작", "m2", "㎡"]):
        if "대지" in context_hint or "부지" in context_hint: return "kmua:hasSiteArea"
        return "kmua:hasTotalArea"
    # 높이
    if any(unit in text_value for unit in ["척", "촌", "미터", "m"]):
        return "kmua:hasHeight"

    # [5] 공간 및 기타
    if "Storey" in ontology_tag: return "bot:hasStorey"
    if "Space" in ontology_tag: return "bot:containsZone"
    if "isLocatedIn" in ontology_tag: return "kmua:isLocatedIn"

    return "kmua:relatedTo"

# ==========================================
# 3. 파싱 엔진 (XML -> Triples)
# ==========================================
def extract_text_from_xml(xml_content):
    try:
        soup = BeautifulSoup(xml_content, "html.parser")
        text_tag = soup.find("text")
        return text_tag.get_text() if text_tag else xml_content
    except:
        return xml_content

def parse_wiki_text(doc_name, wiki_source):
    triples = []
    # 기본 노드 생성
    triples.append({"Subject": doc_name, "Predicate": "rdf:type", "Object": "ModernArchitecture", "Label": "Building"})

    lines = wiki_source.split('\n')
    for line in lines:
        line_soup = BeautifulSoup(line, "html.parser")
        current_context = line_soup.get_text() # 현재 줄의 텍스트를 문맥으로 사용
        
        spans = line_soup.find_all("span")
        for span in spans:
            if span.has_attr("title"):
                tag = span["title"]
                val = span.get_text().strip()
                
                # 관계명 추론
                pred = get_predicate(tag, val, context_hint=current_context)
                
                # 라벨(Entity Type) 결정
                label = "Entity"
                if "Participant" in tag: label = "Actor"
                elif "Storey" in tag or "Space" in tag: label = "Space"
                elif "brick" in tag: label = "Facility"
                elif "Material" in tag or "Covering" in tag: label = "Material"
                
                triples.append({"Subject": doc_name, "Predicate": pred, "Object": val, "Label": label})
    return triples

# ==========================================
# 4. 실행 (Batch Process)
# ==========================================
def run_batch_conversion():
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Error: 입력 폴더가 없습니다 -> {SOURCE_DIR}")
        return

    xml_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.xml')]
    
    if not xml_files:
        print(f"⚠️ 경고: {SOURCE_DIR} 폴더에 XML 파일이 하나도 없습니다!")
        return

    print(f"🚀 총 {len(xml_files)}개의 XML 파일을 변환합니다...")

    for filename in xml_files:
        # 파일명에서 확장자 제거하여 문서 ID로 사용 (예: 07_11_경성재판소)
        doc_name = os.path.splitext(filename)[0]
        # 한글이나 특수문자가 있을 수 있으므로 안전하게 처리
        safe_doc_name = doc_name.replace(" ", "_")

        file_path = os.path.join(SOURCE_DIR, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = extract_text_from_xml(f.read())
            
            triples = parse_wiki_text(safe_doc_name, content)
            df = pd.DataFrame(triples)
            
            # 결과 저장
            output_csv = f"kmua_{safe_doc_name}.csv"
            output_path = os.path.join(OUTPUT_DIR, output_csv)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            print(f"  ✅ 변환 완료: {filename} -> {output_csv}")
            
        except Exception as e:
            print(f" 실패 ({filename}): {e}")

    print("\n ㄴ모든 변환 작업이 끝났습니다!")

if __name__ == "__main__":
    run_batch_conversion()