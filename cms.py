from flask import Blueprint, render_template, current_app, abort, session
from app_extensions import tryton

cms = Blueprint('cms', __name__, template_folder='templates')

def _galatea_website():
    return current_app.config.get('TRYTON_GALATEA_SITE')

def _visibility():
    visibility = ['public']
    if session.get('logged_in'):
        visibility.append('register')
    if session.get('manager'):
        visibility.append('manager')
    return visibility

@cms.route("/<slug>", endpoint="article")
@tryton.transaction()
def article(lang, slug):
    '''Article detaill'''
    Website = tryton.pool.get('galatea.website')
    Article = tryton.pool.get('galatea.cms.article')
    galatea_website = _galatea_website()

    website = Website(galatea_website)

    domain = [
        ('slug', '=', slug),
        ('active', '=', True),
        ('visibility', 'in', _visibility()),
        ]
    if hasattr(Article, 'websites'):
        domain.append(('websites', 'in', [galatea_website]))
    else:
        domain.append(('galatea_website', '=', galatea_website))
    articles = Article.search(domain, limit=1)

    if not articles:
        abort(404)
    article, = articles
    return render_template('cms-article.html',
            article=article,
            website=website,
            )
