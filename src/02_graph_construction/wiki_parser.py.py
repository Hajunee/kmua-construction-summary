# 파일명: src/02_graph_construction/wiki_parser.py
import os
import pandas as pd
import html
import re
from bs4 import BeautifulSoup

# ==========================================
# 1. 경로 설정
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

# 입력: 청소된 XML (Clean Version)
SOURCE_DIR = os.path.join(ROOT_DIR, 'data', '04_clean_xml')
# 출력: v3.0 그래프 CSV
OUTPUT_DIR = os.path.join(ROOT_DIR, 'data', '05_graph_csv')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ==========================================
# 2. v3.0 온톨로지 매핑 로직
# ==========================================
def analyze_entity_v3(tag, text_value, context_hint=""):
    """
    XML 태그와 문맥을 분석하여 v3.0 기준의 Class와 Attribute를 도출
    Returns: (Class, Attribute_Name, Attribute_Value)
    """
    # 1. Actor (인물/기관)
    if "Participant" in tag or "Architect" in tag or "Builder" in tag:
        role = "Unspecified"
        if any(k in context_hint for k in ["설계", "건축사", "기사"]): role = "Architect (설계)"
        elif any(k in context_hint for k in ["시공", "청부", "공사", "조", "작업"]): role = "Builder (시공)"
        elif any(k in context_hint for k in ["납품", "상점", "상회"]): role = "Supplier (납품)"
        elif any(k in context_hint for k in ["감리", "감독"]): role = "Supervisor (감리)"
        return "Actor", "Role", role

    # 2. Structure (구조)
    if "StructuralSystem" in tag or "BuildingElement" in tag:
        st_type = "Structure Element"
        if any(k in context_hint for k in ["철근", "RC", "콘크리트"]): st_type = "RC"
        elif any(k in context_hint for k in ["벽돌", "조적"]): st_type = "Masonry"
        elif any(k in context_hint for k in ["목조", "지붕"]): st_type = "Timber/Roof"
        return "Structure", "Type", st_type

    # 3. Material (재료)
    if "Material" in tag or "Covering" in tag or "Finish" in tag:
        return "Material", "Name", text_value

    # 4. Facility (설비)
    if "brick" in tag or "Heating" in tag or "Plumbing" in tag or "Lighting" in tag or "Equipment" in tag:
        fac_type = "General Facility"
        if any(k in tag for k in ["Heating", "Heat"]): fac_type = "Heating (난방)"
        elif any(k in tag for k in ["Plumbing", "Water", "Sanitary"]): fac_type = "Plumbing (위생)"
        elif any(k in tag for k in ["Lighting", "Elec", "Power"]): fac_type = "Electrical (전기)"
        elif any(k in tag for k in ["Elevator", "Transport"]): fac_type = "Transport (승강기)"
        return "Facility", "Type", fac_type

    # 5. Location (위치)
    if "isLocatedIn" in tag or "Address" in tag:
        return "Location", "AddressOld", text_value

    # 6. Year (연도/시기)
    if "TimeSpan" in tag or "Date" in tag or "Year" in tag:
        attr_name = "EventDate"
        if "착공" in context_hint: attr_name = "StartDate"
        elif "준공" in context_hint: attr_name = "EndDate"
        return "Year", attr_name, text_value

    # 7. Building Attributes (건물 자체 속성)
    # 면적
    if "Area" in tag or any(unit in text_value for unit in ["평", "m2", "㎡"]):
        attr_name = "TotalArea"
        if "대지" in context_hint or "부지" in context_hint: attr_name = "SiteArea"
        return "Building", attr_name, text_value
    # 높이
    if "Height" in tag or any(unit in text_value for unit in ["척", "m", "미터"]):
        return "Building", "Height", text_value
    # 층수
    if "Storey" in tag or "Floors" in tag:
        return "Building", "Floors", text_value
    # 용도
    if "Function" in tag or "Use" in tag:
        return "Building", "Function", text_value

    # 매핑되지 않는 기타 태그
    return "Etc", "Description", text_value

# ==========================================
# 3. 파싱 엔진
# ==========================================
def extract_text_from_xml(xml_content):
    try:
        soup = BeautifulSoup(xml_content, "html.parser")
        text_tag = soup.find("text")
        if text_tag:
            return html.unescape(text_tag.get_text())
        else:
            return html.unescape(xml_content)
    except:
        return xml_content

def parse_wiki_text_v3(doc_name, wiki_source):
    rows = []
    
    # 기본 행: 건물 자체 정의
    rows.append({
        "Source_Document": doc_name,
        "Class": "Building",
        "Entity_Name": doc_name, # 건물명이 곧 Entity
        "Attribute_Type": "Name",
        "Attribute_Value": doc_name,
        "Original_Context": "Document Title"
    })

    lines = wiki_source.split('\n')
    for line in lines:
        line_soup = BeautifulSoup(line, "html.parser")
        current_context = line_soup.get_text().strip()
        
        spans = line_soup.find_all("span")
        for span in spans:
            if span.has_attr("title"):
                tag = span["title"]
                val = span.get_text().strip()
                
                # v3.0 분석 실행
                cls, attr_type, attr_val = analyze_entity_v3(tag, val, context_hint=current_context)
                
                # 데이터 행 추가
                rows.append({
                    "Source_Document": doc_name,
                    "Class": cls,             # Actor, Material, Facility ...
                    "Entity_Name": val,       # 실제 텍스트 (예: 다전순삼랑, 대리석)
                    "Attribute_Type": attr_type, # Role, Type, Origin ...
                    "Attribute_Value": attr_val, # Builder, RC, Heating ...
                    "Original_Context": current_context[:100] # 검증용 문맥 (너무 길면 자름)
                })
    return rows

# ==========================================
# 4. 실행 (Batch)
# ==========================================
def run_batch_conversion():
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Error: 입력 폴더가 없습니다 -> {SOURCE_DIR}")
        return

    xml_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.xml')]
    print(f"🚀 [KMUA v3.0] 총 {len(xml_files)}개의 XML을 분석합니다...")

    for filename in xml_files:
        doc_name = os.path.splitext(filename)[0].replace(" ", "_")
        file_path = os.path.join(SOURCE_DIR, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = extract_text_from_xml(f.read())
            
            # v3 파싱
            parsed_rows = parse_wiki_text_v3(doc_name, content)
            df = pd.DataFrame(parsed_rows)
            
            # v3부터는 'Label' 대신 'Class'와 'Attribute' 컬럼을 중심으로 저장
            output_csv = f"kmua_v3_{doc_name}.csv"
            output_path = os.path.join(OUTPUT_DIR, output_csv)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            print(f"  ✅ 변환 완료: {filename} -> {output_csv}")
            
        except Exception as e:
            print(f"  ❌ 실패 ({filename}): {e}")

    print("\n🎉 모든 변환 작업이 완료되었습니다! (v3.0 Schema Applied)")

if __name__ == "__main__":
    run_batch_conversion()