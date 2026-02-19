**Appendix A: FHIR (Fast Healthcare Interoperability Resources) in the NIAID Ecosystem**

This appendix expands on Module 2 (FAIR Principles and FAIR APIs) and Module 4 (Review of Existing APIs) by focusing on **FHIR**, a widely adopted global standard that functions as a highly structured, RESTful API framework. FHIR is especially relevant for clinical, trial, and immunology data within NIAID-funded repositories and aligns directly with NIAID’s goals for interoperability and the NIH Data Management & Sharing Policy.

### What is FHIR?
**Fast Healthcare Interoperability Resources (FHIR)** is an open standard developed by HL7 (Health Level Seven International). It defines:
- **Resources** — modular, reusable building blocks (e.g., Patient, Observation, ResearchStudy, Specimen, DiagnosticReport) that represent real-world healthcare concepts.
- **RESTful API** — standardized HTTP-based endpoints (GET, POST, PUT, etc.) that return data in JSON (default), XML, or RDF.
- **Profiles & Implementation Guides (IGs)** — constraints and extensions for specific use cases (e.g., US Core, research data).

FHIR is designed for **quick, lightweight exchange** of health data between systems (EHRs, research repositories, apps, public health platforms). Unlike older HL7 standards (v2, CDA), FHIR uses modern web technologies and is explicitly API-first.

**Official Site**: https://hl7.org/fhir/  
**Current Release**: R5 (with R4 still widely used).

### FHIR as a FAIR API Framework
FHIR is one of the strongest examples of a **FAIR-by-design API**. The official **HL7 FHIR for FAIR Implementation Guide (v1.0.0, STU 1)** — which includes **NIAID contributors Anupama Gururaj and Steve Tsang** — explicitly maps FHIR capabilities to the FAIR principles:

| FAIR Pillar       | How FHIR Supports It                                                                 |
|-------------------|--------------------------------------------------------------------------------------|
| **Findable**      | Persistent resource IDs, searchable metadata, GUIDs, rich indexing                   |
| **Accessible**    | Standardized REST endpoints, controlled access (OAuth2, JWT, SMART-on-FHIR)          |
| **Interoperable** | Common data models, ontologies (SNOMED, LOINC, RxNorm), JSON Schema, RDF support     |
| **Reusable**      | Provenance, versioning, licenses in metadata, machine- and human-readable formats    |

FHIR enables **semantic interoperability** across repositories, making it ideal for the NIAID Data Ecosystem Blueprint’s emphasis on harmonized metadata and cross-repository discovery.

### FHIR Adoption in the NIAID Ecosystem
Several repositories in the reviewed community have adopted or standardized on FHIR, particularly those handling clinical or human-subject data:

| Repository                  | FHIR Implementation Details                                                                 | Relevance to Users / Providers |
|-----------------------------|---------------------------------------------------------------------------------------------|--------------------------------|
| **ImmPort** (https://www.immport.org/) | Full production **FHIR Server** at `https://fhir.immport.org/fhir` (HAPI FHIR R5). Maps immunology assays, studies, subjects, lab results, etc. to standard resources. | Users: Query clinical immunology data via standard FHIR clients. Providers: Submit/reuse data in a format familiar to clinical systems. |
| **TB Portals** (https://tbportals.niaid.nih.gov/) | **All data** follows HL7 FHIR standard with uniform data dictionary and medical terminology. APIs enforce FHIR-compliant standardization for submitted cases. | Enables consistent TB clinical/genomic data exchange; integrates with accessclinicaldata.niaid.nih.gov. |
| **AccessClinicalData@NIAID** & related clinical portals (ACTG, ITN TrialShare, MWCCS) | TB Portals data (and similar NIAID clinical trials) use FHIR for structure and exchange. | Controlled-access clinical datasets become more interoperable post-approval. |
| **Broader NIAID / NIH**     | NIH Notice NOT-OD-19-122 (2019) encourages FHIR use for research data. NIAID contributors to FHIR for FAIR IG. Discovery Portal metadata harvesting benefits from FHIR-structured sources. | Supports ecosystem-wide harmonization. |

**ImmPort FHIR Server Highlights** (live example):
- **Base URL**: `https://fhir.immport.org/fhir`
- **Authentication**: JWT token via `POST https://www.immport.org/auth/token` (valid 1 hour).
- **Current Mappings** (examples):
  - ResearchStudy → Study design & NIAID sponsorship
  - Patient / ResearchSubject → Human subjects
  - Observation / DiagnosticReport → Lab tests & assessments
  - Specimen → Biosamples
  - Group / Organization / Practitioner → Cohorts & personnel
- Future mappings: Planned visits, mechanistic assays, interventions.

**Example Query (cURL – retrieve a study)**:
```bash
# 1. Get token
curl -X POST https://www.immport.org/auth/token \
  -d username=YOUR_USERNAME -d password=YOUR_PASSWORD

# 2. Query (replace $TOKEN)
curl -H "Authorization: bearer $TOKEN" \
  "https://fhir.immport.org/fhir/ResearchStudy/SDY1"
```

Response is a full JSON ResearchStudy resource including title, conditions, sponsor (NIAID), etc.

**Web Interface**: https://fhir.immport.org (OAuth2 login with ImmPort credentials).

### Benefits for NIAID API Users and Providers
**For Users (Researchers/Analysts):**
- Use familiar FHIR tools (e.g., Postman, FHIR clients in Python/R, SMART apps, HAPI FHIR Java client).
- Combine ImmPort immunology data with EHRs, ClinicalTrials.gov (FHIR export), or other FHIR-enabled systems.
- Automated pipelines for secondary analysis, real-world evidence, or AI-ready datasets.

**For Providers (Repository Teams):**
- Reduce custom API maintenance by adopting a global standard.
- Increase reuse and citations by making data consumable by clinical audiences.
- Align with NIH expectations and future mandates for standardized APIs.

**Ecosystem Impact**: FHIR bridges basic research repositories (e.g., IEDB, VEuPathDB – which use domain-specific REST) with clinical ones, supporting the NIAID Discovery Portal’s unified search and the “robust, sustainable data architecture” described in the Blueprint.

### Best Practices for Implementing or Using FHIR APIs
- Follow the [**FHIR for FAIR IG** recommendations](https://build.fhir.org/ig/HL7/fhir-for-fair/).
- Use official profiles (US Core for U.S. data) and validation tools (FHIR Validator).
- Document with CapabilityStatement and OpenAPI/Swagger.
- Provide bulk export (FHIR Bulk Data Access IG) for large datasets.
- Secure with OAuth2 / SMART-on-FHIR for controlled access.

### Resources
- ImmPort FHIR Documentation: https://docs.immport.org/fhir/documentation/
- TB Portals Data Standards: https://tbportals.niaid.nih.gov/what-types-of-data-do-we-have
- FHIR for FAIR Implementation Guide (NIAID contributors): https://build.fhir.org/ig/HL7/fhir-for-fair/
- HL7 FHIR Core Specification: https://hl7.org/fhir/
- NIH FHIR Guidance: https://grants.nih.gov/grants/guide/notice-files/NOT-OD-19-122.html
- NIAID FAIR Page (mentions ecosystem standards): https://www.niaid.nih.gov/research/fair-data-principles

**Hands-on Exercise Suggestion**: Register for an ImmPort account, obtain a JWT token, and query the ResearchStudy or Observation resources. Compare the FHIR JSON output with the same study data downloaded via the standard ImmPort REST API.

This appendix can be inserted after Module 8 or used as a standalone reference. It positions FHIR as a powerful, ready-to-use FAIR API solution already operating within the reviewed NIAID community. For updates, code samples, or workshop demos, contact the ImmPort or NIAID Data Science teams.
