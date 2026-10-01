import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration & UI Theme
# ---------------------------------------------------------
st.set_page_config(
    page_title="FootLens Analytics | Player Injury Dashboard",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FootLens Analytics: Player Injuries & Team Performance")
st.markdown("*Data-driven decision support for technical directors and sports managers.*")
st.markdown("---")

# ---------------------------------------------------------
# 1. Data Loading & Preprocessing (Step 2 of Assignment)
# ---------------------------------------------------------
@st.cache_data
def load_and_preprocess_data():
    try:
        # Load dataset from data directory
        df = pd.read_csv("data/player_injuries.csv")
    except FileNotFoundError:
        # Fallback dataset structure if local CSV is not present
        np.random.seed(42)
        n = 100
        clubs = ['Arsenal', 'Chelsea', 'Liverpool', 'Man City', 'Real Madrid']
        injuries = ['Hamstring Strain', 'ACL Tear', 'Ankle Sprain', 'Calf Strain', 'Groin Pull']
        
        df = pd.DataFrame({
            'Player Name': [f'Player {i}' for i in range(1, n+1)],
            'Club': np.random.choice(clubs, n),
            'Age': np.random.randint(18, 35, n),
            'Injury Type': np.random.choice(injuries, n),
            'Injury Start Date': pd.date_range(start='2024-01-01', periods=n, freq='D'),
            'Injury End Date': pd.date_range(start='2024-03-01', periods=n, freq='D'),
            'Rating Before': np.random.uniform(6.5, 9.5, n).round(1),
            'Rating After': np.random.uniform(5.5, 9.5, n).round(1),
            'Team Win % Normal': np.random.uniform(50, 80, n).round(1),
            'Team Win % During Absence': np.random.uniform(20, 60, n).round(1)
        })

    # Standardize column headers to lowercase with underscores
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Handle Missing Values (NaNs)
    if 'rating_before' in df.columns:
        df['rating_before'] = df['rating_before'].fillna(df['rating_before'].median())
    if 'rating_after' in df.columns:
        df['rating_after'] = df['rating_after'].fillna(df['rating_after'].median())
    
    # Drop rows missing crucial identifier fields
    required_fields = [col for col in ['player_name', 'injury_start_date'] if col in df.columns]
    if required_fields:
        df = df.dropna(subset=required_fields)

    # Convert Date fields to Datetime format
    if 'injury_start_date' in df.columns:
        df['injury_start_date'] = pd.to_datetime(df['injury_start_date'], errors='coerce')
        df['injury_month'] = df['injury_start_date'].dt.strftime('%B')
    
    if 'injury_end_date' in df.columns:
        df['injury_end_date'] = pd.to_datetime(df['injury_end_date'], errors='coerce')

    # Feature Engineering
    if 'injury_start_date' in df.columns and 'injury_end_date' in df.columns:
        df['injury_duration_days'] = (df['injury_end_date'] - df['injury_start_date']).dt.days
        df['injury_duration_days'] = df['injury_duration_days'].fillna(0)

    if 'rating_before' in df.columns and 'rating_after' in df.columns:
        # Performance drop index calculation
        df['performance_drop_index'] = (df['rating_before'] - df['rating_after']).round(2)
        df['rating_change_post_recovery'] = (df['rating_after'] - df['rating_before']).round(2)

    return df

df = load_and_preprocess_data()

# ---------------------------------------------------------
# Sidebar Controls & Filters
# ---------------------------------------------------------
st.sidebar.header("🔍 Filter Options")

club_col = 'club' if 'club' in df.columns else df.columns[0]
injury_col = 'injury_type' if 'injury_type' in df.columns else df.columns[1]

selected_clubs = st.sidebar.multiselect(
    "Select Club(s)", 
    options=df[club_col].unique(), 
    default=df[club_col].unique()
)

selected_injuries = st.sidebar.multiselect(
    "Select Injury Type(s)", 
    options=df[injury_col].unique(), 
    default=df[injury_col].unique()
)

filtered_df = df[
    (df[club_col].isin(selected_clubs)) & 
    (df[injury_col].isin(selected_injuries))
]

# ---------------------------------------------------------
# Key Metrics Summary (KPI Banner)
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Injuries", len(filtered_df))

if 'injury_duration_days' in filtered_df.columns:
    col2.metric("Avg Recovery Duration", f"{filtered_df['injury_duration_days'].mean():.1f} Days")
else:
    col2.metric("Avg Recovery Duration", "N/A")

if 'performance_drop_index' in filtered_df.columns:
    col3.metric("Avg Rating Drop", f"{filtered_df['performance_drop_index'].mean():.2f} pts")
else:
    col3.metric("Avg Rating Drop", "N/A")

if 'team_win_%_normal' in filtered_df.columns and 'team_win_%_during_absence' in filtered_df.columns:
    win_drop = (filtered_df['team_win_%_normal'] - filtered_df['team_win_%_during_absence']).mean()
    col4.metric("Avg Win Rate Drop", f"{win_drop:.1f}%")
else:
    col4.metric("Avg Win Rate Drop", "N/A")

st.markdown("---")

# ---------------------------------------------------------
# Main Tabs Navigation
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Impact Analysis", "📅 Injury Patterns", "📋 Dataset & Aggregations"])

with tab1:
    st.subheader("Performance & Injury Impact")
    col_a, col_b = st.columns(2)

    with col_a:
        # Visual 1: Top Injuries by Performance Drop
        if 'performance_drop_index' in filtered_df.columns:
            avg_drop = filtered_df.groupby(injury_col)['performance_drop_index'].mean().reset_index()
            fig1 = px.bar(
                avg_drop, x=injury_col, y='performance_drop_index',
                color='performance_drop_index',
                title="1. Avg Rating Drop by Injury Type",
                labels={'performance_drop_index': 'Avg Rating Drop'},
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        # Visual 2: Age vs. Performance Drop
        if 'age' in filtered_df.columns and 'performance_drop_index' in filtered_df.columns:
            fig2 = px.scatter(
                filtered_df, x='age', y='performance_drop_index',
                color=injury_col, size='injury_duration_days' if 'injury_duration_days' in filtered_df.columns else None,
                hover_data=['player_name'] if 'player_name' in filtered_df.columns else None,
                title="2. Player Age vs. Performance Drop Index"
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Visual 3: Leaderboard - Player Comebacks
    st.subheader("3. Comeback Leaderboard (Post-Recovery Rating Change)")
    if 'rating_change_post_recovery' in filtered_df.columns:
        leaderboard = filtered_df.sort_values(by='rating_change_post_recovery', ascending=False)
        st.dataframe(leaderboard, use_container_width=True)

with tab2:
    st.subheader("Clustering & Team Results")
    col_c, col_d = st.columns(2)

    with col_c:
        # Visual 4: Monthly Injury Frequency
        if 'injury_month' in filtered_df.columns:
            monthly_counts = filtered_df.groupby(['injury_month', club_col]).size().reset_index(name='count')
            fig4 = px.bar(
                monthly_counts, x='injury_month', y='count', color=club_col,
                title="4. Monthly Injury Clusters Across Clubs",
                barmode='stack'
            )
            st.plotly_chart(fig4, use_container_width=True)

    with col_d:
        # Visual 5: Team Win Rate Comparison
        if 'team_win_%_normal' in filtered_df.columns and 'team_win_%_during_absence' in filtered_df.columns:
            team_impact = filtered_df.groupby(club_col)[['team_win_%_normal', 'team_win_%_during_absence']].mean().reset_index()
            fig5 = go.Figure()
            fig5.add_trace(go.Bar(x=team_impact[club_col], y=team_impact['team_win_%_normal'], name='Normal Win %'))
            fig5.add_trace(go.Bar(x=team_impact[club_col], y=team_impact['team_win_%_during_absence'], name='Win % During Absence'))
            fig5.update_layout(barmode='group', title="5. Win Rate: Normal vs. Absence")
            st.plotly_chart(fig5, use_container_width=True)

with tab3:
    st.subheader("Exploratory Data Summary & Preprocessed Table")
    st.write(filtered_df.describe())
    st.dataframe(filtered_df)
