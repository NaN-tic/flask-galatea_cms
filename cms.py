from flask import Blueprint, render_template, current_app, abort, g
from galatea.tryton import tryton
from galatea.utils import get_tryton_locale

cms = Blueprint('cms', __name__, template_folder='templates')

Article = tryton.pool.get('galatea.cms.article')

galatea_website = current_app.config.get('TRYTON_GALATEA_SITE')

@tryton.default_context
def default_context():
    language = get_tryton_locale(g.language)
    return {'language': language}

@cms.route("/<slug>", endpoint="article")
@tryton.transaction()
def article(lang, slug):
    '''Article detaill'''
    articles = Article.search([
        ('slug', '=', slug),
        ('active', '=', True),
        ('galatea_website', '=', galatea_website),
        ], limit=1)

    if not articles:
        abort(404)
    article, = articles
    return render_template('cms-article.html',
            article=article)
