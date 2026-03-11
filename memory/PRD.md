# TA Engine PRD - PHASE 13.1 Alpha Node Registry

## Original Problem Statement
TA Engine - Institutional-grade quant trading platform. Building autonomous Alpha Factory for systematic signal generation. PHASE 13.1 implements Alpha Node Registry as foundation for Feature Library, Alpha Graph, and Alpha DAG.

## Architecture Overview
```
backend/
├── core/
│   └── database/              # Unified MongoDB Connection
│       ├── __init__.py
│       └── mongo.py           # Singleton MongoClient, MongoRepository
├── modules/
│   ├── alpha_factory/         # PHASE 13.1 ✅
│   │   ├── alpha_types.py     # Node types, AlphaNode dataclass
│   │   ├── alpha_node_registry.py  # Central registry
│   │   ├── alpha_repository.py     # MongoDB persistence
│   │   └── alpha_routes.py    # API endpoints
│   └── [other modules...]
├── datasets/                  # Historical data (BTC, SPX, DXY)
└── server.py                  # FastAPI application
```

## What's Been Implemented

### PHASE 13.1 — Alpha Node Registry (2026-03-11) ✅
**Core Features:**
- Node Schema with 9 types: alpha, structure, liquidity, microstructure, context, correlation, portfolio, feature, factor
- MongoDB persistence with indexes
- CRUD API endpoints
- **89 nodes registered** (exceeds 50+ requirement)
- Stats and search endpoints
- DAG-ready design (inputs/outputs)
- Graph-ready design (supports/contradicts/amplifies)

**Node Breakdown:**
| Type | Count | Examples |
|------|-------|----------|
| alpha | 15 | trend_strength, breakout_pressure, volatility_compression |
| structure | 6 | bos, choch, swing_high, swing_low |
| liquidity | 9 | stop_cluster, liquidation_zone, liquidity_wall |
| microstructure | 7 | buyer_aggression, seller_aggression, flow_pressure |
| context | 8 | funding_extreme, oi_expansion, macro_risk_on |
| correlation | 5 | btc_spx_correlation, btc_dxy_inverse |
| portfolio | 4 | drawdown_state, risk_budget, portfolio_health |
| feature | 22 | price_returns, rsi, atr, macd, volume_sma |
| factor | 12 | trend_momentum_factor, entry_quality_factor |

**API Endpoints:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/alpha-factory/health` | GET | Health check |
| `/api/alpha-factory/stats` | GET | Registry statistics |
| `/api/alpha-factory/nodes` | GET | List all nodes (filterable) |
| `/api/alpha-factory/nodes/{id}` | GET | Get specific node |
| `/api/alpha-factory/nodes` | POST | Create new node |
| `/api/alpha-factory/nodes/{id}` | PUT | Update node |
| `/api/alpha-factory/nodes/{id}` | DELETE | Deprecate node |
| `/api/alpha-factory/nodes/types` | GET | Get node types breakdown |
| `/api/alpha-factory/nodes/search` | GET | Search nodes |
| `/api/alpha-factory/nodes/{id}/relationships` | GET | Get node relationships |
| `/api/alpha-factory/nodes/{id}/dependents` | GET | Get dependent nodes (DAG) |
| `/api/ta/registry` | GET | TA registry summary |
| `/api/ta/patterns` | GET | Available patterns |

**Bootstrap Data:**
- BTC: 5,692 daily candles
- SPX: 19,242 daily candles
- DXY: 13,366 daily candles
- Calibration config (Phase 8.6)
- Strategy registry (11 strategies)
- Regime activation map

## Test Results
- 21/21 backend tests passed (100%)
- MongoDB connected and healthy
- All CRUD operations working

## Roadmap

### Current Phase
- [x] PHASE 13.1 — Alpha Node Registry ✅

### Next Phases
- [ ] PHASE 13.2 — Alpha Feature Library (300-500 base features)
- [ ] PHASE 13.3 — Alpha Graph (logical relationships)
- [ ] PHASE 13.4 — Alpha DAG (computational dependencies)
- [ ] PHASE 13.5 — Factor Generator
- [ ] PHASE 13.6 — Factor Ranker
- [ ] PHASE 13.7 — Alpha Deployment

### Future
- PHASE 14 — Meta Portfolio Layer
- PHASE 15 — Risk Intelligence

## Tech Stack
- Python (FastAPI)
- MongoDB (ta_engine database)
- python-dotenv for environment loading

## Core Requirements
- Registry должен быть универсальным: node = signal | state | feature | factor | strategy_component
- DAG-ready: inputs/outputs для computation graph
- Graph-ready: supports/contradicts/amplifies для logical relationships
- Regime dependency: nodes активны только в определённых режимах
