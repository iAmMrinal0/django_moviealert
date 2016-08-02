# Movie Alert
A web front end for the CLI application at [Movie Alert](https://github.com/iammrinal0/movie-alert)

## Requirements
1. Software requirements are `Python 3`, `Postgres`, `Redis`
2. Install Python packages using `pip install -r requirements/testing.txt` for `test` or whatever environment you prefer.


## Setup
Following are the environment variables required:

``` shell
SECRET_KEY # Django secret key
DATABASE_NAME # database info
DATABASE_USER
DATABASE_PASSWORD
GMAIL_ID # Email login info for sending emails
GMAIL_PASSWORD
```


## Working

The way this works is that, you signup/in and add alerts for movies you want with city, language, and date and every hour a task runner fetches tasks and scrapes BookMyShow for showtimes in that particular city with language and date and sends you an email when the criteria matches.

## Features
1. Signin using Google
2. Add movie, city, date, language of your choice.
3. List out all alerts added by you

### License
 See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT)
