Equities Trader

There are two ways to install and use the program:

1) [Using a Docker image](#using-docker)

2) [Using a Github Repository](#using-github-repository)

## **Using Docker**

*****Make sure you have Docker install*

1) Pull the Docker image from the Docker Hub using:

```
docker pull katie:equities_trader
```

2) Run the image with interactive mode flag:

```
docker run -ti equities_trader
```



## **Using Github Repository**

Requirements: Python 3.x,pip, BeautifulSoup, tabulate (see below for instructions)

1) Clone the repository

```
git clone https://github.com/vaMuchenje/equities_trader.git
```

2) Switch into the directory and install dependencies

```
pip install --no-cache-dir -r requirements.txt
```

3) Run the app:

```
python app.py
```

