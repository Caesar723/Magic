// Cosmetic data only. Prices, inventory and card contents come from the server.
const PackArt = Object.freeze({
    Original: {file: 'original', color: '#a45f50', trim: '#d8c5a0', shape: 'folio', depth: .55},
    Legend: {file: 'legend', color: '#465f78', trim: '#c8bf9e', shape: 'crown', depth: .85},
    Antiquities: {file: 'antiquities', color: '#a58d6b', trim: '#656e68', shape: 'slab', depth: .95},
    Red: {file: 'red', color: '#984f48', trim: '#d7b18d', shape: 'spire', depth: .65},
    Green: {file: 'green', color: '#63785b', trim: '#b9bc91', shape: 'leaf', depth: .7},
    Blue: {file: 'blue', color: '#547f89', trim: '#bbd0c3', shape: 'arch', depth: .7},
    Black: {file: 'black', color: '#625568', trim: '#ac9c9a', shape: 'octagon', depth: .85},
    White: {file: 'white', color: '#c5bca2', trim: '#6c7e7d', shape: 'wing', depth: .65}
});

function getPackArt(pack) {
    const style = PackArt[pack.name];
    const fallback = '/' + String(pack.pack_url || '').replace(/^\/+/, '');
    return {...(style || PackArt.Original), image: style ? '/webpages/draw_card/art/packs/' + style.file + '.webp' : fallback, fallback};
}
