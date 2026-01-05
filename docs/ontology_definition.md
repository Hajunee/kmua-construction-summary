# KMUA Ontology Definition (v2.3)
> **Data Model & Schema Specification**

본 문서는 KMUA 프로젝트의 데이터 구조를 정의한다. 텍스트 마이닝을 통해 도출된 6대 클러스터를 기반으로 클래스를 설계하였으며, 국제 표준(ISO/W3C)을 참조하여 호환성을 확보했다.

## 1. Schema Diagram
![KMUA Data Schema](kmua_ontology_schema.png)

---

## 2. Class & Predicate Table (클래스 및 관계 정의)

데이터는 크게 **Archive(문헌/관리)**, **Core(구조/물리)**, **Detail(상세/기술)** 3가지 레이어로 구분된다.

| Layer | Cluster (Class) | Ontology Ref. | Key Predicates (Relations) | Description |
| :--- | :--- | :--- | :--- | :--- |
| **ARCHIVE** | **kmua:ProjectOverview**<br>(기본 개요) | IFC Project | `kmua:hasName` (건물명)<br>`kmua:hasSiteArea` (대지면적)<br>`kmua:hasTotalArea` (연면적) | 건축물의 식별 정보 및 물리적 규모 |
| **ARCHIVE** | **kmua:ManagementData**<br>(공사 관리) | CIDOC CRM (E5) | `kmua:hasParticipant` (참여자)<br>`kmua:hasTimeSpan` (공사기간)<br>`kmua:hasTotalBudget` (공사비) | 설계, 시공, 감리 등 행위자 및 비용 정보 |
| **CORE** | **kmua:StructuralSystem**<br>(구조 시스템) | IFC BuildingElement | `kmua:hasStructure` (주체구조)<br>`kmua:hasFoundation` (기초)<br>`kmua:hasRoofType` (지붕) | 건물을 지탱하는 물리적 골조 및 시스템 |
| **DETAIL** | **kmua:SpatialUnit**<br>(공간 구성) | W3C BOT | `bot:hasStorey` (층)<br>`bot:containsZone` (실/구역)<br>`kmua:hasFunction` (용도) | 층별, 실별 공간의 위계 및 기능 |
| **DETAIL** | **kmua:FinishDetail**<br>(마감 상세) | IFC Covering | `kmua:hasFloorFinish` (바닥마감)<br>`kmua:hasWallFinish` (벽마감)<br>`kmua:hasCeiling` (천장마감) | 각 공간을 구성하는 재료 및 마감 상세 |
| **DETAIL** | **kmua:FacilitySystem**<br>(부대 설비) | Brick Schema | `brick:feedsHeatTo` (난방)<br>`brick:providesWater` (위생)<br>`brick:hasLighting` (전기) | 건물 내 기계, 전기, 위생 설비 시스템 |

---

## 3. Semantic Rules (추론 규칙)
* **Hierarchy Rule**: `SpatialUnit`은 `StructuralSystem`의 물리적 공간 내에 위치(`kmua:isLocatedIn`)한다.
* **Service Rule**: `FacilitySystem`은 특정 `SpatialUnit`에 기능을 제공(`brick:serves`)한다.
## 2. Class & Predicate Table (클래스 및 관계 정의)

데이터는 크게 **Archive(문헌/관리)**, **Core(구조/물리)**, **Detail(상세/기술)** 3가지 레이어로 구분된다.

| Layer | Cluster (Class) | Ontology Ref. | Key Predicates (Relations) | Description |
| :--- | :--- | :--- | :--- | :--- |
| **ARCHIVE** | **kmua:ProjectOverview**<br>(기본 개요) | IFC Project | `kmua:hasName` (건물명)<br>`kmua:hasSiteArea` (대지면적)<br>`kmua:hasTotalArea` (연면적) | 건축물의 식별 정보 및 물리적 규모 |
| **ARCHIVE** | **kmua:ManagementData**<br>(공사 관리) | CIDOC CRM (E5) | `kmua:hasParticipant` (참여자)<br>`kmua:hasTimeSpan` (공사기간)<br>`kmua:hasTotalBudget` (공사비) | 설계, 시공, 감리 등 행위자 및 비용 정보 |
| **CORE** | **kmua:StructuralSystem**<br>(구조 시스템) | IFC BuildingElement | `kmua:hasStructure` (주체구조)<br>`kmua:hasFoundation` (기초)<br>`kmua:hasRoofType` (지붕) | 건물을 지탱하는 물리적 골조 및 시스템 |
| **DETAIL** | **kmua:SpatialUnit**<br>(공간 구성) | W3C BOT | `bot:hasStorey` (층)<br>`bot:containsZone` (실/구역)<br>`kmua:hasFunction` (용도) | 층별, 실별 공간의 위계 및 기능 |
| **DETAIL** | **kmua:FinishDetail**<br>(마감 상세) | IFC Covering | `kmua:hasFloorFinish` (바닥마감)<br>`kmua:hasWallFinish` (벽마감)<br>`kmua:hasCeiling` (천장마감) | 각 공간을 구성하는 재료 및 마감 상세 |
| **DETAIL** | **kmua:FacilitySystem**<br>(부대 설비) | Brick Schema | `brick:feedsHeatTo` (난방)<br>`brick:providesWater` (위생)<br>`brick:hasLighting` (전기) | 건물 내 기계, 전기, 위생 설비 시스템 |

---

## 3. Semantic Rules (추론 규칙)
* **Hierarchy Rule**: `SpatialUnit`은 `StructuralSystem`의 물리적 공간 내에 위치(`kmua:isLocatedIn`)한다.
* **Service Rule**: `FacilitySystem`은 특정 `SpatialUnit`에 기능을 제공(`brick:serves`)한다.