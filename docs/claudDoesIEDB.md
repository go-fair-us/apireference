# Claud and IEDB

Can you locate the IEDB.org swagger document and see if there is a call you can make for the epitope SLYNTVATL.   I would want every possible parameter it can return.

---

Now let me fetch the actual OpenAPI/Swagger spec JSON from the query API to see all available fields:The Swagger UI is JavaScript-rendered and the content isn't accessible via fetch. Let me try the raw OpenAPI spec endpoint directly:Now I have enough information to construct the full API call. Let me also fetch the PDF slides that show the full field list:Now I have everything I need. Let me also look at the GitHub use cases to get the full field list:I now have a thorough picture of the IEDB IQ-API. Let me build a comprehensive interactive artifact showing the API call and all available fields for SLYNTVATL:Here's a full breakdown of what I found in the IEDB IQ-API Swagger/OpenAPI spec for the epitope SLYNTVATL.

**About the API**: The IQ-API is built on a PostgREST platform that exposes each database table as a separate endpoint, described interactively at `https://query-api.iedb.org/docs/swagger/`.

**The primary query for SLYNTVATL** uses `eq.` (equals) on the `linear_sequence` field:

```
GET https://query-api.iedb.org/epitope_search?linear_sequence=eq.SLYNTVATL
```

The explorer above covers all six endpoints relevant to this epitope across five tabs:

**Epitope tab** — the core `epitope_search` endpoint returns identity fields (`structure_id`, `structure_iri`, `linear_sequence`), source antigen and organism data (both "curated" per-publication and "parent" reference-proteome grouped), and aggregate assay counts broken out by type and positivity.

**T cell tab** — `tcell_search` returns one row per assay, including the effector cell type, APC type, MHC allele restriction (crucial for SLYNTVATL, which is canonically HLA-A\*02:01 restricted), qualitative/quantitative measurements, assay type, host organism, disease context, and the linked PubMed/reference ID.

**B cell tab** — `bcell_search` with the same `linear_sequence=eq.SLYNTVATL` filter. SLYNTVATL is primarily a CTL epitope so B cell results are likely sparse.

**MHC ligand tab** — `mhc_search` returns binding affinity data including IC50/Kd values, alleles tested, and assay type (competitive binding, elution, etc.).

**Reference and Antigen tabs** — these use the array-contains operator `cs.{}` instead of `eq.`, since one reference or antigen record can contain multiple epitopes.

You can use `select=field1,field2` to limit which columns are returned, and by default results come back as JSON, but adding `-H "accept: text/csv"` returns TSV format instead. The "Try a live query via Claude" button in the widget will ask me to actually call the endpoint and show you the raw JSON if you want to see the live data.