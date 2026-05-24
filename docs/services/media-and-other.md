# Media & Utilities

Beyond the data platform, DataHub.local hosts a set of media management services and everyday utility tools — making the homelab genuinely useful as a personal productivity and entertainment hub.

---

## Media Services

### :material-television-play: [Servarr Stack](https://github.com/datahub-local/servarr)

<div class="svc-tags"><span class="svc-tag">media</span> <span class="svc-tag">streaming</span> <span class="svc-tag">self-hosted</span> <span class="svc-tag">arr-stack</span></div>

The Servarr stack bundles all the *arr applications into a single, cohesive deployment via a custom Helm chart backed by NFS shares on TrueNAS.

| Service | Purpose |
|---------|---------|
| **Jellyfin** | Media server — stream movies, TV, and music to any device |
| **Sonarr** | TV show management — monitor, download, and organize series |
| **Radarr** | Movie management — monitor, download, and organize films |
| **Prowlarr** | Indexer management — unified search across all torrent/Usenet indexers |
| **qBittorrent** | Download client — torrents with a web UI |
| **Bazarr** | Subtitle management — auto-download subtitles for all media |
| **Jellyseerr** | Request management — interface to request new movies/shows |
| **Flaresolverr** | Cloudflare bypass proxy for indexers |

!!! tip "Custom Helm Chart"
    The entire stack is deployed via a single Helm chart [`servarr`](../open-source/index.md), published open source. One `helm install` brings up the complete media server.

---

### :material-rss: [CommaFeed](https://github.com/Athou/commafeed)

<div class="svc-tags"><span class="svc-tag">rss</span> <span class="svc-tag">news</span> <span class="svc-tag">self-hosted</span> <span class="svc-tag">reading</span></div>

Self-hosted RSS reader that works like Google Reader — clean, fast, and without tracking, ads, or algorithmic filtering. Feeds are also consumed by n8n AI workflows for automated news summarization and daily digest generation.

---

### :material-music: MusicGrabber

<div class="svc-tags"><span class="svc-tag">media</span> <span class="svc-tag">music</span> <span class="svc-tag">self-hosted</span></div>

Handles music library acquisition and management, complementing Jellyfin's music streaming capabilities. Automates the process of building and maintaining a local music library from various sources, keeping metadata clean and organized for playback through Jellyfin.

---

## Utility Services

### :material-home-analytics: [Homepage](https://gethomepage.dev/)

<div class="svc-tags"><span class="svc-tag">dashboard</span> <span class="svc-tag">self-hosted</span> <span class="svc-tag">homelab</span> <span class="svc-tag">monitoring</span></div>

Unified homelab dashboard — single pane of glass for all running services. Shows status, links, and live stats (CPU, memory, service health) for every service in the cluster. It's the first thing you see when opening a browser on the home network — one click to reach Grafana, Superset, ArgoCD, or Jellyfin.

---

### :material-file-pdf-box: [Stirling PDF](https://stirlingtools.com/)

<div class="svc-tags"><span class="svc-tag">pdf</span> <span class="svc-tag">tools</span> <span class="svc-tag">self-hosted</span> <span class="svc-tag">privacy</span></div>

Comprehensive self-hosted PDF manipulation toolkit with 40+ PDF operations: merge, split, compress, convert, OCR, sign, watermark, and more — all processed locally. Replaces cloud PDF services like SmallPDF or ILovePDF with full privacy; no files leave the cluster.

---

### :material-tools: [IT Tools](https://it-tools.tech/)

<div class="svc-tags"><span class="svc-tag">developer-tools</span> <span class="svc-tag">utilities</span> <span class="svc-tag">self-hosted</span></div>

Developer and IT utilities — a Swiss Army knife of 60+ web-based tools: JWT decoder, UUID generator, CRON expression builder, JSON formatter, hash generator, base64 encoder, regex tester, and more. No data leaves the cluster.

---

### :material-swap-horizontal: [ConvertX](https://github.com/C4illin/ConvertX)

<div class="svc-tags"><span class="svc-tag">file-conversion</span> <span class="svc-tag">tools</span> <span class="svc-tag">self-hosted</span> <span class="svc-tag">privacy</span></div>

Self-hosted file format converter handling images, documents, audio, and video — without uploading files to external services. Powered by FFmpeg, ImageMagick, and other format-specific tools to handle hundreds of format combinations locally.

---

### :material-dots-grid: Omni Tools

<div class="svc-tags"><span class="svc-tag">utilities</span> <span class="svc-tag">productivity</span> <span class="svc-tag">self-hosted</span></div>

A collection of miscellaneous productivity utilities accessible from the browser. Complements IT Tools with additional general-purpose helpers for everyday tasks — keeping all utility tooling inside the cluster rather than relying on external web services.

---

### :material-image-edit: [Mazanoke](https://github.com/civilblur/mazanoke)

<div class="svc-tags"><span class="svc-tag">image</span> <span class="svc-tag">tools</span> <span class="svc-tag">self-hosted</span> <span class="svc-tag">privacy</span></div>

Client-side image compression and optimization tool — images are processed entirely in the browser and never uploaded to a server. Useful for quickly resizing or compressing screenshots and photos before sharing, without sending data to external services.
