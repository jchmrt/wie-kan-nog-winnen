# Wie-kan-nog-winnen

Soms staat je favoriete club er niet zo goed voor in de Eredivisie en
lijkt het alsof alles verloren is, op dat soort momenten is het
belangrijk je te herinneren wat nog kan gebeuren. Daarom verteld
wie-kan-nog-winnnen hoe hoog elke club dit seizoen nog kan eindigen
(mocht alles perfect in hun voordeel gaan)

# Hoe?

De python files, geleid door main.py, halen de data van de Eredivisie
op, parsen het en doen vervolgens een guided search naar de beste
toekomst (en dus beste plaats) voor elk team. Dit schrijft het dan
naar een json bestand. De bestanden in site geven dit weer en parsen
het weer in de website.

Om de hoogste plaatsen naar json te schrijven moet je dus het volgende
uitvoeren (je hebt het urllib package nodig, te installeren met pip):

```
python3 main.py
```

# Waar?

Je kan de website bewonderen op
[wiekannogwinnen.github.io](https://wiekannogwinnen.github.io).
