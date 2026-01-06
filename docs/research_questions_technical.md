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

##  Analysis Logic (Example)

**[Scenario] Q1. 고급 마감재가 쓰인 층(Storey) 찾기**
```cypher
MATCH (b:Building)-[:containsZone]->(s:Space)
MATCH (s)-[:hasFloorFinish]->(m:Material)
WHERE m.name CONTAINS '대리석' OR m.name CONTAINS '화강석'
RETURN b.name AS Building, s.floor AS Floor, count(*) AS RoomCount
ORDER BY s.floor DESC
