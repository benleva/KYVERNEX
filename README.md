# KYVERNEX Public Site

Sito statico ufficiale di KYVERNEX.

## Anteprima locale

```bash
python -m http.server 8080 --directory site
```

Aprire `http://localhost:8080`.

## Pubblicazione

Il workflow `.github/workflows/kyvernex-site.yml`:

1. valida i file e avvia uno smoke test su ogni pull request;
2. pubblica la cartella `site/` su GitHub Pages dopo il merge in `main`;
3. può essere avviato manualmente da GitHub Actions.

Se il repository resta privato, la disponibilità pubblica di GitHub Pages dipende dal piano e dalle impostazioni dell'account. Per un sito pubblico gratuito, rendere pubblico il repository oppure distribuire la stessa cartella su Cloudflare Pages, Netlify o un hosting tradizionale.

## Dominio personalizzato

Dopo la registrazione del dominio:

1. configurare il dominio nelle impostazioni GitHub Pages;
2. aggiungere un file `site/CNAME` contenente il dominio, per esempio `kyvernex.it`;
3. configurare i record DNS indicati dal provider di hosting.

## Stato del Validator

Il Validator presente nella homepage è una demo deterministica eseguita interamente nel browser. Illustra Context Binding, classificazione degli Atti Cognitivi e rifiuto delle inferenze fabbricate. Non interroga LLM e non sostituisce il Reference Engine o la Compliance Suite.
