# Reverse-engineering Skyscanner

## Context

May is approaching, which means the first season of the cheapest tickets of the year. I'm curious because I miss traveling (the last time I flew was in November). So, I go to the Skyscanner website, I choose to fly from `Lithuania` to `Everywhere`, I click on the time, and what... the `Cheapest month` option is gone!

![Cheapest month removed by the Chinese?](/static/images/kova_su_skyscanner/skscanner-months.png)

I thought my browser was spazzing out, but no. Everyone on reddit has been complaining about Skyscanner removing this feature for a long time now. Chinese move, if you ask me (Skyscanner was sold to the Chinese in 2016). So, I decided that they had overstepped and wanted to bring back this feature for myself.

![ASCII Pepe](/static/images/kova_su_skyscanner/pepe-matrix.gif)

## What is the chance that the functionality is just hidden?

Skyscanner has its own API, so they can't change functionality at will, as many companies use their services. Therefore, my first hypothesis was that the functionality is not removed, it is just hidden.

I tried parsing the URL when the first search is done:

`https://www.skyscanner.net/transport/flights-from/lt/?qp_prevScreen=HOMEPAGE&adultsv2=1&cabinclass=economy&childrenv2=&ref=home&is_banana_refferal=true&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&oym=2304&iym=2305`

The most important parts are the `flights-from/lt` link itself and the `oym=2304&iym=2305` parameters. The first shows that flights are searched by country code (LT, LV, DE, etc.) if the country was entered in the search, and the `oym` and `iym` parameters set the search months. Everything else is bullshit. So, the idea is that, after deleting the parameters, skyscanner should do something interesting. I deleted the settings and this is what was left:

`https://www.skyscanner.net/transport/flights-from/lt/`

I reloaded the page. For some reason it remained the same. Strange. I racked my brain and realized that they are using my session to retrieve this data and saved the parameters from the previous URL.

I ran the URL with incognito mode (it's not just for watching porn, you horny bastards) and voila - the hypothesis was correct. The functionality was simply hidden from users!

![Success!](/static/images/kova_su_skyscanner/sk_cheap_flights.jpg)

## Let's go deep

That's it, I got what I wanted. But wait, this data comes from somewhere. Let's dive deep with F12 dev-tools. In the network tab, we can view what requests are happening during page loading and notice what information is arriving. But I don't need everything there, the most important thing are files in `.json`, `.xml` or `.txt` format. APIs are usually in `.json` format. So, I reload the page, group the files by size, and here's the result:

![Long URL and largest in size](/static/images/kova_su_skyscanner/sk_network.jpg)

The very first URL immediately caught my eye, so I opened it. Jackpot.

![I shouldn't be here, but the public API is public ¯\_(ツ)_/¯](/static/images/kova_su_skyscanner/sk_api1.jpg)

After analyzing the API URL, the most important parts were `/LT/anywhere/anytime/anytime/` and `?apikey=8aa374f4e28e4664bf268f850f767535`. The first part defines the parameters for the API server to generate information, and the second part is the public API key that authenticates my request to the server.

After analyzing the API objects, I got the following impression:

* `Id`: is the country code
* `Direct`: defines whether the flight is direct
* `Name`: is the name of the country
* `IndirectPrice`: The price of the cheapest indirect flight
* `DirectPrice`: The price of the cheapest direct flight
* `IndirectQuoteDateTime`: When was the price of indirect flights last updated
* `DirectQuoteDateTime`: When was the price of direct flights last updated

An idea came up.

## Reverse-engineering API with Python

I created a skyscanner workflow for performing a standard search that looks like this:

1. Choose which country you are flying from
2. Choose which country you are flying to
3. Choose the airport to which country you are flying
4. Choose the airport from which country you are flying
5. Choose the flight dates
6. You get up-to-date prices and times

I wrote `class Skyscanner` and put the flow of actions in one function:

![Workflow pseudocode](/static/images/kova_su_skyscanner/sk_workflow.jpg)

### First step: the country you are flying from

The purpose of this function is to select the departure location. Skyscanner has a dedicated API for this.

`https://www.skyscanner.net/g/autosuggest-search/api/v1/search-flight/UK/en-GB/{SEARCH QUERY}?isDestination=false&enable_general_search_v2=false`

The search API call occurs every time a button is pressed (aka. OnKeyPress event) if there are at least two letters in the search. The results are generated on the server.

![Search API return data](/static/images/kova_su_skyscanner/sk_search_api.jpg)

It was a bit unclear how to distinguish a country from an airport, but I came up with a very simple idea: if the name of the object (PlaceName) matches the name of the country (CountryName), it is a country.

The code is not special, since the calculations are performed by the API server itself:

![The object is returned](/static/images/kova_su_skyscanner/sk_search.jpg)

### Second step: the country you are flying to

This is where the fun begins.

The purpose of this function is to generate a list of countries that can be flown to, rank them by cheapest, and determine whether the flight is direct or not. I already mentioned before that skyscanner has a special API for this data.

`https://www.skyscanner.net/g/browse-view-bff/dataservices/browse/v3/bvweb/LT/EUR/en-GB/destinations/{COUNTRY OR AIRPORT CODE}/anywhere/anytime/anytime /?apikey=8aa374f4e28e4664bf268f850f767535`

So now the API data would be generated based on any country you want to fly from and a list of countries can be created from that.

However, there are no flight prices for some countries, so the resulting list should be filtered. That is, if the flight price is 0, the indicated flight does not exist. Otherwise, you should check whether there are direct and indirect flights to the country at the same time, and choose a cheaper option. I put this filter in a separate function. Then I sorted the countries with a custom function by price.

When printing, I also made it show whether the cheapest flight from a country is direct or not.

![Selections from Lithuania](/static/images/kova_su_skyscanner/sk_to_country.jpg)

### Step three: Airport to the country you are flying to

Further actions require precision. Therefore, you need to insert country instead of `/anywhere/` in the aforementioned URL. In this case, the API generates the airports.

![Airports in Sweden](/static/images/kova_su_skyscanner/sk_api2.jpg)

The code is more or less analogous to the previous step.

What I can say is that Skyscanner has good API designers.

![From Lithuania to Sweden](/static/images/kova_su_skyscanner/sk_to_airport.jpg)

### Step four: The airport you are flying from

If the airport was not selected at the beginning, this function is skipped, but its purpose is similar to the previous one. So, below, only the API URL itself changes to:

`https://www.skyscanner.net/g/browse-view-bff/dataservices/browse/v3/bvweb/LT/EUR/en-GB/destinations/{COUNTRY_CODE_CHANGE}/{AIRPORT_TO_WHERE_FLIGHT}/anytime/anytime/? apikey=8aa374f4e28e4664bf268f850f767535`

Then the API generates the airports for the country you are flying from:

![From Lithuanian airport](/static/images/kova_su_skyscanner/sk_from_airport.png)

### Step five: choose your flight dates

The calendar, where you can choose flight days, also has its own separate API.

`https://www.skyscanner.net/g/browse-view-bff/dataservices/browse/v3/bvweb/LT/EUR/en-GB/destinations/{AIRPORT_FROM}/{AIRPORT_TO}/anytime/anytime/? apikey=8aa374f4e28e4664bf268f850f767535`

Opening this URL was the first what the fuck moment. It seems mystical.

![Well it looks like data](/static/images/kova_su_skyscanner/sk_wtf.jpg)

![This is wtf](/static/images/kova_su_skyscanner/sk_wtf2.jpg)

Those `Traces` still look like data, but `PriceGrid` it looks like a jigsaw puzzle. Maybe those pricegrids are coordinates? I had to force myself to think hard again. And then I discovered this:

![Hmm, what's this?](/static/images/kova_su_skyscanner/sk_api3.jpg)

Direct - it's probably a flight. Okay, April has 30 days, counting starts from 0 and ends with 29 - that's 30 options. Okay, I will choose the price calendar displayed by skyscanner, some day is the 12th, and another is the 2nd. The first number is the day of departure and the second is the day of arrival, and when there is a flight on those days, the price is shown! It all clicked.

Now I can generate all the prices for the cheapest flight period to that country, and sort them all by price:

![Cheapest flights from Kaunas to Gothenburg](/static/images/kova_su_skyscanner/sk_dates_by_price.jpg)

You can imagine that it is the same as clicking on each arrival/departure day in the calendar with your hands and writing them all in a table according to the price.

### Step six: up-to-date-prices

The purpose of this function is to generate a URL and allow you to view flight tickets at the point of purchase. Here was the easy part.

![Url to point of purchase](/static/images/kova_su_skyscanner/sk_url.jpg)

## Additional functionality: all flights for the year are sorted by price

The calendar API felt like a sandbox to me.

After digging deeper, I realized that I could expand the functionality to make it pull flight prices not only for the cheapest month, but also for a **LONGER PERIOD** (usually up to a year) ahead, starting with the current month.

Now imagine going through Skyscanner's entire calendar for a single flight, clicking on each arrival and departure day, writing down flight prices by hand and then sorting them by price. I'm sure there are people who do it like that, especially when you have to plan vacations around work, but the amount of time this new functionality saves is enormous.

![Scans annual flights from Vilnius to Athens](/static/images/kova_su_skyscanner/sk_calendar_scan.jpg)

The photo shows how all flights from Vilnius to Athens displayed this year are scanned. Then the different flights (of which there are over 800 from Vilnius to Athens) are sorted by price - all you have to do is choose the most convenient date. ***THIS IS A NEW FUNCTIONALITY THAT NORMAL USERS HAVE NEVER SEEN AND WILL NEVER SEE!***. In the following photo, you can see the difference between the first four cheapest flights, which is less than 10 euros, but the dates differ by even 5 months in one place.

![Several options in May and one in October. The difference is less than 10 euros](/static/images/kova_su_skyscanner/sk_year_cheapest.jpg)

Skyscanner representatives, if you are reading this, you can already hire me for freelance work.

## Ending words

So, for now, this is the end of the Skyscanner API journey. If you know how to spoof POST requests with Python (not childishly), please contact me.

For those who want to play with the code or plan their future vacation in the most efficient way, here is the project link: [https://github.com/NorthOC/fast_scanner](https://github.com/NorthOC/fast_scanner)

