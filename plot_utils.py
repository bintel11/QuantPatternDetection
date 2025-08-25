import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import config


def save_pattern_plot(pat, symbol, pattern_id):
    """
    Save static PNG plot using matplotlib (reliable).
    """
    df = pat["df"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["timestamp"], df["close"], label="Price", color="blue")
    ax.set_title(f"Cup & Handle Pattern - {symbol} (ID {pattern_id})")
    ax.legend()

    filepath = os.path.join(config.PATTERNS_DIR, f"cup_handle_{pattern_id}.png")
    plt.savefig(filepath)
    plt.close(fig)

    return filepath


def save_pattern_html(pat, symbol, pattern_id):
    """
    Save interactive HTML plot using plotly.
    """
    df = pat["df"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["timestamp"], 
        y=df["close"],
        mode="lines", 
        name="Price"
    ))

    fig.update_layout(
        title=f"Cup & Handle Pattern - {symbol} (ID {pattern_id})",
        xaxis_title="Time",
        yaxis_title="Price",
        template="plotly_white"
    )

    filepath = os.path.join(config.PATTERNS_DIR, f"cup_handle_{pattern_id}.html")
    fig.write_html(filepath, include_plotlyjs="cdn")

    return filepath





