# Lega Fantagufi — sito

Sito statico, zero dipendenze, zero build. Un `index.html`, otto file JSON in `data/` e gli stemmi in `assets/`.

## Deploy su GitHub Pages

Serve una repo **pubblica**: il piano gratuito di Pages non pubblica da repo private.

1. Su github.com crea una repo vuota, es. `fantagufi` — senza README, senza .gitignore.
2. Da questa cartella:

   ```
   git init
   git add .
   git commit -m "Sito Lega Fantagufi"
   git branch -M main
   git remote add origin https://github.com/TUO-UTENTE/fantagufi.git
   git push -u origin main
   ```

3. Repo → **Settings → Pages** → Source: *Deploy from a branch* → Branch **main**, cartella **/ (root)** → Save.
4. Dopo un minuto o due è online su `https://TUO-UTENTE.github.io/fantagufi/`

Gli aggiornamenti successivi sono `git add -A`, `git commit -m "..."`, `git push`: il sito si aggiorna da solo in un minuto.

### Il dominio non serve

L'URL `TUO-UTENTE.github.io/fantagufi` è gratuito e ha già HTTPS. Un dominio tuo (es. `fantagufi.it`, 10-15 € l'anno) serve solo se vuoi un indirizzo più corto da dire a voce.

Se lo vuoi: comprane uno, scrivilo in Settings → Pages → Custom domain, poi dal pannello del registrar crea un record `CNAME` che punta a `TUO-UTENTE.github.io`. GitHub genera il certificato HTTPS da sé. Il file `CNAME` nella repo viene creato automaticamente da GitHub, non serve scriverlo a mano.

### File di servizio

- **`.nojekyll`** — file vuoto che dice a GitHub di non passare il sito attraverso Jekyll. Non ci serve e senza questo file cartelle o file che iniziano con `_` verrebbero ignorati.
- **`.gitignore`** — tiene fuori `anteprima.html` (si rigenera in locale) e i residui delle immagini.

## Cosa c'è dentro

Sette tab: **Home** (le 10 squadre con stemma, allenatore, motto e palmarès), Classifica, Calendario, Coppa, Albo d'Oro, Regolamento, Sponsor. Nell'Albo d'Oro un menù a tendina scegli l'annata e mostra podio, classifica finale e premi di quell'anno; Bacheca Eterna e Record stanno in fondo alla pagina.

| File | Contenuto | Stato |
|---|---|---|
| `data/lega.json` | Nome, stagione, stato, benvenuto | ✅ 2026/27 |
| `data/squadre.json` | Le 10 squadre: logo, motto, allenatore, nomi precedenti | ⚠️ allenatori vuoti |
| `data/classifica.json` | Classifiche indicizzate per stagione | ✅ 2025/26 |
| `data/calendario.json` | Giornate e risultati | ⬜ vuoto, dopo l'asta |
| `data/coppa.json` | Tabellone + albo coppa | ⚠️ solo il vincitore |
| `data/albo.json` | Annate (podio + premi), bacheca, record | ⚠️ solo 2025/26 |
| `data/premi.json` | Catalogo dei premi (nome + descrizione) | ✅ completo |
| `data/regolamento.json` | Sezioni di regolamento | ⬜ vuoto, dopo l'asta |
| `data/sponsor.json` | Sponsor della stagione | ⚠️ manca il logo |
| `assets/logo.png` | Stemma della lega | ✅ |
| `assets/squadre/*.jpg` | I 10 stemmi delle squadre | ✅ |

### Cosa resta da riempire

- **`squadre.json` → `allenatore`** — vuoti. Finché lo sono, la home scrive "allenatore da inserire".
- **`squadre.json` → `nomiPrecedenti`** — due squadre del 2025/26 non sono collegate: **Iron First FC** e **JuZar**. Vedi sotto.
- **`coppa.json`** — quarti, semifinali e risultato della finale. Il vincitore (Scarsenal) c'è già.
- **`albo.json`** — le stagioni dal 2017/18 al 2024/25.
- **`calendario.json` e `regolamento.json`** — si compilano dopo l'asta di settembre 2026. Ora mostrano uno stato di attesa.

### Rinomine: come funzionano

Ogni squadra ha un `id` stabile e un elenco `nomiPrecedenti`. Lo storico resta scritto col nome dell'epoca, ma il sito mostra **sempre il nome attuale**, con un `(ex vecchio nome)` accanto.

```json
{
  "id": "tecnotazza",
  "nome": "Tecnotazza",
  "nomiPrecedenti": ["FC ETTANERA"]
}
```

Così `FC ETTANERA` nella classifica 2025/26 appare come `Tecnotazza (ex FC ETTANERA)` in classifica, podio, premi, bacheca e record — senza toccare i dati storici.

Collegamenti attivi:

| Nome storico | Squadra oggi |
|---|---|
| `complimenti per la vittoria` | Complimenti per la Vittoria |
| `ICinesiNonEsistono` | I Cinesi Non Esistono |
| `FC ETTANERA` | Tecnotazza |
| `Il RE AMMINISTRATORE` | Real Lucoli |
| `Iron First FC` | Akatsuki FC |
| `JuZar` | Akatsuki FC |

Un nome storico non collegato non rompe niente: viene semplicemente mostrato così com'è.

### Fusioni

`nomiPrecedenti` accetta più nomi, quindi una fusione si dichiara elencandoli entrambi:

```json
{
  "id": "akatsuki",
  "nome": "Akatsuki FC",
  "nomiPrecedenti": ["Iron First FC", "JuZar"]
}
```

Nella home la scheda mostra `ex Iron First FC + JuZar`. Nella Bacheca Eterna **Akatsuki FC compare due volte**, una per ciascuna squadra da cui deriva: sono le due carriere che confluiscono, tenute separate perché nel 2025/26 erano due squadre distinte con due classifiche distinte. Se preferisci una riga sola con i totali sommati, si può fare — ma i numeri diventerebbero 2 stagioni e ~4985 fantapunti per una squadra al primo anno di vita.

### Squadre ritirate

`"attiva": false` toglie una squadra dalla griglia principale e la sposta nel riquadro **Squadre ritirate**, in grigio, sotto le altre. Resta nell'anagrafica, quindi continua a risolvere i nomi nello storico e a comparire nella bacheca eterna.

È il caso di **Toduto**, ritirata dopo il 2025/26: il suo posto in lega è andato ad **Akatsuki FC**, che è una squadra nuova e non una rinomina — quindi due schede distinte, non un `nomiPrecedenti`.

### Errori nei loghi

Due stemmi riportano un nome diverso da quello ufficiale della squadra. Il campo `notaLogo` lo dichiara e la home lo mostra con un ⚠ nella scheda:

- il logo di **Complimenti per la Vittoria** aggiunge «del Fanta»
- il logo di **Ji Impalatori** scrive «Gli Impalatori»

Fa fede il nome nel campo `nome`. Quando rifate i loghi, togliete `notaLogo` e l'avviso sparisce.

### premi.json e albo.json: come si incastrano

`premi.json` è il **catalogo**: definisce ogni premio una volta sola, con un `id`.

```json
{ "id": "cucchiaio", "emoji": "🥄", "nome": "Cucchiaio di Legno",
  "descrizione": "All'ultimo in classifica. Paga la cena." }
```

`albo.json` dice **chi l'ha vinto in quale anno**, richiamando l'`id`:

```json
"premi": [
  { "id": "cucchiaio", "vincitore": "Sellone Ciompi",
    "dettaglio": "Ultimo con più fantapunti del secondo. Paga comunque." }
]
```

Così la descrizione del premio la scrivi una volta e ogni anno aggiungi solo vincitore e battuta. Per inventare un premio nuovo: aggiungi una voce a `premi.json` con un `id` nuovo, poi usalo nell'annata che vuoi. Un `id` che non esiste nel catalogo viene mostrato comunque, ma senza emoji né descrizione.

### Aggiungere una stagione all'albo

1. Aggiungi la classifica finale in `classifica.json` sotto la chiave della stagione (es. `"2024/25"`). Podio e cucchiaio si calcolano da sola.
2. Aggiungi il blocco in `albo.json` → `titoli` con `stagione`, `coppa`, `nota` e la lista `premi`.
3. Aggiorna `bacheca`: `stagioni` +1 per tutti, `titoli`/`coppe`/`podi`/`cucchiai` per chi ha vinto qualcosa, e **somma** i fantapunti, i gol fatti e i gol subiti di quell'anno ai totali esistenti.

I totali di carriera non si calcolano da soli: sono numeri scritti a mano in `bacheca`, perché il sito non conserva le classifiche complete delle stagioni passate. Un controllo utile: la somma dei GF di tutte le squadre deve essere uguale alla somma dei GS (ora 513 = 513).

## Aggiornare i dati

Modifica i JSON, fai push. Nessuna ricompilazione.

### classifica.json

È un oggetto indicizzato per stagione, così la stessa tabella serve al tab Classifica e all'Albo d'Oro:

```json
{
  "2025/26": [
    {
      "squadra": "ICinesiNonEsistono",
      "allenatore": "",       // opzionale, appare sotto il nome squadra
      "punti": 55,
      "g": 36, "v": 17, "n": 4, "p": 15,
      "gf": 59, "gs": 51,
      "totalePunti": 2555.5,
      "soprannome": "Il Terzo Incomodo",
      "nota": "Riga di sfottò sotto il nome."
    }
  ]
}
```

Il tab Classifica mostra la stagione indicata in `lega.json`. L'Albo d'Oro mostra quella scelta nel menù a tendina.

Ordinamento automatico: punti → differenza reti → fantapunti. Primo (👑) e ultimo (🥄) evidenziati da soli. Miglior e peggior fantapunteggio colorati verde/rosso come nell'app.

**Podio automatico**: se una stagione ha la sua classifica qui, campione, secondo, terzo e cucchiaio dell'Albo d'Oro vengono calcolati da essa e i campi corrispondenti in `albo.json` sono ignorati. Servono solo per le vecchie annate di cui ricordi il vincitore ma non la tabella completa.

### regolamento.json

Ora è vuoto: `sezioni: []` e un messaggio in `vuoto` che il sito mostra come stato d'attesa. Dopo l'asta aggiungi le sezioni, ognuna con `icona`, `titolo`, una lista `regole` e una `nota` opzionale:

```json
{
  "sezioni": [
    { "icona": "⏰", "titolo": "FORMAZIONI E GONG",
      "regole": ["Dopo il gong non si tocca più niente."],
      "nota": "Riga di commento in corsivo, opzionale." }
  ]
}
```

Appena `sezioni` contiene qualcosa, lo stato d'attesa scompare da solo.

### sponsor.json

Alimenta il tab **Sponsor**. Ogni voce dell'array `sponsor`:

```json
{
  "id": "antonelli",
  "nome": "Macelleria Antonelli",
  "stagione": "2026/27",
  "contributo": "Paga il caminetto all'asta",
  "logo": "assets/sponsor/antonelli.jpg",
  "sito": "https://...",
  "nota": "Riga in corsivo, opzionale."
}
```

`logo` e `sito` possono restare vuoti. Senza logo compare un segnaposto 🥩 con scritto "logo in arrivo": quando arriva quello vero, mettilo in `assets/sponsor/` e scrivi il percorso nel campo.

Se l'array `sponsor` è vuoto il tab resta, con uno stato d'attesa che si può personalizzare col campo `vuoto`.

### calendario.json

Ora è un array vuoto `[]` e il tab mostra "calendario non pubblicato", con il testo preso da `lega.json` → `notaCalendario`.

Formato di una giornata, quando la compilerai:

```json
[
  { "giornata": 1, "data": "2026-09-13", "giocata": false,
    "partite": [
      { "casa": "Tecnotazza", "trasferta": "Scarsenal",
        "golCasa": null, "golTrasferta": null,
        "puntiCasa": null, "puntiTrasferta": null,
        "commento": "" }
    ] }
]
```

Punteggi a `null` e `"giocata": false` → il sito mostra "DA GIOCARE". Il campo `commento` è lo sfottò della singola partita. Con almeno una giornata compare il selettore, che si apre sulla prima non giocata.

### coppa.json

Come `classifica.json`, è indicizzato per stagione — sotto la chiave `edizioni`:

```json
{
  "nome": "COPPA FANTAGUFI",
  "edizioni": {
    "2025/26": {
      "formato": "Otto squadre, eliminazione diretta.",
      "vincitore": "Scarsenal",
      "finalista": "???",
      "fasi": [
        { "nome": "FINALE", "partite": [ { "casa": "Scarsenal", "trasferta": "???", "golCasa": null, "golTrasferta": null } ] }
      ]
    }
  },
  "vuoto": "Testo mostrato quando la coppa dell'anno in corso non è ancora iniziata."
}
```

Il tab **Coppa** mostra solo l'edizione della stagione indicata in `lega.json`: se non c'è, compare lo stato d'attesa e niente altro. Le edizioni passate stanno nell'**Albo d'Oro**: scegliendo l'annata, il tabellone appare tra la classifica finale e i premi.

Ogni elemento di `fasi` è un turno con le sue partite (stesso formato del calendario). Le squadre scritte `???` appaiono in grigio. Rimuovi il campo `avviso` quando hai finito di compilare.

### Aggiungere o togliere squadre

Modifica la stagione corrente in `classifica.json`: tabelle, contatori e ticker si adattano. Il calendario invece va rigenerato a mano.

### I loghi

`assets/logo.png` è lo stemma della lega con lo sfondo reso trasparente (420px, 68 KB), `assets/favicon.png` la versione per la scheda del browser.

Gli stemmi delle squadre sono in `assets/squadre/`, un JPEG a 400px per squadra (~50 KB ciascuno). Lo sfondo **non** è trasparente: molti stemmi hanno il fondo nero e ritagliarlo svuotava il disegno, quindi la home li mostra su una tessera scura che ne fa da cornice.

Per sostituirne uno: rimpiazza il file mantenendo il nome, oppure cambia il percorso nel campo `logo` di `squadre.json`.

## Vederlo subito

**`anteprima.html`** — doppio click, si apre nel browser. Ha i dati incorporati dentro, quindi funziona anche offline e senza server. Serve solo a guardare: **non modificarlo**, perché i dati veri stanno nei JSON.

Per rigenerarla dopo aver aggiornato i JSON, dalla cartella del progetto:

```
python rigenera_anteprima.py
```

Lo script segnala anche se uno dei JSON non è valido, quindi vale come controllo rapido dopo una modifica a mano.

`anteprima.html` non va caricata su GitHub Pages: online serve `index.html`.

## Provare il sito vero in locale

Il doppio click su `index.html` **non funziona**: il browser blocca `fetch()` sui file locali. Serve un server:

```
cd fantalega
python -m http.server 8000
```

Poi apri http://localhost:8000

## Note

- Repo pubblica = tutto visibile a chiunque trovi l'URL. Di solito è il punto, ma tienilo presente prima di scrivere sfottò troppo specifici.
- I font arrivano da Google Fonts. Senza rete il sito funziona comunque, con un font di sistema.
- Tutto in un file: `index.html`. Modificalo a mano senza timore, `git revert` esiste.
