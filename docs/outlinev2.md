**Training Resource: APIs and FAIR APIs in the NIAID Ecosystem**  
**Target Audience:** API Users (researchers, analysts, data consumers) and Providers (repository developers, data stewards, NIAID-funded teams)  
**Format Recommendation:** Modular handbook (Markdown/PDF), slide deck for workshops, or interactive web module with code examples and links. Include hands-on exercises (e.g., Postman collections, Jupyter notebooks).  
**Version:** 1.0 (February 2026) | **Source:** Synthesized from NIAID official resources, FAIR Cookbook, repository documentation, and ecosystem reviews.  

### Module 1: Introduction to APIs in Biomedical Research
An **API** (Application Programming Interface) defines rules for software components to communicate. In NIAID contexts, APIs enable programmatic access to data on infectious diseases, immunology, clinical trials, genomics, and more—replacing manual downloads or web scraping.

**Common Types in NIAID Ecosystem:**
- RESTful APIs (most common; use HTTP methods like GET/POST, return JSON/TSV).
- GraphQL (flexible queries; used in some pathogen databases).
- Specialized: GA4GH DRS (Data Repository Service) for controlled-access files; JSON-RPC for bioinformatics tools.

**Benefits for Users:**
- Automation (batch queries, pipelines in R/Python).
- Integration (combine IEDB epitopes with VEuPathDB genomics or ImmPort immune data).
- Scalability (analyze thousands of records without GUI limits).

**Benefits for Providers:**
- Reduced server load vs. file downloads.
- Controlled access (tokens, auth).
- Enhanced visibility and reuse of your repository.

**Relevance to NIAID:** APIs make data machine-readable, supporting NIH/NIAID Data Management & Sharing Policy and accelerating discoveries in allergy, infectious, and immune-mediated diseases.

### Module 2: FAIR Principles and FAIR APIs
**FAIR Data Principles** (from NIAID FAIR page, 2025): Guidelines to make digital assets **F**indable, **A**ccessible, **I**nteroperable, and **R**eusable.

- **Findable**: Persistent IDs (DOIs, ORCIDs), rich machine-readable metadata, indexed in searchable repositories.
- **Accessible**: Retrievable via standard protocols (e.g., HTTP); authentication where needed.
- **Interoperable**: Standardized formats, vocabularies, ontologies (e.g., NCBI taxonomy, GO terms).
- **Reusable**: Clear licenses, provenance, domain standards.

**How APIs Enable FAIR Data:**
- Machine-readable access (JSON responses with metadata).
- Automated discovery and integration (e.g., NIAID Discovery Portal harvests via APIs).
- Interoperability across repositories.

**FAIR APIs** (APIs themselves made FAIR; see FAIR Cookbook "Developing FAIR API for the Web"):
- **Findable**: Document with OpenAPI/Swagger YAML; register in catalogs like SmartAPI.info (adds semantic annotations linking fields to identifiers.org, e.g., ncbigene).
- **Accessible**: Standard protocols, authentication docs, uptime guarantees.
- **Interoperable**: Use JSON Schema, RDF-friendly extensions (SmartAPI), common response structures; align with NIAID Minimal API Specifications (for metadata exposure).
- **Reusable**: Versioning, examples, client libraries (Python/R), reusable components/schemas.

**NIAID Context:** The NIAID Data Ecosystem Blueprint (2025) includes **Minimal API Specifications** for exposing metadata to machines, enabling the Discovery Portal to unify search. Standardized APIs across repositories create a "robust, sustainable data architecture."

**Key Quote (NIAID):** "APIs enable quick data access, efficient sharing across platforms, and automated updates."

### Module 3: NIAID Data Ecosystem Overview
NIAID funds an interconnected ecosystem of repositories for infectious/immunologic data. The **NIAID Data Ecosystem Discovery Portal** (data.niaid.nih.gov) provides unified search via harvested metadata + APIs. It aligns with FAIR and includes its own public metadata API (BioThings-style).

**Blueprint to Connect Data Across the Ecosystem** emphasizes:
- Minimal Metadata Schema.
- Persistent Identifiers.
- Minimal API Specs (standardized endpoints for metadata retrieval/citation).
- Minimal Citation Requirements.
- Point of Contact.

This promotes harmonization so users query once across multiple systems.

### Module 4: Review of Existing APIs in the Provided NIAID Community Repositories
Review based on official sites, docs, and NIAID references (as of 2026). Bioinformatics-focused repositories generally offer strong public/programmatic APIs; clinical/trial data often use portals with controlled access (request-based or token-auth).

| Repository/Link | Focus | API/Programmatic Access | FAIR Alignment Notes | User Tips / Examples |
|-----------------|-------|--------------------------|----------------------|----------------------|
| https://statepi.jhsph.edu/mwccs/ (MWCCS) | Multicenter AIDS Cohort Study (clinical/epidemiologic) | Limited; primarily web portal/downloads. Possible internal programmatic upon approval. | Metadata harvesting to Discovery Portal supports Findability. | Request access via portal; use for cohort studies. |
| https://actgnetwork.org/ (ACTG) | AIDS Clinical Trials Group (trials data) | Portal-based; restricted access. No prominent public API. | Controlled access aligns with Accessibility/Reusability rules. | Data requests via network; integrate post-approval. |
| https://www.iedb.org/ (IEDB) | Immune epitopes (antibody/T-cell, infectious/autoimmune) | **Strong**: IQ-API (PostgREST-based query to tables; Swagger docs); Tools API (predictions, analysis). REST/JSON/TSV. | Rich metadata, semantic fields; supports all FAIR pillars. Public, machine-readable. | Example (curl): `curl "https://query-api.iedb.org/epitope_search?linear_sequence=eq.SIINFEKL&limit=10"` (filters, pagination). Python `requests` or Jupyter notebooks available. |
| https://www.immport.org/ (ImmPort) | Shared immunology data (assays, studies, HIPC) | **Comprehensive**: REST APIs for query/search, data submission/upload, batch updater, GA4GH DRS (file access). OpenAPI/Swagger docs at docs.immport.org/apidocumentation/. Token auth. | Excellent metadata standards; DRS for reusable controlled data. | Auth token endpoint → query e.g., `/data/query/result/elisa?studyAccession=SDY2`. R/Python clients recommended. |
| https://www.itntrialshare.org/ (ITN TrialShare) | Immune Tolerance Network trials data | Portal with downloads; limited programmatic (request-based). | FAIR via metadata to ecosystem. | Portal search + download; contact for advanced access. |
| https://immunespace.org/ (ImmuneSpace) | Immune data visualization/queries (HIPC-related, links to ImmPort) | **Good**: R package (ImmuneSpaceR) + internal Plumber API endpoints. Programmatic queries. | Integrates with ImmPort for interoperability. | Install `ImmuneSpaceR`; query studies/datasets directly in R. |
| https://veupathdb.org/ (VEuPathDB) | Eukaryotic pathogens, vectors, hosts (omics, genomics) | **Strong**: REST Web Services/API (newer version enhances programmatic access). Queries for genes, genomes, etc. | Ontology-rich, structured data; highly interoperable. | Docs at veupathdb.org (service-api section). Complex queries via REST; supports large-scale analysis. |
| https://www.bv-brc.org/ (BV-BRC) | Bacterial/viral bioinformatics (genomes, tools) | **Strong**: Data API (REST), JSON-RPC for apps, CLI/FTP integration. | FAIR-compliant for genomics; machine-actionable. | Batch access, command-line tools; enumerate_apps/start_app via API. |
| https://www.ceirr-network.org/ (CEIRR) | Centers for Excellence in Influenza Research | Network portal; data likely via linked repositories (e.g., ImmPort/BV-BRC). Limited direct API. | Contributes metadata to Discovery Portal. | Cross-reference with partner repos. |
| https://clinepidb.org/ (ClinEpiDB) | Clinical epidemiology (infectious disease studies) | Query interface + downloads; programmatic options via underlying platform (e.g., similar to VEuPathDB). | Metadata standards support Findability/Interoperability. | Web queries; export for local use. |
| https://accessclinicaldata.niaid.nih.gov/ | NIAID clinical data access (controlled) | Request-based portal; possible API post-approval (e.g., DRS-like). | Strict Accessibility with provenance. | Apply for access; programmatic if approved. |
| https://tbportals.niaid.nih.gov/ (TB Portals) | Tuberculosis data (images, clinical, genomics) | **Good**: Data API + Analytic API (cohort creation/export). R wrapper (tbportals.depot.api). File/Aspera + programmatic. | Supports reuse with analytic tools. | Tidy API in R; explore via portal then API for cohorts. |

**Summary Insight:** Public bioinformatics repos (IEDB, ImmPort, VEuPathDB, BV-BRC) exemplify mature FAIR-aligned APIs. Clinical ones prioritize controlled access while feeding metadata to the unified Discovery Portal.

### Module 5: Best Practices for Providers (Building FAIR APIs)
Follow NIAID Blueprint Minimal API Specs + FAIR Cookbook:
1. Use OpenAPI 3+ for documentation (YAML/JSON); include info, paths, schemas, examples.
2. Add SmartAPI extensions for semantic linking (e.g., x-responseValueType to identifiers.org).
3. Implement stable versioning (e.g., /v1/), pagination, rate limits, error handling.
4. Expose rich metadata (align with NIAID schema); support OAI-PMH or BioThings-style for harvesting.
5. Security: Tokens/OAuth, GA4GH Passport for controlled data.
6. Test with OpenAPI Generator (clients in Python/R/Java).
7. Register in SmartAPI or NIAID catalogs; provide point of contact.
8. Monitor usage; sustain via long-term funding (as noted in NIH barriers papers).

**Checklist:** Persistent endpoints? Machine-readable responses? Semantic annotations? License in docs?

### Module 6: Best Practices for Users (Consuming APIs)
- Discover via NIAID Discovery Portal or SmartAPI.
- Tools: Postman (test), `requests` (Python), `httr`/`jsonlite` (R), or repo-specific packages (e.g., ImmuneSpaceR).
- Handle auth, pagination, errors.
- Combine data (e.g., IEDB epitopes + VEuPathDB host genes).
- Cite properly (use NIAID minimal citation requirements).
- Example Python snippet (IEDB):
  ```python
  import requests
  response = requests.get("https://query-api.iedb.org/epitope_search", params={"linear_sequence": "eq.SIINFEKL", "limit": 5})
  data = response.json()
  ```

**Hands-on Exercise:** Query ImmPort study data or IEDB epitopes; visualize in Python (pandas + matplotlib).

### Module 7: Challenges, Future Directions & Case Studies
**Challenges:** Inconsistent auth/metadata across repos; controlled-access barriers; sustainability of APIs.
**Future:** Greater harmonization via Blueprint; AI-ready semantic APIs; broader GraphQL adoption.

**Case Study:** ImmPort + IEDB integration enables automated epitope analysis from shared assay data—fully FAIR workflow supporting vaccine research.

**Case Study:** NIAID Discovery Portal aggregates via APIs → one search across 10+ repos, demonstrating interoperability wins.

### Module 8: Resources & Next Steps
- NIAID FAIR Page: https://www.niaid.nih.gov/research/fair-data-principles
- NIAID Data Blueprint & Discovery Portal: https://www.niaid.nih.gov/research/data-blueprint & https://data.niaid.nih.gov/
- FAIR Cookbook (FAIR API recipe): https://fairplus.github.io/the-fair-cookbook/
- ImmPort API Docs: https://docs.immport.org/apidocumentation/
- IEDB API: Search "IQ-API" on help.iedb.org
- SmartAPI Registry: https://smart-api.info/
- NIH Data Repositories List & GREI Initiative
- Training: NIH ODSS webinars; NIAID metadata stewardship resources
- Tools: OpenAPI Editor, Postman, BioThings API explorer

**Recommended Workshop Agenda (2-4 hours):** Intro (30 min) → FAIR Deep Dive (30 min) → Ecosystem Review + Demos (60 min) → Best Practices & Hands-on (60 min) → Q&A.

This material equips both users and providers to leverage and enhance the NIAID API landscape for maximum scientific impact. For customizations (e.g., slide templates, interactive notebooks, or updates), contact NIAID data science support. Feedback welcome to refine for FAIRer ecosystem!
