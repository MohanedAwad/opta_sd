from __future__ import annotations

from datetime import datetime

from ..core import Core, _format_date


class Match(Core):
    _endpoint = "match"

    def resource(self, match_id: str) -> "Match":
        self._resource_id = match_id; return self

    def fixture(self, match_id: str) -> "Match":
        self._feed_params["fx"] = match_id; return self

    def tournament(self, tournament_id: str) -> "Match":
        self._feed_params["tmcl"] = tournament_id; return self

    def stage(self, stage_id: str) -> "Match":
        self._feed_params["stg"] = stage_id; return self

    def competition(self, competition_id: str) -> "Match":
        self._feed_params["comp"] = competition_id; return self

    def contestant(self, contestant_id: str) -> "Match":
        self._feed_params["ctst"] = contestant_id; return self

    def live(self, value: bool = True) -> "Match":
        self._feed_params["live"] = "yes" if value else "no"; return self

    def lineups(self, value: bool = True) -> "Match":
        self._feed_params["lineups"] = "yes" if value else "no"; return self

    def status(self, value: str) -> "Match":
        _valid = {"all", "fixture", "played", "playing", "cancelled", "postponed", "suspended"}
        if value not in _valid:
            raise ValueError(f"Invalid status {value!r}. Choose from: {_valid}")
        self._feed_params["status"] = value; return self

    def time_range(self, from_dt: datetime, to_dt: datetime) -> "Match":
        self._feed_params["startDate"] = _format_date(from_dt)
        self._feed_params["endDate"]   = _format_date(to_dt)
        return self


class MatchStatistics(Core):
    _endpoint = "matchstats"

    def resource(self, match_id: str) -> "MatchStatistics":
        self._resource_id = match_id; return self

    def fixture(self, match_id: str) -> "MatchStatistics":
        self._feed_params["fx"] = match_id; return self

    def detailed(self, value: bool = True) -> "MatchStatistics":
        self._feed_params["detailed"] = "yes" if value else "no"; return self


class MatchEvent(Core):
    _endpoint = "matchevent"

    def resource(self, match_id: str) -> "MatchEvent":
        self._resource_id = match_id; return self

    def fixture(self, match_id: str) -> "MatchEvent":
        self._feed_params["fx"] = match_id; return self


class PassMatrix(Core):
    _endpoint = "passmatrix"

    def resource(self, match_id: str) -> "PassMatrix":
        self._resource_id = match_id; return self

    def fixture(self, match_id: str) -> "PassMatrix":
        self._feed_params["fx"] = match_id; return self


class Possession(Core):
    _endpoint = "possession"

    def resource(self, match_id: str) -> "Possession":
        self._resource_id = match_id; return self

    def fixture(self, match_id: str) -> "Possession":
        self._feed_params["fx"] = match_id; return self


class Commentary(Core):
    _endpoint = "commentary"

    def resource(self, match_id: str) -> "Commentary":
        self._resource_id = match_id; return self

    def fixture(self, match_id: str) -> "Commentary":
        self._feed_params["fx"] = match_id; return self

    def type(self, value: str) -> "Commentary":
        _valid = {"auto", "fallback", "manual"}
        if value not in _valid:
            raise ValueError(f"Invalid type {value!r}. Choose from: {_valid}")
        self._feed_params["type"] = value; return self

    def auto(self)     -> "Commentary": return self.type("auto")
    def fallback(self) -> "Commentary": return self.type("fallback")
    def manual(self)   -> "Commentary": return self.type("manual")


class MatchFacts(Core):
    _endpoint = "matchfacts"

    def resource(self, match_id: str) -> "MatchFacts":
        self._resource_id = match_id; return self

    def fixture(self, match_id: str) -> "MatchFacts":
        self._feed_params["fx"] = match_id; return self


class SeasonalStats(Core):
    _endpoint = "seasonstats"

    def competition(self, competition_id: str) -> "SeasonalStats":
        self._feed_params["comp"] = competition_id; return self

    def tournament(self, tournament_id: str) -> "SeasonalStats":
        self._feed_params["tmcl"] = tournament_id; return self

    def contestant(self, contestant_id: str) -> "SeasonalStats":
        self._feed_params["ctst"] = contestant_id; return self


class Squads(Core):
    _endpoint = "squads"

    def tournament(self, tournament_id: str) -> "Squads":
        self._feed_params["tmcl"] = tournament_id; return self

    def contestant(self, contestant_id: str) -> "Squads":
        self._feed_params["ctst"] = contestant_id; return self

    def detailed(self, value: bool = True) -> "Squads":
        self._feed_params["detailed"] = "yes" if value else "no"; return self

    def people(self, value: bool = True) -> "Squads":
        self._feed_params["people"] = "yes" if value else "no"; return self


class TeamStandings(Core):
    _endpoint = "standings"

    def stage(self, stage_id: str) -> "TeamStandings":
        self._feed_params["stg"] = stage_id; return self

    def tournament(self, tournament_id: str) -> "TeamStandings":
        self._feed_params["tmcl"] = tournament_id; return self

    def live(self, value: bool = True) -> "TeamStandings":
        self._feed_params["live"] = "yes" if value else "no"; return self

    def type(self, value: str) -> "TeamStandings":
        _valid = {"total", "home", "away", "form-total", "form-home", "form-away"}
        if value not in _valid:
            raise ValueError(f"Invalid type {value!r}. Choose from: {_valid}")
        self._feed_params["type"] = value; return self

    def total(self)      -> "TeamStandings": return self.type("total")
    def home(self)       -> "TeamStandings": return self.type("home")
    def away(self)       -> "TeamStandings": return self.type("away")
    def form_total(self) -> "TeamStandings": return self.type("form-total")
    def form_home(self)  -> "TeamStandings": return self.type("form-home")
    def form_away(self)  -> "TeamStandings": return self.type("form-away")


class PlayerCareer(Core):
    _endpoint = "playercareer"

    def resource(self, person_id: str) -> "PlayerCareer":
        self._resource_id = person_id; return self

    def person(self, person_id: str) -> "PlayerCareer":
        return self.resource(person_id)

    def contestant(self, contestant_id: str) -> "PlayerCareer":
        self._feed_params["ctst"] = contestant_id; return self

    def active(self, value: bool = True) -> "PlayerCareer":
        self._feed_params["active"] = "yes" if value else "no"; return self


class TournamentCalendar(Core):
    _endpoint = "tournamentcalendar"

    def competition(self, competition_id: str) -> "TournamentCalendar":
        self._feed_params["comp"] = competition_id; return self

    def active(self, value: bool = True) -> "TournamentCalendar":
        self._feed_params["active"] = "yes" if value else "no"; return self

    def authorized(self, value: bool = True) -> "TournamentCalendar":
        self._feed_params["authorized"] = "yes" if value else "no"; return self


class MatchPreview(Core):
    _endpoint = "matchpreview"

    def resource(self, match_id: str) -> "MatchPreview":
        self._resource_id = match_id; return self

    def fixture(self, match_id: str) -> "MatchPreview":
        self._feed_params["fx"] = match_id; return self


class Rankings(Core):
    _endpoint = "rankings"

    def resource(self, tournament_id: str) -> "Rankings":
        self._resource_id = tournament_id; return self

    def tournament(self, tournament_id: str) -> "Rankings":
        return self.resource(tournament_id)


class TournamentSchedule(Core):
    _endpoint = "tournamentschedule"

    def resource(self, tournament_id: str) -> "TournamentSchedule":
        self._resource_id = tournament_id; return self

    def tournament(self, tournament_id: str) -> "TournamentSchedule":
        return self.resource(tournament_id)


class Venues(Core):
    _endpoint = "venues"

    def venue(self, venue_id: str) -> "Venues":
        self._feed_params["venue"] = venue_id; return self

    def tournament(self, tournament_id: str) -> "Venues":
        self._feed_params["tmcl"] = tournament_id; return self

    def contestant(self, contestant_id: str) -> "Venues":
        self._feed_params["ctst"] = contestant_id; return self