# KMUA Ontology Definition (v3.0)
> **Data Model & Schema Specification**

본 문서는 KMUA 프로젝트의 데이터 구조를 정의한다. 2026년 1월 6일 회의 결과를 바탕으로, 분석의 효율성과 명확성을 위해 7대 핵심 클래스와 권장 속성을 아래와 같이 설정하였다.

## 1. Schema Diagram
![KMUA Data Schema](kmua_ontology_schema.png)
*(참고: 스키마 다이어그램 이미지는 추후 v3.0에 맞게 업데이트가 필요함)*

---

## 2. Class & Attribute Table (클래스 및 속성 정의)

데이터는 7가지 주요 클래스(Class)로 구분되며, 각 클래스는 분석에 필요한 필수 속성(Attributes)을 포함한다.

| Class (대상 클래스) | Recommended Attributes (권장 속성) | Description (비고) |
| :--- | :--- | :--- |
| **Building**<br>(건물) | `Name` (명칭: 원문/번역)<br>`TotalArea` (연면적)<br>`SiteArea` (대지면적)<br>`Floors` (층수: 지상/지하)<br>`Height` (높이)<br>`Function` (용도/기능) | 건물의 규모와 성격을 수치화하여 비교 분석 가능 |
| **Actor**<br>(인물/기관) | `Name` (성명: 원문/번역)<br>`Nationality` (국적)<br>`Role` (직업분류: 설계/시공/건주) | 인물 간 네트워크 및 국적별 건축 활동 특징 분석 가능 |
| **Location**<br>(위치) | `AddressOld` (당시 지명)<br>`AddressNew` (현재 지명)<br>`Coordinates` (위도/경도) | 추후 GIS(지도) 시각화 서비스와 연동 가능 |
| **Year**<br>(연도) | `StartDate` (착공일)<br>`EndDate` (준공일)<br>*Format: YYYY-MM-DD* | 공사 기간 계산 및 시기별 건축 트렌드 분석 가능 |
| **Structure**<br>(구조) | `Type` (구조종류: RC/목조/벽돌 등)<br>`Method` (세부공법) | 구조 기술의 발전 및 유형별 분포 분석 |
| **Material**<br>(재료) | `Name` (명칭: 원문/번역)<br>`Origin` (산지/출처)<br>`Manufacturer` (제조사)<br>`Brand` (브랜드) | 마감재의 수급 경로 및 산업적 배경 추적 |
| **Facility**<br>(설비) | `Name` (명칭: 원문/번역)<br>`Type` (설비종류: 난방/위생/전기)<br>`Manufacturer` (제조사)<br>`Brand` (브랜드) | 근대적 설비(난방, 승강기 등)의 도입 현황 분석 |

---

## 3. Semantic Rules (데이터 관계 규칙)
* **Actor Relationship**: `Actor`는 `Building`에 대해 특정 `Role`(설계, 시공 등)을 수행한다.
* **Material/Facility Composition**: `Material`과 `Facility`는 `Building`의 물리적 구성 요소로 포함된다.
* **Temporal Scope**: 모든 `Building` 프로젝트는 `Year`(착공~준공)의 시간적 범위를 가진다.