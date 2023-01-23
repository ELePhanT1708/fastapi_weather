# fastapi_weather with openweathermap.org

## Intro 
It was test task from e-commet company to Juniour position in their company(startup).

Link to task : https://docs.google.com/document/d/1F7wsrcq86yC0ZlEwCBPT88DFSnQj6ggBycTXyYh64ec/mobilebasic

I want to say about definition of this task: 

I did not understand how and where I'll have to use scrapy parser. IN this sentence for example: 'Из БД на ваш выбор (любая SQL, но выбор нужно обосновать) нужно получить список городов. '

And I decided to made it in my way without scrapy parser , with request lib to fetch new data from openweathermap.org.

I agreee, it is not right to decline definition of task , but I did not really understand why scrapy needed. 

And other reason to not to use scrapy: 

It is requirement to have Windows SDK as Microsoft C++ tool on thr machine and wothout this lib you can't install the lib scapy from pip.
And it will be a problem when you will start to work on docker container and have to adjust this requirement within container.

## To launch the systme
1. Clone the repo 
2. Launch docker desktop
3. In cloned directory from powershell or something similar write:
    - 'docker-compose up --build'

## Results
1. I adjusted  all services in docker-compose file and all development was done in container from the beginning of the project :
    - Fastapi_app
    - Postgresql
    - PgAdmin for checking Postgresql
    
I have some skeleton repo with adjusted Fastapi-postgres-pgadmin project made by myself.


2. I found from openweathermap.org the archive with all city_names, which exists on the platform as JSON file. Agree , it is not right at all , 
but I use it to select cities to save in db via my API using request lib to semd post request to localhost to my API.

3.In API I implemented 3 main enpoints:
  - Add_city to db
  - Get last_info about all exists cities
  - Statistic about one city (without filtering by time interval)
## My weak places
1. Testing - no one test in project , unfortunately. 
2. Async - I used asyn func only to send requests to my localhost, I am not very good at it, but I try to understand it depthly before using.
I think , if you know how to use async in adding new row in db , it will be great improve the speed of proccessing.
3. I embedded get request to openweathermap.org within endpoint operations , it is not great I know , but I made it that way.


## Thanks 

for reading this , and I will wait feedback


That's all !!
----
     
