# mice-base

Repository for basic functionalities and data structures shared across the MICE project codebase.

## Features

```mermaid
flowchart BT;
    Entropies-->Sizes;
    DirSignSizes-->Sizes;
    DirSignSizes-->Directions;
    TotalFwd/BwdBytes-->Sizes;
    TotalFwd/BwdBytes-->Directions;
    DirSignBurstBytes-->BurstDepth;
    DirSignBurstBytes-->Sizes;
    BurstDepth-->Directions;
    classDef base fill:#3cc;
    classDef derived fill:#de3;
    class Entropies,Sizes,Directions base;
    class DirSignSizes,TotalFwd/BwdBytes,BurstDepth,DirSignBurstBytes derived;
```

## Build

```bash
python setup.py sdist
```

## Install

To install in an editable, debug mode run:

```bash
pip install -e .
```
