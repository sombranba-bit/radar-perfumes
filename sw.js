// Fragans: primero la red (precios siempre frescos); si no hay conexión, lo último que se vio.
const C = 'fragans-v1';
self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin) return;   // fotos de las tiendas y fuentes: las sirve el navegador
  const key = u.origin + u.pathname;                                        // sin ?v= ni ?t=: una sola copia por archivo
  e.respondWith(fetch(e.request).then(r => {
    if (r.ok) { const c = r.clone(); caches.open(C).then(ca => ca.put(key, c)); }
    return r;
  }).catch(() => caches.match(key)));
});
