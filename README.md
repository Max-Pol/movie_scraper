# Ghibli Movie Scraper
A small application that lists the Studio Ghibli movies with the characters in them. Thanks for reading this!


## Getting Started
*Requirements*: `virtualenv`, `Python >= 3.6.9`

To **set up the virtual environment**, simply run the following commands in the root directory:
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt

# The same thing in one command...
virtualenv -p python3 venv && source venv/bin/activate && pip install -r requirements.txt
```

Once the dependencies have been installed, you can **start the App** with:
```
python app.py
```
...and you should be able to see the movie list in [http://0.0.0.0:8000/movies](http://0.0.0.0:8000/movies).

## Testing
In order to launch the tests, run in the root directory:
```
python tests/test_app.py
```

## Project Structure
```
movie_scraper
    ├── tests             <- Unittest folder
    ├── app.py            <- Main file of our application
    ├── config.py         <- Configuration file
    ├── errors.py         <- Custom Exceptions of our application
    └── requirements.txt  <- List of our application dependencies
```

## Comments / Improvements
This app could be improved in a lot of ways.

- **Data Management**: in order to avoid calling the API on every page load, I choose to store the list of all movies in a global variable. This choice was motivated by its simplicity and my time constraint. I would never do this for a real project, for several reasons: it often becomes troublesome to keep track of global variable usage and assignement, and multiple instances of the app would unnecessarily duplicate the data... Most of all, it's usually much more efficient and more robust to separate the data management logic from the application, by storing the data in a database or an external cache for instance.
- **Deployment**: I did not have time for this part, but a flask application need to be properly packaged to be used in production, with a WSGI server, Docker container, ...
- **Logging**: Proper logging need to be added to every application...
- **Testing**: Add more tests, use enhanced tools like pytest or nose.
- **Client** : create a separated module for client
