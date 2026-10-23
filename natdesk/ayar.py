#!/usr/bin/env python3
"""NAT Desk istemci ayarlari -> rdgen derleme dosyasinin bekledigi secrets.json.

  python3 natdesk/ayar.py <profil> secrets.json

Sunucu bilgileri asagida (tum profiller icin ortak); profil farklari natdesk/profiller/<profil>.json.
custom (base64) icerigi rdgen'in (bryangerlach/rdgen, rdgenerator/views.py) urettigiyle ayni yapidadir.
"""
import base64, json, re, sys, uuid
from pathlib import Path

SUNUCU = {
    'server': 'remote.natbilisim.com',
    'serverPort': '21116',
    'key': 'n350+iCGL8zQd2sL62QEIi8eDB0WcxP4VKqQJBQ52bM=',
    'apiServer': 'https://remote.natbilisim.com',
    'urlLink': 'https://natbilisim.com',
    'downloadLink': 'https://natbilisim.com',
    'compname': 'NAT Bilisim',
}


def slug(s):
    s = re.sub(r'[^\w\s-]', '', s.lower()).strip()
    return re.sub(r'[-\s]+', '-', s)


def main(profil, cikti):
    p = json.loads((Path(__file__).parent / 'profiller' / f'{profil}.json').read_text(encoding='utf-8'))
    appname, filename = p['appname'], p['exename']
    assert appname.isascii() and re.fullmatch(r'[A-Za-z0-9_-]+', filename), 'ad ve exe adi ASCII olmali'
    # Uygulama adinda bosluk olmamali: RustDesk kurulumu servis/taskkill komutlarinda adi tirnaksiz kullaniyor
    assert re.fullmatch(r'[A-Za-z0-9_-]+', appname), 'uygulama adinda bosluk / ozel karakter olmamali'
    c = {'conn-type': p['direction'], 'app-name': appname, 'override-settings': {}, 'default-settings': {}}
    if not p.get('installation', True):
        c['disable-installation'] = 'Y'
    if not p.get('settings', True):
        c['disable-settings'] = 'Y'
    if p.get('permanentPassword'):
        c['password'] = p['permanentPassword']
    if p.get('theme', 'system') != 'system':
        c['default-settings']['theme'] = p['theme']
    c['enable-lan-discovery'] = 'N' if p.get('denyLan') else 'Y'
    c['allow-auto-disconnect'] = 'N'
    d = c['default-settings']
    d.update({
        'access-mode': 'custom', 'enable-keyboard': 'Y', 'enable-clipboard': 'Y', 'enable-file-transfer': 'Y',
        'enable-audio': 'Y', 'enable-tunnel': 'Y', 'enable-remote-restart': 'Y', 'enable-record-session': 'Y',
        'enable-block-input': 'Y', 'allow-remote-config-modification': 'N', 'direct-server': 'N',
        'verification-method': 'use-both-passwords', 'approve-mode': p.get('passApproveMode', 'password-click'),
        'allow-hide-cm': 'N', 'allow-remove-wallpaper': 'Y', 'enable-remote-printer': 'Y', 'enable-camera': 'Y',
        'enable-terminal': 'Y',
    })
    custom = base64.b64encode(json.dumps(c).encode('ascii')).decode('ascii')
    out = dict(SUNUCU)
    out.update({
        'custom': custom, 'uuid': str(uuid.uuid4()),
        'iconlink_url': 'yerel', 'iconlink_uuid': 'yerel', 'iconlink_file': 'icon.png',
        'logolink_url': 'yerel', 'logolink_uuid': 'yerel', 'logolink_file': 'logo.png',
        'privacylink_url': 'false', 'privacylink_uuid': 'false', 'privacylink_file': 'false',
        'appname': appname, 'slug_appname': slug(appname), 'genurl': '',
        'delayFix': 'true', 'rdgen': 'true', 'xOffline': 'false', 'removeNewVersionNotif': 'true',
        'update_public_key': '', 'androidappid': 'com.natbilisim.natdesk', 'filename': filename,
    })
    Path(cikti).write_text(json.dumps(out), encoding='utf-8')
    print(f'{profil}: {appname} / {filename}.exe / {p["direction"]} -> {cikti}')
    print('custom:', json.dumps(c, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
