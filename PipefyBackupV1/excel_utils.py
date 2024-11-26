# excel_utils.py

import pandas as pd

def save_to_excel(data, output_filename):
    df = pd.DataFrame(data)

    with pd.ExcelWriter(output_filename, engine='xlsxwriter') as writer:
        for phase in df["Phase"].unique():
            phase_data = df[df["Phase"] == phase].drop(columns=["Phase"])
            phase_data.to_excel(writer, sheet_name=phase[:30], index=False)  # Crear una hoja por fase
    print(f"Datos guardados en {output_filename}")
