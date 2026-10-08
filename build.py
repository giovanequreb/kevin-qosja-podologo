from pathlib import Path
from urllib.parse import quote

OUT = Path(__file__).parent
# Bozza: finché restano segnaposto il sito non deve finire su Google. Mettere False al lancio.
DRAFT = True

TEL = "tel:+393923014253"
TEL_LABEL = "392 301 4253"


def wa(msg="Buongiorno, vorrei prenotare una visita podologica."):
    return "https://wa.me/393923014253?text=" + quote(msg)


WA = wa()
NAV = [("index.html", "Home"), ("servizi.html", "Servizi"), ("chi-sono.html", "Chi sono"), ("contatti.html", "Contatti")]

# title, one line for the home tile, full description for the services page
TREATMENTS = [
    ("Unghia incarnita", "Sollievo dal dolore e correzione dell'unghia, senza chirurgia quando possibile.",
     "Trattamento conservativo dell'onicocriptosi e rieducazione dell'unghia con ortonixia, per risolvere il dolore ed evitare che si ripresenti."),
    ("Calli e duroni", "Rimozione indolore e ricerca della causa, perché non tornino.",
     "Rimozione indolore di ipercheratosi e tilomi e valutazione di appoggio e calzature, che spesso ne sono la causa."),
    ("Verruche plantari", "Diagnosi e trattamento mirato, con controlli fino alla scomparsa.",
     "Riconoscimento della lesione e trattamento podologico con protocolli mirati e controlli periodici."),
    ("Piede diabetico", "Prevenzione e controlli regolari per chi convive con il diabete.",
     "Screening del rischio ulcerativo, cura periodica di pelle e unghie ed educazione alla prevenzione, in collaborazione con il medico curante."),
    ("Plantari su misura", "Ortesi progettate sul tuo piede e sul tuo modo di camminare.",
     "Ortesi plantari realizzate dopo la valutazione dell'appoggio e della postura, per scaricare i punti dolenti e migliorare il cammino."),
    ("Esame baropodometrico", "L'analisi computerizzata di come appoggi il piede, da fermo e in cammino.",
     "Analisi computerizzata delle pressioni plantari in statica e in dinamica: mostra dove il piede lavora troppo e guida la scelta del trattamento."),
    ("Visita podologica", "",
     "Valutazione completa di pelle, unghie, appoggio e cammino, con indicazioni chiare sul percorso di cura."),
    ("Micosi delle unghie", "",
     "Inquadramento dell'onicomicosi, trattamento podologico dell'unghia e monitoraggio della ricrescita."),
]

# anchor, title, tile label, tile caption, short text, long text
AUDIENCE = [
    ("bambini", "Bambini e ragazzi", "0–17", "anni",
     "Piede piatto, cammino in punta, unghie incarnite: si controlla come cresce il piede.",
     "Si osserva come si sviluppano piede e cammino durante la crescita: piede piatto, punte in dentro, verruche e unghie incarnite sono i motivi di visita più frequenti."),
    ("adulti", "Adulti", "18–64", "anni",
     "Dolore, calli, unghie difficili: si cerca la causa e si sceglie il trattamento.",
     "Dolore al tallone o all'avampiede, calli che tornano, unghie che fanno male: la visita serve a capire la causa e a impostare il trattamento giusto."),
    ("anziani", "Over 65", "65+", "anni",
     "Cure delicate per unghie ispessite, calli e dolore, quando chinarsi è difficile.",
     "Trattamenti delicati e regolari per unghie ispessite, calli e pelle fragile, con attenzione a diabete, circolazione ed equilibrio."),
    ("sportivi", "Sportivi", "Sport", "a ogni livello",
     "Appoggio, sovraccarichi, vesciche: per correre e allenarsi senza fastidi.",
     "Valutazione dell'appoggio e del gesto atletico, prevenzione dei sovraccarichi, gestione di vesciche, unghie nere e microtraumi."),
]

DOTS = '<div class="dots" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>'
DOTS_LEFT = DOTS.replace('class="dots"', 'class="dots dots--left"')
LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><ellipse cx="15.5" cy="22" rx="5" ry="6" fill="#17224d"/>'
        '<ellipse cx="14.5" cy="12" rx="6" ry="4.6" fill="#17224d"/><circle cx="8.5" cy="5" r="2" fill="#3d77f5"/>'
        '<circle cx="13.5" cy="3.4" r="1.7" fill="#3d77f5"/><circle cx="18" cy="4" r="1.5" fill="#3d77f5"/>'
        '<circle cx="21.8" cy="5.8" r="1.3" fill="#3d77f5"/><circle cx="24.6" cy="8.6" r="1.1" fill="#3d77f5"/></svg>')
ROBOTS = '  <meta name="robots" content="noindex, nofollow">\n' if DRAFT else ""

HOURS = """<table class="hours">
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


def slug(s):
    return s.lower().replace(" ", "-")


def page(file, title, desc, body):
    links = "\n".join(
        f'            <li><a href="{h}"{" aria-current=\"page\"" if h == file else ""}>{t}</a></li>' for h, t in NAV
    )
    return f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
{ROBOTS}  <meta name="theme-color" content="#17224d">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="it_IT">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preload" href="fonts/geist.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/style.css">
  <script>document.documentElement.classList.add('js')</script>
</head>
<body>
  <a class="skip" href="#contenuto">Vai al contenuto</a>

  <header class="header">
    <div class="wrap header__in">
      <a class="logo" href="index.html">{LOGO}Kevin Qosja</a>
      <button class="burger" aria-label="Apri il menu" aria-expanded="false" aria-controls="nav"><span></span></button>
      <nav class="nav" id="nav" aria-label="Principale">
        <ul>
{links}
        </ul>
        <a class="btn btn--sm" href="{WA}">Prenota</a>
      </nav>
    </div>
  </header>

  <main id="contenuto">
{body}
  </main>

  <footer class="footer">
    <div class="wrap">
      <div class="footer__in">
        <span>© <span data-year>2026</span> Dott. Kevin Qosja · Podologo a Lucca</span>
        <ul>
          <li><a href="{TEL}">{TEL_LABEL}</a></li>
          <li><a href="mailto:[EMAIL]">[EMAIL]</a></li>
          <li>P.IVA [P.IVA]</li>
          <li><a href="privacy.html">Privacy</a></li>
        </ul>
      </div>
      <p class="footer__legal">Iscritto all'Albo dei Podologi di [PROVINCIA ALBO] n. [N. ALBO]. Le informazioni di questo sito hanno scopo informativo e non sostituiscono la visita.</p>
    </div>
  </footer>

  <div class="dock">
    <a class="btn" href="{WA}">WhatsApp</a>
    <a class="btn btn--ghost" href="{TEL}">Chiama</a>
  </div>

  <script src="js/main.js" defer></script>
</body>
</html>
"""


def page_hero(title, lead):
    return f"""    <section class="hero hero--page">
      {DOTS}
      <div class="wrap">
        <h1>{title}</h1>
        <p class="lead">{lead}</p>
      </div>
    </section>"""


def book(title="Prenota una visita"):
    return f"""    <section class="book">
      {DOTS_LEFT}
      <div class="wrap">
        <div data-reveal>
          <h2>{title}</h2>
          <p>Scrivimi su WhatsApp o chiama: fissiamo insieme giorno e ora.</p>
          <a class="book__tel" href="{TEL}">{TEL_LABEL}</a>
          <div class="btn-row">
            <a class="btn" href="{WA}">Scrivi su WhatsApp</a>
            <a class="btn btn--light" href="{TEL}">Chiama ora</a>
          </div>
        </div>
        <div class="book__card" data-reveal>
          <h3>Orari dello studio</h3>
          {HOURS}
          <p class="note" style="margin:1rem 0 0">[INDIRIZZO], [CAP] Lucca (LU) · si riceve su appuntamento</p>
        </div>
      </div>
    </section>"""


def who_cards(long=False):
    out = []
    for anchor, title, big, small, short, full in AUDIENCE:
        tail = "" if long else f'\n            <a class="btn btn--sm" href="servizi.html#{anchor}">Scopri di più</a>'
        ident = f' id="{anchor}"' if long else ""
        out.append(f"""          <article class="who"{ident} data-reveal>
            <div class="who__tile">{DOTS}<span>{big}<small>{small}</small></span></div>
            <h3>{title}</h3>
            <p>{full if long else short}</p>{tail}
          </article>""")
    return "\n".join(out)


tiles = "\n".join(
    f"""        <a class="tile" href="servizi.html#{slug(t)}" data-reveal>
          <h3>{t}</h3>
          <p>{short}</p>
          <span class="btn btn--sm">Scopri</span>
        </a>"""
    for t, short, _ in TREATMENTS if short
)

rows = "\n".join(
    f"""        <li class="row" id="{slug(t)}" data-reveal>
          <h3>{t}</h3>
          <p>{full}</p>
        </li>"""
    for t, _, full in TREATMENTS
)

index = f"""    <section class="hero">
      {DOTS}
      <div class="wrap">
        <h1>Podologo a Lucca</h1>
        <p class="lead">Sono Kevin Qosja. Nel mio studio mi prendo cura dei tuoi piedi con attenzione e metodo: prevenzione, trattamento e riabilitazione, a ogni età.</p>
        <div class="btn-row">
          <a class="btn" href="{WA}">Prenota su WhatsApp</a>
          <a class="btn btn--ghost" href="{TEL}">Chiama {TEL_LABEL}</a>
        </div>
      </div>
    </section>

    <section class="split">
      <div class="panel panel--mist">
        <div class="foot" data-reveal>
          <span class="foot__tag">Appoggio del piede · simulazione</span>
          <canvas data-foot aria-hidden="true"></canvas>
        </div>
      </div>
      <div class="panel panel--navy">
        {DOTS_LEFT}
        <div data-reveal>
          <h2>La cura del piede, per tutta la famiglia</h2>
          <p>Il podologo è il professionista sanitario laureato che previene e tratta i disturbi del piede. Non si occupa solo di unghie e calli: dal modo in cui appoggi il piede dipendono il cammino, la postura e spesso anche ginocchia e schiena.</p>
          <p>In studio seguo bambini, adulti, anziani e sportivi, con un percorso costruito sulla persona e spiegato passo per passo.</p>
          <div class="btn-row"><a class="btn btn--light" href="chi-sono.html">Chi sono</a></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap audience">
        <div class="audience__title">
          {DOTS_LEFT}
          <h2>A chi mi rivolgo</h2>
        </div>
        <div class="audience__cards">
{who_cards()}
        </div>
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="wrap">
        <div class="center" data-reveal>
          <h2>Terapie e trattamenti</h2>
          <p class="lead">I motivi più frequenti per cui si viene in studio. Ogni percorso parte da una visita, per capire la causa prima di trattare.</p>
        </div>
        <div class="tiles">
{tiles}
        </div>
        <div class="center"><div class="btn-row"><a class="btn btn--ghost" href="servizi.html">Tutti i servizi</a></div></div>
      </div>
    </section>

    <section class="section" style="background:var(--mist)">
      <div class="wrap center">
        <h2 data-reveal>Come funziona</h2>
        <ol class="steps">
          <li data-reveal><h3>Mi scrivi o mi chiami</h3><p>Mi racconti il problema e fissiamo giorno e ora della visita.</p></li>
          <li data-reveal><h3>Prima visita</h3><p>Valuto il piede e ti spiego cosa succede e quali sono le opzioni.</p></li>
          <li data-reveal><h3>Trattamento e controlli</h3><p>Iniziamo il percorso; i controlli si programmano solo quando servono.</p></li>
        </ol>
      </div>
    </section>

{book()}"""

servizi = f"""{page_hero("Servizi e trattamenti", "Ogni percorso parte da una visita: prima si capisce la causa, poi si sceglie il trattamento più adatto.")}

    <section class="section">
      <div class="wrap">
        <div class="center" data-reveal><h2>Trattamenti</h2></div>
        <ul class="rows">
{rows}
        </ul>
      </div>
    </section>

    <section class="section" style="background:var(--mist)">
      <div class="wrap">
        <div class="center" data-reveal style="margin-bottom:3rem"><h2>A chi mi rivolgo</h2></div>
        <div class="audience__cards" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">
{who_cards(long=True)}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap two">
        <div data-reveal>
          <h2>Domande frequenti</h2>
          <p class="lead">Quello che di solito ci si chiede prima di venire in studio.</p>
        </div>
        <div class="faq" data-reveal>
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

{book("Non sai quale trattamento ti serve?")}"""

chi = f"""{page_hero("Dott. Kevin Qosja", "Podologo a Lucca. Laureato in Podologia presso [UNIVERSITÀ], iscritto all'Albo dei Podologi di [PROVINCIA ALBO] n. [N. ALBO].")}

    <section class="split">
      <div class="panel panel--navy">
        {DOTS_LEFT}
        <div data-reveal>
          <h2>Il mio approccio</h2>
          <p>[BIO — due o tre frasi su Kevin: da quanto esercita, dove ha lavorato, di cosa si occupa in particolare.]</p>
          <p>Credo in una podologia che spiega. Ogni visita parte dall'ascolto e finisce con indicazioni che puoi seguire a casa, perché la cura del piede continua anche fuori dallo studio.</p>
        </div>
      </div>
      <div class="panel panel--mist" style="align-items:stretch">
        <div data-reveal>
          <h3>Formazione</h3>
          <ul class="list">
            <li>Laurea in Podologia — [UNIVERSITÀ], [ANNO]</li>
            <li>[CORSO / MASTER / SPECIALIZZAZIONE]</li>
            <li>Aggiornamento continuo ECM</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap center">
        <h2 data-reveal>Cosa trovi in studio</h2>
        <ol class="steps steps--plain">
          <li data-reveal><h3>Tempo</h3><p>Appuntamenti senza fretta: il tempo della seduta è tutto per te.</p></li>
          <li data-reveal><h3>Chiarezza</h3><p>Ti spiego cosa vedo, cosa propongo e quanto costa prima di iniziare.</p></li>
          <li data-reveal><h3>Igiene</h3><p>Strumenti sterilizzati in autoclave e materiale monouso.</p></li>
          <li data-reveal><h3>Collaborazione</h3><p>Quando serve lavoro con il tuo medico, l'ortopedico o il diabetologo.</p></li>
        </ol>
      </div>
    </section>

{book("Vuoi fissare una prima visita?")}"""

contatti = f"""{page_hero("Contatti", "Il modo più veloce per prenotare è WhatsApp: scrivimi quando vuoi, ti rispondo appena esco dalla seduta.")}

    <section class="section">
      <div class="wrap">
        <div class="info">
          <div data-reveal>
            <h3>Dove</h3>
            <p>[INDIRIZZO]<br>[CAP] Lucca (LU)</p>
            <div class="btn-row"><a class="btn btn--sm" href="https://www.google.com/maps/search/?api=1&amp;query=[INDIRIZZO+PER+MAPS]" target="_blank" rel="noopener">Apri in Google Maps</a></div>
          </div>
          <div data-reveal>
            <h3>Telefono e WhatsApp</h3>
            <p><a href="{TEL}">{TEL_LABEL}</a></p>
            <div class="btn-row"><a class="btn btn--sm" href="{WA}">Scrivi su WhatsApp</a></div>
          </div>
          <div data-reveal>
            <h3>Email</h3>
            <p><a href="mailto:[EMAIL]">[EMAIL]</a></p>
          </div>
        </div>
        <p class="muted" style="margin-top:2rem" data-reveal>[COME ARRIVARE — parcheggio, mezzi pubblici, piano, accesso senza barriere.]</p>
      </div>
    </section>

{book()}"""

privacy = f"""{page_hero("Informativa privacy", "[BOZZA DA FAR VERIFICARE — questo testo è un punto di partenza e non sostituisce la consulenza di un professionista.]")}

    <section class="section">
      <div class="wrap prose">
        <h2>Titolare del trattamento</h2>
        <p>Dott. Kevin Qosja, [INDIRIZZO], [CAP] Lucca (LU) — P.IVA [P.IVA] — [EMAIL].</p>
        <h2>Dati raccolti dal sito</h2>
        <p>Questo sito non usa cookie di profilazione, strumenti di tracciamento né moduli di contatto. Non raccoglie dati personali dei visitatori.</p>
        <h2>Contatti via telefono, WhatsApp ed email</h2>
        <p>Se ci contatti, i dati che comunichi (nome, numero, contenuto del messaggio) sono usati solo per rispondere e gestire l'appuntamento. WhatsApp è un servizio di terze parti, soggetto alla propria informativa.</p>
        <h2>I tuoi diritti</h2>
        <p>Puoi chiedere in ogni momento accesso, rettifica o cancellazione dei tuoi dati scrivendo a [EMAIL], e proporre reclamo al Garante per la protezione dei dati personali.</p>
      </div>
    </section>"""

PAGES = {
    "index.html": ("Kevin Qosja — Podologo a Lucca", "Studio di podologia a Lucca: unghia incarnita, calli, verruche, piede diabetico, plantari su misura. Per bambini, adulti, anziani e sportivi.", index),
    "servizi.html": ("Servizi — Kevin Qosja, Podologo a Lucca", "Trattamenti podologici a Lucca: unghia incarnita, calli, verruche, piede diabetico, plantari su misura, esame baropodometrico.", servizi),
    "chi-sono.html": ("Chi sono — Kevin Qosja, Podologo a Lucca", "Dott. Kevin Qosja, podologo a Lucca: formazione, approccio e metodo di lavoro.", chi),
    "contatti.html": ("Contatti e orari — Kevin Qosja, Podologo a Lucca", "Indirizzo, orari e contatti dello studio di podologia di Kevin Qosja a Lucca. Prenota su WhatsApp o per telefono.", contatti),
    "privacy.html": ("Privacy — Kevin Qosja, Podologo", "Informativa privacy del sito.", privacy),
}

for f, (t, d, b) in PAGES.items():
    (OUT / f).write_text(page(f, t, d, b), encoding="utf-8")
    print("ok", f)
