import pandas as pd
import plotly.express as px
import streamlit as st


# This is the CSV already included in the project folder.
DEFAULT_DATA_FILE = "ai_jobs_market_2025_2026.csv"


# Page settings control the browser tab title and give the dashboard more space.
st.set_page_config(page_title="AI Career Navigator", layout="wide")


def find_column(dataframe, keywords):
    """Find a column by checking whether its name contains any keyword."""
    for column in dataframe.columns:
        clean_name = column.lower().replace(" ", "_")
        if any(keyword in clean_name for keyword in keywords):
            return column
    return None


def format_money(value):
    """Turn a number into a clean dollar format for KPI cards and labels."""
    if pd.isna(value):
        return "N/A"
    return f"${value:,.0f}"


def split_skills(skill_series):
    """Split the skills column into one skill per row so we can count skills."""
    return (
        skill_series.dropna()
        .astype(str)
        .str.split(r"[,|;/]", regex=True)
        .explode()
        .str.strip()
        .replace("", pd.NA)
        .dropna()
    )


def get_filter_options(dataframe, column):
    """Get clean filter options from a column."""
    if not column:
        return []
    return sorted(dataframe[column].dropna().astype(str).unique())


def apply_filter(dataframe, column, selected_values):
    """Keep only rows that match the selected filter values."""
    if not column or not selected_values:
        return dataframe
    return dataframe[dataframe[column].astype(str).isin(selected_values)]


def show_filter(dataframe, column, label, key):
    """Create a multiselect filter with options from the current DataFrame."""
    options = get_filter_options(dataframe, column)

    if not options:
        return []

    # Keep Streamlit stable when earlier filters change the available options.
    current_values = st.session_state.get(key, [])
    valid_values = [value for value in current_values if value in options]
    if valid_values != current_values:
        st.session_state[key] = valid_values

    return st.sidebar.multiselect(label, options, key=key)


def show_single_filter(dataframe, column, label, key):
    """Create a single-select filter with an All option."""
    options = get_filter_options(dataframe, column)

    if not options:
        return []

    if isinstance(st.session_state.get(key), list):
        st.session_state[key] = "All"

    selected_value = st.sidebar.selectbox(label, ["All"] + options, key=key)
    if selected_value == "All":
        return []

    return [selected_value]


def make_horizontal_bar(dataframe, x_column, y_column, title, color_column=None):
    """Create a consistent horizontal bar chart."""
    fig = px.bar(
        dataframe,
        x=x_column,
        y=y_column,
        orientation="h",
        title=title,
        color=color_column or x_column,
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        margin={"l": 20, "r": 20, "t": 60, "b": 20},
    )
    return fig


def load_data(uploaded_file):
    """Load either the uploaded CSV or the default project CSV."""
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file), uploaded_file.name
    return pd.read_csv(DEFAULT_DATA_FILE), DEFAULT_DATA_FILE


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
    }
    div[data-baseweb="tag"] {
        background-color: #2563eb !important;
        color: white !important;
    }
    div[data-baseweb="tag"] span {
        color: white !important;
    }
    div[data-baseweb="select"] > div {
        border-color: #cbd5e1 !important;
    }
    div[data-baseweb="select"] > div:focus-within {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 1px #2563eb !important;
    }
    li[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] {
        background-color: #dbeafe !important;
        color: #1e3a8a !important;
    }
    li[role="option"]:hover,
    div[role="option"]:hover {
        background-color: #eff6ff !important;
        color: #1e3a8a !important;
    }
    li[role="option"] mark,
    div[role="option"] mark {
        background-color: #bfdbfe !important;
        color: #1e3a8a !important;
    }
    [data-baseweb="menu"] li[aria-selected="true"],
    [data-baseweb="menu"] div[aria-selected="true"] {
        background-color: #dbeafe !important;
        color: #1e3a8a !important;
    }
    div.stButton > button {
        border-color: #2563eb !important;
        color: #2563eb !important;
    }
    div.stButton > button:hover,
    div.stButton > button:focus {
        border-color: #1d4ed8 !important;
        color: #1d4ed8 !important;
        background-color: #eff6ff !important;
    }
    div.stButton > button:active {
        border-color: #1e40af !important;
        color: white !important;
        background-color: #2563eb !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("AI Career Navigator")
st.caption(
    "Explore AI roles, skills, and salary trends with simple filters."
)

st.sidebar.title("AI Career Navigator")
uploaded_file = st.sidebar.file_uploader("Upload a different CSV", type=["csv"])

# Load the default dataset first so the demo works immediately.
df, data_source = load_data(uploaded_file)

# Detect the columns we need. This keeps the app flexible for future CSV files.
job_title_col = find_column(df, ["job_title", "title", "role", "position"])
category_col = find_column(df, ["job_category", "category", "function"])
experience_col = find_column(df, ["experience_level", "experience", "seniority"])
salary_col = find_column(df, ["annual_salary", "salary", "compensation", "pay"])
salary_min_col = find_column(df, ["salary_min", "min_salary"])
salary_max_col = find_column(df, ["salary_max", "max_salary"])
city_col = find_column(df, ["city"])
country_col = find_column(df, ["country"])
location_col = find_column(df, ["location", "state", "area"]) or country_col or city_col
salary_location_col = city_col or location_col or country_col
remote_col = find_column(df, ["remote_work", "work_mode", "remote", "work_type"])
company_size_col = find_column(df, ["company_size", "company"])
industry_col = find_column(df, ["industry", "sector"])
education_col = find_column(df, ["education"])
skills_col = find_column(df, ["required_skills", "tech_skills", "skills", "requirements"])

filter_configs = [
    {
        "section": "Geography",
        "column": country_col,
        "label": "Country",
        "key": "country_filter",
    },
    {
        "section": "Geography",
        "column": city_col,
        "label": "City",
        "key": "city_filter",
    },
    {
        "section": "Career",
        "column": category_col,
        "label": "Job category",
        "key": "category_filter",
    },
    {
        "section": "Career",
        "column": job_title_col,
        "label": "Job title",
        "key": "job_title_filter",
    },
    {
        "section": "Career",
        "column": experience_col,
        "label": "Experience level",
        "key": "experience_filter",
    },
    {
        "section": "Workplace",
        "column": remote_col,
        "label": "Work mode",
        "key": "work_mode_filter",
    },
    {
        "section": "Workplace",
        "column": industry_col,
        "label": "Industry",
        "key": "industry_filter",
    },
]

st.sidebar.caption(f"Data source: {data_source}")
st.sidebar.header("Filters")

# Clear filters is useful during a demo when switching between scenarios.
if st.sidebar.button("Clear filters"):
    for config in filter_configs:
        if config["key"] == "country_filter":
            st.session_state[config["key"]] = "All"
        else:
            st.session_state[config["key"]] = []

filtered_df = df.copy()
active_filters = []

# Geography filters come first. Country narrows the city options.
st.sidebar.subheader("Geography")
selected_countries = show_single_filter(df, country_col, "Country", "country_filter")
filtered_df = apply_filter(filtered_df, country_col, selected_countries)
if selected_countries:
    active_filters.append(f"Country: {', '.join(selected_countries)}")

selected_cities = show_filter(filtered_df, city_col, "City", "city_filter")
filtered_df = apply_filter(filtered_df, city_col, selected_cities)
if selected_cities:
    active_filters.append(f"City: {', '.join(selected_cities)}")

# Career filters are based on the selected geography.
st.sidebar.subheader("Career")
for column, label, key in [
    (category_col, "Job category", "category_filter"),
    (job_title_col, "Job title", "job_title_filter"),
    (experience_col, "Experience level", "experience_filter"),
]:
    selected_values = show_filter(filtered_df, column, label, key)
    filtered_df = apply_filter(filtered_df, column, selected_values)
    if selected_values:
        active_filters.append(f"{label}: {', '.join(selected_values)}")

# Workplace filters are based on geography plus career selections.
st.sidebar.subheader("Workplace")
for column, label, key in [
    (remote_col, "Work mode", "work_mode_filter"),
    (industry_col, "Industry", "industry_filter"),
]:
    selected_values = show_filter(filtered_df, column, label, key)
    filtered_df = apply_filter(filtered_df, column, selected_values)
    if selected_values:
        active_filters.append(f"{label}: {', '.join(selected_values)}")

# Convert numeric columns safely so calculations do not break on text values.
salary = pd.to_numeric(filtered_df[salary_col], errors="coerce") if salary_col else None

st.subheader("Dataset Overview")

if active_filters:
    st.success(
        "Current view is filtered by "
        + " | ".join(active_filters)
        + ". All KPIs, skills, salaries, roles, and the table below use this filtered data."
    )
else:
    st.info("Current view shows the full dataset. Add filters in the sidebar to personalize the dashboard.")

overview_cols = st.columns(3)
overview_cols[0].metric("Job Postings", f"{len(filtered_df):,}")
overview_cols[1].metric("Median Salary", format_money(salary.median() if salary_col else pd.NA))
overview_cols[2].metric("Average Salary", format_money(salary.mean() if salary_col else pd.NA))

st.divider()

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Top Job Roles")

    if job_title_col:
        top_titles = (
            filtered_df[job_title_col].dropna().astype(str).value_counts().head(10)
        )

        if not top_titles.empty:
            title_chart = top_titles.reset_index()
            title_chart.columns = ["Job Title", "Postings"]
            fig = make_horizontal_bar(
                title_chart,
                "Postings",
                "Job Title",
                "Top 10 Job Titles for Current View",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No job titles match the current filters.")
    else:
        st.info("No job title column found.")

with right_col:
    st.subheader("Top Skills To Learn")

    if skills_col:
        top_skills = split_skills(filtered_df[skills_col]).value_counts().head(15)

        if not top_skills.empty:
            skills_chart = top_skills.reset_index()
            skills_chart.columns = ["Skill", "Postings"]
            fig = make_horizontal_bar(
                skills_chart,
                "Postings",
                "Skill",
                "Top 15 Skills for Current View",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No skills match the current filters.")
    else:
        st.info("No skills column found.")

st.subheader("Salary Explorer")

salary_left, salary_right = st.columns(2)

with salary_left:
    if salary_col and job_title_col:
        salary_by_role = (
            filtered_df.assign(_salary=salary)
            .dropna(subset=[job_title_col, "_salary"])
            .groupby(job_title_col, as_index=False)["_salary"]
            .median()
            .sort_values("_salary", ascending=False)
            .head(10)
        )

        if not salary_by_role.empty:
            fig = px.bar(
                salary_by_role,
                x="_salary",
                y=job_title_col,
                orientation="h",
                title="Highest Median Salary by Role",
                labels={"_salary": "Median Salary", job_title_col: "Job Title"},
                color="_salary",
                color_continuous_scale="Greens",
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No salary by role data available.")
    else:
        st.info("Salary by role needs salary and job title columns.")

with salary_right:
    if salary_col and salary_location_col:
        salary_by_location = (
            filtered_df.assign(_salary=salary)
            .dropna(subset=[salary_location_col, "_salary"])
            .groupby(salary_location_col, as_index=False)["_salary"]
            .median()
            .sort_values("_salary", ascending=False)
            .head(10)
        )

        if not salary_by_location.empty:
            fig = px.bar(
                salary_by_location,
                x="_salary",
                y=salary_location_col,
                orientation="h",
                title=f"Highest Median Salary by {salary_location_col.replace('_', ' ').title()}",
                labels={"_salary": "Median Salary", salary_location_col: "Location"},
                color="_salary",
                color_continuous_scale="Greens",
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No salary by location data available.")
    else:
        st.info("Salary by location needs salary and location columns.")

if salary_col:
    salary_distribution = filtered_df.assign(_salary=salary).dropna(subset=["_salary"])

    if not salary_distribution.empty:
        fig = px.histogram(
            salary_distribution,
            x="_salary",
            nbins=25,
            title="Salary Distribution",
            labels={"_salary": "Annual Salary"},
            color_discrete_sequence=["#2563eb"],
        )
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Role Details")

detail_columns = [
    column
    for column in [
        job_title_col,
        category_col,
        experience_col,
        salary_col,
        salary_min_col,
        salary_max_col,
        city_col,
        country_col,
        remote_col,
        company_size_col,
        industry_col,
        education_col,
        skills_col,
    ]
    if column
]

if detail_columns:
    st.dataframe(filtered_df[detail_columns], use_container_width=True, hide_index=True)
else:
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
