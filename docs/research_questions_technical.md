#  KMUA Research Questions & Scenarios
> **Data-Driven Analysis of Modern Architecture in Colonial Korea (1920-1930s)**

본 문서는 KMUA 지식 그래프를 통해 규명하고자 하는 핵심 연구 질의(Research Questions)와 이를 해결하기 위한 데이터 분석 시나리오를 기술한다.

---

## Core Research Questions (Q1~Q5)

### Q1. Space & Hierarchy (공간 위계와 마감재)
> **"권위적 공간은 어디에 위치하며 무엇으로 치장되었는가?"**
* **Target Layer**: `Detail (Space)` ↔ `Detail (Finish)`
* **질문**: 3층 이상의 고층 건물에서 **'임원실', '응접실', '법정'** 등 위계가 높은 공간은 주로 몇 층에 배치되었으며, 이 공간들은 어떤 고급 마감재(대리석, 쪽모이 세공 등)를 공유하는가?
* **분석 목표**: 도면이 소실된 건물의 경우, 텍스트 데이터만으로 내부 공간의 권력 구조(Hierarchy)를 역추적한다.

### Q2. Modern Technology Adoption (설비의 도입과 편재)
> **"근대적 기술(설비)은 어떤 곳에 쓰였는가?"**
* **Target Layer**: `Detail (Facility)` ↔ `Core (Structure)`
* **질문**: '증기 난방(Steam Heating)'이나 '승강기(Elevator)'가 도입된 건물은 주로 어떤 용도(관공서 vs 상업시설)인가? 또한, 이러한 설비는 건물 전체를 커버하는가, 아니면 특정 구역(고위직 공간)에만 집중되는가?

### Q3. Construction Network (시공 네트워크)
> **"누가 1930년대의 경성을 건설했는가?"**
* **Target Layer**: `Archive (Context)`
* **질문**: 당시 주요 관공서 공사를 수주한 상위 시공사(Top-tier Builders)는 누구이며, 이들과 반복적으로 협업한 하도급 업체(전기, 위생)의 네트워크는 어떻게 형성되어 있는가?

---

=======
# KMUA Research Questions
> **327건의 신축공사 데이터로 읽는 1930년대 경성의 풍경**

본 연구는 1920-30년대 「신축공사개요」 327건을 전수 조사하여, 개별 건물의 특수성이 아닌 **시대의 보편적인 경향성**을 정량적으로 규명한다. 전문가가 아닌 사람들도 공감할 수 있는 거시적인 질문을 통해 당시의 도시 풍경과 삶의 질을 데이터로 시각화한다.

---

## Core Themes

### 1. Construction & Market (건설의 주체)
> **“언제, 어디서, 누가 주도했는가?”**
* 특정 시공사나 시기별 건축 활동의 추이와 규모 변화를 정량적으로 분석하여, 식민지 건설 시장의 흐름과 독점 구조를 규명함.
* **Target Data**: `Archive (시공사/건축가)` ↔ `Core (규모/시기)`

### 2. Technology & Comfort (기술의 보급)
> **“근대적 편리함은 얼마나 보편적이었는가?”**
* 327건의 전체 데이터 중 난방, 위생, 승강기 등 현대적 설비의 도입 비율을 정량 분석하여, 실제 도시의 생활 수준과 쾌적함의 불평등한 분배를 실증함.
* **Target Data**: `Core (용도)` ↔ `Detail (설비 시스템)`

### 3. Material & Hierarchy (권위의 연출)
> **“도시의 권위는 어떻게 시각화되었는가?”**
* 건물의 용도와 규모에 따른 외장(석재/타일) 및 내장(대리석/목재) 마감재의 사용 패턴을 통계적으로 분석하여, 건축물이 위계를 드러내는 방식과 도시의 시각적 풍경을 파악함.
* **Target Data**: `Detail (공간)` ↔ `Detail (마감재)`

---

<<<<<<<< HEAD:docs/research_questions.md
## Expected Value (연구의 가치)
* **정량적 실증**: "화려했을 것이다", "편리했을 것이다"라는 막연한 추측을 327건의 구체적인 통계 수치로 검증.
* **거시적 조망**: 소수의 랜드마크가 아닌, 중소규모 건축물까지 포함한 1930년대 경성의 '평균적인' 근대화 수준 제시.
========
>>>>>>> c2e7e35e810234f59ee1a53c455348be9de8c029
##  Analysis Logic (Example)

**[Scenario] Q1. 고급 마감재가 쓰인 층(Storey) 찾기**
```cypher
MATCH (b:Building)-[:containsZone]->(s:Space)
MATCH (s)-[:hasFloorFinish]->(m:Material)
WHERE m.name CONTAINS '대리석' OR m.name CONTAINS '화강석'
RETURN b.name AS Building, s.floor AS Floor, count(*) AS RoomCount
<<<<<<< HEAD
ORDER BY s.floor DESC
=======
ORDER BY s.floor DESC
>>>>>>>> c2e7e35e810234f59ee1a53c455348be9de8c029:docs/research_questions_technical.md
>>>>>>> c2e7e35e810234f59ee1a53c455348be9de8c029
