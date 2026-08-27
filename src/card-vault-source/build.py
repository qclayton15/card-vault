"""Assemble the single-file app.

One codebase, one build per game. `CV_GAME` picks the game profile that
build_data.py used; everything game-specific comes out of DATA.game, so the shell,
CSS and JavaScript here are shared verbatim between builds.

    python3 build_data.py && python3 build.py                 # Pokémon (default)
    CV_GAME=game_onepiece CV_JSON=onepiece.json python3 build_data.py
    CV_GAME=game_onepiece CV_JSON=onepiece.json CV_HTML=one-piece-vault.html python3 build.py
"""
import importlib, json, os

GAME = importlib.import_module(os.environ.get("CV_GAME", "game_pokemon")).GAME
DATA = os.environ.get("CV_JSON", "cards.json")
HTML = os.environ.get("CV_HTML", "card-vault.html")

shell = open('shell.html').read()
css   = open('style.css').read()
js    = open('app.js').read()
data  = open(DATA).read()
icons = json.load(open('icons_ball.json'))     # produced by make_icons.py

out = (shell.replace('__CSS__', css)
            .replace('__DATA__', data)
            .replace('__ICONS__', json.dumps(icons, separators=(',', ':')))
            .replace('__ICON_FAV__', icons['fav'])
            .replace('__ICON_APPLE__', icons['apple'])
            .replace('__TITLE__', GAME['title'])
            .replace('__DESC__', GAME['desc'])
            .replace('__NAME__', GAME['name'])
            .replace('__TAGLINE__', GAME['tagline'])
            .replace('__JS__', js))
for token in ('__CSS__', '__DATA__', '__JS__', '__ICONS__', '__ICON_FAV__', '__ICON_APPLE__',
              '__TITLE__', '__DESC__', '__NAME__', '__TAGLINE__'):
    assert token not in out, token

# The storage key is what stands between the user and losing their collection.
# If a build ever ships pointing at the wrong key, every logged card disappears.
assert ('"key":"%s"' % GAME['key']) in data, "cards.json was built for a different game"

open(HTML, 'w').write(out)
print('%s  %d bytes  (%s, storage key %s)' % (HTML, len(out), GAME['id'], GAME['key']))
