# opta_sd

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://pypi.org/project/opta_sd/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Python client for the **OPTA Sports Data Soccer API (OPTA SDAPI)**.  

---

## Installation

```bash
pip install optasd
```

Or from source:

```bash
git clone https://github.com/MohanedAwad/opta_sd
cd opta_sd
pip install -e ".[dev]"
```

---

## Configuration

### Environment variables

```bash
API_URL=https://api.performfeeds.com
API_TOKEN=your-token-here
REFERER_DOMAIN=https://{your-referer}.com
```

---

## Quick Start

```python
from opta_sd.soccer import Match, TournamentCalendar, TeamStandings
from opta_sd.cache import MemoryCache
from datetime import datetime, timedelta

# Basic match lookup
match = await Match().resource("bsu6pjne1eqz2hs8r3685vbhl").live().lineups().get()
print(match.data)

# Competition matches within a time window
now = datetime.utcnow()
matches = await (
    Match()
    .competition("722fdbecxzcq9788l6jqclzlw")
    .time_range(now - timedelta(days=1), now + timedelta(days=1))
    .get()
)

# With in-memory caching (60-second TTL)
standings = (
    TeamStandings(cache=MemoryCache(ttl=60))
    .tournament("408bfjw6uz5k19zk4am50ykmh")
    .total()
    .get()
)
print(standings.from_cache)       # False on first call
print(standings.response_time_ms) # round-trip time in ms
```

---

## Available Feeds

| Feed                         | Class                      | Endpoint                           |
|------------------------------|----------------------------|------------------------------------|
| Fixtures & Results           | `Match`               | `/soccerdata/match/`               |
| Match Statistics             | `MatchStatistics`     | `/soccerdata/matchstats/`          |
| Match Events                 | `MatchEvent`          | `/soccerdata/matchevent/`          |
| Pass Matrix & Avg Formation  | `PassMatrix`          | `/soccerdata/passmatrix/`          |
| Possession                   | `Possession`          | `/soccerdata/possession/`          |
| Commentary                   | `Commentary`          | `/soccerdata/Commentary/`          |
| Match Facts                  | `MatchFacts`          | `/soccerdata/matchfacts/`          |
| Seasonal Stats               | `SeasonalStats`       | `/soccerdata/seasonstats/`         |
| Squads                       | `Squads`              | `/soccerdata/squads/`              |
| Team Standings               | `TeamStandings`       | `/soccerdata/standings/`           |
| Player Career                | `PlayerCareer`        | `/soccerdata/playercareer/`        |
| Tournament Calendars         | `TournamentCalendar`  | `/soccerdata/tournamentcalendar/`  |
| Match Preview                | `MatchPreview`        | `/soccerdata/matchpreview/`        |
| Rankings                     | `Rankings`            | `/soccerdata/rankings/`            |
| Tournament Schedule          | `TournamentSchedule`  | `/soccerdata/tournamentschedule/`  |
| Venues                       | `Venues`              | `/soccerdata/venues/`              |


---

## License

MIT — see [LICENSE](LICENSE).