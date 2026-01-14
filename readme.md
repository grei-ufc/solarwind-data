![Head](.\input\assets\header.png)

Hi, this documentantion had 3 versions, one in [american english](#english-version), one in [brazilian portugues](#versão-em-pt-br), and one in [italian](#versione-italiana). Just click in the prefered languagem, there're hiperlink! :3

# ENGLISH VERSION
## *General Overview*

Before using this library, it is important to note that it was originally developed to be applied to the State of Ceará, in northeastern Brazil, where it was created.

If you intend to analyze data within the Ceará region and already have a Copernicus API key, the code is ready for use, and you can proceed to the [Script Usage](https://www.google.com/search?q=%23script-usage) section. If you do not have a key, follow the instructions for [API Key Creation](https://www.google.com/search?q=%23api-key-creation). If you are not analyzing a point within Ceará, follow the instructions for [Downloading Input Data](https://www.google.com/search?q=%23downloading-input-data) required for analyzing other regions.

### *Inputs*

The script utilizes public data to perform calculations:

* **Capacity Factor** - Extracted from the Global Wind Atlas.
* GeoTIFF file of capacity factors considering IEC CLASS II turbines: In the default version of the library, the input file is located in the `input` folder and was downloaded specifically for the onshore and offshore zones of the state of Ceará.

* **Wind Speed Data** - Copernicus Database:
* This data is automatically downloaded using the CDS API.

* **Solar Radiation Data** - Copernicus Database:
* This data is automatically downloaded using the CDS API.

### Outputs

The script calculates the mean, standard deviation, and variance of solar and wind energy production density for the state of Ceará (onshore and offshore). It takes coordinates as input and generates 8 output files:

* **6 .pdf files:** - Solar_Monthly_Average_PV_Density_Lat_{LAT}*Lon*{LON}.pdf
* Solar_PV_Production_3D_Lat_{LAT}*Lon*{LON}.pdf
* Wind_Standard_Deviation_3D_Lat_{LAT}*Lon*{LON}.pdf
* Wind_Coefficient_of_Variation_Lat_{LAT}*Lon*{LON}.pdf
* Wind_Monthly_Average_Energy_Density_Lat_{LAT}*Lon*{LON}.pdf
* Wind_Monthly_Standard_Deviation_Lat_{LAT}*Lon*{LON}.pdf


* **2 .html files:**
* Solar_PV_Production_3D_Lat_{LAT}*Lon*{LON}.html
* Wind_Standard_Deviation_3D_Lat_{LAT}*Lon*{LON}.html

## Script Usage

### Library Installation

### Running the Script

You can use the functions for solar and wind variable calculations individually or together. Enter the command according to your needs, as shown in the examples:

* `main.py --lat -4.58 --lon -38.18` -> Runs both wind and solar functions.
* `solar_only --lat -4.58 --lon -38.18` -> Runs only solar functions.
* `wind_only --lat -4.58 --lon -38.18` -> Runs only wind functions.

---

## API Key Creation

The user must register to generate an API key that allows for wind speed data requests. Subsequently, the download is performed automatically by the Python script once the user specifies the coordinate points of interest. After downloading, the file containing wind speed data at 100m is compiled into NetCDF (Network Common Data Form) format, which is used especially in atmospheric sciences, oceanography, and climatology to store multidimensional array data oriented by variables such as temperature, pressure, and altitude.

To use the API, you must:

1. **Create an account.** Access:
[Log in to ECMWF](https://accounts.ecmwf.int/auth/realms/ecmwf/protocol/openid-connect/auth?client_id=cds&scope=openid%20email&response_type=code&redirect_uri=https%3A%2F%2Fcds.climate.copernicus.eu%2Fapi%2Fauth%2Fcallback%2Fkeycloak&state=X0ZFK66lgHktDi7q448c4FTx4mWvyApaPLSTGx3HIOs&code_challenge=UEQ-ytrY96TE4mal3ALECQ0zwiPNKRbFgqpE9SmuGZw&code_challenge_method=S256)

2. **Access the CDS API page:**
[CDSAPI setup - Climate Data Store](https://accounts.ecmwf.int/auth/realms/ecmwf/protocol/openid-connect/auth?client_id=cds&scope=openid%20email&response_type=code&redirect_uri=https%3A%2F%2Fcds.climate.copernicus.eu%2Fapi%2Fauth%2Fcallback%2Fkeycloak&state=X0ZFK66lgHktDi7q448c4FTx4mWvyApaPLSTGx3HIOs&code_challenge=UEQ-ytrY96TE4mal3ALECQ0zwiPNKRbFgqpE9SmuGZw&code_challenge_method=S256)

Once logged in, access the link above and scroll down to view the following panel:

In this panel, your API key will appear in place of `<PERSONAL-ACCESS-TOKEN>`. Keep it in a safe place, as it is your identifier for requesting data.

3. **Accept the terms of use.**
To do this, access the Copernicus datasets page and open any of them:
[Catalogue — Climate Data Store](https://cds.climate.copernicus.eu/datasets)

[Source: COPERNICUS CLIMATE CHANGE SERVICE. ERA5 monthly averaged data on single levels from 1940 to present](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means?tab=download)

With the account logged in, there is a checkbox that must be checked to accept the terms of use. Only after acceptance will both the website and the API be able to fulfill information requests. This procedure only needs to be done once. When accessing the dataset, go to the download page and scroll to the bottom of the variable selection field:

---

## Downloading Input Data

If you want to use the library for areas outside the state of Ceará, you must insert several files into the "input" folder, including:

* 1 shapefile of the region of interest.
* 1 IEC CLASS II capacity factor .tiff extracted from the Global Wind Atlas.
* 12 solar energy density GeoTIFFs extracted from the Global Solar Atlas.

### Downloading Shapefiles for Regions in Brazil:

If you want to analyze a specific state in Brazil, access the IBGE website:
[State Shapefiles - IBGE](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15774-malhas.html)

Clicking on any state will automatically start the download of a .zip file. Unzip the folder and save all contents in the "input" folder.

### Downloading Capacity Factor GeoTIFF:

To calculate power density, the capacity factor is required—an index that relates actual production to the maximum possible production of a wind turbine. This information is available on the Global Wind Atlas platform and can be downloaded. The platform allows for the upload of georeferenced files to delimit areas in the “MyAreas” tab:

[Source: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas. DTU Wind Energy. 2025](https://globalwindatlas.info/en.html)

Once the file for the desired area is inserted into the Global Wind Atlas platform, it will be available in “MyAreas”:

[Source: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas. DTU Wind Energy. 2025](https://globalwindatlas.info/en.html)

Now configure the parameters in the menu on the right, as shown in the following image:
[Source: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas. DTU Wind Energy. 2025](https://globalwindatlas.info/en.html)

Click “Generate plot,” and a new map will appear. Then, click the “Energy” menu and download the file with the capacity factors in GeoTIFF (.tiff) format:

[Source: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas. DTU Wind Energy. 2025](https://globalwindatlas.info/en.html)

Save this file in the "input" folder and change the filename in the wind calculation code.

# Versão em PT-BR
## *Descrição geral*
Antes de usar a biblioteca, é importante saber que ela foi originalmente elaborada para ser aplicada ao Estado do Ceará, no nordeste do Brasil, local em que foi elaborado.
Se você pretende analisar dados dentro da área do Ceará e possui uma chave da API Copernicus, o código pode ser prontamente utilizado e você pode seguir para a sessão de [uso do script](#uso-do-script). Caso não possua a chave, siga para a instrução de [criação da chave de API](#criação-de-chave-de-api) e caso não vá analisar um ponto dentro do Ceará, siga para as instruções de [download de inputs](#download-de-dados-de-entrada) necessários para analise de outras regiões.

### *Entradas*
O script se utiliza de dados públicos para realizar os cálculos:

* Fator de capacidade (Capacity Factor) - Extraído da Global Wind Atlas
    - Arquivo Geottif de fatores de capacidade considerando turbinas IEC CLASS II: na versão padrão da biblioteca, o arquivo de entrada está na pasta input e foi baixado somente para as zonas onshore e offshore do estado do Ceará.
* Dados de velocidade de ventos - Copernicus Database:
    -  Esses dados são baixados automaticamente utilizando a API CDS.
* Dados de radiação solar - Copernicus Database
    -  Esses dados são baixados automaticamente utilizando a API CDS.

### Saídas
O script calcula a média, desvio padrão e variância da densidade de produção de energia solar e eólica para o estado do Ceará, onshore e offshore. Tendo como entrada as coordenadas e como saída 8 arquivos:

- 6 arquivos .pdf: 
    - Solar_Monthly_Average_PV_Density_Lat_{LAT}_Lon_{LON}.pdf
    - Solar_PV_Production_3D_Lat_{LAT}_Lon_{LON}.pdf
    - Wind_Standard_Deviation_3D_Lat_{LAT}_Lon_{LON}.pdf
    - Wind_Coefficient_of_Variation_Lat_{LAT}_Lon_{LON}.pdf
    - Wind_Monthly_Average_Energy_Density_Lat_{LAT}_Lon_{LON}.pdf
    - Wind_Monthly_Standard_Deviation_Lat_{LAT}_Lon_{LON}.pdf

- 2 arquivos .html:
 - Solar_PV_Production_3D_Lat_{LAT}_Lon_{LON}.html
 - Wind_Standard_Deviation_3D_Lat_{LAT}_Lon_{LON}.html


## Uso do script

### Instalação de bibliotecas

### Chamando script
É possível utilizar as funções para calculos da variaveis solares e éolicas individualmente ou conjuntamente. Digite o comando conforme o tipo de uso, como nos exemplos

main.py --lat -4.58 -- lon -38.18 -> Usa as funções de éolica e solar 
solar_only --lat -4.58 -- lon -38.18 -> Usa somente as funções de solar
wind_only  --lat -4.58 -- lon -38.18 -> Usa somente as funções de eólica

## Criação de chave de API

O usuário realiza um cadastro para gerar a chave de API que permite  realizar a requisição dos dados de velocidade, em seguida, é feito o download de forma automática pelo próprio script em python após o usuário determinar os pontos de coordenadas de interesse para estudo. Após o download, o arquivo contendo os dados de velocidade a 100m é compilado em formato NetCDF (Network Common Data Form) que é utilizado especialmente em ciências atmosféricas, oceanografia e climatologia, para armazenar dados de array multidimensionais orientados a variáveis, como temperatura, pressão, e altitude. 

Para usar a API, deve-se:

1. Criar uma conta. Acesse [9]:

[Log in to ECMWF](https://accounts.ecmwf.int/auth/realms/ecmwf/protocol/openid-connect/auth?client_id=cds&scope=openid%20email&response_type=code&redirect_uri=https%3A%2F%2Fcds.climate.copernicus.eu%2Fapi%2Fauth%2Fcallback%2Fkeycloak&state=X0ZFK66lgHktDi7q448c4FTx4mWvyApaPLSTGx3HIOs&code_challenge=UEQ-ytrY96TE4mal3ALECQ0zwiPNKRbFgqpE9SmuGZw&code_challenge_method=S256)
 
2. Acessar a página da CDS API [10]:
[CDSAPI setup - Climate Data Store](https://accounts.ecmwf.int/auth/realms/ecmwf/protocol/openid-connect/auth?client_id=cds&scope=openid%20email&response_type=code&redirect_uri=https%3A%2F%2Fcds.climate.copernicus.eu%2Fapi%2Fauth%2Fcallback%2Fkeycloak&state=X0ZFK66lgHktDi7q448c4FTx4mWvyApaPLSTGx3HIOs&code_challenge=UEQ-ytrY96TE4mal3ALECQ0zwiPNKRbFgqpE9SmuGZw&code_challenge_method=S256)

Agora com o login feito, acesse o link acima e role a tela para visualizar o seguinte painel:

![Tela de token de acesso da CDS API - Fonte: COPERNICUS CLIMATE CHANGE SERVICE.](.\input\assets\copernicus_api_key_screen.png)
 
Nele, no lugar de <PERSONAL-ACESS-TOKEN>  aparecerá sua chave de API, guarde-a em um local seguro, pois é seu identificador para requisitar dados.

3. Aceitar os termos de uso.
 Para tal, acesse a página de datasets  da Copernicus e abra qualquer um deles:

[Catalogue — Climate Data Store](https://cds.climate.copernicus.eu/datasets)

![Páginas de datasets da Copernicus - Fonte: COPERNICUS CLIMATE CHANGE SERVICE](.\input\assets\copernicus_dataset_screen.png) 
 

![Página do dataset “ERA5 monthly averaged data on single levels from 1940 to present.](.\input\assets\copernicus_requests_config_screen.png) 

 [Fonte: COPERNICUS CLIMATE CHANGE SERVICE. ERA5 monthly averaged data on single levels from 1940 to present](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means?tab=download)

Com a conta logada, há uma checkbox que deve ser marcada, aceitando os termos de uso. Somente após o aceite, tanto o site quanto a api ficam aptos à atender à solicitação de informações. O procedimento só precisa ser feito uma vez. Ao acessar o dataset  vá para a página de download e role a tela até o final do campo de seleção de variáveis:

![Aceitar termos de uso](.\input\assets\copernicus_conditions_screen.png)

## Download de dados de entrada
Caso você queria utilizar a biblioteca para áreas fora do estado do Ceará, é necessário inserir na pasta "input" alguns arquivos, dentre eles:

- 1  shapefile da região e interesse
- 1 .tiff de fator de capacidade IEC  CLASSE II extraído do Global Wind  Atlas. 
- 12 geotiffs de densidade de energia solar extraídos da Global Solar Atlas.

### Download de shapefile de região do Brasil:
Se deseja analisar todo um estado do Brasil, acesso o site do IBGE:

[Shapefiles de estados - IBGE](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15774-malhas.html)

![Mapas de estados e municípios do Brasil disponiveis no IBGE](.\input\assets\copernicus_requests_config_screen.png) 

Ao clicar em qualquer estado, será realizado automaticamente o download de um arquivo .zip. Descompacte a pasta e salve todo o conteudo em na pasta "input"

### Download de geotiff de fator de capacidade:

Para o cálculo de densidade de potência, é necessário o fator de capacidade, um índice que relaciona a produção real à máxima produção possível de um aerogerador. Estas informações estão disponíveis na plataforma Global Wind Atlas e podem ser baixadas. A plataforma permite o upload de arquivos georreferenciados para delimitação de áreas, na aba “MyAreas”:

![Visualização da interface inicial do Global Wind Data](.\input\assets\my_areas_global_wind.png) 
[Fonte: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas.DTU Wind Energy. 2025](https://globalwindatlas.info/en.html)

Com o arquivo da área desejada já inserido na plataforma Global Wind Atlas, este ficará disponível em “MyAreas”:

![Menu do Global Wind Atlas indicando as áreas salvas pelo usuário](.\input\assets\menu_global_wind.png) 
[Fonte: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas.DTU Wind Energy. 2025](https://globalwindatlas.info/en.html)

Agora configure os parâmetros no menu à direita, conforme a imagem a seguir:
![Menu do Global Wind Atlas na aba de configurações.](.\input\assets\menu_global_wind_config.png) 
[Fonte: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas.DTU Wind Energy. 2025](https://globalwindatlas.info/en.html)


Clique em “Generate plot” e um novo mapa surgirá. Clique então no menu “Energy” e baixe o arquivo com os fatores de capacidade, no formato Geottif (.tiff):

![Menu do Global Wind Atlas na aba de downloads](.\input\assets\final_area_global_wind.png) 
[Fonte: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas.DTU Wind Energy. 2025](https://globalwindatlas.info/en.html)

Salve esse arquivo na pasta "input" e no código de eólica, altere o nome do arquivo.

# Versione italiana

Descrizione Generale
Prima di utilizzare la libreria, è importante sapere che è stata originariamente sviluppata per essere applicata allo Stato del Ceará, nel nord-est del Brasile, luogo in cui è stata creata.

Se intendi analizzare dati all'interno dell'area del Ceará e possiedi una chiave API Copernicus, il codice è pronto all'uso e puoi passare alla sezione Uso dello Script. Se non possiedi la chiave, segui le istruzioni per la Creazione della chiave API; nel caso in cui tu non debba analizzare un punto all'interno del Ceará, segui le istruzioni per il Download dei dati di input necessari per l'analisi di altre regioni.

Input
Lo script utilizza dati pubblici per eseguire i calcoli:

Fattore di capacità (Capacity Factor) - Estratto dal Global Wind Atlas.

File GeoTIFF dei fattori di capacità considerando turbine IEC CLASS II: nella versione standard della libreria, il file di input si trova nella cartella input ed è stato scaricato solo per le zone onshore e offshore dello stato del Ceará.

Dati sulla velocità dei venti - Database Copernicus:

Questi dati vengono scaricati automaticamente utilizzando l'API CDS.

Dati sulla radiazione solare - Database Copernicus:

Questi dati vengono scaricati automaticamente utilizzando l'API CDS.

Output
Lo script calcola la media, la deviazione standard e la varianza della densità di produzione di energia solare ed eolica per lo stato del Ceará, onshore e offshore. Riceve come input le coordinate e genera in uscita 8 file:

6 file .pdf:

Solar_Monthly_Average_PV_Density_Lat_{LAT}Lon{LON}.pdf

Solar_PV_Production_3D_Lat_{LAT}Lon{LON}.pdf

Wind_Standard_Deviation_3D_Lat_{LAT}Lon{LON}.pdf

Wind_Coefficient_of_Variation_Lat_{LAT}Lon{LON}.pdf

Wind_Monthly_Average_Energy_Density_Lat_{LAT}Lon{LON}.pdf

Wind_Monthly_Standard_Deviation_Lat_{LAT}Lon{LON}.pdf

2 file .html:

Solar_PV_Production_3D_Lat_{LAT}Lon{LON}.html

Wind_Standard_Deviation_3D_Lat_{LAT}Lon{LON}.html

Uso dello script
Installazione delle librerie
Chiamata dello script
È possibile utilizzare le funzioni per il calcolo delle variabili solari ed eoliche individualmente o congiuntamente. Digita il comando in base al tipo di utilizzo, come negli esempi:

main.py --lat -4.58 --lon -38.18 -> Usa le funzioni eolica e solare.

solar_only --lat -4.58 --lon -38.18 -> Usa solo le funzioni solari.

wind_only --lat -4.58 --lon -38.18 -> Usa solo le funzioni eoliche.

Creazione della chiave API
L'utente effettua una registrazione per generare la chiave API che permette di richiedere i dati di velocità; successivamente, il download viene effettuato automaticamente dallo script Python dopo che l'utente ha determinato i punti di coordinate di interesse per lo studio. Dopo il download, il file contenente i dati di velocità a 100m viene compilato in formato NetCDF (Network Common Data Form), utilizzato specialmente nelle scienze atmosferiche, oceanografia e climatologia per memorizzare dati di array multidimensionali orientati alle variabili, come temperatura, pressione e altitudine.

Per usare l'API, è necessario:

Creare un account. Accedi a [9]: Log in to ECMWF

Accedere alla pagina della CDS API [10]: CDSAPI setup - Climate Data Store

Una volta effettuato il login, accedi al link sopra indicato e scorri la schermata per visualizzare il seguente pannello:

In esso, al posto di <PERSONAL-ACCESS-TOKEN> apparirà la tua chiave API; conservala in un luogo sicuro, poiché è il tuo identificativo per richiedere i dati.

Accettare i termini d'uso. A tal fine, accedi alla pagina dei dataset di Copernicus e aprine uno qualsiasi: Catalogue — Climate Data Store

Fonte: COPERNICUS CLIMATE CHANGE SERVICE. ERA5 monthly averaged data on single levels from 1940 to present

Con l'account collegato, c'è una casella di controllo da spuntare per accettare i termini d'uso. Solo dopo l'accettazione, sia il sito che l'API saranno abilitati a rispondere alla richiesta di informazioni. La procedura deve essere eseguita una sola volta. Quando accedi al dataset, vai alla pagina di download e scorri fino alla fine del campo di selezione delle variabili:

Download dei dati di input
Se desideri utilizzare la libreria per aree esterne allo stato del Ceará, è necessario inserire nella cartella "input" alcuni file, tra cui:

1 shapefile della regione d'interesse.

1 .tiff del fattore di capacità IEC CLASSE II estratto dal Global Wind Atlas.

12 GeoTIFF di densità di energia solare estratti dal Global Solar Atlas.

Download dello shapefile della regione del Brasile:
Se desideri analizzare un intero stato del Brasile, accedi al sito dell'IBGE: Shapefiles degli stati - IBGE

Cliccando su qualsiasi stato, verrà eseguito automaticamente il download di un file .zip. Decomprimi la cartella e salva tutto il contenuto nella cartella "input".

Download del GeoTIFF del fattore di capacità:
Per il calcolo della densità di potenza è necessario il fattore di capacità, un indice che mette in relazione la produzione reale con la massima produzione possibile di un aerogeneratore. Queste informazioni sono disponibili sulla piattaforma Global Wind Atlas e possono essere scaricate. La piattaforma permette l'upload di file georeferenziati per la delimitazione delle aree, nella scheda “MyAreas”:

Fonte: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas. DTU Wind Energy. 2025

Con il file dell'area desiderata già inserito nella piattaforma Global Wind Atlas, questo sarà disponibile in “MyAreas”:

Fonte: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas. DTU Wind Energy. 2025

Ora configura i parametri nel menu a destra, come nell'immagine seguente: Fonte: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas. DTU Wind Energy. 2025

Clicca su “Generate plot” e apparirà una nuova mappa. Clicca quindi sul menu “Energy” e scarica il file con i fattori di capacità, in formato GeoTIFF (.tiff):

Fonte: TECHNICAL UNIVERSITY OF DENMARK - DTU. Global Wind Atlas. DTU Wind Energy. 2025

Salva questo file nella cartella "input" e, nel codice dell'eolica, modifica il nome del file.







