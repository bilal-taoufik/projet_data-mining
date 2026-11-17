"""Scrape le texte de la page publique OpenPrices après rendu JavaScript."""
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

from .config import DATA, AGENT
from .commun import fetch, save

BASE = 'https://prices.openfoodfacts.org'


def collecter():
    from playwright.sync_api import sync_playwright

    folder = DATA / 'openprices'
    folder.mkdir(parents=True, exist_ok=True)

    # Vérifier les règles du site avant de lancer le navigateur.
    robots = fetch(BASE + '/robots.txt')
    (folder / 'robots.txt').write_text(robots, encoding='utf-8')
    rules = RobotFileParser()
    rules.parse(robots.splitlines())
    if not rules.can_fetch(AGENT, BASE + '/'):
        raise ValueError('Collecte interdite par robots.txt')
    terms = fetch('https://raw.githubusercontent.com/openfoodfacts/open-prices/main/docs/guides/data.md')
    (folder / 'conditions-donnees.md').write_text(terms, encoding='utf-8')
    if 'odbl' not in terms.lower():
        raise ValueError('Conditions modifiées : vérifier la licence avant de collecter.')

    # La page utilise JavaScript : Chromium doit la charger avant extraction.
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            context = browser.new_context(user_agent=AGENT, service_workers='block')

            def verifier_requete(route):
                url = route.request.url
                if urlsplit(url).netloc == urlsplit(BASE).netloc and not rules.can_fetch(AGENT, url):
                    route.abort()
                else:
                    route.continue_()

            context.route('**/*', verifier_requete)
            page = context.new_page()
            page.goto(BASE + '/', wait_until='networkidle', timeout=90000)
            page.wait_for_function("document.body.innerText.includes('€') || document.querySelectorAll('a[href*=\"/products/\"]').length > 0", timeout=60000)
            html = page.content()
            text = page.locator('body').inner_text()
        finally:
            browser.close()

    if not text.strip():
        raise ValueError('La page ne contient pas de texte exploitable.')
    (folder / 'index.html').write_text(html, encoding='utf-8')
    save(folder / 'page.json', {'url': BASE + '/', 'textes': text.splitlines()})
    print('OpenPrices : texte de la page collecté (pas de table de prix structurée).')
