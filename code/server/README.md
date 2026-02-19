# Server

## About

This is a simple server that provides documents from the data directory in patterns that align to the guidance.  
It was used to test the creation of the client code based on the OpenAPI/Swagger document.   
There is a Go and Python-based version.

It is a simple demo only of no real value.

However, it does demonstrate that those wishing to expose a collection of documents in something like an S3 store or even from a GitHub repository via raw links, how little code is needed.  


## Commands

Running the serer:

```bash
 python main.py 
```


Simple curl commands to test the server:

```bash
curl http://localhost:8080/id/dataset/1     
```

