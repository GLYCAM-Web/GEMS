# Readme for the delegator

The delegator entity is responsible for directing incoming requests to other GEMS entities.   Because of this, delegator offers only a few services.

## Services

- `ListEntities` - return a list of entities to which the delegator can forward requests.
- `ListServices` - return a list of services offered by the delegator
- `Marco` - return an affirmation that connection to the delegator is working

## Request redirection

When the `$GEMSHOME/bin/delegate.py` script is given JSON, either via a file passed as an argument or as pure JSON stdin, Delegator's reception module (`gemsModules/delegator/receive.py`) is given this this request as a string. Delegator's reception module parses the JSON and determines the Entity to which the request should be forwarded.  Delegator's reception module then hands off the request to the appropriate entity's reception module. Delegator's reception module then waits for a response from the entity's reception module and returns this response to the caller.


## Delegator Entity Config and Redirector Settings

The delegator entity is configured by the `known_entities.json` file.  This file is located in the `gemsModules/delegator` directory.  The file is a JSON object with the following key/value pairs: "EntityName": "EntityModule". Tere EntityModule should be equivalent to EntityName or the value "DeprecatedDelegator", which indicates that the entity is to be handled by the deprecated delegator. 

The editable and committed `known_entities.json` allows choosing which entities you would like to enable, after configuring this, it is baked so that the delegator has a static list of entities and to avoid the generation overhead. The delegator will not be able to see any changes to the `known_entities.json` file until the baked version is deleted and the delegator is restarted. The baked version is located in the `gemsModules/delegator` directory and is named `delegator.baked.git-ignore-me.json`. 

The baked delegator config can be deleted directly or by using `python $GEMSHOME/bin/manage_gemsModules.py --unbake`.
