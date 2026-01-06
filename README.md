# KMUA Project: New Construction Summary Knowledge Graph
> **Korea Modern Urban Architecture (KMUA) Research Lab**
> **Sub-Project**: 근대 건축물 「신축공사개요」 지식 그래프 구축

## 1. Project Overview (개요)
본 프로젝트는 **'조선과 건축(KMUA)'** 의 하위 프로젝트입니다. 1920-30년대 『조선과 건축(朝鮮と建築)』 등에 수록된 「신축공사개요」를 텍스트 마이닝하여, 근대 건축의 생산과 구성을 입체적으로 분석할 수 있는 지식 그래프를 구축하는 것을 목표로 합니다.

### Objective (목표)
- **Datafication**: 비정형 텍스트(Text)로 존재하는 1차 사료를 시맨틱 데이터(Semantic Data)로 변환
- **Connectivity**: 문헌(Archive) - 구조(Core) - 상세(Detail) 간의 연결 고리 규명
- **Analysis**: 시공 네트워크, 자재 수급, 공간 위계 등에 대한 정량적 역사 분석 수행

---

## 2. Data Model: KMUA Ontology v2.3
본 연구는 건축학적 위계에 따라 데이터를 3대 레이어(Layer)와 6대 클러스터(Cluster)로 구조화했습니다.

| Layer | Color | Focus Area | Ontology Standard |
| :--- | :--- | :--- | :--- |
| **ARCHIVE** | Grey | **Context & Management**<br>(개요, 공사관리, 참여자) | CIDOC CRM |
| **CORE** | Blue | **Physical Structure**<br>(구조 시스템, 골조) | IFC Element |
| **DETAIL** | Orange | **Tech & Finish**<br>(마감재, 설비, 공간구성) | IFC Covering / Brick / BOT |

---

## 3. Tech Pipeline (구축 과정)
원문 사료가 지식 그래프가 되기까지의 기술적 흐름입니다.

1.  **Semantic Tagging (Wiki)**
    * MediaWiki 문법을 활용하여 원문 텍스트에 온톨로지 태그 부착
    * 예: `<span title="kmua:constructedBy">다전순삼랑</span>`
2.  **Parsing & ETL (Python)**
    * XML 파싱 및 고해상도 관계명(Predicate) 매핑
    * `Role Inference`: 단순 참여자를 설계/시공/납품으로 구분
    * `Context Mapping`: 마감재의 위치(바닥/벽/천장) 및 수치 단위(평, 척, 원) 자동 추론
3.  **Graph Database (Neo4j)**
    * CSV Import 및 Cypher Query를 통한 그래프 시각화

---

## 4. Usage (실행 방법)

### Prerequisites & Installation

이 프로젝트는 Python 3.8 이상 환경에서 동작하며, 데이터 분석 및 파싱을 위해 아래 라이브러리들이 필요합니다.

### Required Libraries
* pandas: 데이터 프레임 처리 및 CSV/Excel 입출력
* janome: 일본어 텍스트 형태소 분석
* beautifulsoup4: 위키 데이터(XML/HTML) 파싱
* openpyxl: 엑셀 파일(.xlsx) 입출력 지원

### Installation
터미널에서 아래 명령어를 입력하여 필수 패키지를 설치하십시오.

```bash
pip install pandas janome beautifulsoup4 openpyxl

- © 2025 KMUA Project.
