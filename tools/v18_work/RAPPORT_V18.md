# EarthBound Beginnings FR — V18 locale

Base : V17 autonome validée localement (non publiée sur GitHub).
ROM USA 1.2 originale : SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

## Résultats
- **16 nouveaux blocs/dialogues réellement modifiés**, 16 scripts distincts.
- **16 enregistrements IPS V18** ajoutés à chacune des variantes V17.
- Source comparée octet par octet, pointeurs littéraux de début vérifiés, absence de pointeurs littéraux intérieurs, longueurs et encodage vérifiés, aucune collision avec V17.
- Roundtrip IPS autonome et conservation des octets V17 vérifiés pour accents et ASCII.
- Tests unitaires hérités V17 : **45 réussis, 0 échec**.
- Émulation : **non effectuée**. Pointeurs indirects, compression, graphismes : **non validés**.
- GitHub : **aucun commit** (travail local demandé).

## SHA-256 des IPS V18
- `EarthBound_Beginnings_FR_v18_accents.ips` : `57d51063d9f809846312862dfcf0737887c475750de42b0b6a967d2b21c61c7b`
- `EarthBound_Beginnings_FR_v18_ascii.ips` : `fb45610ef36547fffdbc4a2102a6e56ae25459605135983090ef7e6ab2a5778c`

## Notes
La découverte automatisée a identifié 18 candidats simples, dont deux libellés techniques internes laissés inchangés. Les 16 autres sont intégrés. Les scripts multisegments et les dialogues longs nécessitent une stratégie séparée. Aucun essai de gameplay n’a été fait.
