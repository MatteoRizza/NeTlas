# NeTlas - installing guide
## Creation and installation 

1. Create a Neo4j database (name: netlas, password: netlas)

2. Add APOC plugin to Neo4j db - https://neo4j.com/developer/neo4j-apoc/

3. Run database

4. Install the following packages
### python:

```
pip install neo4j
pip install pathlib
pip install pandas-profiling[notebook]
pip install tdqm
```

### node:
```
npm install --save express
npm install neo4j-driver
npm install cytoscape
npm install cytosnap
npm install cytoscape-fcose
```

5. Create the file **globalvars.py** in the folder [PythonProject](PythonProject/) with this code changing the **serverurl**, **servername** and **serverpassword** with the relative data: 

```
#Global vars
serverurl = '' # Database URL 
servername = '' # Database USERNAME
serverpassword = '' # Database PASSWORD
#todo: set vars according to the database
```


6. Create the file **globalvars.js** in the folder [JavascriptProject/nodejsserver](JavascriptProject/nodejsserver) with this code changing the **serverurl**, **servername** and **serverpassword** with the relative data: 

```
// Global vars
const serverurl = '' // Database URL 
const servername = '' // Database USERNAME
const serverpassword = '' // Database PASSWORD

// Export the variables
module.exports = {
  serverurl,
  servername, 
  serverpassword
}
``` 

7. Create the file **globalvars.js** in the folder [JavascriptProject](JavascriptProject) with this code changing the **serverurl**, **servername** and **serverpassword** with the relative data: 

```
//Global vars
const serverurl = '' // Database URL 
const servername = '' // Database USERNAME
const serverpassword = '' // Database PASSWORD
``` 

8. The first time, to populate the database run the following command:

```
python3 PythonProject/main.py
```

9. The first time, to create files important for the rendering phase run the following command: 

```
node --max-old-space-size=8192 nodejsserver/server.js
node JavascriptProject/nodejsserver/server.js
```

10. When all is finished, to check the installation run:

```
python3 -m http.server 7794
```

and select the JavascriptProject Folder.


## Start NetLas

#### Backend 
To start the node server used for the backend:

```
node --max-old-space-size=8192 nodejsserver/server-start.js
node JavascriptProject/nodejsserver/server-start.js
```

#### Frontend 
To start the frontend page :

```
python3 -m http.server 7794
```

and select the JavascriptProject Folder.