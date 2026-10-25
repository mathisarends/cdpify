# cdpify Review: Performance, Bugs und Developer Experience

Stand: 2026-10-25, Version 0.3.0

Die bisherigen Review-Änderungen einschließlich
Queue-Limits, optionalem `orjson`, direkter Event-Zustellung, gemeinsamen
Listener-Methoden, der Namen `CdpClient`/`CdpSession` und einheitlicher
`type`-Aliase stehen in `CHANGELOG.md`.

Erledigte Aufgaben sind hier entfernt. API-Brüche sind erlaubt und werden im
Changelog dokumentiert.

## Offene Umsetzungspunkte

- [ ] Event-Modelle pro Event und Zieltyp einmal decodieren und zwischen
  Listenern teilen; das neue Verhalten dokumentieren und testen.

## Bisherige Messwerte

| Messung | Wert |
| --- | --- |
| Generierte Dataclasses | 1.373 |
| Größe von `cdpify/domains/` | 4,4 MB |
| `encode_cdp(NavigateParams(...))` | 0,7 µs |

---

## Bewusste Entscheidungen

### Öffentliche Params-Dataclasses bleiben

Die Params-Dataclasses wegoptimieren und direkt Dicts generieren: Encoden kostet ~0,7 µs,
ein CDP-Roundtrip dauert Millisekunden. Die Dataclasses sind öffentliche, nützliche Typen.

### Öffentliche Executor-Schnittstelle bleibt

- `CommandExecutor` steht in `cdpify.__all__`, obwohl Nutzer es kaum brauchen. Es ist aber
  der Typ, den generierte Domain-Klassen im Konstruktor erwarten. Daher drin lassen.
- `CdpClient.execute` ruft absichtlich `self._transport` direkt auf, weil es eine
  beliebige `session_id` annimmt. Der `BoundCommandExecutor` ist an eine Session gebunden.
