import fire
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import pyplot

icd_translations = {
    "401": "Hypertension",
    "427": "Cardiac dysrhythmias",
    "276": "Disorders of fluid electrolyte",
    "272": "Disorders of lipoid metabolism",
    "250": "Diabetes",
    "414": "Chronic ischemic heart disease",
    "428": "Heart failure",
    "518": "Other diseases of lung",
    "285": "Unspecified anemias",
    "584": "Acute kidney failure",
    "599": "Urinary tract disorders",
    "V586": "Drug Use",
    "530": "Diseases of esophagus",
    "585": "Chronic kidney disease",
    "403": "Hypertensive chronic kidney disease",
    "038": "Septicemia",
    "V458": "Postprocedural status",
    "995": "Adverse effects",
    "424": "Diseases of endocardium",
    "785": "Cardiovascular Symptoms",
    "410": "Acute myocardial infarction",
    "997": "Complications",
    "305": "Abuse of drugs",
    "780": "General symptoms",
    "998": "Complications of Procedures",
    "244": "Hypothyroidism",
    "458": "Hypotension",
    "486": "Pneumonia",
    "496": "Chronic airway obstruction",
    "996": "Complications peculiar",
    "041": "Bacterial infection",
    "E878": "Operations caused by abnormal reaction",
    "287": "Purpura",
    "V158": "Personal history presenting hazards to health",
    "790": "Findings on examination of blood",
    "507": "Pneumonitis due to solids and liquids",
    "311": "Depressive disorder",
    "493": "Asthma",
    "511": "Pleurisy"
}

column_translate = {
    "AFRICAN_AMERICAN": "AFRICAN AMERICAN",
    "F": "Female",
    "M": "Male",
    "T": "Transgender"
}


def plot(shift_data_path: str, num_classes: int = None, fixed_range=True):
    sns.set_style("darkgrid")

    shift_data = pd.read_csv(shift_data_path)

    if num_classes is not None:
        shift_data = shift_data.iloc[:, :num_classes]

    shift_data = shift_data.rename(columns=icd_translations)
    plot_heatmap(shift_data, fixed_range)


def plot_bars(df):
    tidy = df.melt(id_vars='group').rename(columns=str.title)
    fig, ax1 = pyplot.subplots(figsize=(40, 10))
    sns.barplot(x='Variable', y='Value', hue='Group', data=tidy, ax=ax1, palette="viridis")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
    plt.show()


def plot_line(dfs):
    sns.set_style("whitegrid")

    df = pd.concat(dfs).reset_index(drop=True)
    df = df.rename(columns={"group": "Age", "mortality_risk": "Mortality Risk"})
    plt.figure(figsize=(12, 10))
    ax = sns.lineplot(x="Age", y="Mortality Risk", hue="model", data=df)
    plt.xticks([0, 12, 22, 32, 42, 52, 62, 72], size="x-large")
    plt.yticks(fontsize="x-large", rotation=0)
    ax.xaxis.label.set_fontsize("x-large")
    ax.yaxis.label.set_fontsize("x-large")
    plt.show()


def plot_heatmap(df, fixed_range):
    fig, ax = pyplot.subplots(figsize=(15, 10))
    sns.set(font_scale=2)
    if fixed_range:
        b = sns.heatmap(create_offsets(df), ax=ax, vmin=-0.035, vmax=0.035, cmap="vlag")
    else:
        b = sns.heatmap(create_offsets(df), ax=ax, cmap="vlag")
    b.set_yticklabels(b.get_yticklabels(), size=22)

    fig.subplots_adjust(left=0.35)
    plt.show()


def create_offsets(df):
    offset_df = df.copy()
    offset_df = offset_df.set_index('group').T
    columns = offset_df.columns.values
    for col in columns:
        other_columns = [c for c in columns if c is not col]
        offset_df[f"{col}_offset"] = offset_df[col] - offset_df[other_columns].mean(axis=1)
    offset_columns = [f"{col}_offset" for col in columns]
    offset_df = offset_df[offset_columns]
    offset_df = offset_df.rename(columns=dict(zip(offset_columns, columns)))
    offset_df = offset_df.rename(columns=column_translate)
    return offset_df


if __name__ == '__main__':
    fire.Fire(plot)
