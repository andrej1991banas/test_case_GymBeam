# Databázová analýza

## 1 Návrh dátového modelu v ER diagrame

![Untitled (1)](https://github.com/user-attachments/assets/94855225-b9da-4ec2-8123-809c485e3801)


## 2 Návrh hviezdicového schémy pre analytické potreby
Tento dokument popisuje návrh dátového modelu vo forme hviezdicového schémy (star schema) pre analýzu predajov podľa času, produktov, kategórií a regiónov. Hviezdicové schéma je optimalizované pre dátové sklady a reporting, s jednou centrálnou faktovou tabuľkou a viacerými dimenzionálnymi tabuľkami.

**Krok 1: Identifikácia dimenzií a faktov**

*Dimenzionálne tabuľky (Dimensions):* Obsahujú popisné údaje používané na filtrovanie a zoskupovanie (napr. produkty, kategórie, zákazníci, regióny, čas).
*Faktová tabuľka (Facts)*: Obsahuje kvantitatívne údaje (metriky) ako predaje, množstvá, ceny.

Dimenzionálne tabuľky
**DimProduct (Produkty)**

Zdroj: *Tabuľka Product*
Atribúty:
- product_id (integer, primárny kľúč)
- product_name (varchar(30))
- description (varchar(250))
- availability (boolean)
- created_at (timestamp)
- category_id (integer, cudzí kľúč na DimCategory)

Účel: Umožňuje analýzu predajov podľa produktov (napr. najpredávanejšie produkty, dostupnosť).


**DimCategory (Kategórie)**

Zdroj: *Tabuľka Category*
Atribúty:
- category_id (integer, primárny kľúč)
- category_name (varchar(50))
- level_up_category (integer, cudzí kľúč na seba, nullable pre hierarchiu)

Účel: Analýza predajov podľa kategórií a ich hierarchie (napr. predaje v hlavných alebo podradených kategóriách).


**DimCustomer (Zákazníci)**

Zdroj: *Tabuľka Customers*
Atribúty:
- customer_id (integer, primárny kľúč)
- name (varchar(50))
- email (varchar(50))
- address (varchar(250))
- region_id (integer, cudzí kľúč na DimRegion)
- created_at (timestamp)

Účel: Analýza správania zákazníkov (napr. predaje podľa regiónu, noví vs. starí zákazníci).


**DimRegion (Regióny)**

Zdroj: *Tabuľka Region*
Atribúty:
region_id (integer, primárny kľúč)
- country (varchar(50))

Účel: Analýza predajov podľa geografického regiónu alebo krajiny.


**DimDate (Čas)**

Zdroj: *Generovaná tabuľka na základe časových atribútov (napr. created_at z Orders, Product, Transactions)*
Atribúty:
- date_id (integer, primárny kľúč)
- date (date)
- year (integer)
- quarter (integer)
- month (integer)
- day (integer)
- weekday (varchar)

Účel: Analýza časových trendov (napr. predaje podľa mesiaca, štvrťroka, dní v týždni).


Faktová tabuľka
**FactSales (Predaje)**

Zdroj: *Tabuľky Orders, Order_items, Transactions*
Atribúty:
- order_item_id (integer, primárny kľúč, zo Order_items)
- order_id (integer, cudzí kľúč na Orders)
- product_id (integer, cudzí kľúč na DimProduct)
- customer_id (integer, cudzí kľúč na DimCustomer)
- region_id (integer, cudzí kľúč na DimRegion)
- date_id (integer, cudzí kľúč na DimDate, odvodené z Orders.created)
- quantity (integer, zo Order_items.quantity)
- unit_price (decimal, zo Order_items.unit_price)
- total_price (decimal, vypočítané ako quantity * unit_price)
- order_status_shipped (boolean, zo Orders.order_status_shipped)

Účel: Umožňuje analýzu predajov podľa času, produktov, kategórií, zákazníkov a regiónov (napr. celkový obrat, počet predaných kusov, predaje podľa regiónu).




DBML kód pre hviezdicové schéma

```dbml
Table DimProduct {
  product_id integer [primary key]
  product_name varchar(30) [not null]
  description varchar(250)
  availability boolean [default: true]
  created_at timestamp
  category_id integer [ref: > DimCategory.category_id]
}

Table DimCategory {
  category_id integer [primary key]
  category_name varchar(50) [not null]
  level_up_category integer [ref: > DimCategory.category_id, null]
}

Table DimCustomer {
  customer_id integer [primary key]
  name varchar(50)
  email varchar(50) [not null, unique]
  address varchar(250) [not null]
  region_id integer [ref: > DimRegion.region_id, not null]
  created_at timestamp
}

Table DimRegion {
  region_id integer [primary key]
  country varchar(50) [not null]
}

Table DimDate {
  date_id integer [primary key]
  date date
  year integer
  quarter integer
  month integer
  day integer
  weekday varchar
}

Table FactSales {
  order_item_id integer [primary key]
  order_id integer
  product_id integer [ref: > DimProduct.product_id, not null]
  customer_id integer [ref: > DimCustomer.customer_id, not null]
  region_id integer [ref: > DimRegion.region_id, not null]
  date_id integer [ref: > DimDate.date_id, not null]
  quantity integer [default: 1, not null]
  unit_price decimal [not null]
  total_price decimal [note: 'quantity * unit_price']
  order_status_shipped boolean [default: false]
}
```


![Untitled](https://github.com/user-attachments/assets/3d521369-1820-4023-8746-6729c97b97ce)




## 3a. Primárne a cudzie kľúče

### Primárne kľúče
Primárny kľúč (PK) jednoznačne identifikuje každý záznam v tabuľke. Nasledujú primárne kľúče v jednotlivých tabuľkách:

- **Product**: `product_id` (integer)
- **Category**: `category_id` (integer)
- **Customers**: `customer_id` (integer)
- **Region**: `region_id` (integer)
- **Orders**: `order_id` (integer)
- **Order_items**: `order_item_id` (integer)
- **Transactions**: `transaction_id` (integer)

### Cudzie kľúče
Cudzie kľúče (FK) definujú vzťahy medzi tabuľkami. Nasledujú cudzie kľúče v jednotlivých tabuľkách:

- **Product**:
  - `category_id` → odkazuje na `Category.category_id`
- **Category**:
  - `level_up_category` → odkazuje na `Category.category_id` (rekurzívny vzťah, nullable pre hierarchiu)
- **Customers**:
  - `region` → odkazuje na `Region.region_id`
- **Orders**:
  - `customer_id` → odkazuje na `Customers.customer_id`
- **Order_items**:
  - `order_id` → odkazuje na `Orders.order_id`
  - `product` → odkazuje na `Product.product_id`
- **Transactions**:
  - `order_id` → odkazuje na `Orders.order_id`


## 3b. Možné normalizačné kroky a úrovne normalizácie

Normalizácia eliminuje redundancie a zabezpečuje konzistenciu dát. Model bol analyzovaný podľa normalizačných foriem (1NF, 2NF, 3NF).

### Aktuálny stav normalizácie

1. **Prvá normálna forma (1NF)**:
   - **Požiadavky**: Všetky atribúty musia byť atomické (nedeliteľné), žiadne opakujúce sa skupiny.
   - **Stav**: Všetky tabuľky spĺňajú 1NF, pretože atribúty (napr. `product_name`, `price`, `address`) sú atomické a nie sú použité opakujúce sa skupiny.
   - **Problémy**: Žiadne.

2. **Druhá normálna forma (2NF)**:
   - **Požiadavky**: Tabuľka musí byť v 1NF a ne-kľúčové atribúty musia byť plne funkčne závislé na primárnom kľúči.
   - **Stav**: Všetky tabuľky majú jednoduché primárne kľúče, takže 2NF je automaticky splnená (napr. v `Order_items` sú `quantity` a `unit_price` plne závislé na `order_item_id`).
   - **Problémy**: Žiadne.

3. **Tretia normálna forma (3NF)**:
   - **Požiadavky**: Tabuľka musí byť v 2NF a ne-kľúčové atribúty nesmú byť závislé na iných ne-kľúčových atribútoch (žiadne tranzitívne závislosti).
   - **Stav**: Väčšina tabuliek spĺňa 3NF. Potenciálna tranzitívna závislosť je v tabuľke `Customers`:
     - Atribút `address` môže obsahovať informácie o krajine (napr. „Bratislava, Slovensko“), ktorá je už uložená v `Region.country`, čo spôsobuje redundanciu.
   - **Problémy**:
     - `Customers.address`: Môže obsahovať redundantné informácie (napr. mesto, krajina), ktoré by mohli byť extrahované do samostatných atribútov.

### Možné normalizačné kroky

1. **Rozdelenie adresy v tabuľke Customers**:
   - **Problém**: Atribút `address` (varchar(250)) môže obsahovať rôzne časti adresy (ulica, mesto, krajina), čo vedie k potenciálnej redundancii s `Region.country`.
   - **Riešenie**: Rozdeliť `address` na atribúty: `street`, `city`, `postal_code`. Odstrániť redundanciu s `Region.country`.
   - **Navrhovaná štruktúra**:


     ```dbml
     Table Customers {
       customer_id integer [primary key]
       name varchar(50)
       email varchar(50) [not null, unique]
       street varchar(100)
       city varchar(50)
       postal_code varchar(20)
       region_id integer [ref: > Region.region_id, not null]
       created_at timestamp [default: `now()`]
     }
     ```
     
   - **Úroveň po kroku**: Plná 3NF, odstránenie tranzitívnej závislosti.

2. **Hierarchia kategórií**:
   - **Stav**: Tabuľka `Category` je v 3NF, pretože `level_up_category` podporuje hierarchiu bez tranzitívnych závislostí.
   - **Riešenie**: Nie je potrebná zmena, ale hierarchia môže byť denormalizovaná pre analytické účely (viď nižšie).

3. **Unit_price v Order_items**:
   - **Stav**: Atribút `unit_price` je normalizovaný, uchováva cenu produktu v čase objednávky, čím sa predchádza závislosti na `Product.price`.
   - **Riešenie**: Žiadna zmena nie je potrebná.

### Aktuálna úroveň normalizácie
Model je takmer v **3NF**, s výnimkou potenciálnej tranzitívnej závislosti v `Customers.address`. Po rozdelení adresy by model dosiahol plnú **3NF**.

## 3c. Denormalizácia pre analytické dotazy

Denormalizácia znižuje počet spojení (JOINs) v dotazoch, čím zvyšuje výkonnosť analytických dotazov v dátových skladoch (OLAP). Nasledujú návrhy na denormalizáciu:

1. **Spojenie Product a Category v DimProduct**:
   - **Problém**: Analytické dotazy (napr. predaje podľa kategórií) vyžadujú spojenie `Product` a `Category` cez `category_id`, čo môže byť pomalé pri veľkom objeme dát.
   - **Denormalizácia**:
     - Pridať `category_name` a `parent_category_name` do `DimProduct`.
   - **Výhoda**: Eliminuje potrebu spájania s `DimCategory`.
   - **Príklad**:
     
     ```dbml
     Table DimProduct {
       product_id integer [primary key]
       product_name varchar(30) [not null]
       price decimal(10,2)
       description varchar(250)
       availability boolean [default: true]
       created_at timestamp
       category_id integer [ref: > DimCategory.category_id]
       category_name varchar(50) [note: 'Denormalizované z Category']
       parent_category_name varchar(50) [note: 'Denormalizované z Category.level_up_category']
     }
     ```

2. **Spojenie Customers a Region v DimCustomer**:
   - **Problém**: Analýzy podľa regiónu vyžadujú spojenie `Customers` a `Region` cez `region_id`.
   - **Denormalizácia**:
     - Pridať `country` do `DimCustomer` z `Region.country`.
   - **Výhoda**: Znižuje počet JOIN operácií pri geografických analýzach.
   - **Príklad**:
     
     ```dbml
     Table DimCustomer {
       customer_id integer [primary key]
       name varchar(50)
       email varchar(50) [not null, unique]
       address varchar(250) [not null]
       region_id integer [ref: > DimRegion.region_id, not null]
       country varchar(50) [note: 'Denormalizované z Region']
       created_at timestamp
     }
     ```

3. **Časové atribúty v FactSales**:
   - **Problém**: Časové analýzy (napr. predaje podľa mesiaca) vyžadujú spojenie `FactSales` s `DimDate` cez `date_id`.
   - **Denormalizácia**:
     - Pridať `year`, `quarter`, `month` do `FactSales` z `Orders.created`.
   - **Výhoda**: Eliminuje spojenia s `DimDate` pre bežné časové analýzy.
   - **Príklad**:
     
     ```dbml
     Table FactSales {
       order_item_id integer [primary key]
       order_id integer
       product_id integer [ref: > DimProduct.product_id, not null]
       customer_id integer [ref: > DimCustomer.customer_id, not null]
       region_id integer [ref: > DimRegion.region_id, not null]
       date_id integer [ref: > DimDate.date_id, not null]
       quantity integer [default: 1, not null]
       unit_price decimal [not null]
       total_price decimal [note: 'quantity * unit_price']
       order_status_shipped boolean [default: false]
       year integer [note: 'Denormalizované z DimDate']
       quarter integer [note: 'Denormalizované z DimDate']
       month integer [note: 'Denormalizované z DimDate']
     }
     ```

4. **Hierarchia kategórií v DimCategory**:
   - **Problém**: Rekurzívne dotazy na hierarchiu kategórií (`level_up_category`) sú pomalé pri veľkom počte kategórií.
   - **Denormalizácia**:
     - Pridať `category_path` (napr. „Electronics > Phones > Smartphones“) do `DimCategory`.
   - **Výhoda**: Umožňuje rýchle filtrovanie podľa hierarchie bez rekurzívnych dotazov.
   - **Príklad**:
     
     ```dbml
     Table DimCategory {
       category_id integer [primary key]
       category_name varchar(50) [not null]
       level_up_category integer [ref: > DimCategory.category_id, null]
       category_path varchar(200) [note: 'Denormalizovaná cesta hierarchie']
     }
     ```

## Zhrnutie
- **Primárne a cudzie kľúče**: Model má jasne definované primárne a cudzie kľúče, s opraveným vzťahom medzi `Orders` a `Order_items`.
- **Normalizácia**: Model je takmer v 3NF, s odporúčaním rozdeliť `Customers.address` na samostatné atribúty (`street`, `city`, `postal_code`) pre plnú 3NF.
- **Denormalizácia**: Pre OLAP odporúčam pridať:
  - `category_name` a `parent_category_name` do `DimProduct`.
  - `country` do `DimCustomer`.
  - `year`, `quarter`, `month` do `FactSales`.
  - `category_path` do `DimCategory`.
  Tieto zmeny zlepšia výkonnosť analytických dotazov znížením počtu JOIN operácií.


## 4 Databázové schéma
Tento dokument obsahuje definíciu databázového schémy vo formáte DBML, ktorá popisuje štruktúru tabuliek a ich vzťahy pre systém správy produktov, kategórií, zákazníkov, regiónov, objednávok, položiek objednávok a transakcií. Schéma je navrhnutá pre použitie v dbdiagram.io na vizualizáciu ER diagramu.

DBML kód:
```dbml
Table Product {
  product_id integer [primary key]
  product_name varchar(30) [not null]
  price decimal(10,2)
  description varchar(250)
  availability boolean [default: true]
  created_at timestamp [default: `now()`]
  category_id integer [ref: > Category.category_id]
}

Table Category {
  category_id integer [primary key]
  category_name varchar(50) [not null]
  level_up_category integer [ref: > Category.category_id, null]
}

Table Customers {
  customer_id integer [primary key]
  name varchar(50)
  email varchar(50) [not null, unique]
  address varchar(250) [not null]
  region integer [ref: > Region.region_id, not null]
  created_at timestamp [default: `now()`]
}

Table Region {
  region_id integer [primary key]
  country varchar(50) [not null]
}

Table Orders {
  order_id integer [primary key]
  customer_id integer [ref: > Customers.customer_id, not null]
  created timestamp [default: `now()`]
  order_status_shipped boolean [default: false]
}

Table Order_items {
  order_item_id integer [primary key]
  order_id integer [ref: > Orders.order_id, not null]
  product integer [ref: > Product.product_id, not null]
  quantity integer [default: 1, not null]
  unit_price decimal [not null]
}

Table Transactions {
  transaction_id integer [primary key]
  order_id integer [ref: > Orders.order_id, not null]
  transaction_date timestamp [default: `now()`]
  payment_method varchar [not null]
  price decimal(10,2)
}
```

Popis tabuliek

**Product:** Uchováva informácie o produktoch, vrátane názvu, ceny, popisu, dostupnosti a kategórie.

**Category:** Uchováva hierarchiu kategórií produktov s možnosťou nadradených kategórií cez level_up_category.

**Customers:** Uchováva údaje o zákazníkoch, vrátane mena, e-mailu, adresy a regiónu.

**Region:** Uchováva informácie o geografických regiónoch (krajinách).

**Orders:** Uchováva informácie o objednávkach zákazníkov, vrátane dátumu vytvorenia a stavu odoslania.

**Order_items:** Uchováva položky objednávok, vrátane prepojenia na objednávku, produkt, množstvo a cenu za jednotku.

**Transactions:** Uchováva údaje o transakciách spojených s objednávkami, vrátane spôsobu platby a sumy.

Vzťahy

Product ↔ Category: M:1 (jeden produkt patrí do jednej kategórie, jedna kategória môže obsahovať viac produktov).

Category ↔ Category: 1:N (hierarchia – jedna kategória môže byť nadradená viacerým podkategóriám).

Customers ↔ Region: M:1 (jeden zákazník patrí do jedného regiónu, jeden región môže obsahovať viac zákazníkov).

Orders ↔ Customers: 1:N (jedna objednávka patrí jednému zákazníkovi, jeden zákazník môže mať viac objednávok).

Order_items ↔ Orders: 1:N (jedna položka patrí do jednej objednávky, jedna objednávka môže mať viac položiek).

Order_items ↔ Product: 1:N (jedna položka odkazuje na jeden produkt, jeden produkt môže byť v rôznych položkách).

Transactions ↔ Orders: 1:N (jedna transakcia patrí do jednej objednávky, jedna objednávka môže mať viac transakcií).

## Diskusia na záver

# Aké kompromisy by ste spravili medzi normalizáciou a výkonnosťou?
- z pohľadu  normalizácie by som premýšľal nad rozzdelením **Customers.address** pre transakčné systémy, aktualizácie historických zmien a konzistenciu dát
- z pohľadu výkonosti pridať napríklad **category_name, country, year** do tabuliek pre zrýchlenie dotazov, elimináciu JOIN metód
  
# Ako by ste riešili historické zmeny (napr. zmena ceny produktu, adresa zákazníka)?
- premýšľal by som čo si v danom momente môžem dovoliť a pri zmenách sa snažil zachovať historické údaje
- teda pri zmene ceny produktu vytvoriť nový produkt s údajmi starého a zmenenou cenou, pri starom produkte pridať položku **cena_platná_do** a vďaka tomu filtrovať výstupné dáta alebo dáta pre porovnanie historických predajov toho istého produktu pri rozdielnej cene
- pri zmene adresy zákazníka pri totožnom procese sledovať jeho historické nákupy s tými aktuálnymi
- tento postup by však vyvinul veľké požiadavky na systém a úložisko

- druhá možnosť by bola doplniť do tabuľky produktov položky "cena_platná_od" a "cena_platná_do" a na základe nich filtrovať výstupy
- tento spôsob by šetril miesto na úložiskua avšak komplikoval by samotné skripty

  
# Aké indexy by ste pridali na zlepšenie výkonnosti dotazov?
 - index na product_id, customer_id, region_id, date_id (cudzie kľúče), pretože sú často používané vo filtroch a JOINoch.
 ```plain
   CREATE INDEX idx_factsales_product_id ON FactSales (product_id);
CREATE INDEX idx_factsales_customer_id ON FactSales (customer_id);
CREATE INDEX idx_factsales_region_id ON FactSales (region_id);
CREATE INDEX idx_factsales_date_id ON FactSales (date_id);
```
 - index na order_status_shipped (boolean) pre rýchle filtrovanie odoslaných/neodoslaných objednávok
```plain
CREATE BITMAP INDEX idx_factsales_status ON FactSales (order_status_shipped);
```
 - B-tree index na category_id pre rýchle spojenie s DimCategory
```plain
CREATE INDEX idx_dimproduct_category_id ON DimProduct (category_id);
```
 - B-tree index na region_id pre analýzy podľa regiónu
  ```plain
   CREATE INDEX idx_dimcustomer_region_id ON DimCustomer (region_id);
```
- B-tree index na year, quarter, month pre rýchle časové agregácie
```plain
  CREATE INDEX idx_dimdate_year_month ON DimDate (year, month);
```
- ak sú pridané category_name, country, year atď., vytvoriť indexy na tieto stĺpce pre rýchle filtrovanie
```plain
  CREATE INDEX idx_dimproduct_category_name ON DimProduct (category_name);
CREATE INDEX idx_dimcustomer_country ON DimCustomer (country);
CREATE INDEX idx_factsales_year_month ON FactSales (year, month);
```
