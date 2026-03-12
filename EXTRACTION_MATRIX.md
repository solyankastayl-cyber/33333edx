# EXTRACTION MATRIX: FOMO-SEOFv1.69 → Текущий проект

**Дата:** Февраль 2026  
**Архитектурный вердикт:** Точечный extraction, НЕ массовый перенос

---

## MERGE INVENTORY (Engine-by-Engine)

| Engine | Current | FOMO | Сильнее | Решение | Новый модуль | Статус |
|--------|---------|------|---------|---------|--------------|--------|
| Funding/OI | TS: funding.service.ts (100% match) | TS: идентичен | Равны | Не переносить TS. Построить Python engine | exchange_intelligence/funding_oi_engine.py | DONE |
| Derivatives Pressure | TS: partial (indicators) | TS: идентичен | Равны | Построить Python engine | exchange_intelligence/derivatives_pressure_engine.py | DONE |
| Liquidation Engine | TS: cascade.service.ts (100% match) | TS: идентичен | Равны | Построить Python engine | exchange_intelligence/exchange_liquidation_engine.py | DONE |
| Exchange Flow | TS: order-flow.service.ts (100% match) | TS: идентичен | Равны | Построить Python engine | exchange_intelligence/exchange_flow_engine.py | DONE |
| Volume Context | TS: partial | TS: идентичен | Равны | Построить Python engine | exchange_intelligence/exchange_volume_engine.py | DONE |
| Context Aggregator | Нет | Нет | — | Новый | exchange_intelligence/exchange_context_aggregator.py | DONE |
| URI (Reliability) | Нет | FOMO: reliability/ | FOMO | Перенести как safeguard | adaptive_intelligence/reliability/ | PENDING |
| Drift Detection | Нет | FOMO: drift/ | FOMO | Перенести как safeguard | adaptive_intelligence/drift/ | PENDING |
| Capital Guard | Нет | FOMO: lifecycle/capital* | FOMO | Перенести позже | adaptive_intelligence/ | P2 |
| Universe Loader | Нет | FOMO: universe_loader | FOMO | Перенести позже | exchange_intelligence/ | P2 |
| Prediction API | Нет | FOMO: Python routes | FOMO | НЕ переносить (другой контур) | — | SKIP |
| Chart/UI | Нет | FOMO: chart/ | FOMO | НЕ переносить | — | SKIP |
| Combined Boost | Нет | FOMO | FOMO | Reference only | — | SKIP |
| Simulation Engine | Нет | FOMO: exchange-sim/ | FOMO | Частично позже | — | P2 |

---

## КЛЮЧЕВОЙ ПРИНЦИП

```
TA Engine (Signal Source 1) ────────┐
                                     ├── Trading Decision Layer
Exchange Intelligence (Source 2) ───┘
```

**TA ничего не знает про Exchange.**  
**Exchange ничего не знает про TA.**  
**Они встречаются ТОЛЬКО в Trading Decision Layer.**
