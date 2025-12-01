
# Alat za vizualizaciju FPGA

**Specijalizovana CLI (Command-line) aplikacija za vizualizaciju i analizu rezultata FPGA rutiranja generisanih putem VTR (Verilog-to-Routing) alata.**

Razvijen tokom predmeta **Razvoj Informacionih Sistema (PRIS)** na Univerzitetu u Novom Sadu, ovaj projekat pruža ključne uvide u arhitekturu čipa, zagušenje signala i konflikte rutiranja za napredno istraživanje automatizacije elektronskog dizajna (EDA).

**Tim:** PRIS Tim 6 (Andrej Rajkov i Jovan Stepančev)

**Datum:** Oktobar 2025

## 💡 Problem i naše rešenje

Napredno istraživanje i dizajn FPGA čipova i pratećih CAD algoritama (kao što je VTR/VPR) često se suočavaju sa otvorenim pitanjima o optimalnoj arhitekturi i strategijama plasiranja/rutiranja. Odgovaranje na ova pitanja zahteva alate koji mogu vizualizovati i izdvojiti statističke podatke iz rezultata rutiranja.

Naše rešenje je specijalizovani alat za vizualizaciju koji obrađuje VTR podatke o rutiranju i pruža istraživačima više analitičkih pogleda (grafikone, heatmape i izveštaje) za proučavanje ponašanja signala, zagušenja i konflikata.

## Galerija Slika

<div style="width: 100%; overflow-x: auto; padding: 10px 0; border: 1px solid #e2e8f0; border-radius: 8px;">

<!-- Inner container: Forces all content onto a single line that exceeds the viewport width -->

<div style="white-space: nowrap; min-width: 3000px; text-align: left;">

<a href="<https://github.com/user-attachments/assets/6a6e85bf-e258-45ef-a57f-ba02c867b0d8>" target="_blank"> <img src="<https://github.com/user-attachments/assets/6a6e85bf-e258-45ef-a57f-ba02c867b0d8>" alt="FPGA Main Menu" height="200px" style="display: inline-block; object-fit: cover; margin: 0 10px; border: 2px solid #333; border-radius: 5px; cursor: pointer;" /> </a>

<a href="<https://github.com/user-attachments/assets/dc92d0c9-ffe8-4921-8c26-424442120604>" target="_blank"> <img src="<https://github.com/user-attachments/assets/dc92d0c9-ffe8-4921-8c26-424442120604>" alt="FPGA Architecture" height="200px" style="display: inline-block; object-fit: cover; margin: 0 10px; border: 2px solid #333; border-radius: 5px; cursor: pointer;" /> </a>

<a href="<https://github.com/user-attachments/assets/391e86ce-d121-442c-82e3-09020a17b3d7>" target="_blank"> <img src="<https://github.com/user-attachments/assets/391e86ce-d121-442c-82e3-09020a17b3d7>" alt="FPGA Many Signals" height="200px" style="display: inline-block; object-fit: cover; margin: 0 10px; border: 2px solid #333; border-radius: 5px; cursor: pointer;" /> </a>

<a href="<https://github.com/user-attachments/assets/ee956d47-3ccf-4848-aa87-5a910e5fe46a>" target="_blank"> <img src="<https://github.com/user-attachments/assets/ee956d47-3ccf-4848-aa87-5a910e5fe46a>" alt="FPGA Filtered Signals" height="200px" style="display: inline-block; object-fit: cover; margin: 0 10px; border: 2px solid #333; border-radius: 5px; cursor: pointer;" /> </a>

<a href="<https://github.com/user-attachments/assets/7967f51b-b632-4e24-924b-3b4a8fe0c3fe>" target="_blank"> <img src="<https://github.com/user-attachments/assets/7967f51b-b632-4e24-924b-3b4a8fe0c3fe>" alt="FPGA Signal Report" height="200px" style="display: inline-block; object-fit: cover; margin: 0 10px; border: 2px solid #333; border-radius: 5px; cursor: pointer;" /> </a>

<a href="<https://github.com/user-attachments/assets/0ecfdb18-ca7a-4270-b6f9-5388b8aca4ab>" target="_blank"> <img src="<https://github.com/user-attachments/assets/0ecfdb18-ca7a-4270-b6f9-5388b8aca4ab>" alt="FPGA Bounding Boxes" height="200px" style="display: inline-block; object-fit: cover; margin: 0 10px; border: 2px solid #333; border-radius: 5px; cursor: pointer;" /> </a>

<a href="<https://github.com/user-attachments/assets/b6437f03-4cd8-4acd-a318-da99ac323b3d>" target="_blank"> <img src="<https://github.com/user-attachments/assets/b6437f03-4cd8-4acd-a318-da99ac323b3d>" alt="FPGA HEATMAP" height="200px" style="display: inline-block; object-fit: cover; margin: 0 10px; border: 2px solid #333; border-radius: 5px; cursor: pointer;" /> </a>

<a href="<https://github.com/user-attachments/assets/d08f6b60-527b-409e-aa61-f1e0afea3a60>" target="_blank"> <img src="<https://github.com/user-attachments/assets/d08f6b60-527b-409e-aa61-f1e0afea3a60>" alt="FPGA REPORT" height="200px" style="display: inline-block; object-fit: cover; margin: 0 10px; border: 2px solid #333; border-radius: 5px; cursor: pointer;" /> </a>

<a href="<https://github.com/user-attachments/assets/ff5976f0-2098-44bd-8769-7868f59d81d8>" target="_blank"> <img src="<https://github.com/user-attachments/assets/ff5976f0-2098-44bd-8769-7868f59d81d8>" alt="FPGA LOG FILE" height="200px" style="display: inline-block; object-fit: cover; margin: 0 10px; border: 2px solid #333; border-radius: 5px; cursor: pointer;" /> </a> </div> </div>

## 🚀 Ključne funkcije i vizualizacije

Alat obrađuje VTR-ov format datoteke `.route` i pruža nekoliko ključnih funkcionalnosti putem CLI-ja vođenog menijem:

### Vizualizacija arhitekture

-   **Raspored čipa (Chip Layout):** Prikazuje 2D matricu CLB-ova (Configurable Logic Blocks) i IO (Input/Output) blokova.
    
-   **Ivice rutiranja (Routing Edges):** Opcionalno prikazuje konceptualne međusobno povezujuće ivice i kanale rutiranja.
    

### Vizualizacija rutiranja signala

-   **Praćenje putanje Signala (Signal Path Tracing):** Crtanje fizičke putanje (stabla rutiranja) pojedinačnih ili više odabranih signala preko resursa za rutiranje čipa (žica i prekidačkih blokova).
    
-   **Filtriranje:** Omogućava napredno filtriranje i vizualizaciju signala na osnovu metrika kao što je broj izlaznih čvorova (MINSINK/MAXSINK) ili veličina njihovog graničnog okvira (MINBB/MAXBB).
    
-   **Izveštaji o signalima:** Generisanje detaljnih tekstualnih izveštaja filtriranih signala, uključujući izračunate dimenzije njihovog Graničnog okvira (npr. površina, visina, širina).
    

### Analiza graničnog okvira (Bounding Box - BB)

- **Vizualizacija:** Iscrtavanje najmanjeg opisanog pravougaonika **(Bounding Box)**, koji obuhvata putanju rutiranja signala, ključne metrike za procenu dužine žice ($\text{HPWL}$ - Half-Perimeter Wirelength).

- **Izveštavanje o preklapanju:** Generisanje detaljnog izveštaja koji navodi svaki par signala čiji se granični okviri preklapaju, pružajući koordinate i parove konflikata.

### Vizualizacija toplotne mape (Heatmap)

- **Mapiranje zagušenja:** Prikaz prostorne distribucije iskorišćenosti/zagušenja čvorova širom čipa.

- **Legenda korišćenja:** Korišćenje legende kodirane bojama za prikaz učestalosti korišćenja čvorova rutiranja, ističući visoko zagušena područja.

- **Izveštaj o čvorovima:** Izlazak tekstualnog izveštaja koji detaljno opisuje teško i umereno korišćene čvorove rutiranja, navodeći broj signala i njihove ID-ove koji prolaze kroz njih.

### Analiza konfliktnog grafa

- **Izveštaj o konfliktu:** Generisanje izveštaja koji identifikuje sve parove signala koji su u konfliktu (dele resurse) tokom PathFinder iterativnog procesa rutiranja.

- **Težina konflikta:** Izveštava o težini konflikta (npr. broj zajedničkih čvorova), što je ključno za analizu težine rutiranja.

## 🛠️ Tehnologije (Technology Stack)

**Kontekst glavnog alata**: Verilog-to-Routing (VTR)

**Podržani sistemi**: macOS, Windows i Linux

## 💻 Instalacija i korišćenje

Aplikacija se pokreće preko interfejsa komandne linije (CLI) i zahteva Python 3.

### 1. Klonirajte repozitorijum

```
git clone [https://github.com/andrej1011/pris_team6/](https://github.com/andrej1011/pris_team6/)
cd pris_team6
```

### 2. Instalirajte zavisnosti

Potrebna biblioteka za vizualizaciju je `matplotlib`.

```
pip install matplotlib
```

### 3. Pokretanje alata

Pokrenite aplikaciju iz glavnog direktorijuma:

```
python3 main.py
```

Ovo će pokrenuti glavni meni, omogućavajući vam da odaberete opcije vizualizacije i izveštavanja.

### 4. Upravljanje izlazom

Pri svakom izvršavanju, program beleži metapodatke i generisane fajlove:

- **Izveštaji dnevnika (Log Reports):** Detaljan log fajl se automatski generiše (npr. `log_70.log`), i beleži vreme izvršavanja, ulaznu datoteku, odabrane opcije i nazive svih generisanih izlaznih datoteka.

- **Generisane datoteke:** Vizualizacije (PNG slike) i tekstualni izveštaji (npr. `heatmap_report_75.log`) se čuvaju u folderima `slike/` i `reports/`.
