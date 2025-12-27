# System Architecture Diagram - AI Request Enhancement Pipeline

## High-Level Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           SYSTEM ARCHITECTURE LAYERS                                │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                   USER                                              │
│                            (External Entity)                                        │
│                         HTTP/HTTPS Requests                                         │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                               API GATEWAY LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │
│  │   P1: Gateway   │    │  Security       │    │   Request       │                │
│  │   • Routing     │◄──►│  • SSPL Signing │◄──►│   Validation    │                │
│  │   • Load Bal.   │    │  • Nonce Check  │    │   • Auth        │                │
│  │   • Rate Limit  │    │  • Bearer Token │    │   • Schema      │                │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            BUSINESS LOGIC LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │
│  │ P2: Creator     │    │ P3: Noopur      │    │ P6: Enhancement │                │
│  │     Router      │───►│     Client      │───►│   • Context     │                │
│  │ • Context Prep  │    │ • HTTP Client   │    │     Merging     │                │
│  │ • Module Route  │    │ • Auth Headers  │    │ • Data Fusion   │                │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                │
│                                  │                        │                        │
│                                  ▼                        ▼                        │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │
│  │ P7: Memory      │    │ P8: Agent       │    │   Response      │                │
│  │     Storage     │◄───│     Response    │◄───│   Formatter     │                │
│  │ • Interaction   │    │ • Business      │    │ • JSON Serial   │                │
│  │   Logging       │    │   Logic         │    │ • Status Codes  │                │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              AI PROCESSING LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │
│  │ P4: Noopur      │    │ P5: AI          │    │   ML Pipeline   │                │
│  │     Backend     │───►│     Similarity  │───►│ • Transformers  │                │
│  │ • Flask App     │    │ • Cosine Dist   │    │ • Embeddings    │                │
│  │ • AI Endpoints  │    │ • Score Ranking │    │ • Vector Ops    │                │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                │
│           │                        │                        │                      │
│           ▼                        ▼                        ▼                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                        AI MODEL COMPONENTS                                  │  │
│  │  • Sentence Transformers (all-MiniLM-L6-v2)                               │  │
│  │  • NumPy Vector Operations                                                 │  │
│  │  • SciPy Cosine Distance Calculation                                      │  │
│  │  • Embedding Generation & Storage                                         │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              DATA PERSISTENCE LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │
│  │ DS1: Noopur     │    │ DS2: Core       │    │ DS3: MongoDB    │                │
│  │     SQLite      │    │     Integrator  │    │     Atlas       │                │
│  │ • AI Embeddings │    │ • User Context  │    │ • Cloud Storage │                │
│  │ • Generated     │    │ • Interactions  │    │ • Primary Data  │                │
│  │   Content       │    │ • Fallback Mem  │    │ • Scalability   │                │
│  │ • Similarity    │    │ • Local Cache   │    │ • Replication   │                │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                │
│           │                        │                        │                      │
│           ▼                        ▼                        ▼                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                         DATABASE OPERATIONS                                 │  │
│  │  • SQLAlchemy ORM • Transaction Management • Connection Pooling            │  │
│  │  • Embedding BLOB Storage • Vector Similarity Queries • Cloud Sync        │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## Component Interaction Matrix

| Component | Interacts With | Data Exchange | Protocol |
|-----------|----------------|---------------|----------|
| **User** | P1: Gateway | JSON Request/Response | HTTPS |
| **P1: Gateway** | P2: CreatorRouter | Internal Python Objects | Function Calls |
| **P2: CreatorRouter** | P3: NoopurClient | Prepared Context Dict | Method Invocation |
| **P3: NoopurClient** | P4: Noopur Backend | HTTP JSON Payload | REST API |
| **P4: Noopur Backend** | DS1: SQLite | SQL Queries, Embeddings | SQLAlchemy ORM |
| **DS1: SQLite** | P5: AI Similarity | Vector Arrays | NumPy/SciPy |
| **P5: AI Similarity** | P6: Enhancement | Ranked Context List | Python Objects |
| **P6: Enhancement** | P7: Memory Storage | Enhanced JSON | Internal Transfer |
| **P7: Memory Storage** | DS2: Core DB | Interaction Logs | SQLite Insert |
| **P7: Memory Storage** | P8: Agent Response | Final Data | Python Dict |
| **P8: Agent Response** | User | Business Response | JSON over HTTPS |

## Technology Stack Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              TECHNOLOGY STACK                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  Frontend/Client          │  Backend Services        │  AI/ML Components           │
│  ─────────────────        │  ─────────────────       │  ─────────────────          │
│  • HTTP Clients           │  • Flask/FastAPI         │  • Sentence Transformers    │
│  • REST API Consumers     │  • Python 3.14+          │  • NumPy/SciPy             │
│  • JSON Processors        │  • SQLAlchemy ORM        │  • Cosine Similarity       │
│                           │  • Requests Library      │  • Vector Operations        │
│                           │                          │                             │
│  Security Layer           │  Database Layer          │  Infrastructure             │
│  ─────────────────        │  ─────────────────       │  ─────────────────          │
│  • SSPL Middleware        │  • SQLite (Local)        │  • MongoDB Atlas (Cloud)   │
│  • Bearer Token Auth      │  • MongoDB (Cloud)       │  • Connection Pooling      │
│  • Nonce Protection       │  • Connection Pooling    │  • Auto-scaling            │
│  • HTTPS/TLS              │  • Transaction Mgmt      │  • Load Balancing          │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            DEPLOYMENT TOPOLOGY                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │
│  │   Load Balancer │    │  Core Integrator │    │  Noopur Service │                │
│  │   (Optional)    │───►│   Gateway        │───►│  (localhost:    │                │
│  │   • Nginx       │    │   (Main App)     │    │   5001)         │                │
│  │   • HAProxy     │    │   • Port 8000    │    │   • Flask App   │                │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                │
│                                   │                        │                        │
│                                   ▼                        ▼                        │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │
│  │  Local SQLite   │    │  MongoDB Atlas  │    │   AI Models     │                │
│  │  • context.db   │    │  • Cloud DB     │    │   • Transformers│                │
│  │  • nonce.db     │    │  • user1:user1  │    │   • Embeddings  │                │
│  │  • noopur.db    │    │  • Replication  │    │   • Cached      │                │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## Performance & Scalability Metrics

| Metric | Current Value | Scalability Target |
|--------|---------------|-------------------|
| **Response Time** | 100-500ms | <200ms |
| **Concurrent Users** | 10-50 | 1000+ |
| **Database Ops/sec** | 100 | 10,000+ |
| **AI Processing** | 1 req/sec | 100 req/sec |
| **Memory Usage** | 512MB | 2GB |
| **Storage Growth** | 1MB/day | 1GB/day |

## System Capabilities Summary

✅ **Multi-Layer Architecture** - Separation of concerns  
✅ **AI-Enhanced Processing** - Sentence transformers integration  
✅ **Hybrid Database Strategy** - Local + Cloud storage  
✅ **Enterprise Security** - SSPL + Bearer token authentication  
✅ **Scalable Design** - Microservices-ready architecture  
✅ **Real-time Processing** - Sub-second response times  
✅ **Comprehensive Logging** - Full request/response tracking