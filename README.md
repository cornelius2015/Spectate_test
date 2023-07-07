# Find Internal Nodes:
***See file find_internal_nodes.py***

# REST Application:
# To Start:
### Run "set_up_database.py" to set up the SQLite database. Then run "rest_application.py"


# Creation:

### Create a new Sport

To create a new Sport, send a POST request to the `/sports` endpoint with a JSON body containing the sport's details. 

For example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"Baseball","slug":"baseball", "active":true}' http://localhost:5000/sports
```
### Create a new Event

To create a new Event, send a POST request to the `/events` endpoint with a JSON body containing the event's details. 

For example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"Wimbledon ", "slug":"wimbledon", "active":true, "type":"preplay", "sport_id":3, "status":"Pending","scheduled_start":"2023-06-26T18:00:00Z", "actual_start":"2023-06-26T18:00:00Z"}' http://localhost:5000/events
```


### Creating a new Selection
To create a new Selection, send a POST request to the /selection endpoint with a JSON body containing the selections details.

For example:
Command:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"Real Madrid to Win", "event_id":1, "price":1.50, "active":true, "outcome":"Unsettled"}' http://localhost:5000/selections
```

# Searching:
### Sport:

```bash
curl -X GET "http://localhost:5000/sports?name=Football&active=True"
```
***Result:***

{
  "sports": [
    [
      1,
      "Football",
      "football",
      1
    ]
  ]
}

### Events:
```bash
curl -X GET "http://localhost:5000/sports/1/events"
```
***Result:***
```json
{
  "events": [
    [
      1,
      "UEFA Europa League",
      "uefa-europa-league",
      1,
      "preplay",
      1,
      "Pending",
      "2023-07-10 20:00:00",
      null
    ],
    [
      4,
      "Champions League",
      "champions_league",
      1,
      "preplay",
      1,
      "Pending",
      "2023-06-26T18:00:00Z",
      "2023-06-26T18:00:00Z"
    ]
  ]
}
```

```bash
curl -X GET "http://localhost:5000/events?type=inplay"
```
***Result***
```json
{
  "events": [
    [
      2,
      "NBA Finals",
      "nba-finals",
      1,
      "inplay",
      2,
      "Started",
      "2023-06-01 19:30:00",
      "2023-06-01 19:35:00"
    ]
  ]
}
```


### Selections:

```bash
curl -X GET "http://localhost:5000/events/1/selections"
```
***Result:***
```json
{
  "selections": [
    [
      1,
      "Man Utd Win",
      1,
      1.9,
      1,
      "Unsettled"
    ],
    [
      2,
      "Draw",
      1,
      3.4,
      1,
      "Unsettled"
    ],
    [
      3,
      "AC Milan Win",
      1,
      4.0,
      1,
      "Unsettled"
    ],
    [
      6,
      "Real Madrid to Win",
      1,
      1.5,
      1,
      "Unsettled"
    ],
    [
      7,
      "Real Madrid to Win",
      1,
      1.5,
      1,
      "Unsettled"
    ],
    [
      8,
      "Real Madrid to Win",
      1,
      1.5,
      1,
      "Unsettled"
    ]
  ]
}
```

```bash
curl -X GET "http://localhost:5000/selections?active=False"
```

***Result***
```json
{
  "selections": [
    [
      5,
      "Heat Win",
      2,
      2.2,
      0,
      "Unsettled"
    ]
  ]
}

```


# Updating:
### Sport:
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name":"Football", "slug":"football", "active":false}' http://localhost:5000/sports/1
```
***Result***
```json
{
  "status": "success"
}
```



### Events:
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name":"Wimbledon", "slug":"wimbledon", "active":true, "type":"inplay", "sport_id":3, "status":"Started", "scheduled_start":"2023-01-01T00:00:00Z", "actual_start":"2023-01-01T00:00:00Z"}' http://localhost:5000/events/3
```
***Result:***

{
  "message": "Event updated successfully"
}


### Selections:
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name":"Celtic Win", "event_id":1, "price":2.5, "active":false, "outcome":"Win"}' http://localhost:5000/selections/2
```

***Result:***

{
  "message": "Selection updated successfully"
}


## Testing:  When all the selections of a particular event are inactive, the event becomes inactive

```bash
curl -X GET "http://localhost:5000/selections?event_id=2"
```
***Result:***
```json


{
  "selections": [
    [
      4,
      "Lakers Win",
      2, --EVENT-ID
      1.6,
      1, --ACTIVE
      "Unsettled"
    ],
    [
      5,
      "Heat Win",
      2, --Event-ID
      2.2,
      0, --InActive
      "Unsettled"
    ]
  ]
}
```
#### We need to make the "Lakers win" inactive and then check events where event=2 is set to inactive
```bash
curl -X GET "http://localhost:5000/events?active=True"
```
***Returns:***
```json
 "events": [
  
    [
      2, --event_id
      "NBA Finals",
      "nba-finals",
      1, --Active
      "inplay",
      2,
      "Started",
      "2023-06-01 19:30:00",
      "2023-06-01 19:35:00"
    ],
```

***And :*** 
```bash
curl -X GET "http://localhost:5000/events?active=False"
```
***Result:***
```json
{
  "error": "No events found for the provided filters."
} 
```



***We now update "Lakers win" to be in-active and check if the event "NBA finals" becomes inactive i.e. set active = false***
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name":"Lakers%20Win", "event_id":2, "price":1.6, "active":false, "outcome":"Unsettled"}' http://localhost:5000/selections/4
```
***Result:***
```json
{
  "message": "Selection updated successfully"
}
```

***Now we run again:***
```bash
curl -X GET "http://localhost:5000/events?active=False" 
```
***and we get:***
```json
{
  "events": [
    [
      2,
      "NBA Finals",
      "nba-finals",
      0, --InActive
      "inplay",
      2,
      "Started",
      "2023-06-01 19:30:00",
      "2023-06-01 19:35:00"
    ]
  ]
}
```
***The NBA finals are now inactive proving that when all the selections of a particular event are inactive, the event becomes inactive***

## Testing: When all the events of a sport are inactive, the sport becomes inactive

```bash
 curl -X GET "http://127.0.0.1:5000/sports?name=Tennis"
```
***Result: Tennis is an active sport:***
```json
{
  "sports": [
    [
      3,
      "Tennis",
      "tennis",
      1 ---Active
    ]
  ]
}
```
```bash
curl -X GET "http://127.0.0.1:5000/events?sport_id=3"
```
***Result:***
```json
{
  "events": [
    [
      5,
      "Wimbledon ",
      "wimbledon",
      1,
      "preplay",
      3,
      "Pending",
      "2023-06-26T18:00:00Z",
      "2023-06-26T18:00:00Z"
    ]
  ]
}
```

***Now we set the "Wimbledon"  event (with id = 5) to be inactive in events i.e.***
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name":"Wimbledon", "slug":"wimbledon", "active":false, "type":"inplay", "sport_id":3, "status":"Started", "scheduled_start":"2023-01-01T00:00:00Z", "actual_start":"2023-01-01T00:00:00Z"}' http://127.0.0.1:5000/events/5
```

***Result:***

```json
{
  "message": "Event updated successfully"
}
```
***We can now check if "Tennis" in the "sports" table is still and active sport***

```bash
curl -X GET "http://127.0.0.1:5000/sports?name=Tennis"
```

***And we see that it has been set to inactive i.e.***
```json
{
  "sports": [
    [
      3,
      "Tennis",
      "tennis",
      0 --InActive
    ]
  ]
}
```
***Thus proving the test to be successful***

## Unittests:
***unittest_model.py***

***unittests_rest_application.py***

## Docker Image
***To build the Docker Image from the Dockerfile run:***
```command
docker build -t rest_application .
```
***Then to run the application***
```command
docker run -p 5000:5000 rest_application
```
