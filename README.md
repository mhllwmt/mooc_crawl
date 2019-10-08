# mooc_crawler
An implementation of BIT-IR final project crawler part

## Getting Started
```shell script
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Prerequisites
- Python >= 3.6
- [geckodriver](https://github.com/mozilla/geckodriver/releases) should be pre-installed

## Run
```shell script
# up to now, only email login supported, so the login arguments should be valid
scrapy runspider [spider_name].py -a category=[content to be crawled] -a username=[login username] -a password=[login password]
```

## Deployment

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Acknowledgements