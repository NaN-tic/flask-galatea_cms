from flask import Blueprint, render_template, current_app, abort
from galatea.tryton import tryton

cms = Blueprint('cms', __name__, template_folder='templates')

Article = tryton.pool.get('galatea.cms.article')

GALATEA_WEBSITE = current_app.config.get('TRYTON_GALATEA_SITE')

@cms.route("/<slug>", endpoint="article")
@tryton.transaction()
def article(lang, slug):
    '''Article detaill'''
    articles = Article.search([
        ('slug', '=', slug),
        ('active', '=', True),
        ('galatea_website', '=', GALATEA_WEBSITE),
        ], limit=1)

    if not articles:
        abort(404)
    article, = articles
    return render_template('cms-article.html',
            article=article,
            cache_prefix='cms-article-%s-%s' % (article.id, lang),
            )
