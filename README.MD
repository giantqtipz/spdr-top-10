# SPDR Top 10 Consolidator

Python GUI application allowing users to consolidate SPDRs Top 10 Holdings
Using holdings from Sector SPDR's website, and holdings displayed in print publications

Consolidated holdings file is used to update FINRA required disclaimers in Sector SPDR's
Ticker Targeting ads.

### Workflow

1 - Download holdings for each sector from Sector SPDR's website
2 - Upload holdings schedule displayed in print publications
3 - Consolidate #1 and #2 to create an output to update Ticker Targeting ad disclaimers

### Packages
pandas
xlrd
pysimplegui