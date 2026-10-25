# cdpify Review: Performance, Bugs und Developer Experience

Stand: 2026-10-25, Version 0.3.0

Erledigte Aufgaben sind entfernt; Änderungen und API-Brüche stehen in `CHANGELOG.md`.

## Offene Umsetzungspunkte

- [ ] Direkte Event-Zustellung als optionale Transport-Fähigkeit.
- [ ] Optionales `cdpify[orjson]` mit JSON-Fallback, Tests und CI-Integration.

## Bisherige Messwerte

| Messung | Wert |
| --- | --- |
| Generierte Dataclasses | 1.373 |
| Größe von `cdpify/domains/` | 4,4 MB |
| `encode_cdp(NavigateParams(...))` | 0,7 µs |

---

## Bewusste Entscheidungen

### Unabhängige Event-Modelle pro Listener

Hören mehrere Listener auf dasselbe Event mit demselben Typ, wird es für jeden
Listener separat decodiert. Ein Cache würde mutable Dataclass-Instanzen teilen:
Änderungen eines Listeners wären bei anderen sichtbar. Der Decoder ist bereits
vorkompiliert; unabhängige Modelle sind die zusätzliche Decodierung wert.

### Öffentliche Params-Dataclasses bleiben

Die Params-Dataclasses wegoptimieren und direkt Dicts generieren: Encoden kostet ~0,7 µs,
ein CDP-Roundtrip dauert Millisekunden. Die Dataclasses sind öffentliche, nützliche Typen.

### Generierte Typaliase behalten ihre Semantik

- **Gemischte Alias-Syntax:** `FrameId = str` neben `type AdFrameType = Literal[...]`.
  Der Codec entpackt `type`-Aliase inzwischen, das ist also nur noch eine Stilfrage.
  Eine Vereinheitlichung auf `type` würde `FrameId("...")` und `isinstance` brechen und
  bringt wenig.

### Öffentliche Executor-Schnittstelle bleibt

- `CommandExecutor` steht in `cdpify.__all__`, obwohl Nutzer es kaum brauchen. Es ist aber
  der Typ, den generierte Domain-Klassen im Konstruktor erwarten. Daher drin lassen.
- `CdpClient.execute` ruft absichtlich `self._transport` direkt auf, weil es eine
  beliebige `session_id` annimmt. Der `BoundCommandExecutor` ist an eine Session gebunden.
