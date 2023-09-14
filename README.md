# **Edna-X**

## Instruction 

To run this project:

1. Install python >=3.6
2. Move to the project directory
3. To install all the dependencies, the terminal run
```shell
pip install -r requirements.txt
```
3. The run
```shell
python app.py
```
4. You can start send a POST query to the endpoint 127.0.0.1:5000/api/bot or localhost:5000/api/bot. This is is how the query must look like.
```json
{
  "username": "string",
  "user_id": "string",
  "query": "string",
  "email": "string", //optional
  "sended_at": "string", //option date time in ISO format
}
```
The response with response code will look like this.

> Code: **200** 
```json
{
    "email": "string",//or null
    "query": "string",
    "query_response": "string",
    "received_at": "string",//datetime in isoformat
    "replyed_at": "string",//datetime in isoformat
    "sended_at": "string",//datetime in isoformat or null
    "success": true,
    "user_id": "string",
    "username": "string"
}
```

or if an error occured 
> Code: **404**, **500**, **503**, **408**
```json
{
    "message": "string", //The error message
    "success": false
}
```

**Code Signification:**
* **200** Everything is okay. Enven if it is a post request You will not receive a 201 response because remember you want to get an information.  
* **404** The information in the query where not found. This will be very rare so, contact us if it happens
* **500** Internal server error. Normaly this does'nt concern You but check the error because it could be due to your query like bad formating and so on.
* **503** The bot has not been aible to find a response to your query
* **408** Time out. The bot take too much time to find a response for your query or some ressource take too much time to be available.

Enjoy this bot without restraint  😁 !!!

By ***Ovide KUICHUA***.
