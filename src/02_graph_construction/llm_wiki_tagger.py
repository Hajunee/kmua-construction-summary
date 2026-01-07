# 파일명: src/02_graph_construction/free_tier_tagger.py
import os
import time
from google import genai
from google.genai import types

# =========================================================
# [설정] 기존에 발급받은 API 키를 그대로 사용하세요
# =========================================================
API_KEY = "AIzaSyDcGuvRXRKOmXN-9406sX7wGtuDIpOVfWo"

# [핵심 변경] 무료 티어에서 가장 제한이 덜한 모델 사용
MODEL_NAME = "gemini-2.0-flash"

client = genai.Client(api_key=API_KEY)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
INPUT_DIR = os.path.join(ROOT_DIR, 'data', '01_raw_txt', 'kr_translated')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'data', '01_raw_txt', 'wiki_ai_tagged')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

SYSTEM_PROMPT = """
당신은 한국 근대 건축 역사학자이자 데이터 엔지니어입니다.
주어지는 [건축 공사 개요 텍스트]를 분석하여 MediaWiki 형식으로 변환하십시오.
반드시 아래 정의된 7가지 Class에 해당하는 단어를 찾아 지정된 HTML 태그(<span title="...">...</span>)로 감싸야 합니다.

[Class 정의]
1. Building (건물 속성): TotalArea, SiteArea, Height, Cost, Floors
2. Actor (인물/조직): Architect, Builder, Supplier
3. Material (재료)
4. Structure (구조)
5. Facility (설비)
6. Location (위치)
7. Year (시기): StartDate, EndDate

[출력 형식]
불필요한 설명 없이 태깅된 텍스트만 출력할 것.
"""

def process_with_flash(filename, text):
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"{SYSTEM_PROMPT}\n\n[입력 텍스트]\n{text}",
            config=types.GenerateContentConfig(
                temperature=0.0
            )
        )
        return response.text
    except Exception as e:
        print(f" [오류] {filename}: {e}")
        return None

def run_tagger():
    if "API_키" in API_KEY:
        print("오류: API 키를 입력해주세요.")
        return

    files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.txt')]
    print(f"무료 티어 태깅 시작 (모델: {MODEL_NAME}): 총 {len(files)}개 파일")

    for idx, filename in enumerate(files):
        print(f"[{idx+1}/{len(files)}] {filename} 처리 중...", end="", flush=True)
        
        file_path = os.path.join(INPUT_DIR, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        tagged_text = process_with_flash(filename, raw_text)

        if tagged_text:
            final_text = f"""__NOTOC__
{{| class="wikitable" style="float:right; width:300px;"
! colspan="2" | {os.path.splitext(filename)[0]}
|-
| colspan="2" | (사진)
|-
! 내용
| AI 자동 태깅 데이터 ({MODEL_NAME})
|}}

{tagged_text}

[[분류:신축공사개요]]
"""
            out_name = f"Wiki_AI_{filename}"
            with open(os.path.join(OUTPUT_DIR, out_name), 'w', encoding='utf-8') as f:
                f.write(final_text)
            print(" - 완료")
        else:
            print(" - 실패")
        
        # 무료 티어 제한(분당 15회)을 지키기 위해 4초 대기 (안전장치)
        time.sleep(4)

    print(f"\n작업 완료. 저장 경로: {OUTPUT_DIR}")

if __name__ == "__main__":
    run_tagger()