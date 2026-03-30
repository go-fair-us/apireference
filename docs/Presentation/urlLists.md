# Slides URL index

### **Slide 1: Application Programming Interfaces (APIs)**

### **Slide 2: Hosted By**

  * **Office of Data Science and Emerging Technologies (ODSET):** [https://www.niaid.nih.gov/research/office-data-science-and-emerging-technologies](https://www.niaid.nih.gov/research/office-data-science-and-emerging-technologies)
  * **GO FAIR US (GFU):** [https://www.gofair.us/](https://www.gofair.us/)
  * **NIAID Data Landscaping and FAIRification Project:** [https://www.niaid.nih.gov/research/data-landscaping-project](https://www.niaid.nih.gov/research/data-landscaping-project)

### **Slide 3: ODSET & GFU work with NIAID repositories**

  * **Read the NIAID Blueprint (DOI 10.5281/zenodo.17161561):** [https://doi.org/10.5281/zenodo.17161561](https://doi.org/10.5281/zenodo.17161561)

### **Slide 5: Play along\!**

  * **Colab Link:** [https://colab.research.google.com/github/go-fair-us/apireference/blob/master/code/NIAID\_API\_homeEdition.ipynb](https://colab.research.google.com/github/go-fair-us/apireference/blob/master/code/NIAID_API_homeEdition.ipynb)
  * **GitHub Link:** [https://github.com/go-fair-us/apireference/blob/master/code/NIAID\_API\_homeEdition.ipynb](https://github.com/go-fair-us/apireference/blob/master/code/NIAID_API_homeEdition.ipynb)
  * **Presentation and code details:** [https://github.com/go-fair-us/apireference](https://github.com/go-fair-us/apireference)

### **Slide 8: APIs and the Blueprint**

  * **NIAID Data Blueprint:** [https://www.niaid.nih.gov/research/data-blueprint](https://www.niaid.nih.gov/research/data-blueprint)
  * **Mayer et al. (2025) DOI:** [http://doi.org/10.5281/zenodo.17161561](http://doi.org/10.5281/zenodo.17161561)
  * **Implementation site:** [https://pubweb-prod.niaid.nih.gov/research/data-blueprint](https://pubweb-prod.niaid.nih.gov/research/data-blueprint)

### **Slide 10: The Web, APIs and the Request Response Sequence**

  * **ImmPort API Search URL:** [https://immport.org/data/query/api/search/study?term=influenza%20vaccine\&fromRecord=0\&pageSize=20\&PreTag=%3Cem%3E\&PostTag=%3C%2Fem%3E\&format=json\&sortFieldDirection=asc\&conditionOrDisease=asthma%20COVID-19%27](https://immport.org/data/query/api/search/study?term=influenza%20vaccine&fromRecord=0&pageSize=20&PreTag=%3Cem%3E&PostTag=%3C%2Fem%3E&format=json&sortFieldDirection=asc&conditionOrDisease=asthma%20COVID-19)

  Or, as a curl command:

```bash
curl --request GET   --url 'https://immport.org/data/query/api/search/study?term=influenza%20vaccine&fromRecord=0&pageSize=20&PreTag=%3Cem%3E&PostTag=%3C%2Fem%3E&format=json&sortFieldDirection=asc&conditionOrDisease=asthma%20COVID-19'
```

If you have jq or some other JSON formatter installed, you can pipe these results through that.  

### **Slide 10: The Web, APIs and the Request Response Sequence**

  * **HTTPie:** [https://httpie.io/](https://httpie.io/)
  * **Bruno:** [https://www.usebruno.com/](https://www.usebruno.com/)

### **Slide 12: Web Architecture**

  * **ImmPort example:** [https://www.dev.immport.org/shared/study/SDY2176/summary](https://www.dev.immport.org/shared/study/SDY2176/summary)
  * **validator.schema.org:** [https://validator.schema.org/#url=https%3A%2F%2Fwww.dev.immport.org%2Fshared%2Fstudy%2FSDY2176%2Fsummary](https://validator.schema.org/#url=https%3A%2F%2Fwww.dev.immport.org%2Fshared%2Fstudy%2FSDY2176%2Fsummary)

### **Slide 13: Addressing Addresses**

  * **Cool URIs (W3C):** [https://www.w3.org/Provider/Style/URI](https://www.w3.org/Provider/Style/URI)
  * **Cool URIs for the Semantic Web:** [https://www.w3.org/TR/cooluris/](https://www.w3.org/TR/cooluris/)
  * **Hash URI example:** [http://example.com/about\#alice](http://example.com/about#alice)  

### **Slide 15: APIs Need Versioning**

  * **URI/Path Versioning example:** [https://api.data.niaid.nih.gov/v1/query](https://api.data.niaid.nih.gov/v1/query)
  * **Cadwyn docs:** [https://docs.cadwyn.dev/](https://docs.cadwyn.dev/)
  * **GitHub API versioning:** [https://docs.github.com/en/rest/about-the-rest-api/api-versions?apiVersion=2022-11-28](https://docs.github.com/en/rest/about-the-rest-api/api-versions?apiVersion=2022-11-28)

### **Slide 18: Describe (Document) Your API**

  * **OpenAPI/Swagger Specification:** [https://swagger.io/specification/](https://swagger.io/specification/)
  * **CTG Clients (GitHub):** [https://github.com/go-fair-us/apireference/tree/master/code/clients/CTG](https://github.com/go-fair-us/apireference/tree/master/code/clients/CTG)
  * **IEDB documentation (GitHub):** [https://github.com/go-fair-us/apireference/blob/master/docs/claudDoesIEDB.md](https://github.com/go-fair-us/apireference/blob/master/docs/claudDoesIEDB.md)

### **Slide 19: Fun with Descriptions**

  * **Immport Clients (GitHub):** [https://github.com/go-fair-us/apireference/tree/master/code/clients/Immport](https://github.com/go-fair-us/apireference/tree/master/code/clients/Immport)
  * **Claude Session (GitHub):** [https://github.com/go-fair-us/apireference/blob/master/docs/cluadeSession.md](https://github.com/go-fair-us/apireference/blob/master/docs/cluadeSession.md)

### **Slide 20: A quick Example From the Notebook**

  * **OpenStreetMap Nominatim:** [https://nominatim.openstreetmap.org/ui/search.html](https://nominatim.openstreetmap.org/ui/search.html)
  * **Unofficial OpenAPI:** [https://sparkfabrik.github.io/nominatim-openapi/\#/](https://sparkfabrik.github.io/nominatim-openapi/#/)
  * **Nominatim Search URL:** [https://nominatim.openstreetmap.org/search](https://nominatim.openstreetmap.org/search)

### **Slide 22: NIAID Data Ecosystem Discovery Portal Use of APIs**

  * **NDE Portal:** [https://data.niaid.nih.gov/](https://data.niaid.nih.gov/)
  * **NDE Portal Search Result:** [https://data.niaid.nih.gov/search?q=hasAPI%3Atrue\&filters=%28date%3A%5B%222000-01-01%22+TO+%222026-12-31%22%5D%29](https://data.niaid.nih.gov/search?q=hasAPI%3Atrue&filters=%28date%3A%5B%222000-01-01%22+TO+%222026-12-31%22%5D%29)


  Or, as a curl command on the NDE Portal API:
  
  ```bash
  curl -X 'GET' 'https://api.data.niaid.nih.gov/v1/query?q=hasAPI%3Atrue&facet_size=10&fetch_all=true' -H 'accept: */*'
  ```

### **Slide 23: APIs in NIAID**

  * **EDAM Ontology:** [http://edamontology.org/topic\_0622](http://edamontology.org/topic_0622)
  * **BioPortal EDAM Redirect:** [https://bioportal.bioontology.org/ontologies/EDAM?p=classes\&conceptid=topic\_0622](https://bioportal.bioontology.org/ontologies/EDAM?p=classes%26conceptid=topic_0622)
 
Leveraging the -I flag we can inspect the headers of the response, which can be useful for understanding the content type and other metadata about the resource. This can be particularly helpful when working with APIs that return different formats based on the Accept header or, as in this case, do a redirection.

  ```bash
  curl -I http://edamontology.org/topic_0622                
  ```

### **Slide 24: AI and APIs: The Model Context Protocol (MCP)**

  * **MCP Details (GitHub):** [https://github.com/go-fair-us/apireference/tree/master/docs/mcp](https://github.com/go-fair-us/apireference/tree/master/docs/mcp)

### **Slide 25: MCP? Or, just APIs with descriptions or CLIs?**

  * **BV-BRC CLI Tutorial:** [https://www.bv-brc.org/docs/cli\_tutorial/index.html](https://www.bv-brc.org/docs/cli_tutorial/index.html)
  * **Google Workspace CLI:** [https://github.com/googleworkspace/cli](https://github.com/googleworkspace/cli)
  * **IEDB Swagger:** [https://query-api.iedb.org/docs/swagger/](https://query-api.iedb.org/docs/swagger/)
  * **TBPortals:** [https://analytic.tbportals.niaid.nih.gov/index.html](https://analytic.tbportals.niaid.nih.gov/index.html)
  * **ImmPort Swagger:** [https://immport.org/data/query/swagger-ui/index.html](https://immport.org/data/query/swagger-ui/index.html)
  * **ClinicalTrials Data API:** [https://clinicaltrials.gov/data-api/api](https://clinicaltrials.gov/data-api/api)

### **Slide 29: Acknowledgements**

  * **NIAID Website:** [https://www.niaid.nih.gov/](https://www.niaid.nih.gov/)

