"""
NBA Points Predictor — Streamlit App
Original logic by Declan Davis (@declandavis03-max)
"""

import streamlit as st
import pandas as pd

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NBA Points Predictor",
    page_icon="🏀",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0d0d;
    color: #f0f0f0;
}

h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem !important;
    letter-spacing: 3px;
    color: #f77f00;
    margin-bottom: 0 !important;
}

h2, h3 {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 2px;
    color: #f77f00;
}

.subtitle {
    color: #888;
    font-size: 0.9rem;
    margin-top: -6px;
    margin-bottom: 24px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.stButton > button {
    background: #f77f00;
    color: #0d0d0d;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    letter-spacing: 2px;
    border: none;
    border-radius: 4px;
    padding: 0.55rem 2.5rem;
    width: 100%;
    transition: background 0.2s;
}
.stButton > button:hover {
    background: #ff9d2f;
    color: #0d0d0d;
}

.result-card {
    background: #1a1a1a;
    border-left: 4px solid #f77f00;
    border-radius: 6px;
    padding: 24px 28px;
    margin-top: 20px;
}

.result-card .big-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    color: #f77f00;
    line-height: 1;
    margin-bottom: 4px;
}

.result-card .big-label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #888;
    margin-bottom: 20px;
}

.breakdown-row {
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #2a2a2a;
    padding: 10px 0;
    font-size: 0.9rem;
}

.breakdown-row .label { color: #aaa; }
.breakdown-row .val   { font-weight: 600; color: #f0f0f0; }
.pos { color: #4ade80 !important; }
.neg { color: #f87171 !important; }

.court-divider {
    border: none;
    border-top: 1px solid #2a2a2a;
    margin: 28px 0;
}

.info-box {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 14px 18px;
    font-size: 0.82rem;
    color: #777;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

# ── Data URLs ──────────────────────────────────────────────────────────────────
DEF_RAT_URL = "https://www.basketball-reference.com/leagues/NBA_2026.html"
PPG_URL     = "https://www.basketball-reference.com/leagues/NBA_2026_per_game.html"

TEAM_ABBREVIATIONS = {
    "Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BKN",
    "Charlotte Hornets": "CHA", "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN", "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW", "Houston Rockets": "HOU", "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA", "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP", "New York Knicks": "NYK", "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR", "Utah Jazz": "UTA", "Washington Wizards": "WAS",
}
ABBREV_TO_TEAM = {v: k for k, v in TEAM_ABBREVIATIONS.items()}
ALL_ABBREVS    = sorted(TEAM_ABBREVIATIONS.values())

# ── Cached data fetchers ───────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def fetch_ppg_table():
    tables = pd.read_html(PPG_URL, flavor="html5lib")
    return tables[0]

@st.cache_data(show_spinner=False)
def fetch_def_rat_table():
    tables = pd.read_html(DEF_RAT_URL, flavor="html5lib")
    df = tables[10]
    try:
        df.columns = df.columns.get_level_values(-1)
    except Exception:
        pass
    return df

@st.cache_data(show_spinner=False)
def get_player_list():
    df = fetch_ppg_table()
    df = df[df["Rk"] != "Rk"]
    return sorted(df["Player"].dropna().unique().tolist())

# ── Core logic ─────────────────────────────────────────────────────────────────
def league_avg_drtg():
    df = fetch_def_rat_table()
    df = df[df["Rk"] != "Rk"]
    row = df[df["Team"] == "League Average"]
    return float(list(row["DRtg"])[0])

def player_ppg(player_name):
    df = fetch_ppg_table()
    df = df[df["Rk"] != "Rk"]
    df["PTS"] = df["PTS"].astype(float)
    row = df[df["Player"] == player_name]
    if len(row) == 0:
        raise ValueError(f"Player '{player_name}' not found.")
    return float(list(row["PTS"])[0])

def team_ppg(team_abbrev):
    df = fetch_ppg_table()
    df = df[df["Rk"] != "Rk"]
    df["PTS"] = df["PTS"].astype(float)
    row = df[df["Team"] == team_abbrev.upper()]
    if len(row) == 0:
        raise ValueError(f"Team '{team_abbrev}' not found.")
    return float(list(row["PTS"])[0])

def opponent_drtg(team_abbrev):
    upper = team_abbrev.upper()
    full_name = ABBREV_TO_TEAM.get(upper, upper)
    df = fetch_def_rat_table()
    df = df[df["Rk"] != "Rk"]
    df["DRtg"] = df["DRtg"].astype(float)
    row = df[df["Team"] == full_name]
    if len(row) == 0:
        raise ValueError(f"Team '{full_name}' not found in DRtg table.")
    return float(list(row["DRtg"])[0])

def scoring_adj(ppg, t_ppg, opp_drtg, lg_drtg):
    drtg_diff   = opp_drtg - lg_drtg
    share       = ppg / t_ppg
    return share * drtg_diff

def location_adj(is_home: bool):
    return 1.0 if is_home else -1.0

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("<h1>🏀 NBA Points Predictor</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">2025–26 Season · Basketball-Reference Data</p>', unsafe_allow_html=True)

st.markdown('<hr class="court-divider">', unsafe_allow_html=True)

# ── Inputs ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Player")
    player_list = []
    with st.spinner("Loading player list…"):
        try:
            player_list = get_player_list()
        except Exception:
            pass

    if player_list:
        player = st.selectbox("Select Player", player_list, index=None, placeholder="Search player…")
    else:
        player = st.text_input("Player Name (exact)", placeholder="e.g. Nikola Jokić")

    player_team = st.selectbox("Player's Team", ALL_ABBREVS, index=None, placeholder="Select team…")

with col2:
    st.markdown("### Matchup")
    opponent = st.selectbox("Opponent Team", ALL_ABBREVS, index=None, placeholder="Select opponent…")
    location = st.radio("Game Location", ["Home 🏠", "Away ✈️"], horizontal=True)

st.markdown('<hr class="court-divider">', unsafe_allow_html=True)

# ── Predict button ─────────────────────────────────────────────────────────────
run = st.button("PREDICT POINTS")

if run:
    if not player or not player_team or not opponent:
        st.warning("Please fill in all fields before predicting.")
    else:
        is_home = location.startswith("Home")
        with st.spinner("Crunching numbers from Basketball-Reference…"):
            try:
                ppg      = player_ppg(player)
                t_ppg    = team_ppg(player_team)
                opp_drtg = opponent_drtg(opponent)
                lg_drtg  = league_avg_drtg()

                def_adj  = scoring_adj(ppg, t_ppg, opp_drtg, lg_drtg)
                loc_adj  = location_adj(is_home)
                predicted = ppg + def_adj + loc_adj

                def fmt_signed(v):
                    sign  = "+" if v >= 0 else ""
                    klass = "pos" if v >= 0 else "neg"
                    return f'<span class="{klass}">{sign}{v:.2f}</span>'

                opp_full   = ABBREV_TO_TEAM.get(opponent.upper(), opponent)
                team_full  = ABBREV_TO_TEAM.get(player_team.upper(), player_team)
                loc_label  = "Home" if is_home else "Away"

                st.markdown(f"""
                <div class="result-card">
                    <div class="big-number">{round(predicted)}</div>
                    <div class="big-label">Predicted Points — {player} vs {opp_full} ({loc_label})</div>

                    <div class="breakdown-row">
                        <span class="label">Base PPG</span>
                        <span class="val">{ppg:.1f}</span>
                    </div>
                    <div class="breakdown-row">
                        <span class="label">Defensive Adjustment <small>({opp_full} DRtg: {opp_drtg:.1f} | League: {lg_drtg:.1f})</small></span>
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

# ── Footer info ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="info-box">
    <strong>How it works:</strong> Base PPG is adjusted by the opponent's Defensive Rating relative to the league average,
    weighted by the player's scoring share of their team's output. A +1 / −1 home/away modifier is then applied.
    Data is fetched live from Basketball-Reference.
</div>
""", unsafe_allow_html=True)
