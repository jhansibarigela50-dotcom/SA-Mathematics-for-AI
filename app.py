import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration & UI Theme
# ---------------------------------------------------------
st.set_page_config(
    page_title="FootLens Analytics | Injury Impact Dashboard",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FootLens Analytics: Player Injuries & Team Performance")
st.markdown("*Data-driven decision support for technical directors and sports managers.*")
st.markdown("---")

# ---------------------------------------------------------
# 1. Data Loading & Preprocessing
# ---------------------------------------------------------
@st.cache_data
def load_and_preprocess_data():
    # Replace 'data/player_injuries.csv' with your dataset path
    try:
        df = pd.read_csv("data/player_injuries.csv")
    except FileNotFoundError:
        # Dummy data generation for testing/structure
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
            'Injury Duration Days': np.random.randint(7, 180, n),
            'Rating Before': np.random.uniform(6.5, 9.5, n).round(1),
            'Rating After': np.random.uniform(5.5, 9.5, n).round(1),
            'Team Win % Normal': np.random.uniform(50, 80, n).round(1),
            'Team Win % During Absence': np.random.uniform(20, 60, n).round(1)
        })
        df['Injury Month'] = df['Injury Start Date'].dt.strftime('%B')
        df['Performance Drop Index'] = (df['Rating Before'] - df['Rating After']).round(2)

    return df

df = load_and_preprocess_data()

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("Filter Options")
selected_club = st.sidebar.multiselect("Select Club(s)", options=df['Club'].unique(), default=df['Club'].unique())
selected_injury = st.sidebar.multiselect("Select Injury Type(s)", options=df['Injury Type'].unique(), default=df['Injury Type'].unique())

filtered_df = df[(df['Club'].isin(selected_club)) & (df['Injury Type'].isin(selected_injury))]

# ---------------------------------------------------------
# Key Performance Indicators (KPIs)
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Injuries Tracked", len(filtered_df))
col2.metric("Avg Recovery Duration", f"{filtered_df['Injury Duration Days'].mean():.1f} Days")
col3.metric("Avg Rating Drop Post-Injury", f"{filtered_df['Performance Drop Index'].mean():.2f} pts")
col4.metric("Avg Team Win Rate Drop", f"{(filtered_df['Team Win % Normal'] - filtered_df['Team Win % During Absence']).mean():.1f}%")

st.markdown("---")

# ---------------------------------------------------------
# Tabs for Layout
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Performance & Impact", "🔍 Injury Patterns", "📋 Raw Data & Analysis"])

with tab1:
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Visual 1: Top Injuries by Performance Drop
        fig1 = px.bar(
            filtered_df.groupby('Injury Type')['Performance Drop Index'].mean().reset_index(),
            x='Injury Type', y='Performance Drop Index',
            color='Performance Drop Index',
            title="1. Top Injuries Leading to Rating Drop",
            labels={'Performance Drop Index': 'Avg Drop in Rating'},
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        # Visual 2: Player Age vs. Performance Drop Index
        fig2 = px.scatter(
            filtered_df, x='Age', y='Performance Drop Index',
            color='Injury Type', size='Injury Duration Days',
            hover_data=['Player Name', 'Club'],
            title="2. Player Age vs. Performance Drop Index"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Visual 3: Leaderboard - Strongest Comebacks vs Drops
    st.subheader("3. Comeback Leaderboard (Rating Change Post-Recovery)")
    leaderboard = filtered_df[['Player Name', 'Club', 'Injury Type', 'Rating Before', 'Rating After', 'Performance Drop Index']].sort_values(by='Performance Drop Index', ascending=True)
    st.dataframe(leaderboard, use_container_width=True)

with tab2:
    col_c, col_d = st.columns(2)
    
    with col_c:
        # Visual 4: Monthly Injury Clusters Heatmap / Bar Chart
        monthly_injuries = filtered_df.groupby(['Injury Month', 'Club']).size().reset_index(name='Injury Count')
        fig4 = px.bar(
            monthly_injuries, x='Injury Month', y='Injury Count', color='Club',
            title="4. Injury Clusters Across Months and Clubs",
            barmode='stack'
        )
        st.plotly_chart(fig4, use_container_width=True)

    with col_d:
        # Visual 5: Team Performance Comparison (Normal vs During Absence)
        team_impact = filtered_df.groupby('Club')[['Team Win % Normal', 'Team Win % During Absence']].mean().reset_index()
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=team_impact['Club'], y=team_impact['Team Win % Normal'], name='Normal Win %'))
        fig5.add_trace(go.Bar(x=team_impact['Club'], y=team_impact['Team Win % During Absence'], name='Win % During Absence'))
        fig5.update_layout(barmode='group', title="5. Club Win Rate: Normal vs. Key Player Absence")
        st.plotly_chart(fig5, use_container_width=True)

with tab3:
    st.subheader("Exploratory Data Summary")
    st.write(filtered_df.describe())
    st.dataframe(filtered_df)
