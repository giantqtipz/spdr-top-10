"""
Returns:
    Resource file with URLs to download Top 10 Holdings for each sector
"""

url = "https://www.sectorspdrs.com/sectorspdr/IndexHoldings/ExportCsv?symbol="

tickers = {
    "xlc": {
        "index": "IXCTR",
        "title": "Communications"
        },
    "xlf": {
        "index": "IXM",
        "title": "Financial"
        },
    "xlv": {
        "index": "IXV",
        "title": "Healthcare"
        },
    "xle": {
        "index": "IXE",
        "title": "Energy"
        },
    "xlk": {
        "index": "IXT",
        "title": "Technology"
        },
    "xlb": {
        "index": "IXB",
        "title": "Materials"
        },
    "xlp": {
        "index": "IXR",
        "title": "Consumer Staples"
        },  
    "xlre": {
        "index": "IXRE",
        "title": "Real Estate"
        },
    "xli": {
        "index": "IXI",
        "title": "Industrial"
        },
    "xly": {
        "index": "IXY",
        "title": "Consumer Discretionary"
        },
    "xlu": {
        "index": "IXU",
        "title": "Utilities"
        },
}

disclaimer = "As of {} {} was {} of the {} Select Sector Index."