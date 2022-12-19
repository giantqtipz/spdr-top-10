"""
Returns:
    Resource file with URLs to download Top 10 Holdings for each sector
"""

url = "https://www.sectorspdr.com/sectorspdr/IDCO.Client.Spdrs.Index/Export/ExportCsv?symbol="

tickers = {
    "xlc": "IXCTR",
    "xlf": "IXM",
    "xlv": "IXV",
    "xle": "IXE",
    "xlk": "IXT",
    "xlb": "IXB",
    "xlp": "IXR",  
    "xlre": "IXRE",
    "xli": "IXI",
    "xly": "IXY",
    "xlu": "IXU",
}