# Book Web Scraping

This project is a web scraping tool developed to collect detailed information about books from Amazon and Google Books. It retrieves data such as title, rating, description, and authors.

## Search Logic

- Books are not fetched randomly. The scraping process requires a custom search string that defines the topic of interest.
Example:

```
"quantum healing and energy and chakras and reiki and law of attraction and natural healing"
```

- This ensures that all results are contextually related to the given search terms.

## Tools and Technologies

- The project integrates three automation and scraping tools:

    - Selenium — for browser automation

    -  Playwright — for fast and reliable web scraping

    -  BeautifulSoup — for parsing and extracting data from HTML

## Data Collected
- For each book, the scraper extracts:

    - Title

    - Author(s)

    - Description

    - Rating (if available)

## Project Goal

- This project is part of a broader data science analysis aimed at exploring how algorithms can identify and predict patterns related to pseudoscientific or misleading content.
The scraped data serves as an initial dataset for classification and pattern recognition models in future stages of the research.

## Academic Context

- Developed as part of a presentation project at the Federal University of Sergipe (UFS), this work demonstrates how data science, web scraping, and automation (RPA) techniques can be applied to detect and analyze materials that potentially spread pseudoscience or misinformation.