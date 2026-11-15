# Maintainer: Amiro <sp.adrian@vp.pl>
pkgname=xpg-maestro-plus-linux-git
pkgver=r1.0000000
pkgrel=1
pkgdesc="Linux USB HID driver for the Adata XPG Maestro Plus 62DA CPU cooler segment display"
arch=('any')
url="https://github.com"
license=('MIT')
depends=('python' 'python-pyusb' 'python-psutil')
makedepends=('git')
provides=('xpg-maestro-plus-linux')
conflicts=('xpg-maestro-plus-linux')
source=("git+${url}.git")
sha256sums=('SKIP')

pkgver() {
  cd "${srcdir}/xpg-maestro-plus-linux"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
  cd "${srcdir}/xpg-maestro-plus-linux"

  # Instalacja głównego skryptu w /usr/bin
  install -Dm755 xpg_display.py "${pkgdir}/usr/bin/xpg-display"

  # Instalacja reguł udev w systemowym katalogu pakietów
  install -Dm644 99-xpg-maestro.rules "${pkgdir}/usr/lib/udev/rules.d/99-xpg-maestro.rules"

  # Instalacja globalnej usługi użytkownika systemd (wskazującej na /usr/bin/xpg-display)
  install -dm755 "${pkgdir}/usr/lib/systemd/user"
  sed 's|%h/.local/bin/xpg_display.py|/usr/bin/xpg-display|g' xpg-display.service > "${pkgdir}/usr/lib/systemd/user/xpg-display.service"
  chmod 644 "${pkgdir}/usr/lib/systemd/user/xpg-display.service"

  # Instalacja licencji i dokumentacji
  install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
  install -Dm644 README.md "${pkgdir}/usr/share/doc/${pkgname}/README.md"
}
