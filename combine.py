fp = 'sewage-data.xlsx'

import pandas as pd

SHEET_NAMES = [
    "Anglian Water 2023",
    "DCWW 2023",
    "Northumbrian Water 2023",
    "Severn Trent 2023",
    "South West Water 2023",
    "Southern Water 2023",
    "Thames Water 2023",
    "United Utilities 2023",
    "Wessex Water 2023",
    "Yorkshire Water 2023"
]

# column names with shortened versions Water Company Name	Site Name (EA Consents Database)	Site Name (WaSC operational) [optional]	EA Permit Reference (EA Consents Database)	WaSC Supplementary Permit Ref. [optional]	Activity Reference on Permit	Storm Discharge Asset Type	Outlet Discharge NGR (EA Consents Database)	WFD Waterbody ID (Cycle 2) (discharge outlet)	WFD Waterbody Catchment Name (Cycle 2) (discharge outlet)	Receiving Water / Environment (common name) (EA Consents Database)	Shellfish Water (only populate for storm overflow with a Shellfish Water EDM requirement)	Bathing Water (only populate for storm overflow with a Bathing Water EDM requirement)	Treatment Method (over & above Storm Tank settlement / screening)	Initial EDM Commission Date	Total Duration (hrs) all spills prior to processing through 12-24h count method	Counted spills using 12-24h count method	Long-term average spill count	No. full years EDM data (years)	EDM Operation - % of reporting period EDM operational	EDM Operation - Reporting % - Primary Reason <90%	EDM Operation - Action taken / planned - Status & timeframe	High Spill Frequency - Operational Review - Primary Reason	High Spill Frequency - Action taken / planned - Status & timeframe	High Spill Frequency - Environmental Enhancement - Planning Position (Hydraulic capacity)	Unique ID

COLUMNS_TO_KEEP = [
    "Water Company Name",
    "WFD Waterbody Catchment Name (Cycle 2)\n(discharge outlet)",
    "Site Name\n(EA Consents Database)",
    "Total Duration (hrs) all spills prior to processing through 12-24h count method"
]

SHORTER_COLUMN_NAMES = [
    "Water Company",
    "River Basin",
    "Site",
    "Spill Days"
]

INDEX_COLUMN = 'Unique ID'

dfs = []
for sheet in SHEET_NAMES:
    df = pd.read_excel(fp, sheet_name=sheet, header=1, index_col=INDEX_COLUMN)
    dfs.append(df)

df = pd.concat(dfs)

df = df[COLUMNS_TO_KEEP]
df.columns = SHORTER_COLUMN_NAMES
df['Spill Days'] = df['Spill Days'] / 24 

PRINCETOWN_PSEUDONYMS = [
    "PRINCETOWN SEWAGE TREATMENT WORKS",
    "BLACKBROOK-CSO-PRINCETOWN"
]

# combine the Princetown sites
df['Site'] = df['Site'].apply(lambda x: 'Princetown' if x in PRINCETOWN_PSEUDONYMS else x)

RIVER_DART_PSEUDONYMS = [
    "Dart",
    "Blackbrook River",
    "Lower Little River Dart",
    "Bidwell Brook"
]


# combine the Dart River Basins
df['River Basin'] = df['River Basin'].apply(lambda x: 'Dart' if x in RIVER_DART_PSEUDONYMS else x)


df = df.sort_values('Spill Days', ascending=False)
df.to_csv('data/by-site.csv', index=False)


df.groupby('Water Company').sum()['Spill Days'].sort_values(ascending=False).to_csv('data/by-company.csv')
df.groupby('River Basin').sum()['Spill Hours'].sort_values(ascending=False).to_csv('data/by-basin.csv')