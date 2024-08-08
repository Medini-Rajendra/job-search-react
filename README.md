# Job Application Portal
This repository fetches job results from the google page and displays in tabular format for the user to apply.

## Packages required
React, Tailwindcss, apify-client, danfojs

## Installation
`npm create vite@latest .`

`npm i`

`npm install -D tailwindcss postcss autoprefixer`

Follow further instructions from https://tailwindcss.com/docs/guides/vite

### Important things

Define api key in .env in project root directory 

`VITE_REACT_API_RAPIDAPI_KEY = "<key value>"`

and use this key as "import.meta.env.<keyname>" for api key initialization