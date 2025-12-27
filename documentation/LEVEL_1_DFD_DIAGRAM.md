# Level 1 Data Flow Diagram (DFD) - AI Request Enhancement Pipeline

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    AI REQUEST ENHANCEMENT PIPELINE - LEVEL 1 DFD                    │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────┐    Simple JSON           ┌──────────────┐    Routed Request
│  USER   │ ──────────────────────► │ P1: Gateway  │ ─────────────────────►
│(External│    {topic, goal, type}   │   (Security  │
│ Entity) │                          │   & Routing) │
└─────────┘                          └──────────────┘
     ▲                                        │
     │                                        ▼
     │ Final Enhanced JSON            ┌──────────────┐    Prepared Context
     │ {topic, goal, type,            │P2: Creator   │ ─────────────────────►
     │  related_context[...]}         │   Router     │
     │                                │ (Context     │
     │                                │  Prep)       │
     │                                └──────────────┘
     │                                        │
     │                                        ▼
┌──────────────┐    Enhanced JSON     ┌──────────────┐    Secure HTTP Call
│P8: Agent     │ ◄─────────────────── │P3: Noopur    │ ─────────────────────►
│   Response   │                      │   Client     │   [SSPL + Bearer Token]
│ (Final       │                      │ (HTTP Call)  │
│  Format)     │                      └──────────────┘
└──────────────┘                              │
     ▲                                        ▼
     │                                ┌──────────────┐
     │ Enhanced JSON                  │P4: Noopur    │
     │                                │   Backend    │ ◄──────────────────────┐
┌──────────────┐    AI-Enhanced       │   (AI Core)  │                        │
│P7: Memory    │ ─────────────────────►│ • Sentence   │                        │
│   Storage    │    Request JSON      │   Transformers│                        │
│ (Logging)    │                      │ • Embedding   │                        │
└──────────────┘                      │   Generation │                        │
     │                                └──────────────┘                        │
     ▼                                        │                                │
┌──────────────┐                             ▼                                │
│DS2: Core     │                     ┌──────────────┐    Embedding Query      │
│Integrator DB │                     │DS1: Noopur   │ ◄──────────────────────┘
│• User        │                     │SQLite DB     │
│  Interactions│                     │• AI          │
│• Fallback    │                     │  Embeddings  │
│  Memory      │                     │• Generated   │
└──────────────┘                     │  Content     │
                                     │• Similarity  │
                                     │  Matching    │
                                     └──────────────┘
                                             │
                                             ▼ Similar Embeddings/Content
                                     ┌──────────────┐
                                     │P5: AI        │
                                     │   Similarity │
                                     │• Cosine      │
                                     │  Distance    │
                                     │• Ranking     │
                                     │• Score Norm  │
                                     └──────────────┘
                                             │
                                             ▼ Generated Text + Context
                                     ┌──────────────┐
                                     │P6: Enhancement│
                                     │ (Context     │
                                     │  Merging)    │
                                     └──────────────┘
                                             │
                                             ▼ AI-Enhanced Request JSON
                                     ┌──────────────┐
                                     │DS3: MongoDB  │
                                     │   Atlas      │
                                     │• Cloud       │
                                     │  Storage     │
                                     │• Primary     │
                                     │  User Data   │
                                     └──────────────┘
```

## Data Flow Specifications

### External Entities
| Entity | Description |
|--------|-------------|
| **USER** | Initiates requests and receives AI-enhanced responses |

### Processes (P1-P8)
| Process | Name | Function | Technology |
|---------|------|----------|------------|
| **P1** | Gateway | Request routing, security validation | Flask/FastAPI, SSPL |
| **P2** | CreatorRouter | Context preparation, module routing | Python, NoopurClient |
| **P3** | NoopurClient | Secure HTTP communication | Requests, Bearer Auth |
| **P4** | Noopur Backend | AI processing, embedding generation | Flask, Sentence Transformers |
| **P5** | AI Similarity | Cosine distance calculation, ranking | NumPy, SciPy |
| **P6** | Enhancement | Context merging with original request | Python Dict Operations |
| **P7** | Memory Storage | Interaction logging, persistence | SQLAlchemy, MongoDB |
| **P8** | Agent Response | Final business response formatting | JSON Serialization |

### Data Stores (DS1-DS3)
| Store | Name | Content | Technology |
|-------|------|---------|------------|
| **DS1** | Noopur SQLite DB | AI embeddings, generated content, similarity data | SQLite, SQLAlchemy |
| **DS2** | Core Integrator DB | User interactions, fallback memory, context | SQLite |
| **DS3** | MongoDB Atlas | Cloud storage, primary user/application data | MongoDB Cloud |

### Data Flows
| Flow | From → To | Data Format | Security |
|------|-----------|-------------|----------|
| 1 | User → P1 | `{"topic": "AI", "goal": "tutorial", "type": "article"}` | HTTPS |
| 2 | P1 → P2 | Routed request with user_id, module, intent | Internal |
| 3 | P2 → P3 | Prepared context payload | Internal |
| 4 | P3 → P4 | HTTP POST with JSON payload | SSPL + Bearer Token |
| 5 | P4 → DS1 | Embedding vectors, generated text | SQLite Transaction |
| 6 | DS1 → P5 | Similar embeddings array | SQL Query Result |
| 7 | P5 → P6 | `{"generated_text": "...", "related_context": [...]}` | Internal |
| 8 | P6 → P7 | Enhanced request with AI context | Internal |
| 9 | P7 → DS2 | Logged interaction record | SQLite Insert |
| 10 | P7 → P8 | Enhanced JSON for response | Internal |
| 11 | P8 → User | `{"status": "success", "result": {...}}` | HTTPS JSON |

## Security Layers
```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: HTTPS/TLS Encryption                              │
│ Layer 2: SSPL Request Signing & Validation                 │
│ Layer 3: Nonce Replay Attack Prevention                    │
│ Layer 4: Bearer Token Authentication                       │
│ Layer 5: Database Connection Security                      │
└─────────────────────────────────────────────────────────────┘
```

## AI Processing Pipeline
```
┌─────────────────────────────────────────────────────────────┐
│                   AI ENHANCEMENT PIPELINE                   │
├─────────────────────────────────────────────────────────────┤
│ Input Text → Sentence Transformers → Vector Embedding      │
│ Embedding → Cosine Similarity → Related Content Matching   │
│ Similarity Scores → Normalization → Ranked Context         │
│ Original Request + AI Context → Enhanced Response          │
└─────────────────────────────────────────────────────────────┘
```

## Performance Metrics
- **Total Processing Time**: 100-500ms
- **AI Model**: all-MiniLM-L6-v2 (Sentence Transformers)
- **Database Operations**: 3 concurrent (SQLite + MongoDB)
- **Context Items**: Top 3 similar matches
- **Similarity Algorithm**: Cosine Distance (70%) + Score Normalization (30%)

## System Capabilities
✅ **AI-Powered Context Awareness**  
✅ **Multi-Database Architecture**  
✅ **Enterprise Security (SSPL)**  
✅ **Real-time Similarity Matching**  
✅ **Scalable Cloud Integration**  
✅ **Comprehensive Logging & Memory**