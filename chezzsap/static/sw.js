self.addEventListener('install', function(event) {
    console.log('Service Worker installed.');
});

self.addEventListener('activate', function(event) {
    console.log('Service Worker activated.');
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        fetch(event.request).catch(function() {
            return caches.match(event.request);
        })
    );
});
