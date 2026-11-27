import pandas as pd
import plotly.express as px


def get_column_types(dataframe):
    """
    Identifies numeric, categorical and date columns.
    """

    numeric_columns = [
        column
        for column in dataframe.select_dtypes(
            include="number"
        ).columns.tolist()
        if not (
            column.lower() == "id"
            or column.lower().endswith("_id")
        )
    ]

    categorical_columns = dataframe.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    date_columns = [
        column
        for column in dataframe.columns
        if (
            pd.api.types.is_datetime64_any_dtype(
                dataframe[column]
            )
            or any(
                keyword in column.lower()
                for keyword in [
                    "date",
                    "time",
                    "month",
                    "year"
                ]
            )
        )
    ]

    return {
        "numeric": numeric_columns,
        "categorical": categorical_columns,
        "date": date_columns
    }


def recommend_chart(dataframe):
    """
    Automatically recommends a visualization
    based on the returned DataFrame.
    """

    if dataframe is None or dataframe.empty:
        return {
            "type": "none",
            "reason": "No data available for visualization."
        }

    if len(dataframe.columns) == 1:

        column = dataframe.columns[0]

        if pd.api.types.is_numeric_dtype(dataframe[column]):
            return {
                "type": "histogram",
                "x": column,
                "reason": "A histogram shows the distribution of values."
            }

        return {
            "type": "pie",
            "names": column,
            "reason": "A pie chart shows the distribution of categories."
        }

    types = get_column_types(dataframe)

    numeric = types["numeric"]
    categorical = types["categorical"]
    dates = types["date"]

    # Date-based trends
    for date_column in dates:

        valid_numeric = [
            column
            for column in numeric
            if column != date_column
        ]

        if valid_numeric:
            return {
                "type": "line",
                "x": date_column,
                "y": valid_numeric[0],
                "reason": "A line chart is suitable for time-based trends."
            }

    # Category vs numerical metric
    if categorical and numeric:

        return {
            "type": "bar",
            "x": categorical[0],
            "y": numeric[0],
            "reason": "A bar chart compares numerical values across categories."
        }

    # Numerical relationships
    if len(numeric) >= 2:

        return {
            "type": "scatter",
            "x": numeric[0],
            "y": numeric[1],
            "reason": "A scatter plot reveals relationships between numerical variables."
        }

    # Categorical distribution
    if categorical:

        return {
            "type": "pie",
            "names": categorical[0],
            "reason": "A pie chart visualizes categorical proportions."
        }

    # Numeric distribution
    if numeric:

        return {
            "type": "histogram",
            "x": numeric[0],
            "reason": "A histogram shows numerical distribution."
        }

    return {
        "type": "none",
        "reason": "No suitable chart could be identified."
    }


def create_chart(dataframe, chart_type=None):
    """
    Generates an interactive Plotly chart.
    """

    if dataframe is None or dataframe.empty:
        return None

    recommendation = recommend_chart(dataframe)

    selected_type = chart_type or recommendation["type"]

    if selected_type == "none":
        return None

    types = get_column_types(dataframe)

    numeric = types["numeric"]
    categorical = types["categorical"]
    dates = types["date"]

    if selected_type == "bar":

        x = categorical[0] if categorical else dataframe.columns[0]

        y = next(
            (column for column in numeric if column != x),
            None
        )

        if y:
            fig = px.bar(
                dataframe,
                x=x,
                y=y,
                title=f"{y} by {x}",
                template="plotly_dark",
                text_auto=".2s"
            )
        else:
            fig = px.histogram(
                dataframe,
                x=x,
                template="plotly_dark"
            )

    elif selected_type == "line":

        x = (
            dates[0]
            if dates
            else dataframe.columns[0]
        )

        y = next(
            (column for column in numeric if column != x),
            None
        )

        if not y:
            return None

        fig = px.line(
            dataframe,
            x=x,
            y=y,
            markers=True,
            title=f"{y} over {x}",
            template="plotly_dark"
        )

    elif selected_type == "pie":

        names = (
            categorical[0]
            if categorical
            else dataframe.columns[0]
        )

        fig = px.pie(
            dataframe,
            names=names,
            title=f"Distribution of {names}",
            template="plotly_dark",
            hole=0.4
        )

    elif selected_type == "scatter":

        if len(numeric) < 2:
            return None

        fig = px.scatter(
            dataframe,
            x=numeric[0],
            y=numeric[1],
            title=f"{numeric[1]} vs {numeric[0]}",
            template="plotly_dark"
        )

    elif selected_type == "histogram":

        x = numeric[0] if numeric else dataframe.columns[0]

        fig = px.histogram(
            dataframe,
            x=x,
            title=f"Distribution of {x}",
            template="plotly_dark"
        )

    else:
        return None

    fig.update_layout(
        autosize=True,
        height=450,
        margin=dict(l=30, r=30, t=60, b=30),
        font=dict(
            family="Arial",
            size=12
        )
    )

    return fig
