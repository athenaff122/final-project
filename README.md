<h1>Fall 2022 SI 507 Final Project</h1>
<h2>Instruction</h2>
<p>This project uses interactive command shell to search the background information of a stock.
The project is mainly divided into two parts:
1) The companies in Forbes Top 2000 in 2022 are web scrapped and saved as a JSON file <>.
   The companies are classified into different countries, which are saved as a JSON file
2) The user can choose the company they want to know from US company list first. It is fulfilled by a search function.
   For example, if user input "apple", all stock which has the "apple" as keyword will be returned in the list.
3) User can decide the stock symbol base on a series of price choice.
4) Users can also choose the background information they want to know about the stock.
5) A SMA-5 and 10 days figure will be showed to help witht the trading decision.</p>

<h2>Data source</h2>
<p> 
1) Web scrapping: https://www.forbes.com/lists/global2000/?sh=1d4699995ac0
   Challenge score: 4. Scraping a new single page
2) API: 
   Stock API : https://www.alphavantage.co/
   Financial data market API: https://polygon.io/
   Challenge score: 4. Web API you haven’t used before that requires API key or HTTP Basic authorization
</p>

<h2>Data structure</h2>

