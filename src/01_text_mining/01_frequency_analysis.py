# 파일명: src/01_text_mining.py
import os
import pandas as pd
from janome.tokenizer import Tokenizer
from collections import Counter

# ==========================================
# 1. 경로 및 설정 (상대 경로 적용)
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # src 폴더
ROOT_DIR = os.path.dirname(BASE_DIR)                  # 루트 폴더

DATA_DIR = os.path.join(ROOT_DIR, 'data', '01_raw_txt')       # 입력: 텍스트 파일들
RESULT_DIR = os.path.join(ROOT_DIR, 'data', '02_analysis_result') # 출력: 결과 CSV

if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)

# 불용어 설정 (분석 제외 단어)
STOP_WORDS = [
    '一', 'の', '二', '三', '四', '五', '六', '七', '八', '九', '十', 
    'こと', 'もの', 'ため', 'よう', 'それ', '이하', '이상', '이내', '부분',
    '공사', '개요', '건축', '설계', '시공', '경성', '소와' # 필요시 추가
]

# ==========================================
# 2. 분석 엔진 (Janome)
# ==========================================
def extract_nouns(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    nouns = []
    
    for token in tokens:
        pos = token.part_of_speech.split(',')
        if pos[0] == '名詞': # 명사만 추출
            word = token.surface
            # 1글자 이상, 숫자 제외, 불용어 제외, 비자립 명사 제외
            if (len(word) > 1 and not word.isdigit() and 
                word not in STOP_WORDS and pos[1] not in ['非自立', '数', '接尾']):
                nouns.append(word)
    return nouns

# ==========================================
# 3. 실행 로직
# ==========================================
def run_mining():
    print(" 텍스트 마이닝 시작...")
    all_nouns = []
    
    file_list = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
    print(f"총 {len(file_list)}개의 파일을 분석합니다.")

    for idx, filename in enumerate(file_list):
        if idx % 50 == 0: print(f"   - 진행률: {idx}/{len(file_list)}")
        
        with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            all_nouns.extend(extract_nouns(content))

    # 빈도 계산
    count = Counter(all_nouns)
    df = pd.DataFrame(count.most_common(), columns=['Word', 'Frequency'])
    
    # 결과 저장
    output_path = os.path.join(RESULT_DIR, 'noun_frequency.csv')
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"분석 완료 결과 저장됨: {output_path}")

if __name__ == "__main__":
    run_mining()