# AI Career Navigator

AI Career Navigator is a Streamlit dashboard that helps users explore AI job market trends using a CSV dataset. The app makes it easier to understand popular AI roles, required skills, salary trends, and job opportunities by location and experience level.

## Project Overview

This project was built as a beginner-friendly data dashboard using Python. It loads an AI jobs dataset and turns it into an interactive career exploration tool.

Users can filter the data and instantly see updated insights for:
- Top AI job roles
- Top required skills
- Salary trends
- Job postings by selected filters

## Features

- Interactive Streamlit dashboard
- Default AI jobs dataset included
- Optional CSV upload
- Sidebar filters for:
  - Country
  - City
  - Job category
  - Job title
  - Experience level
  - Work mode
  - Industry
- KPI cards for:
  - Total job postings
  - Median salary
  - Average salary
- Charts for:
  - Top job roles
  - Top skills
  - Salary by role
  - Salary by location
  - Salary distribution
- Filtered data table at the bottom

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly Express

## Dataset

The app uses the included CSV file:

```text
ai_jobs_market_2025_2026.csv
