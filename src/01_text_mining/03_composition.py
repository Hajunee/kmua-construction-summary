# 파일명: src/01_text_mining/03_composition.py
import os
import pandas as pd
from janome.tokenizer import Tokenizer

# ==========================================
# 1. 프로젝트 경로 자동 설정 (상대 경로)
# ==========================================
# 현재 파일 위치: kmua.../src/01_text_mining/
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
# 프로젝트 루트: kmua.../
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR)) 

# [입력 1] 원본 텍스트 파일들이 있는 폴더
DATA_DIR = os.path.join(ROOT_DIR, 'data', '01_raw_txt')

# [입력 2] 클러스터링 결과 엑셀 파일 (Step 1 결과물)
# ※ 파일명이 'q1_refined_result.xlsx'라고 가정합니다. 다르면 수정하세요.
CLUSTER_FILE = os.path.join(ROOT_DIR, 'data', '02_mining_results', 'q1_refined_result.xlsx')

# [출력] 조성비 계산 결과 저장 경로
OUTPUT_FILE = os.path.join(ROOT_DIR, 'data', '02_mining_results', 'document_composition_scores.xlsx')

# ==========================================
# 2. 실행 로직 (q3_document_scoring.py 내용)
# ==========================================
def run_composition_scoring():
    # (1) 클러스터 데이터 로드
    if not os.path.exists(CLUSTER_FILE):
        print(f"❌ Error: 클러스터 결과 파일이 없습니다 -> {CLUSTER_FILE}")
        return

    print("🚀 문서 조성비 스코어링 시작...")
    df_clusters = pd.read_excel(CLUSTER_FILE)
    
    # 단어-라벨 매핑 사전 생성 (Word -> Cluster ID)
    # 엑셀에 'Word'와 'Cluster' 컬럼이 있어야 합니다.
    word_label_map = dict(zip(df_clusters['Word'], df_clusters['Cluster']))
    unique_labels = sorted(df_clusters['Cluster'].unique())

    # (2) 텍스트 파일 순회 및 점수 계산
    t = Tokenizer()
    doc_scores = []
    
    # 데이터 폴더가 없으면 에러 처리
    if not os.path.exists(DATA_DIR):
        print(f"Error: 데이터 폴더가 없습니다 -> {DATA_DIR}")
        return

    file_list = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
    print(f"📄 총 {len(file_list)}개의 문서를 분석합니다.")

    for idx, filename in enumerate(file_list):
        if idx % 50 == 0: print(f"   - 진행률: {idx}/{len(file_list)}")
        
        file_path = os.path.join(DATA_DIR, filename)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            print(f"⚠️ 파일 읽기 실패 ({filename}): {e}")
            continue
        
        if not text: continue

        # 명사 추출 (Janome)
        tokens = t.tokenize(text)
        words = [token.surface for token in tokens if token.part_of_speech.startswith('名詞')]
        
        # 카운팅 초기화
        counts = {label: 0 for label in unique_labels}
        total_valid_words = 0
        
        # 매핑된 단어 카운트
        for word in words:
            if word in word_label_map:
                label = word_label_map[word]
                counts[label] += 1
                total_valid_words += 1
        
        # 비율 계산 (%)
        if total_valid_words > 0:
            scores = {f"Label_{k}(%)": round((v / total_valid_words) * 100, 1) for k, v in counts.items()}
        else:
            scores = {f"Label_{k}(%)": 0 for k in unique_labels}
            
        scores['FileName'] = filename
        scores['Total_Keywords'] = total_valid_words
        doc_scores.append(scores)

    # (3) 결과 저장
    if not doc_scores:
        print("⚠️ 분석된 결과가 없습니다.")
        return

    df_scores = pd.DataFrame(doc_scores)
    
    # 컬럼 순서 정리: FileName과 Total_Keywords를 맨 앞으로
    cols = ['FileName', 'Total_Keywords'] + [c for c in df_scores.columns if c not in ['FileName', 'Total_Keywords']]
    df_scores = df_scores[cols]
    
    # 폴더가 없으면 생성
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    df_scores.to_excel(OUTPUT_FILE, index=False)
    print(f"분석 완료 결과 저장됨: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_composition_scoring()