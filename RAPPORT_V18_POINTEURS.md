# Audit des pointeurs V18 — 14 octobre 2026

95 scripts présélectionnés ; 125 références HiROM littérales déclarées contrôlées sur la ROM originale USA 1.2, SHA-256 e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c : **125 conformes, 0 échec**.

Reproduction : `python traduction/verifier_pointeurs_v18.py "EarthBound Beginnings (USA) 1.2.sfc"`.

Ce test ne vérifie pas encore les frontières exactes des scripts, les pointeurs indirects/intérieurs, les commandes ou les traductions. Aucun segment V18 intégré ; V17 reste la version autonome publiée.
