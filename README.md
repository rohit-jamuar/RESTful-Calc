#RESTful Calculator

A terminal based RESTful calculator which returns the sum and product of values passed. It allows the user to query on the basis of time at which the request was made. It also persists data with server.

##Functions supported:
  * **compute()** - User will **POST** integers to this endpoint - whose sum and product is expected from this calculator. The calculator will compute the results and send back the expected outcome in **JSON** format. User should **POST** in the following format : 
  
  curl -H "Content-Type: application/json" -X POST -d '{"values":[ *comma-separated integers* ]}' http://127.0.0.1:5000/api
  
    * e.g. curl -H "Content-Type: application/json" -X POST -d '{"values":[100,2,3,4]}' http://127.0.0.1:5000/api

  
  * **get_stored_data()** - User will **POST** an integral value (*minutes*) to the calculator. This value would be used for searching the calculator's internal data-store for queries (and their respective outcomes) which were sent to the calculator, whose time-stamp is greater than or equal to *minutes* minutes. The list of filtered queries would be returned as a **JSON**. User should **POST** in following format : 
  
  curl -H "Content-Type: application/json" -X POST -d '{"minutes":*integer-value*}' http://127.0.0.1:5000/get_stored
  
    * e.g. curl -H "Content-Type: application/json" -X POST -d '{"minutes":1}' http://127.0.0.1:5000/get_stored
  
###To run calculator: 
`python math_engine.py`

###To query calculator:
* Open another *Terminal*
* **curl**-away

###Requirements:
  * Python 2.7
  * Flask

