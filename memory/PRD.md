# TA Engine PRD - PHASE 13.6 Alpha DAG

## Original Problem Statement
TA Engine - Institutional-grade quant trading platform. Building autonomous Alpha Factory for systematic signal generation. PHASE 13.6 implements Alpha DAG - a computational graph for efficient factor calculation with caching and parallel execution.

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
│   ├── alpha_graph/             # PHASE 13.5 - reasoning graph
│   └── alpha_dag/               # PHASE 13.6 ✅
│       ├── dag_types.py         # DagNode, DagEdge, NodeType
│       ├── dag_builder.py       # Build DAG from factors
│       ├── dag_optimizer.py     # Remove duplicates, fusion
│       ├── dag_scheduler.py     # Levelized topological sort
│       ├── dag_executor.py      # Execute DAG
│       ├── dag_cache.py         # Input-hash caching
│       ├── dag_repository.py    # MongoDB persistence
│       ├── dag_routes.py        # API endpoints
│       └── alpha_dag.py         # Main orchestrator
└── server.py                    # FastAPI v13.6.0
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

### PHASE 13.5 — Alpha Graph ✅
- 107 graph nodes, 4843 edges
- 5 relation types: supports, amplifies, contradicts, conditional_on, invalidates
- Coherence scoring engine

### PHASE 13.6 — Alpha DAG (2026-03-11) ✅
**Core Features:**
- **293 DAG nodes** (97 features, 89 transforms, 107 factors)
- **495 edges** (dependencies)
- **Depth: 3 levels** for parallel execution
- **Input-hash caching** with 100% hit rate on repeated calls
- **Execution time: ~2ms** (target was <15ms)

**Node Types:**
| Type | Count | Description |
|------|-------|-------------|
| feature | 97 | Base market features (price_return, volume, etc.) |
| transform | 89 | Transformations (zscore, ema, rolling_mean, etc.) |
| factor | 107 | Final computed factors |

**Transform Types (16):**
- zscore, ema, sma, rolling_mean, rolling_std
- rolling_zscore (fused), lag, diff, percentile, rank
- log, abs, sign, clip, normalize, threshold

**DAG Optimization:**
- Duplicate node removal
- Transform merging
- Transform fusion (e.g., zscore(rolling_mean) → rolling_zscore)
- Depth minimization

**Levelized Scheduling:**
| Level | Nodes | Can Parallelize |
|-------|-------|-----------------|
| 0 | 97 | Yes (features) |
| 1 | 106 | Yes (transforms) |
| 2 | 90 | Yes (factors) |
| **Max Parallelism** | **106** | |

**Cache Layer:**
- Input-hash based validation
- TTL support (60s default)
- Hit rate tracking
- Top hits monitoring

**Execution Modes:**
1. **Snapshot Mode** - for backtesting and analysis
2. **Streaming Mode** - for live trading (tick-by-tick)

**Performance:**
| Metric | Value | Target |
|--------|-------|--------|
| Avg execution | 2.17ms | <15ms ✅ |
| Min execution | 1.81ms | - |
| Max execution | 2.65ms | - |
| Cache hit rate | 100% | - |

**API Endpoints:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/alpha-dag/health` | GET | Health check |
| `/api/alpha-dag/stats` | GET | DAG statistics |
| `/api/alpha-dag/build` | POST | Build DAG |
| `/api/alpha-dag/nodes` | GET | List nodes |
| `/api/alpha-dag/edges` | GET | List edges |
| `/api/alpha-dag/execute` | POST | Execute on snapshot |
| `/api/alpha-dag/execute-stream` | POST | Streaming execution |
| `/api/alpha-dag/execution-order` | GET | Scheduled order |
| `/api/alpha-dag/levels` | GET | Parallel levels |
| `/api/alpha-dag/cache/stats` | GET | Cache statistics |
| `/api/alpha-dag/cache/clear` | POST | Clear cache |
| `/api/alpha-dag/node-types` | GET | Available types |
| `/api/alpha-dag/snapshots` | GET | Build snapshots |
| `/api/alpha-dag/clear` | DELETE | Clear DAG |

## Test Results
- PHASE 13.1: 21/21 passed (100%)
- PHASE 13.2: 95%+ passed
- PHASE 13.3: 48/48 passed (100%)
- PHASE 13.4: 14/14 passed (100%)
- PHASE 13.5: 21/21 passed (100%)
- PHASE 13.6: 24/24 passed (100%)

## Alpha Factory Pipeline (Complete to DAG)
```
Feature Library (315 features)
      ↓
Factor Generator (1236 candidates)
      ↓
Factor Ranker (105 approved)
      ↓
Alpha Graph (107 nodes, 4843 edges)
      ↓
Alpha DAG (293 nodes, 495 edges)  ← CURRENT
      ↓
Alpha Deployment (NEXT)
```

## Roadmap

### Completed Phases
- [x] PHASE 13.1 — Alpha Node Registry ✅ (89 nodes)
- [x] PHASE 13.2 — Alpha Feature Library ✅ (315 features)
- [x] PHASE 13.3 — Factor Generator ✅ (1236 factors)
- [x] PHASE 13.4 — Factor Ranker ✅ (105 approved)
- [x] PHASE 13.5 — Alpha Graph ✅ (107 nodes, 4843 edges)
- [x] PHASE 13.6 — Alpha DAG ✅ (293 nodes, 495 edges)

### Next Phases
- [ ] PHASE 13.7 — Alpha Deployment

### Future
- PHASE 14 — Meta Portfolio Layer
- PHASE 15 — Risk Intelligence

## Database Schema

### alpha_dag_nodes
```json
{
  "node_id": "852bab1c7429",
  "node_type": "feature",
  "operation": "price_return_1m",
  "params": {},
  "inputs": [],
  "outputs": ["798aa8f8496a", "a60b2e113012"],
  "cost": 1.0,
  "latency_estimate": 0.1,
  "level": 0,
  "execution_order": 0,
  "cacheable": true,
  "source_feature_id": "price_return_1m",
  "created_at": "2026-03-11T22:42:40Z"
}
```

### alpha_dag_edges
```json
{
  "edge_id": "abc123def456",
  "source_node": "852bab1c7429",
  "target_node": "798aa8f8496a",
  "created_at": "2026-03-11T22:42:40Z"
}
```

### alpha_dag_snapshots
```json
{
  "snapshot_id": "6494a8de",
  "total_nodes": 293,
  "total_edges": 495,
  "depth": 3,
  "nodes_by_type": {
    "feature": 97,
    "transform": 89,
    "factor": 107
  },
  "total_cost": 551.5,
  "estimated_latency_ms": 2.1,
  "created_at": "2026-03-11T22:42:40Z"
}
```

## Note on Synthetic Data
Factor evaluation currently uses synthetic data that simulates realistic performance characteristics. In production, this would be replaced with real market data backtests.

## Tech Stack
- Python (FastAPI)
- MongoDB (ta_engine database)
- Pure Python metrics (no pandas/numpy required)
