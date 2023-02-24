# Derived Features

Derive features from triple list of entropies, sizes, and directions.

Produces these features:
    * DirSignSizes
    * TotalFwd/BwdBytes
    * BurstDepth
    * DirSignBurstBytes
    * ...

Broad categories:
    * per-packet for the first N packets
    * summary statistics over sliding windows
    * entire flow
