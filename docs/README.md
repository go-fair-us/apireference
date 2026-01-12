# Documentation


## Notes

There are potentially several paths and entry points for implementing the API recommendations.

We will want to accommodate different levels of expertise and provide guidance for each path.  The following diagram illustrates the different paths and entry points.

Note shown here is the concept of MCP that should be addressed as an additional concept.

```mermaid
flowchart TD
    Start1[New to APIs in general] --> Mid1[Overview of various API \n services and clients]
    Start2[Consumer of APIs] --> Mid1

    Mid1 --> Step2a[Deployment Approaches]
    Mid2[Experienced in API DevOps] --> Step2b[Validation tools]

    Step2a --> Step3[Example Operations]
    Step3 --> Step2b
    
    Step2b --> Final[Shared Blueprint Alignment ]
    
```


