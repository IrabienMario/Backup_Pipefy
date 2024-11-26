from queries import fetch_all_cards
from excel_utils import save_to_excel

# Configuración Global
API_TOKEN = "..."  # Reemplaza con tu token
GRAPHQL_ENDPOINT = "https://api.pipefy.com/graphql"
QUERY = """
query ($pipeId: ID!, $afterCursor: String) {
    pipe(id: $pipeId) {
        phases {
            name
            cards(first: 50, after: $afterCursor) {
                edges {
                    node {
                        id
                        title
                        fields {
                            name
                            value
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    }
}
"""

def create_backup(pipe_id):
    """
    Realiza el proceso completo de backup:
    1. Consulta todas las tarjetas de un Pipe dado.
    2. Guarda los datos en un archivo Excel.

    :param pipe_id: ID del Pipefy para el cual se realiza el backup.
    :return: Nombre del archivo generado.
    """
    print(f"Iniciando backup para el Pipe ID: {pipe_id}")

    # Descargar los datos del Pipe
    all_cards_data = fetch_all_cards(pipe_id, API_TOKEN, GRAPHQL_ENDPOINT, QUERY)
    print(f"Datos descargados para el Pipe ID: {pipe_id}. Total de tarjetas: {len(all_cards_data)}")

    # Guardar los datos en un archivo Excel
    output_filename = f"backup_{pipe_id}.xlsx"
    save_to_excel(all_cards_data, output_filename)
    print(f"Archivo guardado: {output_filename}")

    return output_filename
