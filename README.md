# PyPillary
Python interface for Mapillary API

##Example
First of all, import modules
~~~
import pypillary.model as model
import pypillary.request as request
~~~
Simle way for use PyPillary is ApiService class that contains method for create requests and multithreading execution. We must put in ctor path for file, that contains clientId in first raw and clientSecret in secondRaw
```
service = request.APIService("clientInfo.txt")
```