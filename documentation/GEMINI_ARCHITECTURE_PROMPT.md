# Gemini Architecture Generation Prompt

## Project Overview
Generate a comprehensive system architecture diagram and documentation for the **Core Integrator Sprint 1.3** project - a FastAPI-based orchestration platform with advanced security and multi-database support.

## System Description

### Core Purpose
A unified backend bridge that orchestrates requests between multiple AI agents (Finance, Education, Creator) with enterprise-grade security (SSPL Phase III) and multi-database persistence.

### Key Components

#### 1. **API Layer (FastAPI)**
- **Main Application**: `main.py` - FastAPI server with endpoints
- **Core Endpoints**: 
  - `POST /core` - Main processing endpoint (SSPL secured)
  - `GET /get-context` - User context retrieval
  - `GET /system/health` - Health monitoring
  - `GET /system/diagnostics` - System diagnostics
- **Security Middleware**: Optional SSPL Phase III validation

#### 2. **Gateway & Routing**
- **Central Gateway**: `core/gateway.py` - Request routing and processing
- **Agent Management**: Dynamic loading of agents and modules
- **Context Injection**: Memory context provided to all agents
- **Response Normalization**: Standardized response format

#### 3. **Security Layer (SSPL Phase III)**
- **Ed25519 Signatures**: `utils/sspl.py` - Cryptographic validation
- **Nonce Protection**: `db/nonce_store.py` - Replay attack prevention
- **Timestamp Validation**: 5-minute window enforcement
- **Headers Required**: X-SSPL-Timestamp, X-SSPL-Nonce, X-SSPL-Signature, X-SSPL-Public-Key

#### 4. **Multi-Database Architecture**
**Priority Fallback System**:
1. **MongoDB Atlas** (Primary): `db/mongodb_adapter.py` - Cloud database
2. **Noopur Integration** (Secondary): `utils/noopur_client.py` - Remote service
3. **SQLite** (Fallback): `db/memory.py` - Local persistence

**Memory Management**:
- **Context Storage**: Last 5 interactions per user per module
- **Cross-Module Isolation**: Separate contexts for each module
- **Deterministic Retention**: ORDER BY timestamp DESC, id DESC LIMIT 5

#### 5. **Agent System**
**Built-in Agents**:
- **Finance Agent**: `agents/finance.py` - Financial processing
- **Education Agent**: `agents/education.py` - Educational content
- **Creator Agent**: `agents/creator.py` - Content creation with external routing

**Dynamic Modules**:
- **Module Loader**: `core/module_loader.py` - Runtime module discovery
- **Base Module**: `modules/base.py` - Module contract interface
- **Sample Module**: `modules/sample_text/` - Text processing example

#### 6. **External Integrations**
- **Creator Routing**: `creator_routing.py` - External CreatorCore integration
- **Noopur Client**: `utils/noopur_client.py` - Remote memory service
- **MongoDB Atlas**: Cloud database with connection pooling

#### 7. **Observability & Monitoring**
- **Structured Logging**: `utils/logger.py` - JSON formatted logs
- **Health Checks**: Database connectivity, module status
- **Diagnostics**: Memory stats, security status, module info
- **Error Handling**: Comprehensive exception management

#### 8. **Testing Infrastructure**
- **Security Testing**: `test_security_simple.py`, `security_client.py`
- **Database Testing**: `test_mongodb_adapter.py`
- **Integration Tests**: `tests/` directory with comprehensive coverage
- **Load Testing**: Performance validation scripts

### Data Flow Architecture

#### Request Processing Flow:
1. **Request Ingress** → FastAPI endpoint
2. **Security Validation** → SSPL middleware (if enabled)
3. **Gateway Routing** → Central gateway processes request
4. **Context Retrieval** → Memory adapter fetches user context
5. **Agent Processing** → Appropriate agent/module handles request
6. **Response Normalization** → Standardized response format
7. **Context Storage** → Interaction stored in memory
8. **Response Egress** → JSON response to client

#### Database Priority Flow:
1. **MongoDB Atlas** → Primary cloud database
2. **Connection Failure** → Fallback to Noopur (if enabled)
3. **Noopur Failure** → Fallback to SQLite
4. **SQLite** → Always available local persistence

### Configuration Management
- **Environment Variables**: `.env` file with templates
- **Security Settings**: SSPL_ENABLED, timestamp tolerance
- **Database Settings**: Connection strings, database names
- **Module Settings**: Dynamic loading configuration

### Security Architecture
- **Authentication**: Ed25519 public key cryptography
- **Authorization**: Signature validation per request
- **Replay Protection**: Nonce-based with SQLite storage
- **Timestamp Validation**: 5-minute drift tolerance
- **Optional Security**: Can be disabled for testing

### Deployment Architecture
- **Production Ready**: 95%+ test coverage
- **Error Resilience**: Graceful fallbacks at all levels
- **Performance Optimized**: Connection pooling, efficient queries
- **Monitoring**: Health checks, diagnostics, structured logging
- **Scalability**: Modular design, database abstraction

## Architecture Requirements

Please generate:

1. **System Architecture Diagram** showing all components and their relationships
2. **Data Flow Diagram** illustrating request processing pipeline
3. **Database Architecture** showing multi-database fallback system
4. **Security Architecture** detailing SSPL Phase III implementation
5. **Module System Architecture** showing dynamic loading and agent management
6. **Deployment Architecture** with production considerations

## Technical Stack
- **Framework**: FastAPI (Python)
- **Security**: Ed25519 cryptography, SSPL Phase III
- **Databases**: MongoDB Atlas, SQLite, Noopur integration
- **Testing**: pytest, comprehensive test suite
- **Logging**: Structured JSON logging
- **Deployment**: Production-ready with health monitoring

## Key Design Patterns
- **Gateway Pattern**: Central request routing
- **Adapter Pattern**: Multi-database abstraction
- **Strategy Pattern**: Fallback database selection
- **Factory Pattern**: Dynamic module loading
- **Middleware Pattern**: Security validation
- **Observer Pattern**: Logging and monitoring

Generate comprehensive architecture documentation with visual diagrams showing the sophisticated multi-layered system design, security implementation, and database fallback mechanisms.