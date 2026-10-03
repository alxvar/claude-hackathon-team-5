-- The hub: one shared store of everything public in The Bazaar, plus the demand model's outputs.
-- Idempotent: `uv run python -m hub.setup` applies it (owner role). Raw tables are append/upsert only;
-- model tables are replaced on every model run.

create schema if not exists hub;

-- ---------------------------------------------------------------- raw, written by the collectors

-- Every public feed event, keyed by the server's id: any number of collectors can insert the same event.
create table if not exists hub.events (
    id          bigint primary key,
    tick        int not null,
    t_hours     double precision,
    type        text not null,
    scope       text,
    actor       text,
    payload     jsonb not null,
    source      text,                          -- host or file that stored it first
    ingested_at timestamptz not null default now()
);
create index if not exists events_type_tick on hub.events (type, tick);
create index if not exists events_tick on hub.events (tick);

-- One row per leaderboard refresh (the server's snapshot_tick), and one row per team in it.
create table if not exists hub.leaderboard (
    snapshot_tick int primary key,
    tick          int,
    t_hours       double precision,
    round         int,
    fetched_at    timestamptz not null default now(),
    source        text,
    data          jsonb not null
);
create table if not exists hub.team_snapshots (
    snapshot_tick  int not null,
    team           text not null,
    name           text,
    rank           int,
    score          double precision,
    negotiating    double precision,
    market         double precision,
    level          int,
    album_filled   int,
    album_slots    int,
    pages_complete int,
    luck           double precision,
    deals          int,
    venue          text,
    primary key (snapshot_tick, team)
);

-- Every offer ever seen, on any venue: from offer.listed / offer.cancelled events and from the public boards
-- (boards show makers as pseudonyms; the feed names the team).
create table if not exists hub.offers (
    id              bigint primary key,
    venue           text,
    maker           text,                      -- team id (from the feed) when known
    maker_alias     text,                      -- the board's pseudonym
    to_team         text,
    give            jsonb,
    want            jsonb,
    created_tick    int,
    expires_tick    int,
    first_seen_tick int,
    last_seen_tick  int,
    last_seen_at    timestamptz,
    status          text,                      -- open | cancelled | gone (left the board before expiry)
    closed_tick     int
);
create index if not exists offers_venue_status on hub.offers (venue, status);

-- Latest copy of each public state document (clock, schedule, levels, dealers, venues, catalog) and its history.
create table if not exists hub.state (
    kind       text primary key,
    tick       int,
    fetched_at timestamptz not null default now(),
    hash       text,
    data       jsonb not null
);
create table if not exists hub.state_history (
    kind       text not null,
    tick       int,
    fetched_at timestamptz not null default now(),
    hash       text not null,
    data       jsonb not null,
    primary key (kind, hash)
);

-- The card list, from the catalog.
create table if not exists hub.cards (
    ref       text primary key,
    set       text not null,
    name      text,
    rarity    text not null,
    book      int not null,
    print_run int,
    minted    int,
    page      boolean,
    hidden    boolean,
    updated_at timestamptz not null default now()
);

-- Our own private history (imported from Lucas's data/me.jsonl and Dani's logs; the collector itself is keyless).
create table if not exists hub.me_snapshots (
    tick   int not null,
    t      double precision,
    source text not null,
    data   jsonb not null,
    primary key (tick, source)
);

-- Collector health.
create table if not exists hub.heartbeats (
    host          text primary key,
    last_at       timestamptz not null default now(),
    last_tick     int,
    max_event_id  bigint,
    events_stored bigint,
    boards        int,
    last_error    text,
    started_at    timestamptz
);
create table if not exists hub.gaps (
    id        bigserial primary key,
    host      text,
    at        timestamptz not null default now(),
    after_id  bigint,                          -- newest id we had
    before_id bigint,                          -- oldest id the feed still returned
    tick      int
);

-- ---------------------------------------------------------------- demand model outputs (hub.demand)

create table if not exists hub.model_runs (
    run_id      bigserial primary key,
    at          timestamptz not null default now(),
    tick        int,
    events_used bigint,
    params      jsonb,
    summary     jsonb
);
-- Posterior over each team's multiplier for each set.
create table if not exists hub.team_mult (
    team    text not null,
    set     text not null,
    e_mult  double precision,
    p_mult  jsonb,                             -- {"1.6": p, "1.3": p, ...}
    top     double precision,                  -- most likely multiplier
    p_top   double precision,
    n_obs   int,
    run_id  bigint,
    primary key (team, set)
);
-- What one more copy of each card is worth to each team.
create table if not exists hub.team_card_value (
    team         text not null,
    card         text not null,
    set          text,
    rarity       text,
    e_value      double precision,
    q25          double precision,
    q75          double precision,
    p_lacks      double precision,
    p_completes  double precision,
    known_copies int,
    run_id       bigint,
    primary key (team, card)
);
create table if not exists hub.opportunities (
    id          bigserial primary key,
    run_id      bigint,
    kind        text not null,                 -- sell | buy | match
    card        text not null,
    seller      text,
    buyer       text,
    price       int,
    our_value   double precision,
    their_value double precision,              -- E[value] to the counterparty (buyer for sell, seller for buy)
    p_fill      double precision,
    exp_gain    double precision,
    p_completes double precision,
    feeding     text,                          -- ok | page_closer_to_leader | top4 | ...
    why         text
);
-- The observations behind each team's estimate (for the dashboard's drill-down).
create table if not exists hub.evidence (
    run_id bigint,
    team   text,
    set    text,
    card   text,
    kind   text,
    price  double precision,
    tick   int,
    shift  double precision,                   -- how much it moved E[mult] for that set, alone vs a flat prior
    detail jsonb
);

-- ---------------------------------------------------------------- views

-- One row per settlement: a backfilled copy (negative id) yields to the real event when both exist.
create or replace view hub.v_settlements as
select distinct on ((e.payload->>'settlement')::bigint) e.id as event_id, e.tick, e.t_hours,
       (e.payload->>'settlement')::bigint as settlement,
       e.payload->>'kind' as kind,
       e.payload->'parties'->>0 as maker,
       e.payload->'parties'->>1 as taker,
       e.payload->>'venue' as venue,
       e.payload->>'persona' as persona,
       (e.payload->>'price')::int as price,
       (e.payload->>'fee')::int as fee,
       e.payload->'items' as items
from hub.events e
where e.type = 'settlement'
order by (e.payload->>'settlement')::bigint, e.id < 0, e.id;

create or replace view hub.v_trade_items as
select s.event_id, s.tick, s.t_hours, s.settlement, s.kind, s.maker, s.taker, s.venue, s.persona, s.price, s.fee,
       jsonb_array_length(s.items) as n_items,
       (i->>'id')::bigint as asset_id, i->>'kind' as item_kind, i->>'ref' as ref,
       i->>'frm' as frm, i->>'to' as to_team, c.set, c.rarity, c.book
from hub.v_settlements s
cross join lateral jsonb_array_elements(s.items) as i
left join hub.cards c on c.ref = i->>'ref';

-- Single-card cash trades between two teams: the market tape.
create or replace view hub.v_team_trades as
select t.* from hub.v_trade_items t
where t.persona is null and t.item_kind = 'card' and t.n_items = 1 and t.price > 0;

create or replace view hub.v_fill_prices as
select set, rarity, count(*) as n,
       percentile_cont(0.5) within group (order by price) as median_price,
       min(price) as min_price, max(price) as max_price, max(tick) as last_tick
from hub.v_team_trades
group by set, rarity;

create or replace view hub.v_team_latest as
select distinct on (team) * from hub.team_snapshots order by team, snapshot_tick desc;

create or replace view hub.v_health as
select host, last_at, now() - last_at as age, last_tick, max_event_id, events_stored, boards, last_error
from hub.heartbeats;
