# Image Upload API
### Cloud Run Application - Docker
#### Developed by Michael Wesley
---

## After clone:
* First Run: `python -m venv .venv`
* Enter the directory: `.venv` 
* Install dependences: `python -m pip install -r requirements.txt`
* To Run: `python -m flask run`

## Description
* `/imgup`: receives the image file and calls the `/resize` route. At the end, it returns a new generated image file.
* `/resize`: is called by `/imgup` route and resizes the image file to 384x384 or according to the size received by parameter.