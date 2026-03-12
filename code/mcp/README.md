# MCP


## What is it?

The Model Context Protocol (MCP), introduced by Anthropic in November 2024, is an open-standard, open-source framework designed to standardize how AI systems, particularly large language models (LLMs), connect with external tools, data sources, and systems. Sometimes referred to as a "USB-C" for AI.

Note that MCP is not an API specification, it is a wire protocol, in this case JSON-RPC 2.0. It can work locally via standard IO (stdio) or over http.

Some examples from the community:

* ClinicalTrials: https://github.com/cyanheads/clinicaltrialsgov-mcp-server
* BioMCP  https://biomcp.org/   (PubMed, ClinicalTrials.gov, and MyVariant.info and more)   This is a master class on MCP!
* Cracking Shells  https://github.com/CrackingShells  I have a few issues with this one on first review
* BioThings https://github.com/longevity-genie/biothings-mcp  genes, genetic variants, drugs, and taxonomic information
* BioPortal MCP:  https://github.com/ncbo/bioportal-mcp
* Biomni  (impressive) https://biomni.stanford.edu
* Gget: https://github.com/longevity-genie/gget-mcp  genomics queries and analysis, a wrapper of gget library (which I know nothing about)
* OpenGenes https://github.com/longevity-genie/opengenes-mcp
* SynerAge https://github.com/longevity-genie/synergy-age-mcp


## Convention

| Method         | Description                                                                                  |
|----------------|----------------------------------------------------------------------------------------------|
| initialize     | The first message sent. The server must return its capabilities (tools, resources, prompts). |
| resources/list | Returns a list of available data objects the model can read.                                 |
| resources/read | Triggered when the model wants the content of a specific URI.                                |
| tools/list     | Returns a list of executable functions the server provides.                                  |
| tools/call     | The actual execution of a tool with provided arguments.                                      |
| prompts/list   | Returns pre-defined templates for interacting with the model.                                |


## Why not just use APIs (OpenAPI?)

* OpenAPI describes; MCP prescribes. You can't fix inconsistency by documenting it better—you need enforcement at the protocol level.
* Retrofitting fails at scale. OpenAPI would need to standardize transport, mandate single-location inputs, require specific schemas, add bidirectional primitives—essentially becoming a different protocol.
* The ecosystem problem. Even if OpenAPI added these features tomorrow, millions of existing APIs wouldn't adopt them. MCP starts fresh with AI-first principles.

Unlike static API specs, MCP enables agents to query capabilities dynamically, allowing automatic adaptation without new client code.

MCP supports first-class bidirectional flows (e.g., progress updates, clarifications), which are not standard in APIs.

## How to try it

https://github.com/modelcontextprotocol/inspector
```bash
npx @modelcontextprotocol/inspector uvx

```

There are several tools that are starting to enable client connections to MCP servers.  Many developed IDEs like VS-code/Cline, Zed and IntelliJ software can be MCP clients and in some cases are MCP servers too.

Also, tools like Gemini-CLI and Claude-Cli or web-based tools like LibreChat can interact with MCP.   We will use Gemini-CLI and LibreChat here for our examples.

## Demo

I coded up a simple MCP over one of the BVBRC APIs.   I know Kevin has set up an MCP too over an API.  Doing an API gateway with MCP is not the gold standard of MCP, of course.   But it's quick and dirty and mostly what you see going on with this set.

it looks like:

[AI Agent] ⟷ MCP Client ⟷ MCP Server ⟷ REST API ⟷ Service

Later, as people start to leverage MCP for what it can really do, it will get more impressive.

That would be like

[AI Agent] ⟷ MCP Client ⟷ MCP Server ⟷ Service


* BioMCP
* NDE MCP ?
* BVBRC MCP


## Bio Examples



## Other Bio MCP References

* BioMCP  https://biomcp.org/   (PubMed, ClinicalTrials.gov, and MyVariant.info and more)   This is a master class on MCP!
* Cracking Shells  https://github.com/CrackingShells  I have a few issues with this one on first review
* BioThings https://github.com/longevity-genie/biothings-mcp  genes, genetic variants, drugs, and taxonomic information
* BioPortal MCP:  https://github.com/ncbo/bioportal-mcp
* Biomni  (impressive, not MCP and you need to request access) https://biomni.stanford.edu
* Gget: https://github.com/longevity-genie/gget-mcp  genomics queries and analysis, a wrapper of `gget` library (which I know nothing about)
* OpenGenes https://github.com/longevity-genie/opengenes-mcp
* SynerAge https://github.com/longevity-genie/synergy-age-mcp

* https://github.com/tnnandi/agentic_lab
* https://sysbio-curie.github.io/Neko
* https://maboss.curie.fr
* https://physicell.org


## Demo

> I'll convert this to a screencast

So I set up a couple MCP servers with Gemini-CLI. Once I coded up which is a simple one to expose a single BVBRC API via MCP.  The other is an open source bio-related MCP that, among other things, has a pubmed API proxy.

My interaction was interesting and follows

Question asked:
> can you give me synonyms for Synercid using the bvbrc tools

Answer:
```
✦ The synonyms for Synercid are: quinupristin-dalfopristin, RP 59500, and RP-59500.
```
Questions asked:
>  look for articles on these synonyms

Answer
```
✦ I found several articles mentioning "quinupristin-dalfopristin". The majority of these are research papers focusing on antibiotic resistance in various
  bacteria, particularly Enterococcus species. Several articles discuss the effectiveness of quinupristin-dalfopristin against multi-drug resistant organisms.
  Would you like me to refine the search with more specific keywords or filter by publication date?
```

55 results were found  (I truncated the output here.  as it was long with the abstract for each returned

Question asked:
> can you take the most recent three articles and summarize them?  Also note where they agree and diverge


Answer:
```
✦ Here is a summary of the two most recent articles with available abstracts, noting their points of agreement and divergence. The most recent article was a
  preprint and did not have an abstract, so I have summarized the next two most recent articles.
  Summaries
  1. "Comparison of Two Quinupristin-dalfopristin Susceptibility Testing Methods and Two Interpretive Criteria for Enterococcus faecium Bloodstream Isolates from
  Korean Hospitals."
  This Korean study from April 2025 focuses on the practical aspects of laboratory testing for quinupristin-dalfopristin (Q/D) resistance in Enterococcus
  faecium. The researchers compared two common testing methods—disk diffusion (DD) and broth microdilution (Sensititre)—and two different interpretive standards
  (EUCAST and CLSI). They found that the reported resistance rates for Q/D varied significantly depending on the combination of method and standard used, ranging
   from 5.9% to 28.2%. The study concludes that for the DD method, the EUCAST criteria are more effective at identifying resistance, while for the Sensititre
  method, the CLSI criteria are more reliable. The most common resistance genes found in the Q/D-resistant isolates were ermB and msrC. The goal is to help
  clinicians make better treatment decisions for multidrug-resistant E. faecium infections.
  2. "A comprehensive One Health investigation of erythromycin and quinupristin/dalfopristin resistant Enterococcus spp. in Iran."
  This Iranian study from April 2025 takes a broader "One Health" approach to investigate antibiotic resistance. The researchers looked for resistance to
  erythromycin and Q/D in Enterococcus species from a wide range of sources, including patients, healthy people, hospital environments, livestock, poultry, and
  wastewater. They found that while no isolates were resistant to linezolid, 24.9% of E. faecium isolates were resistant to Q/D. This resistance was
  particularly high in isolates from patients and poultry slaughterhouse wastewater. Similar to the Korean study, the most common resistance genes identified
  were msrC and ermB. The study concludes that the widespread presence of erythromycin- and Q/D-resistant enterococci in various environments poses a
  significant public health risk.
  Agreement and Divergence
  Agreement:
   * Focus on *E. faecium*: Both studies identify Enterococcus faecium as a key pathogen of concern regarding quinupristin-dalfopristin resistance.
   * Genetic Basis of Resistance: Both the Korean and Iranian studies found that the ermB and msrC genes were the primary genetic determinants responsible for Q/D
     resistance.
   * Clinical Relevance: Both articles underscore the clinical challenge posed by multidrug-resistant Enterococcus and the importance of accurate susceptibility
     testing to guide treatment.
  Divergence:
   * Scope and Approach: The Korean study has a narrow, methodological focus, comparing laboratory techniques to improve clinical diagnostics. In contrast, the
     Iranian study has a broad, epidemiological "One Health" scope, examining the prevalence of resistance across different human, animal, and environmental
     reservoirs.
   * Primary Goal: The Korean paper aims to provide guidance to clinical laboratories on which testing methods and criteria are most reliable. The Iranian paper
     aims to highlight the interconnectedness of antibiotic resistance between different sectors and warn of a public health threat.
   * Geographic Focus: The studies were conducted in different countries (South Korea vs. Iran), and the specific resistance rates they report reflect local
     epidemiology and antibiotic usage patterns.
   * Reported Resistance Rates: While the resistance rates are in a similar range, they are not identical. The Korean study's reported Q/D resistance in E.
     faecium fluctuated from 5.9% to 28.2% based on the testing method, while the Iranian study found a rate of 24.9%. This difference is expected due to the
     different populations and methodologies.

```

Anyway, a simple and fun interaction with a couple MCP tools mediated by Gemini-CLI


## References

* https://modelcontextprotocol.io/docs/getting-started/intro
* https://claude.com/resources/tutorials/using-the-clinicaltrials-gov-connector-in-claude 
