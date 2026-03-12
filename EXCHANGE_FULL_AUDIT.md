# ПОЛНЫЙ АУДИТ EXCHANGE-ЛОГИКИ
## Текущее состояние проекта — Март 2026

---

## 1. АРХИТЕКТУРНАЯ ДИАГРАММА

```
                        ┌──────────────────────────────────────────────┐
                        │            TRADING SYSTEM (будущее)           │
                        │                                              │
                        │  TA signals  ──┐                             │
                        │                ├── Trading Decision Layer    │
                        │  EX signals  ──┘                             │
                        └──────────────────────────────────────────────┘
                                    ▲                    ▲
                                    │                    │
                    ┌───────────────┘                    └───────────────┐
                    │                                                    │
    ┌───────────────┴───────────────┐        ┌──────────────────────────┴──────┐
    │      TA ENGINE (Python)       │        │  EXCHANGE INTELLIGENCE (Python) │
    │                               │        │      Phase 13.8 — НОВЫЙ        │
    │  TA Module → Features →       │        │                                 │
    │  Factors → Alpha Factory →    │        │  FundingOI Engine               │
    │  Alpha Graph → Alpha DAG →    │        │  Derivatives Pressure Engine    │
    │  Factor Ranker →              │        │  Liquidation Engine             │
    │  Alpha Deployment             │        │  Exchange Flow Engine           │
    │                               │        │  Volume Context Engine          │
    │  308 features                 │        │  Context Aggregator             │
    │  1236 factors                 │        │                                 │
    │  23 deployed                  │        │  Output: ExchangeContext        │
    │  (5 active, 18 shadow)        │        │  (bias, confidence, drivers)    │
    └───────────────┬───────────────┘        └──────────────────┬──────────────┘
                    │                                            │
                    │    ЗНАЮТ ТОЛЬКО ПРО РЫНОК, НЕ ДРУГ О ДРУГЕ │
                    │                                            │
    ┌───────────────┴───────────────┐        ┌──────────────────┴──────────────┐
    │     MARKET DATA (MongoDB)     │        │    EXCHANGE DATA LAYER (TS)     │
    │                               │        │                                 │
    │  candles: 38,300 BTC          │        │  exchange/        (230 файлов)  │
    │  config: 2                    │        │  exchange-ml/     (96 файлов)   │
    │  regime_map: 9                │        │  exchange-alt/    (90 файлов)   │
    │  strategies: 11               │        │                                 │
    │  alpha_deployments: 23        │        │  32 подмодуля                   │
    │  alpha_signals_live: 7+       │        │  36 роутов                      │
    │                               │        │  36 индикаторов                 │
    └───────────────────────────────┘        └─────────────────────────────────┘
```

---

## 2. ПОЛНАЯ КАРТА ЗАВИСИМОСТЕЙ

### 2.1 Exchange Data Layer (TypeScript/Fastify)

```
exchange/ (index.ts — точка входа)
│
├── models/                              ← ФУНДАМЕНТ
│   ├── exchange.types.ts                   Контракты данных (snapshot, config, overview)
│   └── exchange.model.ts                   Mongoose-схемы (StatusCache, Config)
│
├── providers/                           ← ИСТОЧНИКИ ДАННЫХ
│   ├── base.provider.ts                    Абстрактный провайдер
│   ├── binance/                            Binance USDM
│   │   └── binance.usdm.provider.ts
│   ├── coinbase/                           Coinbase
│   ├── bybit.usdtperp.provider.ts         Bybit USDT-perp
│   ├── okx.provider.ts                    OKX
│   ├── mock.provider.ts                   Mock-провайдер
│   ├── provider.registry.ts               Реестр провайдеров
│   ├── provider.selector.ts               Селектор (выбор лучшего)
│   └── provider.health.ts                 Health-чеки
│
├── exchange-data.service.ts             ← POLLING / КЭШИРОВАНИЕ
│   Polling loop → провайдеры → in-memory кэш
│   341 строк
│
├── indicators/                          ← 36 ИНДИКАТОРОВ (сенсоры)
│   ├── indicator.types.ts                  Контракты (6 категорий)
│   ├── indicator.registry.ts               Реестр калькуляторов
│   ├── indicator.service.ts                Orchestration + кэш
│   ├── indicator.snapshot.ts               Снэпшот-билдер
│   ├── indicator.aggregates.ts             Агрегации
│   └── calculators/
│       ├── price-structure/                8 индикаторов
│       ├── momentum/                       6 индикаторов
│       ├── volume/                         6 индикаторов
│       ├── order-book/                     6 индикаторов
│       ├── positioning/                    6 индикаторов
│       └── whale.calculators.ts            6 индикаторов (S10.W)
│
├── order-flow/                          ← АНАЛИЗ ПОТОКА ОРДЕРОВ
│   ├── order-flow.service.ts               Основной сервис
│   ├── order-flow.analyzer.ts              Анализатор
│   ├── imbalance.calculator.ts             Расчёт имбаланса
│   ├── absorption.detector.ts              Детектор абсорбции
│   └── order-flow.types.ts                 Типы
│
├── regimes/                             ← РЫНОЧНЫЕ РЕЖИМЫ
│   ├── regime.service.ts                   Сервис режимов
│   └── indicator-detector.ts               Детектор по индикаторам
│
├── liquidations/                        ← ЛИКВИДАЦИИ
│   ├── cascade.service.ts                  Каскадные ликвидации (298 строк)
│   ├── cascade.detector.ts                 Детектор каскадов
│   ├── cascade.service.types.ts            Типы
│   └── cascade-admin.routes.ts             Админ-роуты
│
├── patterns/                            ← ПАТТЕРНЫ
│   ├── pattern.library.ts                  Библиотека паттернов
│   ├── pattern.detector.ts                 Детектор
│   └── indicator-detector.ts               Детектор по индикаторам
│
├── funding/                             ← ФАНДИНГ
│   ├── funding.service.ts                  Основной сервис (141 строка)
│   ├── funding.normalizer.ts               Нормализация ставок
│   ├── funding.context.classifier.ts       Классификатор контекста
│   ├── funding.registry.ts                 Реестр источников
│   ├── funding.store.ts                    Хранилище
│   ├── adapters/                           Адаптеры бирж
│   │   ├── binance.funding.adapter.ts
│   │   ├── bybit.funding.adapter.ts
│   │   ├── coinbase.funding.adapter.ts
│   │   └── hyperliquid.funding.adapter.ts
│   ├── routes/                             Роуты
│   └── services/                           Вспомогательные сервисы
│
├── whales/                              ← КИТОВАЯ АКТИВНОСТЬ
│   ├── whale.state.ts                      Состояние
│   ├── whale.storage.ts                    Хранилище
│   ├── whale.ingest.ts                     Сбор данных
│   ├── whale.mock.ts                       Mock-данные
│   └── patterns/                           Паттерны китов
│       ├── whale-pattern.detector.ts
│       └── whale-pattern.storage.ts
│
├── observation/                         ← НАБЛЮДЕНИЯ
│   ├── observation.builder.ts
│   ├── observation.storage.ts
│   └── observation.service.ts
│
├── context/                             ← КОНТЕКСТ
│   ├── context.builder.ts                  Билдер контекста
│   └── context.types.ts                    Типы
│
├── verdict/                             ← ВЕРДИКТ
│   ├── verdict.engine.ts                   Движок вердиктов
│   ├── verdict.scoring.ts                  Скоринг
│   └── verdict.types.ts                    Типы
│
├── screener/                            ← СКРИНЕР АЛЬТОВ
│   ├── candidates/                         Кандидаты
│   ├── feature builder                     Построение фич
│   ├── labeler                             Разметка
│   ├── pattern space                       Пространство паттернов
│   ├── similarity                          Сходство
│   ├── winner memory                       Память победителей
│   └── ml/                                 ML-модели для альтов
│       ├── altml.trainer.ts
│       ├── altml.predict.ts
│       └── altml.dataset.builder.ts
│
├── macro/                               ← МАКРО-ОВЕРЛЕЙ
│   ├── macro.state.service.ts
│   ├── macro.funding.overlay.ts
│   └── macro.cluster.context.ts
│
├── sector/                              ← СЕКТОРНАЯ РОТАЦИЯ
│   ├── sector.state.ts
│   ├── sector.wave.ts
│   └── sector.asset.tags.ts
│
├── universe/ + universe-v2/             ← ЮНИВЕРС
│   └── adapters/
│       ├── binance.universe.adapter.ts
│       ├── bybit.universe.adapter.ts
│       └── hyperliquid.universe.adapter.ts
│
├── snapshots/                           ← СНЭПШОТЫ
│   ├── snapshot.builder.ts
│   ├── snapshot.features.ts
│   └── snapshot.db.ts
│
├── clustering/                          ← КЛАСТЕРИЗАЦИЯ
│   ├── kmeans.ts
│   ├── vector.builder.ts
│   └── feature.stats.ts
│
├── labs/                                ← ИССЛЕДОВАНИЯ
│   ├── labs-attribution.service.ts         Attribution
│   ├── labs-explainability.service.ts      Explainability
│   ├── labs-alerting.service.ts            Alerting
│   ├── labs-historical.service.ts          Historical
│   ├── labs-canonical.service.ts           Canonical
│   ├── pattern-risk.service.ts             Pattern risk
│   ├── regime-attribution.service.ts       Regime attribution
│   ├── regime-forward.service.ts           Regime forward
│   ├── sentiment-interaction.service.ts    Sentiment
│   └── whale-risk.service.ts               Whale risk
│
├── intelligence/                        ← СИГНАЛЫ
│   └── signal_intelligence.service.ts
│
├── candidates/                          ← КАНДИДАТЫ
├── returns/                             ← ДОХОДНОСТЬ
├── cache/                               ← КЭШ
├── data/                                ← ДАННЫЕ
├── ws/                                  ← WEBSOCKET
├── backfill/                            ← БЭКФИЛЛ
├── freeze/                              ← ЗАМОРОЗКА
├── forecast/                            ← ПРОГНОЗЫ
├── jobs/                                ← ЗАДАЧИ
├── admin/                               ← АДМИН
└── routes/                              ← РОУТЫ
```

---

### 2.2 Exchange-ML (TypeScript)

```
exchange-ml/ (index.ts)
│
├── ml.types.ts                          ← Типы ML-моделей
├── ml.service.ts                        ← Основной ML-сервис
├── ml.trainer.ts                        ← Тренировка
├── ml.routes.ts                         ← API роуты
├── ml.comparison.ts                     ← Сравнение моделей
├── ml.modifier.service.ts               ← Модификации
├── ml.promotion.service.ts              ← Промоушн моделей
├── ml.shadow.training.ts                ← Shadow-тренировка
├── ml.shadow.monitor.service.ts         ← Мониторинг shadow
│
├── featureExtractor.ts                  ← Извлечение фич
├── macroFeatureExtractor.ts             ← Макро-фичи
├── labeler.ts                           ← Разметка
├── model.registry.ts                    ← Реестр моделей
├── exchange.verdict.service.ts          ← ML-вердикт
│
├── dataset/                             ← Датасеты
├── training/                            ← Тренировка
├── shadow/                              ← Shadow-режим
├── lifecycle/                           ← Жизненный цикл
├── performance/                         ← Производительность
├── perf/                                ← Performance monitor
├── quality/                             ← Качество
├── config/                              ← Конфигурация
├── contracts/                           ← Контракты
├── snapshots/                           ← Снэпшоты
├── segments/                            ← Сегменты
├── iteration/                           ← Итерации
├── jobs/                                ← Задачи
├── dir/                                 ← Direction-модели
├── services/                            ← Сервисы
└── admin/                               ← Админка
```

---

### 2.3 Exchange-Alt (TypeScript)

```
exchange-alt/ (index.ts)
│
├── adapters/         ← Адаптеры альткоинов
├── alt-opps/         ← Alt opportunities
├── alt-sets/         ← Наборы альтов
├── clustering/       ← Кластеризация
├── context/          ← Контекст
├── db/               ← БД
├── explain/          ← Объяснения
├── failure/          ← Обработка ошибок
├── gating/           ← Gating
├── indicators/       ← Индикаторы альтов
├── meta-brain/       ← MetaBrain для альтов
├── ml/               ← ML-модели
├── ml-overlay/       ← ML-оверлей
├── pattern-memory/   ← Память паттернов
├── portfolio/        ← Портфель
├── portfolio-construct/  ← Конструирование
├── portfolio-filter/ ← Фильтрация
├── propagation/      ← Распространение
├── ranking/          ← Ранжирование
├── replay/           ← Replay
├── sector-regime/    ← Секторные режимы
├── shadow/           ← Shadow-режим
├── strategy-survival/ ← Выживание стратегий
├── tuning/           ← Тюнинг
├── universe/         ← Юниверс
└── validation/       ← Валидация
```

---

### 2.4 Exchange Intelligence (Python — PHASE 13.8, НОВЫЙ)

```
exchange_intelligence/ (Python)
│
├── __init__.py
├── exchange_intel_types.py              ← Типы и контракты
│   ├── ExchangeBias (BULLISH/BEARISH/NEUTRAL)
│   ├── FundingState (5 состояний)
│   ├── OIPressureState (5 состояний)
│   ├── DerivativesPressure (4 состояния)
│   ├── LiquidationRisk (4 уровня)
│   ├── FlowDirection (5 типов)
│   ├── VolumeState (6 типов)
│   └── Dataclasses: FundingOISignal, DerivativesPressureSignal,
│       LiquidationSignal, ExchangeFlowSignal, VolumeContextSignal,
│       ExchangeContext
│
├── exchange_intel_repository.py         ← MongoDB R/W
│   Читает: candles, exchange_funding_context, exchange_oi_snapshots,
│           exchange_liquidation_events, exchange_trade_flows
│   Пишет:  exchange_intel_signals, exchange_intel_funding,
│           exchange_intel_volume
│
├── funding_oi_engine.py                 ← Funding + OI Engine
│   Input:  funding_rate, oi_value, oi_change_pct (или candles)
│   Output: FundingOISignal
│   Логика: classify funding state, OI pressure, crowding risk,
│           funding/OI divergence detection
│
├── derivatives_pressure_engine.py       ← Derivatives Engine
│   Input:  long_short_ratio, leverage_index, perp_premium (или candles)
│   Output: DerivativesPressureSignal
│   Логика: squeeze probability, leverage detection,
│           perp premium analysis
│
├── exchange_liquidation_engine.py       ← Liquidation Engine
│   Input:  liquidation events, price (или candles)
│   Output: LiquidationSignal
│   Логика: liquidation zones, cascade probability,
│           trapped positions, net liquidation flow
│
├── exchange_flow_engine.py              ← Flow Engine
│   Input:  taker buy/sell, order flow (или candles)
│   Output: ExchangeFlowSignal
│   Логика: taker ratio, aggressive flow,
│           absorption detection, flow direction
│
├── exchange_volume_engine.py            ← Volume Engine
│   Input:  candles (обязательно)
│   Output: VolumeContextSignal
│   Логика: volume ratio vs MA20, anomaly z-score,
│           breakout/climax/exhaustion detection,
│           buy volume estimation
│
├── exchange_context_aggregator.py       ← АГРЕГАТОР (точка входа)
│   Запускает все 5 engines → вычисляет composite bias
│   Веса: Flow 30%, Funding 20%, Derivatives 20%,
│          Liquidation 15%, Volume 15%
│   Output: ExchangeContext (unified)
│
└── exchange_intel_routes.py             ← FastAPI Routes (8 endpoints)
```

---

### 2.5 Python Exchange Adapters

```
exchanges/ (Python)
│
├── base_exchange_adapter.py             ← Базовый адаптер
├── binance_adapter.py                   ← Binance
├── bybit_adapter.py                     ← Bybit
├── okx_adapter.py                       ← OKX
├── exchange_repository.py               ← MongoDB (411 строк)
├── exchange_types.py                    ← Типы (363 строки)
├── exchange_routes.py                   ← API роуты
├── exchange_router.py                   ← Роутер
└── ws_manager.py                        ← WebSocket менеджер
```

---

## 3. ВСЕ 36 ИНДИКАТОРОВ (Exchange Indicators Layer)

### 3.1 Price Structure (8 индикаторов)
| # | ID | Описание |
|---|-----|----------|
| 1 | `ema_distance_fast` | Расстояние цены до быстрой EMA |
| 2 | `ema_distance_mid` | Расстояние цены до средней EMA |
| 3 | `ema_distance_slow` | Расстояние цены до медленной EMA |
| 4 | `vwap_deviation` | Отклонение от VWAP |
| 5 | `median_price_deviation` | Отклонение от медианной цены |
| 6 | `atr_normalized` | Нормализованный ATR |
| 7 | `trend_slope` | Наклон тренда |
| 8 | `range_compression` | Сжатие диапазона |

### 3.2 Momentum (6 индикаторов)
| # | ID | Описание |
|---|-----|----------|
| 9 | `rsi_normalized` | Нормализованный RSI |
| 10 | `stochastic` | Stochastic oscillator |
| 11 | `macd_delta` | MACD delta |
| 12 | `roc` | Rate of Change |
| 13 | `momentum_decay` | Затухание импульса |
| 14 | `directional_momentum_balance` | Баланс направленного импульса |

### 3.3 Volume (6 индикаторов)
| # | ID | Описание |
|---|-----|----------|
| 15 | `volume_index` | Индекс объёма |
| 16 | `volume_delta` | Дельта объёма |
| 17 | `buy_sell_ratio` | Соотношение buy/sell |
| 18 | `volume_price_response` | Отклик цены на объём |
| 19 | `relative_volume` | Относительный объём |
| 20 | `participation_intensity` | Интенсивность участия |

### 3.4 Order Book (6 индикаторов)
| # | ID | Описание |
|---|-----|----------|
| 21 | `book_imbalance` | Дисбаланс стакана |
| 22 | `depth_density` | Плотность стакана |
| 23 | `liquidity_walls` | Стенки ликвидности |
| 24 | `absorption_strength` | Сила абсорбции |
| 25 | `liquidity_vacuum` | Вакуум ликвидности |
| 26 | `spread_pressure` | Давление спреда |

### 3.5 Positioning (6 индикаторов)
| # | ID | Описание |
|---|-----|----------|
| 27 | `oi_level` | Уровень OI |
| 28 | `oi_delta` | Дельта OI |
| 29 | `oi_volume_ratio` | Соотношение OI/Volume |
| 30 | `funding_pressure` | Давление фандинга |
| 31 | `long_short_ratio` | Соотношение Long/Short |
| 32 | `position_crowding` | Скученность позиций |

### 3.6 Whale Positioning (6 индикаторов)
| # | ID | Описание |
|---|-----|----------|
| 33 | `large_position_presence` | Присутствие крупных позиций |
| 34 | `whale_side_bias` | Сторона китов |
| 35 | `position_crowding_against_whales` | Позиции против китов |
| 36 | `stop_hunt_probability` | Вероятность stop-hunt |
| 37 | `large_position_survival_time` | Время жизни крупной позиции |
| 38 | `contrarian_pressure_index` | Индекс контрарного давления |

**Правило:** Индикаторы = СЕНСОРЫ, не СИГНАЛЫ. Чистые измерения, без бизнес-логики.

---

## 4. ВСЕ API ENDPOINTS

### 4.1 Exchange Intelligence (Python — Phase 13.8)
| Method | Endpoint | Назначение |
|--------|----------|-----------|
| GET | `/api/exchange-intelligence/context/batch` | Batch-контекст для нескольких символов |
| GET | `/api/exchange-intelligence/context/{symbol}` | Полный exchange-контекст |
| GET | `/api/exchange-intelligence/funding/{symbol}` | Funding + OI сигнал |
| GET | `/api/exchange-intelligence/derivatives/{symbol}` | Derivatives pressure |
| GET | `/api/exchange-intelligence/liquidation/{symbol}` | Liquidation risk |
| GET | `/api/exchange-intelligence/flow/{symbol}` | Order flow |
| GET | `/api/exchange-intelligence/volume/{symbol}` | Volume context |
| GET | `/api/exchange-intelligence/history/{symbol}` | История сигналов |
| GET | `/api/exchange-intelligence/engines/status` | Статус всех engines |

### 4.2 Exchange Core TS (36 route-файлов)
| Подмодуль | Endpoints |
|-----------|----------|
| `exchange.routes` | Основные exchange routes |
| `exchange-admin.routes` | Admin exchange |
| `indicator.routes` | Индикаторы |
| `order-flow.routes` | Order flow |
| `order-flow-admin.routes` | Admin order flow |
| `cascade.routes` | Ликвидации |
| `cascade-admin.routes` | Admin ликвидации |
| `regime.routes` | Режимы |
| `regime-admin.routes` | Admin режимы |
| `pattern.routes` | Паттерны |
| `pattern-admin.routes` | Admin паттерны |
| `context.routes` | Контекст |
| `verdict.routes` | Вердикт |
| `funding.routes` | Фандинг |
| `admin_funding_debug.routes` | Debug фандинг |
| `observation.routes` | Наблюдения |
| `observation-admin.routes` | Admin наблюдения |
| `screener.routes` | Скринер |
| `macro.routes` | Макро |
| `rotation.routes` | Секторы |
| `snapshot.routes` | Снэпшоты |
| `universe.routes` | Юниверс |
| `universe_v2.routes` | Юниверс v2 |
| `whale.routes` | Киты |
| `whale-pattern.routes` | Паттерны китов |
| `labs.routes` | Лаборатория |
| `signal_intelligence.routes` | Сигналы |
| `provider.routes` | Провайдеры |
| `realdata.routes` | Данные |
| `backfill.routes` | Бэкфилл |
| `freeze.routes` | Заморозка |
| `alt_movers.routes` | Alt movers |
| `clustering.routes` | Кластеры |
| `exchange_learning_health.routes` | ML health |
| `ws.routes` | WebSocket |

### 4.3 Exchange-ML TS (8 route-файлов)
| Route | Назначение |
|-------|-----------|
| `ml.routes` | ML основные |
| `exchange_ml_admin.routes` | Admin ML |
| `dir.admin.routes` | Direction admin |
| `exchange_monitor.routes` | Мониторинг |
| `exchange_perf.routes` | Производительность |
| `exchange_snapshot.routes` | Снэпшоты |
| `forecast_segment.routes` | Сегменты прогноза |
| `exch_segments.routes` | Итерационные сегменты |

### 4.4 Exchange-Alt TS (4 route-файла)
| Route | Назначение |
|-------|-----------|
| `advanced.routes` | Продвинутые alt-операции |
| `alt-scanner.routes` | Сканер альтов |
| `extended.routes` | Расширенные routes |
| `universe.routes` | Юниверс альтов |

---

## 5. ПОТОК ДАННЫХ (Data Flow)

```
               ПРОВАЙДЕРЫ БИРЖ
          ┌───────────────────────┐
          │ Binance   │  Bybit    │
          │ OKX       │ Coinbase  │
          │ Hyperliquid │ Mock    │
          └─────────────┬─────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │  Exchange Data Service   │  ← TS polling/caching
          │  (exchange-data.service) │
          └─────────┬───────────────┘
                    │
         ┌──────────┼──────────┐
         ▼          ▼          ▼
   ┌──────────┐ ┌────────┐ ┌──────┐
   │ MongoDB  │ │ Cache  │ │ WS   │
   │ candles  │ │ in-mem │ │ push │
   └──────┬───┘ └────────┘ └──────┘
          │
          ▼
   ┌─────────────────────────────────┐
   │  Exchange Intelligence (Python) │
   │                                 │
   │  candles ──► FundingOI Engine   │
   │  candles ──► Derivatives Engine │
   │  candles ──► Liquidation Engine │
   │  candles ──► Flow Engine        │
   │  candles ──► Volume Engine      │
   │                                 │
   │  ──► Context Aggregator ──►     │
   │      ExchangeContext            │
   └─────────────┬───────────────────┘
                 │
                 ▼
   ┌─────────────────────────────────┐
   │  MongoDB                        │
   │  exchange_intel_signals         │
   │  exchange_intel_funding         │
   │  exchange_intel_volume          │
   └─────────────────────────────────┘
```

---

## 6. СТАТУС ЦЕЛОСТНОСТИ

### Что НЕ было тронуто (100% нетронуто):
| Компонент | Файлов | Статус |
|-----------|--------|--------|
| `exchange/` (TS) | 230 | НЕ ТРОНУТО |
| `exchange-ml/` (TS) | 96 | НЕ ТРОНУТО |
| `exchange-alt/` (TS) | 90 | НЕ ТРОНУТО |
| `exchanges/` (Python adapters) | 10 | НЕ ТРОНУТО |
| TA Engine | все модули | НЕ ТРОНУТО |
| Alpha Factory | все модули | НЕ ТРОНУТО |
| Alpha Deployment | все модули | НЕ ТРОНУТО |
| Все остальные Python-модули | 900+ | НЕ ТРОНУТО |

### Что было СОЗДАНО (Phase 13.8):
| Файл | Размер | Статус |
|------|--------|--------|
| `exchange_intelligence/__init__.py` | 18 строк | НОВЫЙ |
| `exchange_intelligence/exchange_intel_types.py` | 259 строк | НОВЫЙ |
| `exchange_intelligence/exchange_intel_repository.py` | 134 строки | НОВЫЙ |
| `exchange_intelligence/funding_oi_engine.py` | 169 строк | НОВЫЙ |
| `exchange_intelligence/derivatives_pressure_engine.py` | 145 строк | НОВЫЙ |
| `exchange_intelligence/exchange_liquidation_engine.py` | 184 строки | НОВЫЙ |
| `exchange_intelligence/exchange_flow_engine.py` | 165 строк | НОВЫЙ |
| `exchange_intelligence/exchange_volume_engine.py` | 180 строк | НОВЫЙ |
| `exchange_intelligence/exchange_context_aggregator.py` | 193 строки | НОВЫЙ |
| `exchange_intelligence/exchange_intel_routes.py` | 135 строк | НОВЫЙ |

### Что было ИЗМЕНЕНО:
| Файл | Изменение |
|------|-----------|
| `server.py` | +5 строк: подключение Exchange Intelligence router |
| `server.py` | Обновление версии: 13.7.0 → 13.8.0 |

**git diff подтверждает:** ни один файл в `backend/src/modules/exchange*/` не был изменён.

---

## 7. ПРОВЕРКА РАБОТОСПОСОБНОСТИ (на момент аудита)

| Endpoint | Статус | Примечание |
|----------|--------|-----------|
| `GET /api/health` | OK | v13.8.0 |
| `GET /api/alpha-deployment/stats` | OK | 23 deployed (5 active, 18 shadow) |
| `GET /api/exchange-intelligence/engines/status` | OK | 6 engines active |
| `GET /api/exchange-intelligence/context/BTC` | OK | Полный ExchangeContext |
| `GET /api/exchange-intelligence/funding/BTC` | OK | FundingOISignal |
| `GET /api/exchange-intelligence/derivatives/BTC` | OK | DerivativesPressureSignal |
| `GET /api/exchange-intelligence/liquidation/BTC` | OK | LiquidationSignal |
| `GET /api/exchange-intelligence/flow/BTC` | OK | ExchangeFlowSignal |
| `GET /api/exchange-intelligence/volume/BTC` | OK | VolumeContextSignal |

---

## 8. ОБЩАЯ СТАТИСТИКА

```
Exchange-related code in project:

  TypeScript (Data Layer):
    exchange/          230 файлов    ← 32 подмодуля, 36 индикаторов
    exchange-ml/        96 файлов    ← ML pipeline
    exchange-alt/       90 файлов    ← Alt-токены
    ────────────────────────────
    Итого:             416 TS-файлов

  Python (Intelligence + Adapters):
    exchange_intelligence/  10 файлов  ← Phase 13.8 (НОВЫЙ)
    exchanges/              10 файлов  ← Адаптеры бирж
    ────────────────────────────
    Итого:                  20 Python-файлов

  Всего Exchange-related: 436 файлов
  API route-файлов: 48 (36 + 8 + 4 + 1 Python)
  Индикаторов: 36 (6 категорий)
  Exchange провайдеров: 5 (Binance, Bybit, OKX, Coinbase, Mock)
  + 4 Funding-адаптера (+ Hyperliquid)
  + 3 Universe-адаптера (Binance, Bybit, Hyperliquid)
```
