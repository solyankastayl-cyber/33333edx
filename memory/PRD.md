# TA Engine PRD - PHASE 13.5 Alpha Graph

## Original Problem Statement
TA Engine - Institutional-grade quant trading platform. Building autonomous Alpha Factory for systematic signal generation. PHASE 13.5 implements Alpha Graph - a reasoning engine that analyzes relationships between approved factors.

## Architecture Overview
```
backend/
├── core/database/              # MongoDB Connection
├── modules/alpha_factory/         
│   ├── alpha_types.py           # PHASE 13.1 - 89 nodes
│   ├── alpha_node_registry.py
│   ├── feature_library/         # PHASE 13.2 - 308+ features
│   ├── factor_generator/        # PHASE 13.3 - 1236+ factors
│   ├── factor_ranker/           # PHASE 13.4 - 105 approved
│   └── alpha_graph/             # PHASE 13.5 ✅
│       ├── alpha_graph_types.py    # GraphNode, GraphEdge, RelationType
│       ├── alpha_graph_builder.py  # Build graph from factors
│       ├── alpha_graph_reasoner.py # Coherence scoring engine
│       ├── alpha_graph_repository.py # MongoDB persistence
│       ├── alpha_graph_routes.py   # API endpoints
│       └── alpha_graph.py          # Main orchestrator
└── server.py                    # FastAPI v13.5.0
```

## What's Been Implemented

### PHASE 13.1 — Alpha Node Registry ✅
- 89 nodes across 9 types

### PHASE 13.2 — Alpha Feature Library ✅
- 315+ features across 8 categories

### PHASE 13.3 — Factor Generator ✅
- 1236+ factors from 8 templates

### PHASE 13.4 — Factor Ranker ✅
- 105 approved factors (4 STRONG + 101 PROMISING)

### PHASE 13.5 — Alpha Graph (2026-03-11) ✅
**Core Features:**
- **107 graph nodes** from approved factors
- **4843 edges** (relationships between factors)
- **5 relation types**: supports, amplifies, contradicts, conditional_on, invalidates
- **Coherence scoring engine** for signal quality evaluation
- **Support/conflict chain detection**

**Relation Types Distribution:**
| Type | Count | Description |
|------|-------|-------------|
| supports | 3165 | A supports B |
| amplifies | 21 | A amplifies B |
| contradicts | 212 | A contradicts B |
| conditional_on | 1445 | A works only if B |
| invalidates | 0 | A invalidates B |

**Nodes by Family:**
| Family | Count |
|--------|-------|
| momentum | 49 |
| breakout | 28 |
| regime | 17 |
| correlation | 4 |
| structure | 4 |
| microstructure | 3 |
| volume | 1 |
| macro | 1 |

**Family Relationship Matrix:**
```
FAMILY_SUPPORTS:
  momentum → trend, breakout
  trend → momentum, structure
  breakout → momentum, volatility
  volatility → breakout, regime
  volume → breakout, momentum, liquidity
  liquidity → reversal, microstructure
  microstructure → liquidity, volume
  structure → trend, reversal
  correlation → macro, regime
  macro → correlation, regime
  regime → macro, volatility
  reversal → liquidity, structure

FAMILY_CONTRADICTS:
  trend ← → reversal
  reversal ← → momentum
  breakout ← → regime
```

**Coherence Score Formula:**
```
base_score = 0.5
+ supports * 0.015
+ amplifies * 0.02
+ conditionals * 0.01
- conflicts * 0.03
- invalidations * 0.04
+ support_chains * 0.05
+ amplify_chains * 0.07
```

**Signal Quality Thresholds:**
| Quality | Coherence | Conditions |
|---------|-----------|------------|
| INVALIDATED | Any | invalidations > 0 |
| CONFLICTED | < 0.35 | conflicts > 2 |
| STRONG | ≥ 0.75 | - |
| MODERATE | ≥ 0.55 | - |
| WEAK | ≥ 0.35 | - |

**API Endpoints:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/alpha-graph/health` | GET | Health check |
| `/api/alpha-graph/stats` | GET | Graph statistics |
| `/api/alpha-graph/build` | POST | Build graph from factors |
| `/api/alpha-graph/nodes` | GET | List nodes with filters |
| `/api/alpha-graph/edges` | GET | List edges with filters |
| `/api/alpha-graph/relation-types` | GET | Available relation types |
| `/api/alpha-graph/reason` | POST | Evaluate signal coherence |
| `/api/alpha-graph/context/{id}` | GET | Node context |
| `/api/alpha-graph/conflicts` | GET | All conflicts |
| `/api/alpha-graph/network/{id}` | GET | Support network |
| `/api/alpha-graph/snapshots` | GET | Graph snapshots |
| `/api/alpha-graph/clear` | DELETE | Clear graph |

## Test Results
- PHASE 13.1: 21/21 passed (100%)
- PHASE 13.2: 95%+ passed
- PHASE 13.3: 48/48 passed (100%)
- PHASE 13.4: 14/14 passed (100%)
- PHASE 13.5: 21/21 passed (100%)

## Alpha Factory Pipeline (Complete to Graph)
```
Feature Library (315 features)
      ↓
Factor Generator (1236 candidates)
      ↓
Factor Ranker (105 approved)
      ↓
Alpha Graph (107 nodes, 4843 edges) ← CURRENT
      ↓
Alpha DAG (NEXT)
      ↓
Alpha Deployment
```

## Roadmap

### Completed Phases
- [x] PHASE 13.1 — Alpha Node Registry ✅ (89 nodes)
- [x] PHASE 13.2 — Alpha Feature Library ✅ (315 features)
- [x] PHASE 13.3 — Factor Generator ✅ (1236 factors)
- [x] PHASE 13.4 — Factor Ranker ✅ (105 approved)
- [x] PHASE 13.5 — Alpha Graph ✅ (107 nodes, 4843 edges)

### Next Phases
- [ ] PHASE 13.6 — Alpha DAG (computational dependencies)
- [ ] PHASE 13.7 — Alpha Deployment

### Future
- PHASE 14 — Meta Portfolio Layer
- PHASE 15 — Risk Intelligence

## Database Schema

### alpha_graph_nodes
```json
{
  "node_id": "50f21c54f791",
  "factor_id": "50f21c54f791",
  "family": "momentum",
  "template": "pair_feature",
  "inputs": ["rsi_14", "macd_signal"],
  "composite_score": 0.62,
  "verdict": "PROMISING",
  "ic": 0.025,
  "sharpe": 0.45,
  "weight": 1.0,
  "active": true,
  "outgoing_edges": 30,
  "incoming_edges": 29,
  "created_at": "2026-03-11T22:23:02Z"
}
```

### alpha_graph_edges
```json
{
  "edge_id": "ee6eb444d5",
  "source_node": "50f21c54f791",
  "target_node": "cd394e6e27bd",
  "relation_type": "supports",
  "strength": 0.6,
  "confidence": 0.7,
  "reason": "momentum supports breakout",
  "auto_generated": true,
  "created_at": "2026-03-11T22:23:02Z"
}
```

### alpha_graph_snapshots
```json
{
  "snapshot_id": "d84db3ba",
  "total_nodes": 107,
  "total_edges": 4843,
  "edges_by_type": {
    "supports": 3165,
    "amplifies": 21,
    "contradicts": 212,
    "conditional_on": 1445,
    "invalidates": 0
  },
  "nodes_by_family": {...},
  "created_at": "2026-03-11T22:23:03Z"
}
```

## Note on Synthetic Data
Factor evaluation currently uses synthetic data that simulates realistic performance characteristics. In production, this would be replaced with real market data backtests.

## Tech Stack
- Python (FastAPI)
- MongoDB (ta_engine database)
- Pure Python metrics (no pandas/numpy required)
