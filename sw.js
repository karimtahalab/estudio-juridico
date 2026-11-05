// Guarda la pantalla en el celular: abre al instante y se actualiza sola en segundo plano.
const V = 'consultas-20261105174145';
const BASE = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-180.png', './favicon.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(BASE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin) return; // los datos van directo al servidor
  e.respondWith(caches.open(V).then(c => c.match(e.request, { ignoreSearch: true }).then(hit => {
    const red = fetch(e.request).then(r => { if (r && r.ok) c.put(e.request, r.clone()); return r; }).catch(() => hit);
    return hit || red;
  })));
});
