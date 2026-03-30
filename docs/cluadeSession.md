#  ImmPort OpenAPI and CLI clients



```
 ▐▛███▜▌   Claude Code v2.1.5
▝▜█████▛▘  Opus 4.5 · Claude Team
  ▘▘ ▝▝    ~/src/Projects/NIAID/apireference

❯ review https://immport.org/data/query/v3/api-docs and see which services could be used without authentication and can provide information on TB studies

● I'll fetch the ImmPort API documentation to review the available services.

● Fetch(https://immport.org/data/query/v3/api-docs)
  ⎿  Received 286.3KB (200 )

● Let me explore the API further by testing the unauthenticated endpoints to find TB studies.

● Fetch(https://immport.org/data/query/v3/api/lookup/lkDisease)
  ⎿  Error: Request failed with status code 404

● Fetch(https://immport.org/data/query/v3/api/search/study?searchTerm=tuberculosis)
  ⎿  Error: Request failed with status code 404

● Let me try to get the OpenAPI specification in JSON format to understand the exact endpoint structure.

● Fetch(https://immport.org/data/query/v3/api-docs/)
  ⎿  Received 286.3KB (200 )

● Fetch(https://immport.org/data/query/api-docs)
  ⎿  Error: Request failed with status code 401

● Let me try the correct endpoint paths.

● Fetch(https://immport.org/data/query/api/search/study?searchTerm=tuberculosis)
  ⎿  Received 79.4KB (200 )

● Fetch(https://immport.org/data/query/api/lookup/lkDisease)
  ⎿  Received 123.5KB (200 )

● Let me search for more TB-related studies using "mycobacterium" and check available facets.

● Fetch(https://immport.org/data/query/api/search/study?searchTerm=mycobacterium)
  ⎿  Received 79.4KB (200 )

● Fetch(https://immport.org/data/query/api/lookup/lkResearchFocus)
  ⎿  Received 5.2KB (200 )

● Let me try filtering by condition to get the full count of TB studies.

● Fetch(https://immport.org/data/query/api/search/study?conditionOrDisease=tuberculosis)
  ⎿  Received 80.4KB (200 )

● ImmPort API Services for TB Studies (No Authentication Required)

  Based on my review of the ImmPort API at https://immport.org/data/query/v3/api-docs, here's what you can access without authentication:

  Unauthenticated Endpoints
  ┌─────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────┐
  │            Endpoint             │                                 Description                                  │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ GET /api/search/study           │ Full-text search with faceted filters (condition, species, research focus)   │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ GET /api/search/subject         │ Search subjects by demographics, assay methods, biosample types              │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ GET /api/lookup/lkDisease       │ Controlled vocabulary for diseases (includes DOID:399 - Tuberculosis)        │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ GET /api/lookup/lkResearchFocus │ Research focus areas (Infection Response, Immune Response, Vaccine Response) │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ 30+ additional lookup endpoints │ Species, sample types, assay methods, etc.                                   │
  └─────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────┘
  TB Studies Available

  There are 33 tuberculosis studies accessible via public search. Key examples:
  ┌───────────┬──────────────────────────────────────────────────────────────────────────────┬─────────────────────────────────┐
  │ Accession │                                    Title                                     │              Notes              │
  ├───────────┼──────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────┤
  │ SDY2977   │ Antibody-Fab and -Fc features promote Mycobacterium tuberculosis restriction │ IMPAc-TB Center                 │
  ├───────────┼──────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────┤
  │ SDY1381   │ Host Determinants Of Protection Against Tuberculosis In Adolescents          │ 150 South African adolescents   │
  ├───────────┼──────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────┤
  │ SDY1446   │ Comparing aerosol and intradermal boost regimes of MVA85A                    │ Clinical trial, 37 participants │
  ├───────────┼──────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────┤
  │ SDY2268   │ Immune cells in BAL fluid - resisters vs. infected (Uganda)                  │ Human subjects                  │
  ├───────────┼──────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────┤
  │ SDY2942   │ Intravenous BCG vaccination in rhesus macaques                               │ Animal model                    │
  ├───────────┼──────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────┤
  │ SDY3410   │ BCG vaccination induces effector functions in Vdelta1/3 T cells              │ Recent (March 2026)             │
  └───────────┴──────────────────────────────────────────────────────────────────────────────┴─────────────────────────────────┘
  Example Queries (No Auth)

  # Search TB studies
  curl "https://immport.org/data/query/api/search/study?searchTerm=tuberculosis"

  # Filter by condition
  curl "https://immport.org/data/query/api/search/study?conditionOrDisease=tuberculosis"

  # Get disease vocabulary
  curl "https://immport.org/data/query/api/lookup/lkDisease"

  What Requires Authentication

  - Detailed study data (demographics, biosamples, experiments)
  - Result data (PCR, ELISA, HAI, HLA typing)
  - File downloads and manifests
  - DRS download endpoints

✻ Brewed for 1m 26s
```

Second requestion


```

❯ can you get me details on SDY3410
● Fetch(https://immport.org/data/query/api/search/study?searchTerm=SDY3410)                                                                                                                                   ⎿  Received 79.4KB (200 )
                                                                                                                                                                                                            ● Fetch(https://immport.org/data/query/api/study/SDY3410)
  ⎿  Error: Request failed with status code 401
● The detailed study endpoint requires authentication. Let me try different search approaches.
● Fetch(https://immport.org/data/query/api/search/study?conditionOrDisease=tuberculosis&pageSize=50)                                                                                                          ⎿  Received 137.7KB (200 )
                                                                                                                                                                                                            ● Fetch(https://immport.org/shared/study/SDY3410)
  ⎿  Received 17.1KB (200 )
● I found the details. Let me also check for any associated publications.
● pubmed - Search articles (MCP)(query: "BCG vaccination Vdelta1 Vdelta3 T cells tuberculosis protection", max_results: 5)                                                                                    ⎿  Error: Streamable HTTP error: Error POSTing to endpoint: {"error":"Session not found","message":"Session ID 'e9fa6e24-abac-4b78-8a97-78b42ca258fe' does not exist. Please initialize a new session
     first."}

● Web Search("BCG vaccination Vdelta1 Vdelta3 T cells tuberculosis protection Megan Maerz publication 2025 2026")
  ⎿  Did 1 search in 18s

● Study SDY3410 - Full Details

  Basic Information
  ┌────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │     Field      │                                                                 Value                                                                 │
  ├────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Accession      │ SDY3410                                                                                                                               │
  ├────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Title          │ BCG vaccination induces antibacterial effector functions among Vδ1/3 T cells that are associated with protection against tuberculosis │
  ├────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ DOI            │ https://doi.org/10.21430/M3TM9Y230F                                                                                                   │
  ├────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Program        │ Immune Mechanisms of Protection Against Mycobacterium tuberculosis Center (IMPAc-TB)                                                  │
  ├────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Research Focus │ Immune Response                                                                                                                       │
  ├────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Condition      │ Tuberculosis                                                                                                                          │
  ├────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Study Type     │ Non-clinical trial                                                                                                                    │
  ├────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ PI             │ Megan Maerz, University of Washington                                                                                                 │
  ├────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Data Release   │ DR62 (March 26, 2026)                                                                                                                 │
  └────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
  Study Description

  This study examines how γδ T cells expressing Vδ1/3 receptors respond to BCG vaccination. Researchers used:
  - Multimodal single-cell RNA sequencing
  - Mass cytometry
  - Flow cytometry

  to profile these cells from human infants and macaques.

  Key Findings

  1. Vδ1/3 T cells in BCG-vaccinated human infants show clonal expansion and differentiation into Mtb-reactive cytotoxic effector cells
  2. In macaques, intravenous BCG induces pro-inflammatory and cytotoxic responses among Vδ1/3 T cells enriched in the airway
  3. Cytokine-producing Vδ1/3 T cells in the airway correlate with protection against tuberculosis

  Associated Publication

  Cell Reports Medicine (2026 Jan 20;7(1):102536)

  - Authors: Megan D. Maerz et al. (University of Washington, NIH Vaccine Research Center)
  - Publication DOI: https://doi.org/10.1016/j.xcrm.2025.102536
  - PMID: https://pubmed.ncbi.nlm.nih.gov/41529694/
  - PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC12866138/

  Access Limitations

  Detailed data (biosamples, assay results, subject demographics) requires ImmPort authentication. The public search endpoint provides only metadata.

  Sources:
  - https://pubmed.ncbi.nlm.nih.gov/41529694/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC12866138/
  - https://www.sciencedirect.com/science/article/pii/S2666379125006093

✻ Brewed for 1m 4s
```