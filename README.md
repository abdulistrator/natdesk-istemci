# NAT Desk istemcisi

NAT Desk (remote.natbilisim.com) için Windows istemcisini GitHub Actions üzerinde derler.
Derleme dosyası [rdgen](https://github.com/bryangerlach/rdgen) (GPL-3.0) üzerine kuruludur; rdgen sunucusu gerekmez,
ayarlar bu depodadır.

## Derleme

1. **Actions** › **NAT Desk Windows** › **Run workflow**
2. Profil seç: `host` (NATDesk Host: personel, sadece bağlanılır, servis durdurulamaz) veya `natdesk` (NATDesk: IT, iki yönlü)
3. Yaklaşık 40-60 dakika sonra çalışmanın sayfasında **Artifacts** altından `natdesk-host` / `natdesk`
   paketini indir: içinde `.exe` ve `.msi` var.

## Ayarlar

| Dosya | İçerik |
|---|---|
| `natdesk/ayar.py` | Sunucu adresi, anahtar, API adresi (tüm profiller) |
| `natdesk/profiller/*.json` | Profil farkları: bağlantı yönü, ayarlar menüsü, LAN keşfi, kalıcı parola |
| `natdesk/varliklar/icon.png`, `logo.png` | Simge (512×512) ve pencere logosu |
| `.github/workflows/natdesk-macos.yml` | macOS derlemesi (Intel + Apple Silicon .dmg) |
| `natdesk/rdgen-kaynak.txt` | Temel alınan rdgen sürümü (yamalar bu sürümden indirilir) |

Not: RustDesk istemcisi AGPL-3.0 lisanslıdır. Değiştirilmiş istemci başka şirketlere dağıtılırsa kaynak kodu
(bu depo ve kullanılan RustDesk sürümü) erişilebilir tutulmalıdır.
