"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaign_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_date: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - cons_price_idx
    - euribor_three_months



    """
    import glob
    import os
    import zipfile
    import pandas as pd

    input_dir = "files/input"
    output_dir = "files/output"
    os.makedirs(output_dir, exist_ok=True)

    # Lee y concatena todos los csv.zip sin descomprimirlos a disco
    dfs = []
    for zip_path in sorted(glob.glob(os.path.join(input_dir, "*.zip"))):
        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                if name.endswith(".csv"):
                    with zf.open(name) as f:
                        dfs.append(pd.read_csv(f))

    df = pd.concat(dfs, ignore_index=True)

    # ---------- client.csv ----------
    client = df[
        ["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]
    ].copy()
    client["job"] = (
        client["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    )
    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].replace("unknown", pd.NA)
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)
    client.to_csv(os.path.join(output_dir, "client.csv"), index=False)

    # ---------- campaign.csv ----------
    campaign = df[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "day",
            "month",
        ]
    ].copy()
    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(int)
    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)

    month_num = campaign["month"].str.strip().apply(
        lambda m: pd.to_datetime(m, format="%b").month
    )
    campaign["last_contact_date"] = (
        "2022-"
        + month_num.astype(str).str.zfill(2)
        + "-"
        + campaign["day"].astype(str).str.zfill(2)
    )
    campaign = campaign.drop(columns=["day", "month"])
    campaign.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)

    # ---------- economics.csv ----------
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    economics.to_csv(os.path.join(output_dir, "economics.csv"), index=False)

    return


if __name__ == "__main__":
    clean_campaign_data()