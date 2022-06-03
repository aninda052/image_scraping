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

### Available Request parameters

- `image_id` : 
  - Data type : Int
  - Expected value : id of any Image
- `image_size`
  - Data type : String
  - Expected value : `small`, `medium` & `large`
- `image_source`
  - Data type : String
  - Expected value : original image source of any Image
- `scraped_url`
  - Data type : String
  - Expected value : the url from where image has been scraped
- `domain`
  - Data type : String
  - Expected value : domain name from where image has been scraped

### The response body have 4 parameters

- count : total number of image
- next : next page link (`null` if there is no next page)
- previous : previous page link (`null` if there is no previous page)
- results : list of image objects

## Request-Response Example

Get image with id `5`

#### Request Url

`http://127.0.0.1:8000/api/get-image/?image_id=5`

#### Response 

```angular2html
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "image_id": 5,
            "image_source": "https://www.lg.com/lg5-common/images/common/header/logo-experience-happiness.png",
            "scraped_url": "https://www.lg.com/us/refrigerators",
            "domain": "www.lg.com",
            "download_date": "2022-06-04",
            "image": "http://127.0.0.1:8081/media/images/www.lg.com/logo-experience-happiness_fkmmKcQ.png",
            "image_dimension": "100*30"
        }
    ]
}

```

Get images with a domain `lg` and image size `small`

#### Request Url

`http://127.0.0.1:8000/api/get-image/?domain=lg&image_size=small`

#### Response 

```angular2html

{
    "count": 12,
    "next": http://127.0.0.1:8000/api/get-image/?domain=lg&image_size=small&page=2,
    "previous": null,
    "results": [
        {
            "image_id": 1,
            "image_source": "https://www.lg.com/lg5-common/images/common/header/logo-experience-happiness.png",
            "scraped_url": "https://www.lg.com/us/refrigerators",
            "domain": "www.lg.com",
            "download_date": "2022-06-04",
            "image": "http://127.0.0.1:8081/media/images/www.lg.com/logo-experience-happiness_fkmmKcQ.png",
            "image_dimension": "100*30"
        },
        {
            "image_id": 2,
            "image_source": "https://www.lg.com/us/images/gnb/lg-thinkq-logo-2.png",
            "scraped_url": "https://www.lg.com/us/refrigerators",
            "domain": "www.lg.com",
            "download_date": "2022-06-04",
            "image": "http://127.0.0.1:8081/media/home/aninda/image_scraping/media/images/www.lg.com/lg-thinkq-logo-2_dt0PPDo_small.png",
            "image_dimension": "256*50"
        }
        ...
        
    ]
}

```

