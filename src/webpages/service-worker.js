const CACHE_NAME = 'image-cache-v1';

self.addEventListener('fetch', event => {
    console.log(1)
    if (event.request.destination === 'image' && /\.(png|jpg|jpeg)$/.test(event.request.url)) {
        event.respondWith(
            caches.match(event.request)
                .then(response => {
                    if (response) {
                        return response; // 从缓存返回图片
                    }

                    return fetch(event.request).then(
                        response => {
                            if (!response || response.status !== 200 || response.type !== 'basic') {
                                return response;
                            }

                            const responseToCache = response.clone();

                            caches.open(CACHE_NAME)
                                .then(cache => {
                                    cache.put(event.request, responseToCache); // 缓存图片
                                });

                            return response;
                        }
                    );
                })
        );
    }
});

self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName); // 删除旧缓存
                    }
                })
            );
        })
    );
});
