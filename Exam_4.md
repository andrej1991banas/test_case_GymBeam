## Výkonnostný problém v SQL transformácii

Najpravdepodobnejšími príčinami sú rast dát, neoptimálne dotazy alebo nedostatočné zdroje.

# 1 Rast dát
**Dáta pribúdajú a dá sa predpokladať, že aj zbieranie dát z čoraz väčšieho modelu bude trvať dlhšie.**
- efektívna správa dát, validácie a aktualizácie dát, premazávanie starých a nepotrebných dát
- rozdeľovanie tabuliek na viacero podtabuliek, kde sa dáta prerozdelia a vhodnými JOIN metódami či INDEXami ich získavať späť
- zväčšené množstvo dát má za následok aj zvýšené požiadavky na CPU, zvážiť preto aj aktualizáciu hardveru

# 2 Neoptimálne SQL dotazy
**Zastaralé metódy, nevhodné skripty, neindexovanie často využívaných stĺpcov, neharmonizované dátové formáty.**
- nesprávny SQL skrip môže získavať stĺpce, ktoré nepotrebujeme, prechádzať tabuľky, ktoré nie sú potrebné alebo duplikovať zozbierané dáta
- neindexovanie často vyhľadávaných stĺpcov má za následok, že pri každom spustení skriptu sa celá tabuľka musí prejsť znova
- zastaralé skripty môžu spomaliť celý proces
- nevhondý JOIN môže zbierať údaje, ktoré reálne nepotrebujeme a tak enefektívne využiť kapacitu CPU

# 3 Nedostatočné zdroje
**Preťaženie CPU, nedostatok miesta na diskoch, prechod na platformy pre spracovanie veľkého množstva dát**
- prechod na robustnejšie riešenie, ako streamové spracovanie (napr. Apache Kafka, Spark) pre veľké objemy dát
- sledovanie metriky servera (CPU, I/O, pamäť) počas behu transformácie
  
