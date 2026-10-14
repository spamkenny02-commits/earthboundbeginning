# Audit technique V18 — 14 octobre 2026

V17 reste la dernière version autonome publiée. V18 n'a encore aucun segment intégré.

Sur ROM USA 1.2 originale : 125/125 références HiROM de début conformes ; 95/95 empreintes FNV64 du texte anglais normalisé conformes ; 95/95 layouts de commandes et retours de ligne cohérents. Le préfixe spécial `01` représente deux retours de ligne dans 42 scripts.

18 références HiROM littérales intérieures touchent 11 scripts : exclus. Il reste **84 scripts** et **211 segments textuels anglais** candidats à traduction. Voir `traduction/v18_audit_scripts.json`.

Non effectués : validation des pointeurs indirects, émulation, intégration V18. L'empreinte normalisée ne remplace pas une comparaison de tous les octets de commande.
