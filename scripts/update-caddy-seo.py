"""Run on the existing VPS through SSH; changes only the nmaus.ru block.
Default: preview. --apply validates before reload, restores original on failure.
"""
from pathlib import Path
import os, subprocess, sys, tempfile

path = Path('/etc/caddy/Caddyfile')
original = path.read_text()
start = original.index('\nnmaus.ru {') + 1
end = original.index('\nwww.nmaus.ru {', start)
old = original[start:end]
assert '    @old_about path /contacts /contacts/ /license' in old, 'Unexpected config: stop for review'
block = old.replace('@old_about path /contacts /contacts/ /license', '@old_about path /license', 1)
addition = '''
    # SEO 2026-10-31: canonical directory URLs and public static cache.
    @nmaindex path_regexp nmaindex ^(.*/)index\\.html$
    redir @nmaindex {re.nmaindex.1}?{query} permanent
    @nmaimmutable path /_astro/*
    header @nmaimmutable Cache-Control "public, max-age=31536000, immutable"
    @nmaassets path *.svg *.png *.jpg *.ico *.webmanifest
    header @nmaassets Cache-Control "public, max-age=86400"
    handle_errors {
        header Cache-Control "no-store"
        rewrite * /404.html
        file_server {
            status {err.status_code}
        }
    }
'''
assert block.count('    import static nmaus.ru') == 1
block = block.replace('    import static nmaus.ru', addition+'\n    import static nmaus.ru')
if '--apply' not in sys.argv:
    print(block)
    sys.exit(0)
assert Path('/var/www/nmaus.ru/contacts/index.html').is_file(), 'Deploy contacts page first'
assert Path('/var/www/nmaus.ru/404.html').is_file(), 'Missing error page'
updated = original[:start]+block+original[end:]
fd, name = tempfile.mkstemp(prefix='nma-seo-', dir='/etc/caddy')
try:
    with os.fdopen(fd, 'w') as out: out.write(updated)
    check = subprocess.run(['caddy','validate','--config',name,'--adapter','caddyfile'],capture_output=True,text=True)
    if check.returncode:
        print('Validation failed; original unchanged.'); sys.exit(1)
    assert path.read_text()==original, 'Config changed concurrently; abort'
    path.write_text(updated)
    reload = subprocess.run(['systemctl','reload','caddy'],capture_output=True,text=True)
    if reload.returncode:
        path.write_text(original)
        subprocess.run(['systemctl','reload','caddy'],check=True)
        raise RuntimeError('Reload failed; original restored')
    print('Validated and reloaded. Only nmaus.ru block changed.')
finally:
    Path(name).unlink(missing_ok=True)
