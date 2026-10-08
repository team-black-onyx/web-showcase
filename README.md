# Layercraft

Layercraft is a static research notebook. Experiment pages and homepage cards are generated from Markdown in `experiments/`.

## Build

Requires Python 3. From the repository root:

```sh
python3 build.py
```

The generated GitHub Pages-ready site is written to `dist/`. Configure the optional shared repository link in `site-config.json`; an experiment may override it with a `code_url` front matter value. Add an experiment by creating a Markdown file with the same front matter shape as `experiments/language-model-puppeteer.md`, then rebuild.

For GitHub Pages, publish the `dist/` directory with the repository's chosen Pages workflow.
