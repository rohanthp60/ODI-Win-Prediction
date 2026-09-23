import pytest

from src.data.preprocess import (
    insert_labels,
    is_extra,
    process_data,
    process_first_innings,
    process_second_innings,
)


def delivery(total, extras=None, wickets=None):
    result = {"runs": {"total": total}}
    if extras:
        result["extras"] = extras
    if wickets:
        result["wickets"] = wickets
    return result


def over(deliveries, over_number=0):
    return {"over": over_number, "deliveries": deliveries}


def innings(overs, team="Team A", target=None):
    result = {
        "team": team,
        "overs": overs,
    }
    if target is not None:
        result["target"] = target
    return result


def test_is_extra_only_treats_wides_and_no_balls_as_non_legal_balls():
    assert is_extra({"runs": {"total": 0}}) is False
    assert is_extra({"runs": {"total": 1}, "extras": {"byes": 1}}) is False
    assert is_extra({"runs": {"total": 1}, "extras": {"wides": 1}}) is True
    assert is_extra({"runs": {"total": 1}, "extras": {"noballs": 1}}) is True


def test_process_first_innings_tracks_runs_wickets_and_legal_balls():
    first_innings = innings(
        [
            over(
                [
                    delivery(1),
                    delivery(2, extras={"wides": 1}),
                    delivery(1),
                    delivery(0, wickets=[{"kind": "bowled", "player_out": "Batter"}]),
                    delivery(
                        0,
                        wickets=[
                            {"kind": "run out", "player_out": "Batter 1"},
                            {"kind": "run out", "player_out": "Batter 2"},
                        ],
                    ),
                    delivery(0),
                    delivery(1, extras={"byes": 1}),
                ]
            ),
            over(
                [
                    delivery(0),
                    delivery(0, extras={"noballs": 1}),
                    delivery(0, extras={"wides": 1}),
                    delivery(0),
                    delivery(4),
                    delivery(6),
                    delivery(0, wickets=[{"kind": "caught", "player_out": "Batter"}]),
                    delivery(0),
                ]
            )
        ]
    )

    assert process_first_innings(first_innings) == [
        {"runs": 1, "wickets": 0, "balls": 1},
        {"runs": 3, "wickets": 0, "balls": 1},
        {"runs": 4, "wickets": 0, "balls": 2},
        {"runs": 4, "wickets": 1, "balls": 3},
        {"runs": 4, "wickets": 3, "balls": 4},
        {"runs": 4, "wickets": 3, "balls": 5},
        {"runs": 5, "wickets": 3, "balls": 6},
        {"runs": 5, "wickets": 3, "balls": 7},
        {"runs": 5, "wickets": 3, "balls": 7},
        {"runs": 5, "wickets": 3, "balls": 7},
        {"runs": 5, "wickets": 3, "balls": 8},
        {"runs": 9, "wickets": 3, "balls": 9},
        {"runs": 15, "wickets": 3, "balls": 10},
        {"runs": 15, "wickets": 4, "balls": 11},
        {"runs": 15, "wickets": 4, "balls": 12},
    ]


def test_process_second_innings_counts_down_from_target():
    second_innings = innings(
        [
            over(
                [
                    delivery(4),
                    delivery(1, extras={"noballs": 1}),
                    delivery(0, wickets=[{"kind": "caught", "player_out": "Batter"}]),
                ]
            ),
            over(
                [
                    delivery(0),
                    delivery(0, extras={"noballs": 1}),
                    delivery(0, extras={"wides": 1}),
                    delivery(0),
                    delivery(4),
                    delivery(6),
                    delivery(0, wickets=[{"kind": "caught", "player_out": "Batter"}]),
                    delivery(0),
                ],
                over_number=1,
            ),
        ],
        team="Team B",
        target={"runs": 20, "overs": 50},
    )

    assert process_second_innings(second_innings) == [
        {"runs": 16, "wickets": 10, "balls": 299},
        {"runs": 15, "wickets": 10, "balls": 299},
        {"runs": 15, "wickets": 9, "balls": 298},
        {"runs": 15, "wickets": 9, "balls": 297},
        {"runs": 15, "wickets": 9, "balls": 297},
        {"runs": 15, "wickets": 9, "balls": 297},
        {"runs": 15, "wickets": 9, "balls": 296},
        {"runs": 11, "wickets": 9, "balls": 295},
        {"runs": 5, "wickets": 9, "balls": 294},
        {"runs": 5, "wickets": 8, "balls": 293},
        {"runs": 5, "wickets": 8, "balls": 292},
    ]


def test_process_second_innings_requires_target():
    with pytest.raises(AssertionError, match="must contain a target"):
        process_second_innings(innings([]))


def test_insert_labels_mutates_and_returns_states():
    states = [{"runs": 3}, {"runs": 7}]

    result = insert_labels(states, 1)

    assert result is states
    assert result == [{"runs": 3, "label": 1}, {"runs": 7, "label": 1}]


def test_process_data_labels_states_by_first_innings_winner():
    match = {
        "innings": [
            innings([over([delivery(4)])], team="Team A"),
            innings(
                [over([delivery(2)])],
                team="Team B",
                target={"runs": 4, "overs": 50},
            ),
        ],
        "info": {"outcome": {"winner": "Team A"}},
    }

    first_innings_data, second_innings_data = process_data([match])

    assert first_innings_data == [{"runs": 4, "wickets": 0, "balls": 1, "label": 1}]
    assert second_innings_data == [{"runs": 2, "wickets": 10, "balls": 299, "label": 1}]