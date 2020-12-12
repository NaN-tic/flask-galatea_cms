from flask import Blueprint, render_template, current_app, abort, session
from galatea.tryton import tryton

cms = Blueprint('cms', __name__, template_folder='templates')

Website = tryton.pool.get('galatea.website')
Article = tryton.pool.get('galatea.cms.article')

GALATEA_WEBSITE = current_app.config.get('TRYTON_GALATEA_SITE')

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
    website = Website(GALATEA_WEBSITE)

    domain = [
        ('slug', '=', slug),
        ('active', '=', True),
        ('visibility', 'in', _visibility()),
        ]
    if hasattr(Article, 'websites'):
        domain.append(('websites', 'in', [GALATEA_WEBSITE]))
    else:
        domain.append(('galatea_website', '=', GALATEA_WEBSITE))
    articles = Article.search(domain, limit=1)

    if not articles:
        abort(404)
    article, = articles
    return render_template('cms-article.html',
            article=article,
            website=website,
            )
