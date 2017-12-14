# Web Scraping Kampala House Data

This project covers web scraping of house data from the [Jumia House website](house.jumia.ug/). 

* Clone the project:

```
git clone https://github.com/brianmusisi/kampala-housing-data.git
```


* Usage:

In the terminal enter the command below: 

```
python gethouses.py num_pages > houses.csv
```  

where num_pages is he number of pages to be scraped from the website. The default is 10 pages if num_pages is not provided.  
The data produced is comma-delimited and should ideally be saved in a csv/txt file as above. houses.csv is the file where the data will be saved otherwise the scraped data will just be displayed in the terminal.

