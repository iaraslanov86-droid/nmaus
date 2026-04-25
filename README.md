# nmaus.ru — сайт ООО «НефтеМонтажАвтоматика»

Astro 5.0 статический сайт строительной компании НМА (нефтегазовая отрасль, Республика Коми и НАО).

## Стек
- **Astro 5.0** — статический генератор, ноль JS на проде, мгновенная загрузка
- **@astrojs/sitemap** — автоматический sitemap-index.xml
- **Vanilla CSS** — без Tailwind, без зависимостей фреймворков
- **Hosting**: Cloudflare Pages (статика + CDN, бесплатно)

## Структура

```
src/
  data/         — все контентные JSON (services, cities, regions, company)
  pages/        — Astro-шаблоны и динамические маршруты
  layouts/      — BaseLayout с meta/og/jsonld
  components/   — переиспользуемые блоки (HeroBackdrop, TrebsaCase)
  styles/       — global.css
public/         — robots.txt, llms.txt, фавиконы, og-картинки
```

132 страницы генерируется при сборке (~750ms):
- `/` — главная
- `/about/` — о компании
- `/{region}/` × 2 (komi, nao)
- `/{region}/{service}/` × 18 (2 региона × 9 услуг)
- `/{region}/{service}/{city}/` × 90 (10 городов × 9 услуг)
- `/uslugi/{service}/` × 9 (общие страницы услуг)
- `/gorod/{city}/` × 10 (городские страницы)
- `/404`

## Локальная разработка

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # сборка в dist/
npm run preview  # просмотр сборки локально
```

## Деплой на Cloudflare Pages

### Одноразовая настройка

1. Запушить в GitHub (уже сделано через `gh repo create`).
2. Зайти на https://dash.cloudflare.com/ → Workers & Pages → Create → Pages → Connect to Git.
3. Выбрать репозиторий `iaraslanov86-droid/nmaus`. Настройки сборки:
   - Framework preset: **Astro**
   - Build command: `npm run build`
   - Build output directory: `dist`
   - Root directory: `/` (по умолчанию)
4. Deploy → через 1–2 минуты сайт доступен на `nmaus.pages.dev`.

### Подключение домена nmaus.ru

1. В Cloudflare Pages → проект `nmaus` → Custom domains → Set up a custom domain → `nmaus.ru`, потом ещё раз → `www.nmaus.ru`.
2. Cloudflare покажет CNAME/A-записи (примерно):
   - `nmaus.ru` → CNAME → `nmaus.pages.dev` (или A-записи Cloudflare)
   - `www.nmaus.ru` → CNAME → `nmaus.pages.dev`
3. В панели reg.ru → Управление DNS домена nmaus.ru → прописать эти записи. TTL 300.
4. HTTPS-сертификат и CDN включаются автоматически в течение 5–15 минут.

⚠️ **На reg.ru сейчас стоит WordPress-сайт** — после смены DNS он перестанет открываться. Перед переключением можно скачать архив текущего сайта (на всякий случай).

### Дальнейшие изменения

```bash
git add .
git commit -m "..."
git push
```

Cloudflare Pages увидит push и через 30–60 секунд задеплоит новую версию на прод.

## SEO

- robots.txt — разрешены Yandexbot, GPTBot, ClaudeBot, PerplexityBot
- llms.txt — паспорт компании для AI-поисковиков (Perplexity, ChatGPT Search)
- sitemap-index.xml — автоматический, дифференцированные приоритеты (1.0 → 0.6)
- JSON-LD: Organization (с ИНН/ОГРН/СРО/МЧС), LocalBusiness на 100+ страницах, FAQPage везде, BreadcrumbList, Service
- Geo meta: geo.region, geo.placename, ICBM на городских страницах
- 6 уникальных вопросов FAQ на главной + 4 вопроса/город × 10 городов + service.faq на каждой услуге

## Контакты

ООО «НефтеМонтажАвтоматика», ИНН 1106028181, ОГРН 1111106001588
8 (82144) 52-0-52 · info@nmaus.ru
