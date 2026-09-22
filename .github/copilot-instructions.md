# Cricsheet JSON Data Format

This document is a practical reference for the Cricsheet JSON match
format (version **1.2.0**). It describes the hierarchy and the fields
needed to interpret a match from metadata down to individual deliveries.

## 1. Top-level structure

A match JSON file is organized around three main sections:

``` json
{
  "meta": {},
  "info": {},
  "innings": []
}
```

-   `meta`: describes the data file itself.
-   `info`: describes the match and its participants.
-   `innings`: contains the ball-by-ball match data.

------------------------------------------------------------------------

## 2. `meta`

The `meta` object contains metadata about the JSON data file.

``` json
"meta": {
  "data_version": "1.2.0",
  "created": "2020-07-06",
  "revision": 1
}
```

### Fields

  ------------------------------------------------------------------------
  Field            Type                          Required Meaning
  ---------------- ---------------- --------------------- ----------------
  `data_version`   string                             Yes Version of the
                                                          Cricsheet JSON
                                                          format.

  `created`        string                             Yes Date the data
                                                          file was first
                                                          created, in
                                                          `YYYY-MM-DD`
                                                          format.

  `revision`       integer                            Yes Revision number
                                                          of the file for
                                                          that data
                                                          version.
  ------------------------------------------------------------------------

------------------------------------------------------------------------

# 3. `info`

`info` contains information about the actual match.

A simplified example:

``` json
"info": {
  "balls_per_over": 6,
  "venue": "Daren Sammy National Cricket Stadium, Gros Islet",
  "dates": ["2016-07-26"],
  "event": {
    "name": "Caribbean Premier League",
    "match_number": 24
  },
  "gender": "male",
  "teams": [
    "St Lucia Zouks",
    "Trinbago Knight Riders"
  ],
  "outcome": {
    "winner": "Trinbago Knight Riders",
    "by": {
      "wickets": 3
    }
  },
  "toss": {
    "decision": "field",
    "winner": "Trinbago Knight Riders"
  },
  "player_of_match": ["Umar Akmal"],
  "match_type": "T20",
  "overs": 20,
  "team_type": "club",
  "registry": {
    "people": {}
  },
  "city": "St Lucia",
  "players": {},
  "season": "2016"
}
```

## Important `info` fields

  ---------------------------------------------------------------------------------
  Field                 Type                          Required Meaning
  --------------------- ---------------- --------------------- --------------------
  `balls_per_over`      integer                            Yes Expected number of
                                                               balls in an over,
                                                               normally 6.

  `bowl_out`            array                               No Balls used in a
                                                               bowl-out, if
                                                               applicable.

  `city`                string                              No City where the match
                                                               took place.

  `dates`               array                              Yes One or more match
                                                               dates, always
                                                               represented as an
                                                               array.

  `event`               object                              No Competition/series
                                                               information.

  `gender`              string                             Yes Gender of the
                                                               players in the
                                                               match.

  `match_type`          string                             Yes Match type such as
                                                               `Test`, `ODI`,
                                                               `T20`, `IT20`,
                                                               `ODM`, or `MDM`.

  `match_type_number`   integer                             No Number of this match
                                                               type when available.

  `missing`             array                               No Information known to
                                                               be missing from the
                                                               data.

  `officials`           object                              No Match officials and
                                                               their roles.

  `outcome`             object                             Yes Result of the match.

  `overs`               integer                             No Scheduled number of
                                                               overs where
                                                               applicable.

  `player_of_match`     array                               No Player(s) of the
                                                               match.

  `players`             object                             Yes Players officially
                                                               involved for each
                                                               team.

  `registry`            object                             Yes Stable IDs for
                                                               people mentioned in
                                                               the file.

  `season`              string                             Yes Season in which the
                                                               match took place.

  `supersubs`           object                             Yes Supersub
                                                               information.

  `team_type`           string                             Yes `international` or
                                                               `club`.

  `teams`               array                              Yes The two teams
                                                               playing the match.

  `toss`                object                             Yes Toss winner and
                                                               decision.

  `venue`               string                              No Venue where the
                                                               match took place.
  ---------------------------------------------------------------------------------

------------------------------------------------------------------------

# 4. Dates

`dates` is always an array, even for a one-day match.

``` json
"dates": [
  "2016-07-26"
]
```

A multi-day match can contain several dates:

``` json
"dates": [
  "2018-03-01",
  "2018-03-02",
  "2018-03-03",
  "2018-03-04",
  "2018-03-05"
]
```

Each date uses:

``` text
YYYY-MM-DD
```

------------------------------------------------------------------------

# 5. Event

`event` identifies the competition or series.

``` json
"event": {
  "name": "Caribbean Premier League",
  "match_number": 24
}
```

Possible fields:

  Field            Type      Meaning
  ---------------- --------- --------------------------------------------------
  `name`           string    Name of the event. Required when `event` exists.
  `match_number`   integer   Match number within the event/series.
  `group`          string    Group in which the match occurred.
  `stage`          string    Stage of the event, such as `Final`.

------------------------------------------------------------------------

# 6. Outcome

`outcome` describes how the match ended.

## Win by wickets

``` json
"outcome": {
  "winner": "Trinbago Knight Riders",
  "by": {
    "wickets": 3
  }
}
```

## Win by runs

``` json
"outcome": {
  "winner": "Australia",
  "by": {
    "runs": 118
  }
}
```

## Win by innings and runs

``` json
"outcome": {
  "winner": "England",
  "by": {
    "innings": 1,
    "runs": 209
  }
}
```

## Tie

``` json
"outcome": {
  "result": "tie",
  "eliminator": "Kings XI Punjab"
}
```

## No result

``` json
"outcome": {
  "result": "no result"
}
```

### Outcome fields

  -----------------------------------------------------------------------
  Field                   Type                    Meaning
  ----------------------- ----------------------- -----------------------
  `winner`                string                  Winning team, when a
                                                  team won.

  `by`                    object                  Margin of victory.

  `result`                string                  `draw`, `no result`, or
                                                  `tie` when applicable.

  `eliminator`            string                  Winner of an
                                                  elimination super-over.

  `bowl_out`              string                  Winner of a bowl-out.

  `method`                string                  Method used to
                                                  determine the result in
                                                  unusual/curtailed
                                                  circumstances.
  -----------------------------------------------------------------------

`by` can contain:

``` json
{
  "runs": 118
}
```

or:

``` json
{
  "wickets": 3
}
```

or:

``` json
{
  "innings": 1,
  "runs": 209
}
```

------------------------------------------------------------------------

# 7. Toss

``` json
"toss": {
  "winner": "Trinbago Knight Riders",
  "decision": "field"
}
```

Fields:

  ------------------------------------------------------------------------
  Field            Type                          Required Meaning
  ---------------- ---------------- --------------------- ----------------
  `winner`         string                             Yes Team that won
                                                          the toss.

  `decision`       string                             Yes `bat` or
                                                          `field`.

  `uncontested`    boolean                             No Indicates that
                                                          the toss was not
                                                          contested.
  ------------------------------------------------------------------------

------------------------------------------------------------------------

# 8. Players

`players` maps each team name to the players officially involved in the
match.

``` json
"players": {
  "Australia": [
    "M Klinger",
    "AJ Finch",
    "BR Dunk"
  ],
  "Sri Lanka": [
    "N Dickwella",
    "WU Tharanga",
    "EMDY Munaweera"
  ]
}
```

This can include the starting XI as well as supersubs, concussion
substitutes, COVID replacements, and other replacements.

------------------------------------------------------------------------

# 9. Registry

The registry maps the names used in the match data to stable person
identifiers.

``` json
"registry": {
  "people": {
    "AJ Finch": "b8d490fd",
    "AJ Turner": "ff1e12a0"
  }
}
```

The same person has the same identifier across matches.

The identifier in this format is an 8-character string consisting of
digits and lowercase letters `a-f`.

Names in the registry are the names used throughout the match file,
whether the person appears as a batter, bowler, fielder, official, or
another participant.

------------------------------------------------------------------------

# 10. Officials

Officials are grouped by role:

``` json
"officials": {
  "match_referees": ["JJ Crowe"],
  "reserve_umpires": ["MW Graham-Smith"],
  "tv_umpires": ["P Wilson"],
  "umpires": ["SD Fry", "SJ Nogajski"]
}
```

Supported roles are:

-   `match_referees`
-   `reserve_umpires`
-   `tv_umpires`
-   `umpires`

------------------------------------------------------------------------

# 11. Bowl-out

A bowl-out is represented as an array containing one entry for each
attempted delivery.

``` json
"bowl_out": [
  {
    "bowler": "V Sehwag",
    "outcome": "hit"
  },
  {
    "bowler": "Yasir Arafat",
    "outcome": "miss"
  }
]
```

Each entry contains:

  Field       Type     Meaning
  ----------- -------- -----------------------------------------
  `bowler`    string   Bowler who delivered the bowl-out ball.
  `outcome`   string   `hit` or `miss`.

------------------------------------------------------------------------

# 12. `innings`

The `innings` field is an array.

Each element represents one innings in chronological order.

``` json
"innings": [
  {
    "team": "Ireland",
    "overs": []
  },
  {
    "team": "India",
    "overs": []
  }
]
```

The main hierarchy is:

``` text
match
└── innings[]
    └── overs[]
        └── deliveries[]
            ├── batter
            ├── bowler
            ├── non_striker
            ├── runs
            ├── extras
            ├── wickets
            ├── review
            └── replacements
```

This is the most important structure for ball-by-ball analysis.

------------------------------------------------------------------------

# 13. Innings fields

  -----------------------------------------------------------------------
  Field                   Type                    Meaning
  ----------------------- ----------------------- -----------------------
  `team`                  string                  Team batting in this
                                                  innings. Required.

  `overs`                 array                   Overs played in the
                                                  innings.

  `absent_hurt`           array                   Players absent hurt.

  `penalty_runs`          object                  Penalty runs added
                                                  before/after the
                                                  innings.

  `declared`              boolean                 Whether the innings was
                                                  declared.

  `forfeited`             boolean                 Whether the innings was
                                                  forfeited.

  `powerplays`            array                   Powerplay information.

  `miscounted_overs`      object                  Details of overs with
                                                  an incorrect number of
                                                  deliveries.

  `target`                object                  Target runs and
                                                  available
                                                  overs/deliveries.

  `super_over`            boolean                 Whether this innings
                                                  was a super over.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 14. Penalty runs

Penalty runs applied before the innings:

``` json
"penalty_runs": {
  "pre": 5
}
```

Penalty runs applied after the innings:

``` json
"penalty_runs": {
  "post": 6
}
```

Penalty runs that occur on a particular delivery are represented in that
delivery's `extras` instead.

------------------------------------------------------------------------

# 15. Powerplays

Powerplays are an array of objects:

``` json
"powerplays": [
  {
    "from": 0.1,
    "to": 5.6,
    "type": "mandatory"
  }
]
```

Fields:

  Field    Type     Meaning
  -------- -------- ------------------------------------------
  `from`   number   First delivery covered by the powerplay.
  `to`     number   Final delivery covered by the powerplay.
  `type`   string   `batting`, `fielding`, or `mandatory`.

------------------------------------------------------------------------

# 16. Miscounted overs

A miscounted over is represented as an object whose keys are over
numbers.

``` json
"miscounted_overs": {
  "36": {
    "balls": 5,
    "umpire": "AV Jayaprakash"
  }
}
```

Fields:

  Field      Type     Meaning
  ---------- -------- ---------------------------------------
  `balls`    number   Number of deliveries actually bowled.
  `umpire`   string   Umpire responsible, if known.

------------------------------------------------------------------------

# 17. Target

A target specifies how many runs must be chased and within how many
overs/deliveries.

``` json
"target": {
  "overs": 20,
  "runs": 151
}
```

For a weather-affected match:

``` json
"target": {
  "overs": 35.1,
  "runs": 253
}
```

Fields:

  Field     Type      Meaning
  --------- --------- -----------------------------
  `overs`   number    Available overs/deliveries.
  `runs`    integer   Runs to be chased.

------------------------------------------------------------------------

# 18. Overs

An innings contains an array of overs.

``` json
"overs": [
  {
    "over": 0,
    "deliveries": [
      {}
    ]
  }
]
```

Each over contains:

  Field          Type       Required Meaning
  -------------- -------- ---------- --------------------------------
  `over`         number          Yes Over number.
  `deliveries`   array           Yes Deliveries bowled in the over.

------------------------------------------------------------------------

# 19. Deliveries

A delivery is the fundamental ball-by-ball unit.

Example:

``` json
{
  "actual_delivery": "12.3",
  "batter": "MJ Prior",
  "bowler": "Harbhajan Singh",
  "non_striker": "AJ Strauss",
  "runs": {
    "batter": 0,
    "extras": 0,
    "total": 0
  },
  "wickets": [
    {
      "kind": "lbw",
      "player_out": "MJ Prior"
    }
  ]
}
```

Required delivery fields:

  Field               Type       Required Meaning
  ------------------- -------- ---------- ----------------------------------
  `actual_delivery`   string          Yes Actual delivery number.
  `batter`            string          Yes Batter facing the ball.
  `bowler`            string          Yes Bowler delivering the ball.
  `non_striker`       string          Yes Batter at the non-striker's end.
  `runs`              object          Yes Runs scored from the delivery.

Optional delivery fields:

-   `extras`
-   `replacements`
-   `review`
-   `wickets`

------------------------------------------------------------------------

# 20. `actual_delivery`

`actual_delivery` represents the actual delivery number and accounts for
wides and no-balls.

For example, if a delivery is a wide, the next legal delivery can have
the same `actual_delivery` over number as the previous recorded attempt.

Example:

``` json
{
  "actual_delivery": "0.1",
  "batter": "WTS Porterfield",
  "bowler": "IK Pathan",
  "runs": {
    "batter": 0,
    "extras": 1,
    "total": 1
  },
  "extras": {
    "wides": 1
  }
}
```

The next delivery may therefore also have:

``` json
"actual_delivery": "0.1"
```

------------------------------------------------------------------------

# 21. Extras

Extras are represented only when they occurred.

``` json
"extras": {
  "wides": 1
}
```

Possible types are:

  Key         Meaning
  ----------- ---------------
  `byes`      Bye runs.
  `legbyes`   Leg-bye runs.
  `noballs`   No-ball runs.
  `penalty`   Penalty runs.
  `wides`     Wide runs.

Multiple types can occur on a delivery when applicable.

Example:

``` json
"extras": {
  "noballs": 1,
  "wides": 2
}
```

Only extra types that actually occurred are included.

------------------------------------------------------------------------

# 22. Runs

Every delivery has a `runs` object.

``` json
"runs": {
  "batter": 4,
  "extras": 0,
  "total": 4
}
```

Fields:

  ------------------------------------------------------------------------
  Field            Type                          Required Meaning
  ---------------- ---------------- --------------------- ----------------
  `batter`         integer                            Yes Runs scored by
                                                          the batter.

  `extras`         integer                            Yes Runs scored as
                                                          extras.

  `total`          integer                            Yes Total runs from
                                                          the delivery.

  `non_boundary`   boolean                             No Indicates that a
                                                          4 or 6 was not
                                                          an actual
                                                          boundary.
  ------------------------------------------------------------------------

The fundamental relationship is:

``` text
total = batter + extras
```

For example:

``` json
"runs": {
  "batter": 1,
  "extras": 2,
  "total": 3
}
```

A four that was not an actual boundary:

``` json
"runs": {
  "batter": 4,
  "extras": 0,
  "total": 4,
  "non_boundary": true
}
```

------------------------------------------------------------------------

# 23. Wickets

If a wicket occurs, `wickets` is an array.

``` json
"wickets": [
  {
    "kind": "caught",
    "player_out": "MS Dhoni",
    "fielders": [
      {
        "name": "Shoaib Malik"
      }
    ]
  }
]
```

A wicket entry contains:

  Field          Type       Required Meaning
  -------------- -------- ---------- ------------------------------
  `kind`         string          Yes Type of dismissal.
  `player_out`   string          Yes Dismissed player.
  `fielders`     array            No Fielders involved, if known.

Supported dismissal kinds in this format include:

-   `bowled`
-   `caught`
-   `caught and bowled`
-   `lbw`
-   `stumped`
-   `run out`
-   `retired hurt`
-   `hit wicket`
-   `obstructing the field`
-   `hit the ball twice`
-   `handled the ball`
-   `timed out`

Normally a delivery has at most one wicket entry, but the format permits
multiple wicket entries for unusual situations.

------------------------------------------------------------------------

# 24. Fielders

When a dismissal involves fielders, they appear inside `fielders`.

Caught example:

``` json
"fielders": [
  {
    "name": "Shoaib Malik"
  }
]
```

Run-out example:

``` json
"fielders": [
  {
    "name": "KP Pietersen"
  },
  {
    "name": "MJ Prior"
  }
]
```

------------------------------------------------------------------------

# 25. Reviews

A delivery can contain a `review` object.

``` json
"review": {
  "by": "England",
  "umpire": "AG Wharf",
  "batter": "Imam-ul-Haq",
  "decision": "upheld"
}
```

Fields:

  ------------------------------------------------------------------------
  Field            Type                          Required Meaning
  ---------------- ---------------- --------------------- ----------------
  `by`             string                             Yes Team requesting
                                                          the review.

  `umpire`         string                              No Umpire whose
                                                          decision was
                                                          reviewed.

  `batter`         string                             Yes Batter for whom
                                                          the decision was
                                                          reviewed.

  `decision`       string                             Yes `struck down` or
                                                          `upheld`.

  `umpires_call`   boolean                             No Indicates a
                                                          review was
                                                          struck down
                                                          because of
                                                          umpire's call.
  ------------------------------------------------------------------------

------------------------------------------------------------------------

# 26. Replacements

`replacements` records player changes that occurred before a delivery.

It can contain:

``` json
"replacements": {
  "match": [],
  "role": []
}
```

There are two types.

## Match replacements

A player completely replaces another player in the match.

``` json
"match": [
  {
    "in": "CP Tremain",
    "out": "DR Sams",
    "team": "Sydney Thunder",
    "reason": "concussion_substitute"
  }
]
```

Fields:

-   `in`: player coming in.
-   `out`: player going out.
-   `team`: affected team.
-   `reason`: reason for replacement.

Possible match-replacement reasons include:

-   `concussion_substitute`
-   `covid_replacement`
-   `injury_substitute`
-   `national_callup`
-   `national_release`
-   `supersub`
-   `tactical_substitute`
-   `unknown`

## Role replacements

A player replaces another player only in a particular role.

``` json
"role": [
  {
    "in": "GH Dockrell",
    "out": "DC Delany",
    "reason": "injury",
    "role": "bowler"
  }
]
```

The `role` is currently either:

``` text
batter
bowler
```

------------------------------------------------------------------------

# 27. Missing information

The `missing` field records information known to be absent rather than
simply omitting it silently.

Simple example:

``` json
"missing": [
  "player_of_match",
  "umpires",
  "reviews"
]
```

It can also describe missing powerplay information:

``` json
"missing": [
  {
    "powerplays": {
      "1": [
        "batting"
      ],
      "2": [
        "batting"
      ]
    }
  }
]
```

Known string values include:

-   `player_of_match`
-   `umpires`
-   `reviews`

Powerplay entries can identify missing:

-   `mandatory`
-   `batting`
-   `fielding`

------------------------------------------------------------------------

# 28. Reading a match programmatically

For most ball-by-ball analysis, the important traversal is:

``` python
for innings in match["innings"]:
    batting_team = innings["team"]

    for over in innings.get("overs", []):
        over_number = over["over"]

        for delivery in over["deliveries"]:
            batter = delivery["batter"]
            bowler = delivery["bowler"]
            non_striker = delivery["non_striker"]

            runs = delivery["runs"]["total"]
```

Extras and wickets should be handled separately:

``` python
extras = delivery.get("extras", {})
wickets = delivery.get("wickets", [])
```

This is preferable to assuming optional fields always exist.

------------------------------------------------------------------------

# 29. Conceptual data model

The format can be understood as:

``` text
MATCH
│
├── meta
│   ├── data_version
│   ├── created
│   └── revision
│
├── info
│   ├── teams
│   ├── dates
│   ├── venue
│   ├── event
│   ├── toss
│   ├── outcome
│   ├── players
│   ├── registry
│   ├── officials
│   └── ...
│
└── innings[]
    │
    ├── team
    ├── target
    ├── powerplays
    ├── penalty_runs
    │
    └── overs[]
        │
        ├── over
        │
        └── deliveries[]
            │
            ├── actual_delivery
            ├── batter
            ├── bowler
            ├── non_striker
            ├── runs
            │   ├── batter
            │   ├── extras
            │   ├── total
            │   └── non_boundary
            │
            ├── extras
            ├── wickets[]
            ├── review
            └── replacements
```

## 30. Important implementation notes

1.  **Optional fields must be checked before accessing them.** For
    example, not every delivery has `extras`, `wickets`, `review`, or
    `replacements`.

2.  **`runs.total` includes both batter runs and extras.**

3.  **The over number is zero-based.** An over represented as
    `"over": 0` is the first over.

4.  **Do not treat the apparent ball suffix as a simple legal-ball
    counter.** Wides and no-balls can cause the same `actual_delivery`
    value to appear more than once.

5.  **Team names are used as keys in several objects**, including
    `players`, `supersubs`, and some other match-level structures.

6.  **The registry should be used when stable player identity matters
    across matches.** Names are the identifiers used within the match
    data, while registry IDs provide stable identity across matches.

7.  **Missing data is explicitly representable.** An omitted optional
    field and an entry in `missing` do not necessarily mean the same
    thing.

## 31. Format version

The supplied documentation describes JSON format version **1.2.0**. The
changelog states that version 1.2.0 added `actual_delivery` as a
required field within deliveries. Version 1.1.0 added `uncontested` to
`toss` and `forfeited` to innings. Version 1.0.0 was the initial JSON
version.
