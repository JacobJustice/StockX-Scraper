# StockX-Scraper

Scrapes StockX for data on sneakers. I cannot reccomend use of this web scraper however as StockX probably doesn't allow for it (see Does StockX allow use of this? below).

The website is subject to change and this readme was written as of June 9th, 2020

# What is StockX?

www.stockx.com

StockX is a website where people can resell certain items of value. 
The items are authenticated by a team of (albeit so-so quality) authenticators employed by StockX themself.
While originally only for sneakers, they have expanded to streetwear, collectible items, handbags, watches and more.


# How to use

Simply run `python sneaker.py` and sit back for a long period of time.

Here is what it should look like:

https://www.youtube.com/watch?v=eEy5Hl3TJ04

# Does StockX allow use of this?

Almost definitely **NO**, but it is not THAT simple. 

Their robots.txt does allow for bots to access any portion of the site with no explicit delay. However, I have seen issues with the selenium driver getting blocked from the site for 10-20 minutes after running the scraper for an hour and I assume it is because of the following lines in their terms of service (https://stockx.com/terms):

```
You must not do any of the following ...
· use any robot, spider, scraper, or other automated or manual means to access our Services, or copy any information thereon, for any purpose without our express written permission;
· probe, scan, test the vulnerability of or breach the authentication measures of, the Sites or any related networks or systems;
· bypass our robot exclusion headers, robots.txt rules or any other measures we may use to prevent or restrict access to our Services;
```
Of course the first line very plainly states that use of this scraper or any other is disallowed.

On the contrary, the line "bypass our robot exclusion headers, robots.txt rules..." makes me think that they must allow scrapers to access non-disallowed portions of the site because that implies that they care about what the robots.txt disallows and therefore also does not disallow. They also don't specify a crawl-delay, which makes me think that perhaps they don't want people using any scraper otherwise they would make it easier for people. 

To me it seems that the robots.txt is poorly implemented, but there for entities that do have express permission to access their site, unfortunately that is a little misleading to the layman and they should update their robots.txt to name these specific agents to make it more clear who is allowed to access which parts of their site with a scraper.

