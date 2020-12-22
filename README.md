### JSON schema validator

#### To run validator use 
`make run`
#### To run tests use 
`make tests`

#### Console output:
```
Validate 3ade063d-d1b9-453f-85b4-dda7bfda4711.json:
There is no schema with name cmarker_calculated!

Validate f5656ff6-29e1-46b0-8d8a-ff77f9cc0953.json:
Everything is OK!

Validate fb1a0854-9535-404d-9bdd-9ec0abb6cd6c.json:
Field data.cmarkers is required!

Validate bb998113-bc02-4cd1-9410-d9ae94f53eb0.json:
Field data.unique_id is required!

Validate a95d845c-8d9e-4e07-8948-275167643a40.json:
Content in event/a95d845c-8d9e-4e07-8948-275167643a40.json is empty!

Validate 29f0bfa7-bd51-4d45-93be-f6ead1ae0b96.json:
Content in event/29f0bfa7-bd51-4d45-93be-f6ead1ae0b96.json is empty!

Validate 2e8ffd3c-dbda-42df-9901-b7a30869511a.json:
There is no schema with name meditation_created!

Validate 6b1984e5-4092-4279-9dce-bdaa831c7932.json:
There is no schema with name meditation_created!

Validate e2d760c3-7e10-4464-ab22-7fda6b5e2562.json:
Node data.user_id should be integer not str

Validate c72d21cf-1152-4d8e-b649-e198149d5bbb.json:
There is no schema with name meditation_created!

Validate cc07e442-7986-4714-8fc2-ac2256690a90.json:
There is no data in file event/cc07e442-7986-4714-8fc2-ac2256690a90.json

Validate ba25151c-914f-4f47-909a-7a65a6339f34.json:
There is no schema with name label_       selected!

Validate 297e4dc6-07d1-420d-a5ae-e4aff3aedc19.json:
Field data.type_ranges[29].type is required!
Field data.type_ranges[31].type is required!
Field data.type_ranges[33].type is required!

Validate ffe6b214-d543-40a8-8da3-deb0dc5bbd8c.json:
Node data.user_id should be integer not NoneType
Node data.cmarkers should be array not str

Validate 1eba2aa1-2acf-460d-91e6-55a8c3e3b7a3.json:
Field data.unique_id is required!
Field data.user is required!
Field data.user_id is required!

Validate 3b4088ef-7521-4114-ac56-57c68632d431.json:
Everything is OK!
```