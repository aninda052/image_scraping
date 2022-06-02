# Django Image Scraper

This is a small image Scraper  project using Django rest Framework.

## Install

#### Cloning the project

```angular2html
git clone https://github.com/aninda052/image_scraping.git
cd image_scraping
```

You can run the project 2 way

- ###  Using `runserver`  command

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver 8000
```

This project scrape image using background task. So after installing 
required parameter and running the project using  `runserver` 
comment, you also need to start worker instance for background task to work properly.

``
python manage.py process_tasks
``

- ### Using `docker-compose`

To run the project using `docker-compose`; `docker` and `docker-compose` must be installed on your system. 
For installation instructions refer to the Docker [docs](https://docs.docker.com/compose/install/).

After you install `docker` and `docker-compose` properly, run -

```angular2html
docker-compose up --build
```

If everything went well, go to `http://127.0.0.1:8000` and paste any url from where you want to scrape images.

To get the list of images there is a api -

```angular2html
http://127.0.0.1:8000/api/get-image/
```

This api only allow `GET` method.

You can also filter/search images through this api by passing multiple query params.

Available params - 

- `image_id`
- `image_source`
- `scraped_url`






