# CineBus 🎬🚌<picture>  <source srcset="https://fonts.gstatic.com/s/e/notoemoji/latest/1f37f/512.webp" type="image/webp">  <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f37f/512.gif" alt="🍿" width="32" height="32"></picture>

Wanna watch a movie? Choose one and go by bus!

## Getting Started
This project is divided in four parts: 

* `billboard.py` : Contains all the code related to obtaining the actual billboard and provifing search methods.

* `buses.py` : Contains all the code related to the construction of the buses graph.


* `city.py` : Contains all the code related to the construction of the city graph (that is, the street graph and the buses graph) and the search for routes between two points of the city.


* `demo.py` : Contains all the code related to user interface of the program.


### Prerequisites
This project is build in `python3`. You can update it with the following commands:
```
pip3 install --upgrade pip3
pip3 install --upgrade python3
```
The librarys used are:
* `typing_extensions` to define new types.
* `BeautifulSoup`, `requests` for web scraping.
* `networkx` to manipulate graphs.
* `osmnx` to obtain streets graphs .
* `haversine` calculating distances between coordinates.
* `staticmap` to draw and plot maps.
* `rich`, `loaders`, `pillow` for user interface
* `pickle` to save big datas to the computer (in this case, the osmnx graph of Bcn)

 
You can install this packages one by one with `pip3 install package_name`, or all at the same time with the following command:
```
pip3 install -r requirements.txt
```

Optionally, exclusifly for user's view, we reccommend to dowload the file `map_pointer.png` in the same directory where to run the program. It does not affect execution of the program.

## Usage
**Things to consider:**
- Currently, this project is exclusively confined to the city of Barcelona, some functionallities will not work outside Barcelona.
- The user interface is made in English, but the language of the Billboard it's in _spanish_. Therefore, all the names and search methods require to use the film names, cinemas names... in spanish.

The `demo.py` module offers a simple menu system for the user's interface. It needs to be executed in a __command prompt__, with the command `#>python demo.py` (or `#>py demo.py`,  depending on your python caller) at the same directory where the dowloaded files are. 

The functionalities offered by `demo.py` are as follows:
- Display today's Billboard and other information, such as all the cinemas and movies from the billboard, types of movie genres...
- Offer filtering and searching methods to apply in the billboard
- Display the buses map and the city map.
- Display the indications and the path the user needs to take (by walking and maybe taking the bus) given it's time disponibility and location to go to the cinema to watch the earliest session of a movie he chooses. 
- Display the names and information of the project autors

Here is a diagram of the menu system:

<div align="center">
  <img src="menu_diagram.png" width="80%" height="80%">
</div>


Note that the format of the filter system is quite specyfic. It's already explained to the user right before entering a filter, as you can see in the image above. 
Here are some examples:
```
- #>Enter filter: time=16:00 - 20:00; city = Barcelona; movie = Star Wars episodio V: El Imperio contraataca
- #>Enter filter: genre = Acción; cinema = Balmes Multicines
```

After choosing what movie you want to see and specifying your time disponibility and your coordinates, the program displays the the cinema where you can watch the movie sooner, along with the indications of how to get there from your current position and an image of the path

### Authors
Developed by [Pau Mateo Bernado](https://github.com/PauMateo) and [Pau Fernández Cester](https://github.com/PauFdz), Data Science students at GCED, UPC. (2022-23).

### Licence
This project is licensed under the Apache 2.0 License.
