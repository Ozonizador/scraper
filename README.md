
Price Scraper API

## Getting started

Firstly, install the dependecies:
```bash
npm install
```

Then, run the development server:
```bash
npm run dev
``` 

Open [http://localhost:5000](http://localhost:5000) with your browser to see the result.

## API
Current available routes:

### POST - Worten
This route is available at [http://localhost:5000/api/crawl](http://localhost:5000/api/crawl).
It's necessary to provide a JSON object with url's.
Ex.
```bash
{
    "urls": [
        "https://www.worten.pt/produtos/arranhador-para-gatos-bege-pawhut-mrkean-8435428737412",
        "https://www.worten.pt/produtos/consola-nintendo-switch-v2-6994947"
    ]
}
```
