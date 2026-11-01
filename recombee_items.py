import pandas as pd
from recombee_api_client.api_requests import SetItemValues, Batch

# TODO 1: Credentialele sunt aceleasi ca la Lab 02, le importam ca sa nu le duplicam
from recombee_properties import client

# TODO 2: Acelasi dataset folosit la Lab 02
PATH_DATASET = 'dataset/products.csv'
BATCH_SIZE = 100


def parse_discount(text):
    """'70% off' -> 70"""
    return int(str(text).split('%')[0])


def parse_sizes(text):
    """'Size:Medium,Small' -> ['Medium', 'Small']; 'Nan' -> None (produs fara marimi)"""
    text = str(text).strip()
    if text.lower() == 'nan' or not text:
        return None
    return [s.strip() for s in text.replace('Size:', '', 1).split(',') if s.strip()]


def send_items():
    """Functie care citeste dataset-ul si trimite item-urile in Recombee"""
    df = pd.read_csv(PATH_DATASET, keep_default_na=False)
    print(f"Se trimit {len(df)} item-uri in Recombee...")

    requests = []
    trimise = 0

    for _, row in df.iterrows():
        # TODO 3: ID-ul unic al produsului (devine itemId in Recombee)
        item_id = str(row['Product ID'])

        # TODO 4: Maparea coloanelor din CSV pe proprietatile definite la Lab 02
        properties = {
            "brand": str(row['BrandName']),
            "descriere": str(row['Brand Desc']),
            "categorie": str(row['Category']),
            "pret": float(row['SellPrice']),
            "discount": parse_discount(row['Discount']),
        }
        marimi = parse_sizes(row['Product Size'])
        if marimi:
            properties["marimi"] = marimi

        # SetItemValues creeaza automat item-ul daca acesta nu exista
        requests.append(SetItemValues(item_id, properties, cascade_create=True))

        # Trimitem in loturi (batch) pentru eficienta
        if len(requests) == BATCH_SIZE:
            client.send(Batch(requests))
            trimise += len(requests)
            requests = []
            print(f"S-au trimis {trimise} item-uri...")

    # Trimitem si restul ramas (daca numarul total nu e multiplu de BATCH_SIZE)
    if requests:
        client.send(Batch(requests))
        trimise += len(requests)

    print(f"Toate cele {trimise} item-uri au fost trimise cu succes!")


if __name__ == "__main__":
    send_items()
