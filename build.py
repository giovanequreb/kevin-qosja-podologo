from pathlib import Path
from urllib.parse import quote

OUT = Path(__file__).parent
# Bozza: finché restano segnaposto il sito non deve finire su Google. Mettere False al lancio.
DRAFT = True
TEL = "tel:+393923014253"


def wa(msg="Buongiorno, vorrei prenotare una visita podologica."):
    return "https://wa.me/393923014253?text=" + quote(msg)


WA = wa()
NAV = [("index.html", "Home"), ("servizi.html", "Servizi"), ("chi-sono.html", "Chi sono"), ("contatti.html", "Contatti")]

SERVICES = [
    ("Visita podologica", "Valutazione completa del piede, della pelle e delle unghie, con indicazioni chiare sul percorso di cura."),
    ("Unghia incarnita", "Trattamento conservativo dell'onicocriptosi e rieducazione ungueale con ortonixia, senza ricorrere subito alla chirurgia."),
    ("Calli e duroni", "Rimozione indolore di ipercheratosi e tilomi e analisi delle cause che li fanno tornare."),
    ("Verruche plantari", "Diagnosi e trattamento delle verruche del piede con protocolli mirati e controlli periodici."),
    ("Piede diabetico", "Prevenzione, screening del rischio ulcerativo e cura periodica per chi convive con il diabete."),
    ("Plantari su misura", "Ortesi plantari progettate sul tuo piede dopo la valutazione posturale e dell'appoggio."),
    ("Esame baropodometrico", "Analisi computerizzata delle pressioni plantari, da fermo e durante il passo."),
    ("Micosi delle unghie", "Inquadramento dell'onicomicosi, trattamento podologico e monitoraggio della ricrescita."),
    ("Podologia sportiva", "Valutazione del gesto atletico, prevenzione dei sovraccarichi e gestione di vesciche e microtraumi."),
    ("Podologia pediatrica", "Controllo dello sviluppo del piede e del cammino nei bambini, dal piede piatto all'unghia incarnita."),
]

CATS = {
    "Visita podologica": "prevenzione",
    "Unghia incarnita": "unghie",
    "Calli e duroni": "pelle",
    "Verruche plantari": "pelle",
    "Piede diabetico": "prevenzione pelle unghie",
    "Plantari su misura": "appoggio",
    "Esame baropodometrico": "appoggio",
    "Micosi delle unghie": "unghie",
    "Podologia sportiva": "appoggio prevenzione",
    "Podologia pediatrica": "appoggio prevenzione",
}

# chip label, panel id, pressure-map zone, related services
ZONES = [
    ("Unghie", "unghie", "dita", ["Unghia incarnita", "Micosi delle unghie"]),
    ("Dita", "dita", "dita", ["Calli e duroni", "Visita podologica"]),
    ("Avampiede", "avampiede", "avampiede", ["Calli e duroni", "Verruche plantari", "Plantari su misura"]),
    ("Arco plantare", "arco", "arco", ["Esame baropodometrico", "Plantari su misura"]),
    ("Tallone", "tallone", "tallone", ["Plantari su misura", "Verruche plantari", "Podologia sportiva"]),
]


def slug(s):
    return s.lower().replace(" ", "-")


def foot(tag="Pressione plantare"):
    return f"""<div class="foot dark">
          <span class="foot__tag">{tag}</span>
          <canvas data-foot aria-hidden="true"></canvas>
          <span class="foot__legend">min<i></i>max</span>
        </div>"""


ROBOTS = '  <meta name="robots" content="noindex, nofollow">\n' if DRAFT else ""


def page(file, title, desc, body):
    links = "\n".join(
        f'          <li><a href="{h}"{" aria-current=\"page\"" if h == file else ""}>{t}</a></li>' for h, t in NAV
    )
    return f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
{ROBOTS}  <meta name="theme-color" content="#0c5f75">
  <link rel="preload" href="fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/geist.woff2" as="font" type="font/woff2" crossorigin>
  <meta property="og:type" content="website">
  <meta property="og:locale" content="it_IT">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="css/style.css">
  <script>document.documentElement.classList.add('js')</script>
</head>
<body>
  <a class="skip" href="#contenuto">Vai al contenuto</a>
  <div class="progress" aria-hidden="true"></div>

  <header class="header">
    <div class="wrap">
      <div class="header__in">
        <a class="logo" href="index.html">Kevin Qosja<span>.</span></a>
        <button class="burger" aria-label="Apri il menu" aria-expanded="false" aria-controls="nav"><span></span></button>
        <nav class="nav" id="nav" aria-label="Principale">
          <ul>
{links}
          </ul>
          <a class="btn btn--sm" href="{WA}">Prenota</a>
        </nav>
      </div>
    </div>
  </header>

  <main id="contenuto">
{body}
  </main>

  <footer class="footer dark">
    <div class="wrap">
      <div class="footer__grid">
        <div>
          <p class="logo">Kevin Qosja<span>.</span></p>
          <p>Studio di podologia a Lucca.<br>Si riceve su appuntamento.</p>
        </div>
        <div>
          <h3>Studio</h3>
          <ul>
            <li>[INDIRIZZO]</li>
            <li>[CAP] Lucca (LU)</li>
            <li><a href="{TEL}">392 301 4253</a></li>
            <li><a href="mailto:[EMAIL]">[EMAIL]</a></li>
          </ul>
        </div>
        <div>
          <h3>Sito</h3>
          <ul>
            <li><a href="servizi.html">Servizi</a></li>
            <li><a href="chi-sono.html">Chi sono</a></li>
            <li><a href="contatti.html">Contatti</a></li>
            <li><a href="privacy.html">Privacy</a></li>
          </ul>
        </div>
      </div>
      <div class="footer__legal">
        <span>© <span data-year>2026</span> Dott. Kevin Qosja · P.IVA [P.IVA] · Iscritto all'Albo dei Podologi di [PROVINCIA ALBO] n. [N. ALBO]</span>
        <span>Le informazioni di questo sito hanno scopo informativo e non sostituiscono la visita.</span>
      </div>
    </div>
    <p class="footer__big" aria-hidden="true">podologo.</p>
  </footer>

  <div class="dock">
    <a class="btn" href="{WA}">WhatsApp</a>
    <a class="btn btn--ghost" href="{TEL}">Chiama</a>
  </div>

  <script src="js/main.js" defer></script>
</body>
</html>
"""


def cta(title="Hai un dolore che non passa? Parliamone."):
    return f"""    <section class="wrap">
      <div class="cta" data-reveal>
        <h2>{title}</h2>
        <div class="btn-row">
          <a class="btn" href="{WA}">Scrivi su WhatsApp</a>
          <a class="btn btn--ghost" href="{TEL}">Chiama lo studio</a>
        </div>
      </div>
    </section>"""


def cards(items, linked=False):
    out = []
    for i, (t, d) in enumerate(items):
        inner = f"""<span class="card__n">{i + 1:02d}</span>
            <h3>{t}</h3>
            <p>{d}</p>"""
        if linked:
            out.append(f"""          <a class="card" href="servizi.html#{slug(t)}" data-reveal style="--i:{i % 3}">
            {inner}
          </a>""")
        else:
            cat = f' data-cat="{CATS[t]}"' if t in CATS else ""
            out.append(f"""          <li class="card" id="{slug(t)}"{cat} data-reveal style="--i:{i % 3}">
            {inner}
          </li>""")
    return "\n".join(out)


def page_hero(eyebrow, title, lead, extra=""):
    return f"""    <section class="hero hero--page">
      <div class="wrap">
        <p class="eyebrow">{eyebrow}</p>
        <h1><span class="line"><span>{title}</span></span></h1>
        <p class="lead" data-reveal>{lead}</p>{extra}
      </div>
    </section>"""


HOURS = """        <table class="hours" data-reveal style="--i:1">
          <tbody>
            <tr><th scope="row">Lunedì</th><td>[ORARIO]</td></tr>
            <tr><th scope="row">Martedì</th><td>[ORARIO]</td></tr>
            <tr><th scope="row">Mercoledì</th><td>[ORARIO]</td></tr>
            <tr><th scope="row">Giovedì</th><td>[ORARIO]</td></tr>
            <tr><th scope="row">Venerdì</th><td>[ORARIO]</td></tr>
            <tr><th scope="row">Sabato</th><td>[ORARIO]</td></tr>
            <tr><th scope="row">Domenica</th><td>Chiuso</td></tr>
          </tbody>
        </table>"""

SIGNS = """    <section class="section band">
      <div class="wrap">
        <div class="head" data-reveal>
          <h2>Quando conviene <em>farsi vedere</em></h2>
          <p class="lead" style="max-width:26em;margin:0">Segnali comuni che vale la pena far valutare, senza aspettare che peggiorino.</p>
        </div>
        <ul class="checks" data-reveal style="--i:1">
          <li>Dolore al tallone o sotto la pianta quando cammini</li>
          <li>Un'unghia che si incarna, si ispessisce o cambia colore</li>
          <li>Calli e duroni che tornano sempre nello stesso punto</li>
          <li>Una lesione sulla pianta che non passa da settimane</li>
          <li>Diabete: il controllo periodico del piede è parte della cura</li>
          <li>Scarpe che si consumano in modo irregolare</li>
          <li>Fastidi che compaiono correndo o dopo lo sport</li>
          <li>Dubbi su come cammina o appoggia il piede tuo figlio</li>
        </ul>
      </div>
    </section>

"""

AUDIENCE = f"""    <section class="section">
      <div class="wrap">
        <div class="head" data-reveal>
          <h2>Per chi è <em>lo studio</em></h2>
          <a class="btn btn--ghost" href="chi-sono.html">Come lavoro</a>
        </div>
        <ul class="grid rail">
{cards([
    ("Chi fa sport", "Corsa, calcio, padel, trekking: valutazione dell'appoggio e gestione dei sovraccarichi."),
    ("Chi ha il diabete", "Controlli programmati, prevenzione delle lesioni e cura regolare di pelle e unghie."),
    ("Over 65", "Trattamenti delicati per unghie difficili, calli e dolore, anche quando chinarsi è complicato."),
    ("Bambini e ragazzi", "Piede piatto, cammino in punta, unghie incarnite: prima si guarda, meglio è."),
])}
        </ul>
      </div>
    </section>

"""

STUDIO = """    <section class="section band">
      <div class="wrap">
        <div class="head" data-reveal>
          <h2>Lo <em>studio</em></h2>
          <p class="lead" style="max-width:26em;margin:0">[DESCRIZIONE STUDIO — una frase su ambiente, attrezzatura e come ci si arriva.]</p>
        </div>
        <div class="gallery" data-reveal style="--i:1">
          <div class="portrait"><span>Foto 1 · sala trattamenti</span></div>
          <div class="portrait"><span>Foto 2 · ingresso</span></div>
          <div class="portrait"><span>Foto 3 · strumenti</span></div>
          <div class="portrait"><span>Foto 4 · pedana baropodometrica</span></div>
        </div>
        <ul class="pills" data-reveal style="--i:2">
          <li>Autoclave e materiale monouso</li>
          <li>Pagamenti tracciabili</li>
          <li>[PARCHEGGIO]</li>
          <li>[ACCESSO SENZA BARRIERE]</li>
        </ul>
      </div>
    </section>

"""

WHERE = f"""    <section class="section">
      <div class="wrap split">
        <div data-reveal>
          <p class="eyebrow">Dove e quando</p>
          <h2>Vieni a <em>trovarmi</em></h2>
          <p class="lead">[INDIRIZZO]<br>[CAP] Lucca (LU)</p>
          <div class="btn-row">
            <a class="btn" href="{WA}">Prenota su WhatsApp</a>
            <a class="btn btn--ghost" href="https://www.google.com/maps/search/?api=1&amp;query=[INDIRIZZO+PER+MAPS]" target="_blank" rel="noopener">Apri in Google Maps</a>
          </div>
        </div>
{HOURS}
      </div>
    </section>

"""

FIRST = """    <section class="section band" style="margin-top:clamp(3.5rem,7vw,6rem)">
      <div class="wrap">
        <div class="head" data-reveal><h2>Come si svolge <em>la prima visita</em></h2></div>
        <ol class="steps">
          <li data-reveal><h3>Ascolto</h3><p>Mi racconti il disturbo, da quanto dura, che scarpe usi, se hai altre patologie o terapie.</p></li>
          <li data-reveal style="--i:1"><h3>Esame del piede</h3><p>Osservo pelle, unghie, appoggio e cammino. Se serve, aggiungiamo l'esame baropodometrico.</p></li>
          <li data-reveal style="--i:2"><h3>Piano di cura</h3><p>Ti spiego cosa ho visto, cosa propongo, tempi e costi. Decidi tu se e quando iniziare.</p></li>
          <li data-reveal style="--i:3"><h3>A casa</h3><p>Esci con indicazioni pratiche su igiene, calzature e prodotti da usare tra una seduta e l'altra.</p></li>
        </ol>
      </div>
    </section>

"""

marquee_items = "".join(f"<span>{t}</span>" for t, _ in SERVICES)

chips = "\n".join(
    f'            <button class="chip" type="button" aria-pressed="false" data-zone="{pid}" data-blob="{blob}">{label}</button>'
    for label, pid, blob, _ in ZONES
)
panels = "\n".join(
    f"""            <div data-panel="{pid}" hidden>
              <h3>{label} — può esserti utile</h3>
              <ul>
{chr(10).join(f'                <li><a href="servizi.html#{slug(s)}">{s}</a></li>' for s in svc)}
              </ul>
              <div class="btn-row"><a class="btn btn--sm" href="{wa(f'Buongiorno, ho un fastidio in questa zona del piede: {label.lower()}. Vorrei prenotare una visita podologica.')}">Scrivimi di questo</a></div>
            </div>"""
    for label, pid, _, svc in ZONES
)

index = f"""    <section class="hero">
      <div class="wrap hero__grid">
        <div>
          <p class="eyebrow">Podologo a Lucca</p>
          <h1>
            <span class="line"><span>Piedi sani,</span></span>
            <span class="line" style="--i:1"><span>passo</span></span>
            <span class="line" style="--i:2"><span class="accent">deciso.</span></span>
          </h1>
          <p class="lead" data-reveal style="--i:4">Sono Kevin Qosja, podologo. Mi occupo di prevenzione, cura e riabilitazione del piede: dall'unghia incarnita ai plantari su misura.</p>
          <div class="btn-row" data-reveal style="--i:5">
            <a class="btn" href="{WA}">Prenota su WhatsApp</a>
            <a class="btn btn--ghost" href="{TEL}">Chiama 392 301 4253</a>
          </div>
        </div>
        {foot("Appoggio · simulazione")}
      </div>
    </section>

    <section class="wrap" aria-label="In breve">
      <ul class="facts">
        <li data-reveal><strong>Solo su appuntamento</strong><span>Nessuna attesa in sala, tempo dedicato a te.</span></li>
        <li data-reveal style="--i:1"><strong>Strumenti sterilizzati</strong><span>Sterilizzazione in autoclave a ogni seduta.</span></li>
        <li data-reveal style="--i:2"><strong>Prestazione sanitaria</strong><span>Fattura detraibile nella dichiarazione dei redditi.</span></li>
      </ul>
    </section>

    <div class="marquee" aria-hidden="true">
      <div class="marquee__track">{marquee_items}{marquee_items}</div>
    </div>

    <section class="section">
      <div class="wrap">
        <div class="head" data-reveal>
          <h2>Di cosa <em>mi occupo</em></h2>
          <a class="btn btn--ghost" href="servizi.html">Tutti i servizi</a>
        </div>
        <div class="bento">
{cards(SERVICES[:4], linked=True)}
          <a class="card card--accent" href="servizi.html" data-reveal style="--i:2">
            <span class="card__n">+{len(SERVICES) - 4}</span>
            <h3>Vedi tutti i trattamenti ↗</h3>
          </a>
        </div>
      </div>
    </section>

{SIGNS}{AUDIENCE}    <section class="section dark" data-finder>
      <div class="wrap finder">
        <div data-reveal>
          {foot("Tocca una zona")}
        </div>
        <div data-reveal style="--i:1">
          <p class="eyebrow">Orientati</p>
          <h2>Dove senti <em>fastidio?</em></h2>
          <p class="lead">Tocca l'impronta o scegli la zona: ti indico i trattamenti che più spesso c'entrano.</p>
          <div class="chips" role="group" aria-label="Zona del piede">
{chips}
          </div>
          <div class="finder__out" aria-live="polite">
            <div data-panel="intro">
              <h3>Come funziona</h3>
              <p class="muted">Tocca una zona qui sopra per vedere i servizi collegati e scrivermi con il messaggio già pronto.</p>
            </div>
{panels}
          </div>
          <p class="note" style="margin-top:1rem">Indicazione orientativa: non è una diagnosi, la valutazione si fa in visita.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="head" data-reveal><h2>Come <em>funziona</em></h2></div>
        <ol class="steps">
          <li data-reveal><h3>Mi scrivi o mi chiami</h3><p>Mi racconti il problema e fissiamo insieme giorno e ora della visita.</p></li>
          <li data-reveal style="--i:1"><h3>Prima visita</h3><p>Valuto il piede, ti spiego cosa succede e quali sono le opzioni di trattamento.</p></li>
          <li data-reveal style="--i:2"><h3>Trattamento e controlli</h3><p>Iniziamo il percorso e programmiamo i controlli solo quando servono davvero.</p></li>
        </ol>
      </div>
    </section>

{STUDIO}    <section class="section">
      <div class="wrap split">
        <div data-reveal>
          <p class="eyebrow">Chi sono</p>
          <h2>Un professionista sanitario, <em>non un estetista.</em></h2>
        </div>
        <div data-reveal style="--i:1">
          <p class="lead">Il podologo è il professionista sanitario laureato che tratta le patologie del piede. In studio trovi ascolto, spiegazioni chiare e un percorso costruito sul tuo caso.</p>
          <div class="btn-row"><a class="btn btn--ghost" href="chi-sono.html">Scopri di più</a></div>
        </div>
      </div>
    </section>

{WHERE}{cta()}"""

servizi = f"""{page_hero("Servizi", "Trattamenti podologici", "Ogni percorso parte da una visita: prima capiamo la causa, poi scegliamo il trattamento più adatto.")}

    <section class="wrap">
      <div class="chips" data-filter role="group" aria-label="Filtra i trattamenti" style="margin-top:0">
        <button class="chip" type="button" aria-pressed="true" data-show="tutti">Tutti</button>
        <button class="chip" type="button" aria-pressed="false" data-show="unghie">Unghie</button>
        <button class="chip" type="button" aria-pressed="false" data-show="pelle">Pelle</button>
        <button class="chip" type="button" aria-pressed="false" data-show="appoggio">Appoggio e postura</button>
        <button class="chip" type="button" aria-pressed="false" data-show="prevenzione">Prevenzione</button>
      </div>
      <ul class="grid">
{cards(SERVICES)}
      </ul>
    </section>

{FIRST}    <section class="section">
      <div class="wrap split">
        <div class="sticky" data-reveal>
          <p class="eyebrow">Domande frequenti</p>
          <h2>Prima di <em>venire in studio</em></h2>
        </div>
        <div class="faq" data-reveal style="--i:1">
          <details name="faq">
            <summary>Serve l'impegnativa del medico?</summary>
            <p>No. Puoi prenotare direttamente una visita podologica senza prescrizione.</p>
          </details>
          <details name="faq">
            <summary>Il trattamento fa male?</summary>
            <p>La maggior parte dei trattamenti è indolore o provoca un fastidio minimo. Se serve, ne parliamo prima di iniziare.</p>
          </details>
          <details name="faq">
            <summary>Quanto dura una seduta?</summary>
            <p>[DURATA] minuti circa, a seconda del trattamento. La prima visita può richiedere un po' più di tempo.</p>
          </details>
          <details name="faq">
            <summary>La spesa è detraibile?</summary>
            <p>Sì. Le prestazioni del podologo sono prestazioni sanitarie: la fattura è detraibile se il pagamento è tracciabile.</p>
          </details>
          <details name="faq">
            <summary>Cosa devo portare?</summary>
            <p>Eventuali esami o referti recenti, l'elenco dei farmaci che assumi e, se hai dolore camminando, le scarpe che usi più spesso.</p>
          </details>
        </div>
      </div>
    </section>

{cta("Non sai quale trattamento ti serve? Scrivimi.")}"""

chi = f"""{page_hero("Chi sono", "Dott. Kevin Qosja", "Podologo, laureato in Podologia presso [UNIVERSITÀ]. Iscritto all'Albo dei Podologi di [PROVINCIA ALBO] n. [N. ALBO].")}

    <section class="wrap split">
      <div class="portrait sticky" data-reveal><span>Foto di Kevin · verticale 4:5</span></div>
      <div data-reveal style="--i:1">
        <h2>Il mio <em>approccio</em></h2>
        <p class="muted">[BIO — due o tre frasi su Kevin: da quanto esercita, dove ha lavorato, di cosa si occupa in particolare.]</p>
        <p class="muted">Credo in una podologia che spiega. Ogni visita parte dall'ascolto e finisce con indicazioni che puoi seguire a casa, perché la cura del piede continua anche fuori dallo studio.</p>
        <ul class="list">
          <li>Laurea in Podologia — [UNIVERSITÀ], [ANNO]</li>
          <li>[CORSO / MASTER / SPECIALIZZAZIONE]</li>
          <li>Aggiornamento continuo ECM</li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="head" data-reveal><h2>Cosa trovi <em>in studio</em></h2></div>
        <ul class="grid rail">
{cards([
    ("Tempo", "Appuntamenti senza fretta: il tempo della seduta è tutto per te."),
    ("Chiarezza", "Ti spiego cosa vedo, cosa propongo e quanto costa prima di iniziare."),
    ("Igiene", "Strumentario sterilizzato in autoclave e materiale monouso."),
    ("Collaborazione", "Quando serve lavoro insieme al tuo medico, all'ortopedico o al diabetologo."),
])}
        </ul>
      </div>
    </section>

{cta("Vuoi fissare una prima visita?")}"""

contatti = f"""{page_hero("Contatti", "Prenota la tua visita", "Il modo più veloce è WhatsApp: scrivimi quando vuoi, ti rispondo appena esco dalla seduta.", f'''
        <div class="btn-row" data-reveal style="--i:1">
          <a class="btn" href="{WA}">Scrivi su WhatsApp</a>
          <a class="btn btn--ghost" href="{TEL}">Chiama 392 301 4253</a>
        </div>''')}

    <section class="wrap">
      <div class="info">
        <div class="card" data-reveal>
          <h3>Dove</h3>
          <p>[INDIRIZZO]<br>[CAP] Lucca (LU)</p>
          <div class="btn-row"><a class="btn btn--ghost btn--sm" href="https://www.google.com/maps/search/?api=1&amp;query=[INDIRIZZO+PER+MAPS]" target="_blank" rel="noopener">Apri in Google Maps</a></div>
        </div>
        <div class="card" data-reveal style="--i:1">
          <h3>Telefono</h3>
          <p><a href="{TEL}">392 301 4253</a></p>
        </div>
        <div class="card" data-reveal style="--i:2">
          <h3>Email</h3>
          <p><a href="mailto:[EMAIL]">[EMAIL]</a></p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap split">
        <div class="sticky" data-reveal>
          <p class="eyebrow">Orari</p>
          <h2>Si riceve <em>su appuntamento</em></h2>
          <p class="muted">[COME ARRIVARE — parcheggio, mezzi pubblici, piano, accesso senza barriere.]</p>
        </div>
{HOURS}
      </div>
    </section>"""

privacy = f"""{page_hero("Privacy", "Informativa privacy", "[BOZZA DA FAR VERIFICARE — questo testo è un punto di partenza e non sostituisce la consulenza di un professionista.]")}

    <section class="wrap prose">
      <h2>Titolare del trattamento</h2>
      <p>Dott. Kevin Qosja, [INDIRIZZO], [CAP] Lucca (LU) — P.IVA [P.IVA] — [EMAIL].</p>
      <h2>Dati raccolti dal sito</h2>
      <p>Questo sito non usa cookie di profilazione, strumenti di tracciamento né moduli di contatto. Non raccoglie dati personali dei visitatori.</p>
      <h2>Contatti via telefono, WhatsApp ed email</h2>
      <p>Se ci contatti, i dati che comunichi (nome, numero, contenuto del messaggio) sono usati solo per rispondere e gestire l'appuntamento. WhatsApp è un servizio di terze parti, soggetto alla propria informativa.</p>
      <h2>I tuoi diritti</h2>
      <p>Puoi chiedere in ogni momento accesso, rettifica o cancellazione dei tuoi dati scrivendo a [EMAIL], e proporre reclamo al Garante per la protezione dei dati personali.</p>
    </section>"""

PAGES = {
    "index.html": ("Kevin Qosja — Podologo a Lucca", "Studio di podologia a Lucca: unghia incarnita, calli, verruche, piede diabetico, plantari su misura. Prenota su WhatsApp o per telefono.", index),
    "servizi.html": ("Servizi — Kevin Qosja, Podologo a Lucca", "Trattamenti podologici a Lucca: visita, unghia incarnita, calli, verruche, piede diabetico, plantari, esame baropodometrico.", servizi),
    "chi-sono.html": ("Chi sono — Kevin Qosja, Podologo a Lucca", "Dott. Kevin Qosja, podologo a Lucca: formazione, approccio e metodo di lavoro.", chi),
    "contatti.html": ("Contatti e orari — Kevin Qosja, Podologo a Lucca", "Indirizzo, orari e contatti dello studio di podologia di Kevin Qosja a Lucca. Prenota su WhatsApp o per telefono.", contatti),
    "privacy.html": ("Privacy — Kevin Qosja, Podologo", "Informativa privacy del sito.", privacy),
}

for f, (t, d, b) in PAGES.items():
    (OUT / f).write_text(page(f, t, d, b), encoding="utf-8")
    print("ok", f)
