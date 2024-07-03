## Currency-Exchanger
The program is a dynamic currency exchanger.

The user inputs the currency type and the amount of money it has in that currency, then the user enters 
the currency it wants the value in. It takes the exchange values of http://www.floatrates.com/json-feeds.html After that,
the script creates .json files with the subtracted data for the US dollars and Euro currencies and stores 
these in the cache(a local folder in the pc in which the script is running). Once that is complete, the script 
verifies if the user requested exchange values are in the cache, if they are, the script gives the value for the new currency 
to the user, if they aren't, the script request the values to the webpage mentioned before, create the .json in the cache and gives
the new currency value to the user.
