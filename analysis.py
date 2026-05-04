"""
NBA Points Predictor — Streamlit App
Original logic by Declan Davis (@declandavis03-max)
"""

import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats
from nba_api.stats.static import teams as nba_teams

st.set_page_config(page_title="NBA Points Predictor", page_icon="🏀", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #0d0d0d; color: #f0f0f0; }
h1 { font-family: 'Bebas Neue', sans-serif; font-size: 3.2rem !important; letter-spacing: 3px; color: #f77f00; margin-bottom: 0 !important; }
h2, h3 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; color: #f77f00; }
.subtitle { color: #888; font-size: 0.9rem; margin-top: -6px; margin-bottom: 24px; letter-spacing: 1px; text-transform: uppercase; }
.stButton > button { background: #f77f00; color: #0d0d0d; font-family: 'Bebas Neue', sans-serif; font-size: 1.2rem; letter-spacing: 2px; border: none; border-radius: 4px; padding: 0.55rem 2.5rem; width: 100%; }
.stButton > button:hover { background: #ff9d2f; }
.result-card { background: #1a1a1a; border-left: 4px solid #f77f00; border-radius: 6px; padding: 24px 28px; margin-top: 20px; }
.result-card .big-number { font-family: 'Bebas Neue', sans-serif; font-size: 5rem; color: #f77f00; line-height: 1; margin-bottom: 4px; }
.result-card .big-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; color: #888; margin-bottom: 20px; }
.breakdown-row { display: flex; justify-content: space-between; border-top: 1px solid #2a2a2a; padding: 10px 0; font-size: 0.9rem; }
.breakdown-row .label { color: #aaa; }
.breakdown-row .val { font-weight: 600; color: #f0f0f0; }
.pos { color: #4ade80 !important; }
.neg { color: #f87171 !important; }
.court-divider { border: none; border-top: 1px solid #2a2a2a; margin: 28px 0; }
.info-box { background: #161616; border: 1px solid #2a2a2a; border-radius: 6px; padding: 14px 18px; font-size: 0.82rem; color: #777; margin-top: 12px; }
</style>
""", unsafe_allow_html=True)

SEASON = "2025-26"

_all_teams = nba_teams.get_teams()
ABBREV_TO_FULL = {t["abbreviation"]: t["full_name"] for t in _all_teams}
ALL_ABBREVS = sorted(ABBREV_TO_FULL.keys())

def match_team(df, team_abbrev):
    abbrev = team_abbrev.upper()
    if "TEAM_ABBREVIATION" in df.columns:
        row = df[df["TEAM_ABBREVIATION"] == abbrev]
        if len(row) > 0:
            return row
    full = ABBREV_TO_FULL.get(abbrev, abbrev)
    return df[df["TEAM_NAME"] == full]

@st.cache_data(show_spinner=False)
def fetch_player_stats():
    return leaguedashplayerstats.LeagueDashPlayerStats(
        season=SEASON, per_mode_detailed="PerGame"
    ).get_data_frames()[0]

@st.cache_data(show_spinner=False)
def fetch_team_offense():
    return leaguedashteamstats.LeagueDashTeamStats(
        season=SEASON,
        per_mode_detailed="PerGame",
        measure_type_detailed_defense="Base"
    ).get_data_frames()[0]

@st.cache_data(show_spinner=False)
def fetch_team_defense():
    # Opponent measure: PTS column = points the team ALLOWS per game
    return leaguedashteamstats.LeagueDashTeamStats(
        season=SEASON,
        per_mode_detailed="PerGame",
        measure_type_detailed_defense="Opponent"
    ).get_data_frames()[0]

@st.cache_data(show_spinner=False)
def get_player_list():
    df = fetch_player_stats()
    return sorted(df["PLAYER_NAME"].dropna().unique().tolist())

def get_player_ppg(player_name):
    df = fetch_player_stats()
    row = df[df["PLAYER_NAME"] == player_name]
    if len(row) == 0:
        raise ValueError(f"Player '{player_name}' not found.")
    return float(row["PTS"].values[0])

def get_team_ppg(team_abbrev):
    df = fetch_team_offense()
    row = match_team(df, team_abbrev)
    if len(row) == 0:
        raise ValueError(f"Team '{team_abbrev}' not found.")
    # Find whichever points column exists
    pts_col = next((c for c in ["OPP_PTS", "PTS", "PTS_PG", "POINTS"] if c in df.columns), None)
    if pts_col is None:
        raise ValueError(f"No PTS column found. Columns: {list(df.columns)}")
    return float(row[pts_col].values[0])

def get_opp_pts_allowed(team_abbrev):
    df = fetch_team_defense()
    row = match_team(df, team_abbrev)
    if len(row) == 0:
        raise ValueError(f"Team '{team_abbrev}' not found in defense table.")
    pts_col = next((c for c in ["OPP_PTS", "PTS", "PTS_PG", "POINTS"] if c in df.columns), None)
    if pts_col is None:
        raise ValueError(f"No PTS column in defense table. Columns: {list(df.columns)}")
    return float(row[pts_col].values[0])

def get_league_avg_pts_allowed():
    df = fetch_team_defense()
    pts_col = next((c for c in ["OPP_PTS", "PTS", "PTS_PG", "POINTS"] if c in df.columns), None)
    if pts_col is None:
        raise ValueError(f"No PTS column in defense table. Columns: {list(df.columns)}")
    return float(df[pts_col].mean())

def scoring_adj(ppg, t_ppg, opp_allowed, lg_avg):
    # Player's scoring share × how much easier/harder this defense is
    return (ppg / t_ppg) * (opp_allowed - lg_avg)

def location_adj(is_home):
    return 1.0 if is_home else -1.0

# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("<h1>🏀 NBA Points Predictor</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">2025–26 Season · Official NBA Data</p>', unsafe_allow_html=True)
st.markdown('<hr class="court-divider">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Player")
    player_list = []
    with st.spinner("Loading players…"):
        try:
            player_list = get_player_list()
        except Exception:
            pass
    if player_list:
        player = st.selectbox("Select Player", player_list, index=None, placeholder="Search player…")
    else:
        player = st.text_input("Player Name (exact)", placeholder="e.g. Nikola Jokic")
    player_team = st.selectbox("Player's Team", ALL_ABBREVS, index=None, placeholder="Select team…")

with col2:
    st.markdown("### Matchup")
    opponent = st.selectbox("Opponent Team", ALL_ABBREVS, index=None, placeholder="Select opponent…")
    location = st.radio("Game Location", ["Home 🏠", "Away ✈️"], horizontal=True)

st.markdown('<hr class="court-divider">', unsafe_allow_html=True)

run = st.button("PREDICT POINTS")

if run:
    if not player or not player_team or not opponent:
        st.warning("Please fill in all fields before predicting.")
    else:
        is_home = location.startswith("Home")
        with st.spinner("Crunching numbers from NBA.com…"):
            try:
                ppg         = get_player_ppg(player)
                t_ppg       = get_team_ppg(player_team)
                opp_allowed = get_opp_pts_allowed(opponent)
                lg_avg      = get_league_avg_pts_allowed()
                def_adj     = scoring_adj(ppg, t_ppg, opp_allowed, lg_avg)
                loc_adj     = location_adj(is_home)
                predicted   = ppg + def_adj + loc_adj

                def fmt_signed(v):
                    sign  = "+" if v >= 0 else ""
                    klass = "pos" if v >= 0 else "neg"
                    return f'<span class="{klass}">{sign}{v:.2f}</span>'

                opp_full  = ABBREV_TO_FULL.get(opponent.upper(), opponent)
                loc_label = "Home" if is_home else "Away"

                st.markdown(f"""
                <div class="result-card">
                    <div class="big-number">{round(predicted)}</div>
                    <div class="big-label">Predicted Points — {player} vs {opp_full} ({loc_label})</div>
                    <div class="breakdown-row">
                        <span class="label">Base PPG</span>
                        <span class="val">{ppg:.1f}</span>
                    </div>
                    <div class="breakdown-row">
                        <span class="label">Defensive Adjustment <small>({opp_full} allows {opp_allowed:.1f} pts/g | League avg: {lg_avg:.1f})</small></span>
                        <span class="val">{fmt_signed(def_adj)}</span>
                    </div>
                    <div class="breakdown-row">
                        <span class="label">Home / Away Adjustment</span>
                        <span class="val">{fmt_signed(loc_adj)}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.markdown("""
<div class="info-box">
    <strong>How it works:</strong> Base PPG is adjusted by the opponent's points allowed per game relative to the league average,
    weighted by the player's scoring share of their team's output. A +1 / −1 home/away modifier is applied.
    Data is fetched live from NBA.com.
</div>
""", unsafe_allow_html=True)
