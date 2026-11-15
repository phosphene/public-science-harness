=== [Pipeline 02] Fetching Cambrian Occurrences from Paleobiology Database (PBDB) ===
  [HTTP GET] https://paleobiodb.org/data1.2/occs/list.json?base_name=Metazoa&interval=Cambrian&show=class%2Cphy%2Ccoords%2Cloc&limit=1000
  [PBDB Response] Retrieved 1000 raw occurrence records.
  [Raw] Saved pbdb_cambrian_metazoa_raw.json (SHA-256: f0071ae3d48818fa...)
  [Curated] Loaded 1000 occurrences into 'cambrian_occurrences'.
  [Guild Summary Breakdown]:
    - MOBILE_APEX_PREDATOR     :  295 distinct taxa |  634 occurrences (mean age ~499.31 Ma)
    - SEDENTARY_FILTER_FEEDER  :   81 distinct taxa |  246 occurrences (mean age ~499.78 Ma)
    - OTHER_UNCLASSIFIED       :   51 distinct taxa |  115 occurrences (mean age ~501.81 Ma)
    - INFAUNAL_BURROWER        :    4 distinct taxa |    5 occurrences (mean age ~498.19 Ma)
=== [Pipeline 02] Complete ===
