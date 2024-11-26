import requests

def fetch_all_cards(pipe_id, api_token, graphql_endpoint, query):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    all_data = []

    # Obtener datos de cada fase
    data = make_api_request(graphql_endpoint, query, {"pipeId": pipe_id}, headers)
    for phase in data["data"]["pipe"]["phases"]:
        phase_name = phase["name"]
        print(f"Descargando tarjetas de la fase: {phase_name}...")
        phase_cards = fetch_phase_cards(phase_name, graphql_endpoint, query, headers, pipe_id)
        all_data.extend(phase_cards)

    return all_data

def make_api_request(url, query, variables, headers):
    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    return response.json()

def fetch_phase_cards(phase_name, graphql_endpoint, query, headers, pipe_id):
    phase_cards = []
    cursor = None
    seen_cursors = set()

    while True:
        variables = {"pipeId": pipe_id, "afterCursor": cursor}  # Cambiado de PIPE_ID a pipe_id
        data = make_api_request(graphql_endpoint, query, variables, headers)

        for phase_entry in data["data"]["pipe"]["phases"]:
            if phase_entry["name"] == phase_name:
                cards = phase_entry["cards"]
                phase_cards.extend(process_cards(cards, phase_name))

                # Manejar paginación
                if cards["pageInfo"]["hasNextPage"]:
                    cursor = cards["pageInfo"]["endCursor"]
                    if cursor in seen_cursors:
                        print(f"Bucle detectado en la fase {phase_name}. Terminando esta fase.")
                        return phase_cards
                    seen_cursors.add(cursor)
                else:
                    return phase_cards

    return phase_cards

def process_cards(cards, phase_name):
    phase_cards = []
    for card in cards["edges"]:
        node = card["node"]
        fields = {field["name"]: field["value"] for field in node["fields"]}
        row = {
            "Phase": phase_name,
            "Card ID": node["id"],
            "Title": node["title"],
            **fields
        }
        phase_cards.append(row)
    print(f"Fase: {phase_name}, Tarjetas procesadas en esta página: {len(cards['edges'])}")
    return phase_cards
