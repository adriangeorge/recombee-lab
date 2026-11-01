# Recombee Lab – Produse de modă pentru femei (India)

Proiect pentru laboratorul de Sisteme de Recomandare: înregistrarea proprietăților unui catalog de produse în **Recombee**.

## Structura repository-ului

```
recombee-lab/
├── dataset/
│   └── products.csv          # setul de date folosit
├── recombee_properties.py    # script care înregistrează proprietățile în Recombee
└── README.md
```

## Dataset

- **Sursă:** 
https://www.kaggle.com/datasets/sujaykapadnis/products-datasets/data
Kari, Venkatram (2023), „Product Dataset", Mendeley Data, V1, doi: [10.17632/v8yt3r8th2.1](https://doi.org/10.17632/v8yt3r8th2.1)
- **Domeniu:** comerț online cu produse pentru femei: îmbrăcăminte, încălțăminte, bijuterii, ceasuri, lenjerie/articole de noapte și parfumuri. Prețurile sunt în rupii indiene (Rs.).
- **Volum:** 4.566 produse (câte un rând per produs), 11 coloane.
- **Fișier:** [`dataset/products.csv`](dataset/products.csv)

### Coloanele din fișier

| Coloană | Descriere | Exemplu |
|---|---|---|
| `S.No` | Numărul rândului (1–4566) | `1` |
| `BrandName` | Brandul produsului (57 de branduri distincte, ex. *and*, *aurelia*, *ayesha*, *biba*, *adidas*) | `aurelia` |
| `Product ID` | Identificator unic al produsului (4.566 valori unice) | `DRW1` |
| `Product Name` | Etichetă de forma `<ID> - <Categorie>` | `DRW1 - Westernwear-Women` |
| `Brand Desc` | Descriere text: material, stil, croi, culoare | `womens v- neck short dress - yellow` |
| `Product Size` | Mărimile disponibile, sub forma `Size:` urmat de o listă separată prin virgulă | `Size:Medium,Small,X-Large` |
| `Currancy` | Moneda (numele coloanei este scris greșit în fișierul original); are mereu valoarea `Rs.` | `Rs.` |
| `MRP` | Prețul maxim de vânzare (prețul de listă, înainte de reducere) | `1899` |
| `SellPrice` | Prețul real de vânzare, după reducere (interval 89–25.995) | `569` |
| `Discount` | Reducerea, ca text (37 de valori distincte; cea mai frecventă este `10% off`) | `70% off` |
| `Category` | Categoria produsului (7 valori) | `Westernwear-Women` |

### Distribuția pe categorii

| Categorie | Produse |
|---|---|
| Westernwear-Women | 1.654 |
| Indianwear-Women | 1.131 |
| Footwear-Women | 480 |
| Jewellery-Women | 438 |
| Lingerie&Nightwear-Women | 367 |
| Watches-Women | 329 |
| Fragrance-Women | 167 |

### Observații despre calitatea datelor

- **`MRP` este deteriorată în multe rânduri:** 757 de rânduri conțin valorile `8.9` sau `.9` (probabil erori de conversie din Excel), 13 sunt goale și cel puțin unul conține `#REF!`. Din acest motiv coloana nu este folosită ca proprietate.
- **`Product Size` lipsește în 1.194 de rânduri:** apare șirul `Nan` la produsele fără mărime (bijuterii, ceasuri, parfumuri). Aceste valori trebuie tratate ca lipsă.
- Coloanele `Product ID`, `BrandName`, `Brand Desc`, `SellPrice`, `Discount` și `Category` sunt complete.

## Proprietăți înregistrate în Recombee

Identificatorul `Product ID` **nu** este proprietate: va deveni `itemId` la încărcarea produselor.

| Proprietate Recombee | Tip | Coloană sursă | Observații |
|---|---|---|---|
| `brand` | `string` | `BrandName` | |
| `descriere` | `string` | `Brand Desc` | |
| `categorie` | `string` | `Category` | |
| `pret` | `double` | `SellPrice` | |
| `discount` | `int` | `Discount` | se extrage procentul: `"70% off"` → `70` |
| `marimi` | `set` | `Product Size` | se elimină prefixul `Size:` și se desparte după virgulă; `Nan` → lipsă |

Coloanele `S.No`, `Product Name`, `Currancy` și `MRP` nu sunt înregistrate (redundante, constante sau cu date corupte).

## Rulare

1. Instalați bibliotecile:
   ```
   pip install recombee-api-client pandas
   ```
2. Setați credențialele ca variabile de mediu (din *Settings -> API Logins* în Recombee Admin UI); tokenul nu se pune în cod:
   ```
   export RECOMBEE_DB_NAME='numele_bazei'
   export RECOMBEE_PRIVATE_TOKEN='tokenul_privat'
   ```
   Regiunea (`REGION`) se schimbă direct în [`recombee_properties.py`](recombee_properties.py), dacă este cazul.
3. Rulați scriptul din rădăcina repository-ului:
   ```
   python recombee_properties.py
   ```

Scriptul verifică dataset-ul, trimite proprietățile către Recombee și apoi listează proprietățile configurate pentru confirmare.

## Încărcarea item-urilor (Laboratorul 3)

Scriptul [`recombee_items.py`](recombee_items.py) citește `dataset/products.csv` și trimite fiecare produs în Recombee prin `SetItemValues`, în loturi (`Batch`) de câte 100.

- `Product ID` → `itemId`
- `BrandName` → `brand`, `Brand Desc` → `descriere`, `Category` → `categorie`, `SellPrice` → `pret`
- `Discount` → `discount` (`"70% off"` → `70`)
- `Product Size` → `marimi` (`"Size:Medium,Small"` → `["Medium", "Small"]`; `Nan` → proprietatea nu se setează)

Credențialele se citesc din [`recombee_properties.py`](recombee_properties.py). Rulare (după `recombee_properties.py`):

```
python recombee_items.py
```

Verificare: în [Recombee Admin UI](https://admin.recombee.com/), la secțiunea *Items*, apar 4.566 produse cu proprietățile completate.
