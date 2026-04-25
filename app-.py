import gradio as gr
import pandas as pd


# DATA LOADING
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)

        for col in ["text", "temp_1.0"]:
            if col in df.columns:
                df[col] = df[col].fillna("")

        return df

    except Exception as e:
        print("Error loading CSV:", e)
        return None


df_1977 = load_data("results/caveman_1977_baffet_letter_ver2.csv")

# HELPERS
def compute_stats(df=df_1977):
    if df is None:
        return "No data loaded."

    text_len = df["text"].str.len().sum()
    cave_len = df["temp_1.0"].str.len().sum()
    saving = (text_len - cave_len) / text_len if text_len > 0 else 0

    return f"""
    <div class="stats-box">
    <div><b>original chars:</b> {text_len:,}</div> 
    <div><b>caveman chars:</b> {cave_len:,}</div>
    <div><b>reduction:</b> {saving:.1%}</div>
    </div>
    """


def render_content():
    if df_1977 is None:
        return "<p>Could not load data.</p>", "<p>Could not load data.</p>", "Error"

    rows_html = ""

    for _, row in df_1977.iterrows():
        rows_html += f"""
        <div class="pair-row">
            <div class="chunk left-block">
                {row["text"]}
            </div>

            <div class="chunk caveman right-block">
                {row["temp_1.0"]}
            </div>
        </div>
        """
    stats_html = compute_stats(df_1977)
    return rows_html, stats_html

# UI
css = """
body {
    background: #f6f7f8;
}

/* page */
.main-title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 8px;
}

.sub-title {
    text-align: center;
    color: #666;
    margin-bottom: 25px;
}

/* NEW split subtitle row */
.header-row {
    display: flex;
    gap: 14px;
    margin-bottom: 14px;
}

.header-box {
    flex: 1;
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    border-bottom: 2px solid #e5e5e5;
    padding-bottom: 8px;
}

/* content rows */
.pair-row {
    display: flex;
    gap: 14px;
    align-items: stretch;
    margin-bottom: 14px;
}

/* blocks */
.chunk {
    flex: 1;
    background: white;
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #e3e3e3;
    line-height: 1.65;
    font-size: 16px;
    box-sizing: border-box;
    display: flex;
    align-items: flex-start;
}

.left-block {
    background: white;
}

.right-block {
    background: #fff8e8;
}

/* stats */
.stats-box {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e3e3e3;
    font-size: 16px;
    line-height: 1.8;
    margin-bottom: 18px;
}

/* footer */
.footer {
    text-align: left;
    color: #777;
    font-size: 14px;
    margin-top: 30px;
}

/* mobile */
@media (max-width: 900px) {

    .header-row,
    .pair-row {
        flex-direction: column;
    }
}
"""


with gr.Blocks(css=css, title="smart caveman") as app:

    gr.Markdown('<div class="main-title">smart caveman</div>')
    gr.Markdown(
        '<div class="sub-title">Warren Buffett 1977 Shareholder Letter. by caveman</div>'
    )

    gr.Markdown("""
    <div class="header-row">
        <div class="header-box">original text</div>
        <div class="header-box">caveman version</div>
    </div>
    """)

    content = gr.HTML()

    gr.Markdown("---")

    stats = gr.HTML()

    gr.Markdown("---")

    gr.Markdown(
        """
        <div class="footer">
        This application is created solely for educational purposes.<br>
        The text in the left column ("Original letter text") from Chairman's Letters for Berkshire Hathaway Inc. shareholders, authored by Warren E. Buffett. 
        Official Source: [Berkshire Hathaway Inc. Website](https://www.berkshirehathaway.com/letters/letters.html)
        </div>
        """
    )

    app.load(
        render_content,
        outputs=[content, stats]
    )

app.launch(debug=False)