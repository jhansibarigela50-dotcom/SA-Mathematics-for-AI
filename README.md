# IADAI2021000480-Jhansi Barigela
# FootLens Analytics: Player Injuries & Team Performance Dashboard
# Candidate Name: Jhansi Barigela
# Candidate Registration Number - 1000480
# CRS Name: Artificial Intelligence
# Course Name - Mathematics for AI
# School name - Birla Open Minds International School, Kollur
# Summative Assessment
# ⚽ FootLens Analytics: Player Injuries & Team Performance Dashboard

An interactive decision-support dashboard built with **Streamlit** and **Plotly** designed for sports managers, technical directors, and analysts. This application analyzes the connection between player injury frequencies, recovery trajectories, and overall club performance.

---

## 📌 Project Overview
FootLens Analytics acquired a comprehensive sports dataset tracking player performance, injury timelines, and team match records. This project processes and cleans the raw data to quantify injury impact and visualize critical performance trends.

### Key Questions Answered:
1. **Injury Impact**: Which specific injury types lead to the steepest drop in player performance ratings?
2. **Team Win Rate Effect**: How does a club's win percentage change during key player absences compared to normal conditions?
3. **Player Comeback Tracking**: Which players show the highest recovery rates post-injury?
4. **Injury Clustering**: Are there specific months or clubs with frequent injury spikes?
5. **Age vs. Severity**: How does player age correlate with recovery duration and rating declines?

---

## 🛠️ Key Features & Data Preprocessing
* **Data Preprocessing & Cleaning**:
  * Cleaned missing values (`NaN`s) in player ratings using statistical median imputation.
  * Converted injury start/end dates to standard `datetime` objects to derive exact recovery duration.
  * Standardized column naming conventions for cleaner data pipeline handling.
* **Feature Engineering**:
  * injury_duration_days: Total days sidelined per injury episode.
  * performance_drop_index: Difference between pre-injury and post-recovery player ratings.
  * rating_change_post_recovery: Quantified comeback rating change.
* **Interactive Visualizations**:
  * **Bar Chart**: Avg Rating Drop by Injury Type.
  * **Scatter Plot**: Player Age vs. Performance Drop Index (sized by recovery duration.
  * **Leaderboard Table**: Ranking players by post-recovery rating improvements.
  * **Stacked Bar Chart**: Monthly injury clusters broken down by club.
  * **Grouped Bar Chart**: Normal Team Win % vs. Win % during key player absence.


---

## 🌐 Live Application 
* **Live Streamlit App**: [Click Here to Access Live App](https://sa-mathematics-for-ai-jk34w2urbgafg7ylmtsey3.streamlit.app/) 

---


## App Screenshots

<img width="2852" height="842" alt="image" src="https://github.com/user-attachments/assets/a87010b5-1713-4cff-8bfc-1421f66ccb1d" />

<img width="2156" height="1144" alt="image" src="https://github.com/user-attachments/assets/08ddc543-bdbf-4ad7-85a7-4f9652bd5d69" />

<img width="2014" height="932" alt="image" src="https://github.com/user-attachments/assets/0928e3c2-42c2-4f8e-a5c3-b7bffdc99a4f" />

<img width="2104" height="1134" alt="image" src="https://github.com/user-attachments/assets/588f6ee9-a31a-433c-8703-79e54032cf77" />

<img width="2264" height="1204" alt="image" src="https://github.com/user-attachments/assets/34d314fa-1ad8-41e3-83df-77c9e0915882" />


## 📂 Repository Structure
```text
.
├── data/
│   └── player_injuries.csv      # Dataset used by the application
├── screenshots/
│   └── dashboard_preview.png    # Preview screenshot of the running app
├── app.py                       # Main Streamlit application logic
├── requirements.txt             # Python project dependencies
└── README.md                    # Project documentation
