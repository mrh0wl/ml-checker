# Mercadolibre Checker
> This repository serves to verify users/emails and passwords in mercadolibre in an automated way.

[![PYTHON Version][py-image]][py-url]
[![Plaform tested][platform-img]]


## Usage example

```
$ git clone https://github.com/MrH0wl/ml-checker.git
$ cd ml-checker
$ python3 -m pip install -r requirements.txt
$ python3 ml.py

  __  __  _            _____  _                  _
 |  \/  || |          / ____|| |                | |
 | \  / || |  ______ | |     | |__    ___   ___ | | __ ___  _ __
 | |\/| || | |______|| |     | '_ \  / _ \ / __|| |/ // _ \| '__|
 | |  | || |____     | |____ | | | ||  __/| (__ |   <|  __/| |
 |_|  |_||______|     \_____||_| |_| \___| \___||_|\_\\___||_|

Correct: the "chromedriver.exe" process was terminated with PID 10948
Filename: <filename.txt>

```.
In the entry <filename> you must put the name of the file with users/emails and passwords (without the "<>") in user:pass format.

## Development setup Linux users

If you are using Linux without a GUI or simply like to use the terminal, you should follow the following steps:

```sh
$ apt-get install -y libappindicator1 fonts-liberation
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ dpkg -i google-chrome-stable_current_amd64.deb
```

If you have an error, use the following:

```sh
$ apt-get install -f
$ dpkg -i google-chrome-stable_current_amd64.deb
```

## Release History

* 0.1.2
    * First version



<!-- Markdown link & img dfn's -->
[py-image]: https://img.shields.io/badge/python-3.7-green.svg?style=flat-square
[py-url]: https://www.python.org/downloads/
[platform-img]: https://img.shields.io/badge/tested-Win%20%7C%20Linux-blue.svg?style=flat-square
