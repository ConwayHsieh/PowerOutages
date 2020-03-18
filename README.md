# PG&E Power Outages 

## About the project

This project aims to dive deeper into what type of customers PG&E Power outages affect the most.

I looked at features such as duration of the average power outage or number of customers affected in a zip code **vs** income and population density.

Below are interactive visuals that summarize my findings:

**Size of circles indicates the average duration of power outage.**

[Link to interactive map: Population Density vs Average Duration of Power Outage](https://conwayhsieh.github.io/PowerOutages/poweroutages_population_duration.html)

[Link to 3D scatter plot comparing Population Density, Median Household Income, and Average Duration of Power Outage (Clustered using Gaussian Mixture Model)](https://conwayhsieh.github.io/PowerOutages/cluster.html)

## Conclusions

Looking at the two visuals, it seems that virtually all high duration power outages occurred in low population density areas, with a less strong, but still noticeable, relationship between low average income and power outage duration as well. 

My recommendation is to prioritize on reducing power outages in low population density areas in order to provide more equal access to electricity for all.

## How I did it:
I first downloaded the data about PG&E power outages, cleaned it, extracted the features I wanted, then merged with US Zip Code data about demographics. I then plotted an interactive map using Folium to visually look for patterns. I then honed in on income and population density, and used a Gaussian Mixture Model to cluster the data into two clusters and plotted it into a 3D scatterplot using Plotly.

### Sources:
https://pge-outages.simonwillison.net/pge-outages

https://uszipcode.readthedocs.io/index.html

## About me:
I graduated from University of California, San Diego with a B.S. in Bioengineering and a Minor in Mathematics and from Carnegie Mellon University with a M.S. in Biomedical Engineering with research emphasis on compuational neuroscience.
