## LOTR.api
## 1. What this project does?
This project is a full-stack CRUD application built around characters from the Lord of the Rings universe.
At its core, it provides a REST API that allows you to:
-create characters
-read one or all characters
-update characters
-delete characters
All character data is stored in a PostgreSQL database, and the API is built using FastAPI.

## 2. Main user flow
1. User opens the page:
The frontend starts from index.html.
It has a main container where characters will be placed:
```JavaScript
<main>
  <div id="characters" class="characters-grid"></div>
</main>
```
It also loads the JavaScript file:
```JavaScript
<script src="app.js"></script>
```
2. JavaScript sends request to the API
When the page loads, app.js calls loadCharacters():
```JavaScript
loadCharacters();
```
Inside that function, the frontend sends a request to the API:
```JavaScript
const response = await fetch(API_URL);
const characters = await response.json();
```
3. FastAPI receives the request
The frontend is requesting:
```python
GET /characters/
```
That request is handled in characters.py:
```python
@router.get("/", response_model=List[CharacterSchema])
async def read_all_characters() -> List[CharacterSchema]:
    return await crud.get_all()
```
4. CRUD layer gets data from database
The route does not directly talk to the database.
Instead, it calls crud.get_all():
```python
async def get_all() -> List[dict]:
    characters = await Character.all().values(
        "id",
        "name",
        "age",
        "race",
        "description",
        "image",
        "created_at",
    )
    return characters
```
This means:
Route → CRUD → Database model → Database

5. Character model defines database data
The database table is represented by the Character model:
```python
class Character(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    age = fields.IntField()
    race = fields.CharField(max_length=255)
    description = fields.TextField()
    image = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
```
So every character returned to the frontend comes from this table structure.

6. API returns JSON to the frontend
The backend returns a list of characters.
Then the frontend loops through them:
```JavaScript
characters.forEach((character) => {
  const card = document.createElement("article");
  card.className = "character-card";
```
7. Frontend creates character cards
For every character, JavaScript creates HTML:
```JavaScript
card.innerHTML = `
  <img src="${character.image}" alt="${character.name}" class="character-image" />
  <div class="character-card-content">
    <h2 class="character-name">${character.name}</h2>
    <p class="character-meta"><strong>Age:</strong> ${character.age}</p>
    <p class="character-meta"><strong>Race:</strong> ${character.race}</p>
    <p class="description-preview">${character.description}</p>
    <p class="click-more">Click to read more...</p>
  </div>
`;
```
This is what the user sees on the page.

8. User clicks a character
Each card gets a click event:
```JavaScript
card.addEventListener("click", () => openModal(character));
```
When clicked, the modal opens with full details:
```JavaScript
modalName.textContent = character.name;
modalAge.textContent = character.age;
modalRace.textContent = character.race;
modalDescription.innerHTML = character.description;
```
## 3. Project structure
```text
LOTR.api/ -> root
  .github/        -> GitHub configuration/workflows
  data/           -> character JSON data used for seeding
  frontend/       -> static frontend shown in the browser
  project/        -> main FastAPI backend application
  docker-compose  -> runs the backend and PostgreSQL together
  README          -> project documentation
  seed_characters -> script for adding/updating character data
```
### project/ structure
```text
project/ -> backend root
  app/            -> main application code
  db/             -> database container setup
  env/            -> local virtual environment
  htmlcov/        -> test coverage HTML report
  migrations/     -> Aerich/Tortoise database migrations
  tests/          -> automated tests

  .coverage       -> raw coverage result file
  .coveragerc     -> coverage configuration
  .dockerignore   -> files ignored by Docker
  Dockerfile      -> builds the backend container
  entrypoint.sh   -> startup script for the container
  pyproject.toml  -> tool configuration, mainly Aerich
```
### app/ structure
```text
app/ -> FastAPI application package
  api/            -> API endpoints and request handling
  models/         -> validation schemas and database models

  __init__.py     -> makes app a Python package
  config.py       -> application settings and environment config
  db.py           -> database setup and Tortoise initialization
  main.py         -> application entry point
```
### app/api structure
```text
api/ -> API layer
  crud.py         -> database operations for creating, reading, updating, and deleting characters
  hello.py        -> health/config check endpoint
  characters.py  -> main character API routes
```
### app/models structure
```text
models/ -> data definitions
  pydantic.py     -> request/response validation schemas
  tortoise.py     -> database model definitions
```
### frontend structure
```text
frontend/ -> browser UI
  index.html      -> page structure
  app.js          -> fetches characters from the API and renders cards
  style.css       -> page styling, cards, modal, responsive layout
```
## 4. Backend flow
The backend flow is the path from an HTTP request to a database action and then back to the client.
```text
Client request
  ↓
main.py
  ↓
characters.py
  ↓
crud.py
  ↓
tortoise.py
  ↓
PostgreSQL database
  ↓
JSON response
```
### main.py
This file starts and connects the backend.
It creates the FastAPI app, adds CORS, registers routes, and initializes the database.
```text
application.include_router(hello.router)
application.include_router(
    characters.router, prefix="/characters", tags=["characters"]
)

app = create_application()

init_db(app)
```
### characters.py
This file is used as a route layer.
It handles the actual HTTP endpoints.
For example, when the client wants all characters:
```python
@router.get("/", response_model=List[CharacterSchema])
async def read_all_characters() -> List[CharacterSchema]:
    return await crud.get_all()
```
So this request:
```python
GET /characters/
```
goes to:
```python
read_all_characters()
```
### pydantic.py
This file validates incoming data.
When the client creates or updates a character, the request body must match this schema:
```python
class CharacterPayloadSchema(BaseModel):
    name: str
    age: int
    race: str
    description: str
    image: str
```
So this JSON is valid:
```JSON
{
  "name": "Frodo",
  "age": 50,
  "race": "Hobbit",
  "description": "Ring bearer",
  "image": "images/frodo.jpg"
}
```
But if name, age, race, description, or image is missing, FastAPI returns a validation error before the database is touched.
### crud.py
This file performs the database operation.
The route does not directly use the database.
Instead, it calls functions from crud.py.
Create flow:
```python
async def post(payload: CharacterPayloadSchema) -> int:
    character = Character(
        name=payload.name,
        age=payload.age,
        race=payload.race,
        description=payload.description,
        image=payload.image,
    )
    await character.save()
    return character.id
```
Read-all flow:
```text
async def get_all() -> List[dict]:
    characters = await Character.all().values(
        "id",
        "name",
        "age",
        "race",
        "description",
        "image",
        "created_at",
    )
    return characters
```
This is the main separation:

characters.py -> decides what endpoint does
crud.py       -> performs the database work

### tortoise.py
This file defines the database table.
It defines the Character database model.
```python
class Character(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    age = fields.IntField()
    race = fields.CharField(max_length=255)
    description = fields.TextField()
    image = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
```
In simple terms:

Character model -> characters table
fields          -> table columns

When crud.py calls:
```python
await character.save()
```
Tortoise ORM turns that into a database insert.

### db.py
This file connects FastAPI to postgreSQL
It registers Tortoise ORM with the FastAPI app.
```python
def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
```
This is what allows the app to use:
```python
Character.all()
Character.filter()
character.save()
```
without manually writing SQL.

### config.py
This file handles environment settings.
It defines settings such as environment, testing mode, and database URL.
```python
class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)
    database_url: str | None = None
```
The /hello route uses these settings to show which environment the app is running in.

## 5. Data validation and database storage
Pydantic handles validation, Tortoise handles persistence.
Clearly separated data validation from database storage.
That separation is one of the most important architectural decisions in the backend.
```text
Pydantic -> validates incoming/outgoing data
Tortoise -> saves and retrieves data from the database
```
### Pydantic → validation layer
Pydantic defines what data the API expects.
```python
class CharacterPayloadSchema(BaseModel):
    name: str
    age: int
    race: str
    description: str
    image: str
```
What Pydantic does?
When a request comes in:
```JSON
{
  "name": "Frodo",
  "age": 50,
  "race": "Hobbit",
  "description": "Ring bearer",
  "image": "images/frodo.jpg"
}
```
Pydantic:
-checks all fields exist
-checks types (age must be int, etc.)
-rejects invalid input before it reaches the database

If something is wrong:
```JSON
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "Field required"
    }
  ]
}
```
This happens before CRUD is even called.

### Tortoise → persistence layer
Tortoise defines how data is stored in PostgreSQL.
```python
class Character(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    age = fields.IntField()
    race = fields.CharField(max_length=255)
    description = fields.TextField()
    image = fields.CharField(max_length=255, null=True)
```
What Tortoise does?
-maps Python objects → database rows
-converts operations into SQL queries
-interacts with PostgreSQL

Example:
```python
await character.save()
```
→ becomes:
```text
INSERT INTO character ...
```
### Where they meet 
The connection happens in crud.py.
```python
async def post(payload: CharacterPayloadSchema) -> int:
    character = Character(
        name=payload.name,
        age=payload.age,
        race=payload.race,
        description=payload.description,
        image=payload.image,
    )
    await character.save()
    return character.id
```
Flow:
```text
Request JSON
  ↓
Pydantic (validated payload)
  ↓
crud.py
  ↓
Tortoise model
  ↓
Database
```
## 6. Frontend flow
The frontend flow is the path from the user opening the page to character cards being shown and opened in a modal.
-index.html loads the page.
-style.css makes it look like a LOTR-themed page.
-app.js runs in the browser.
-app.js calls the backend API.
-The API returns character data as JSON.
-JavaScript creates character cards.
-User clicks a card.
-A modal opens with the full character information.

### index.html 
index.html -> static HTML skeleton
The page has an empty container where characters will be inserted:
```JavaScript
<main>
  <div id="characters" class="characters-grid"></div>
</main>
```
It also has a modal already prepared in the HTML:
```JavaScript
<div id="character-modal" class="modal hidden">
  <div class="modal-content">
    <button id="close-modal" class="close-button">&times;</button>
    <img id="modal-image" class="modal-image" src="" alt="" />
    <h2 id="modal-name"></h2>
    <p><strong>Age:</strong> <span id="modal-age"></span></p>
    <p><strong>Race:</strong> <span id="modal-race"></span></p>
    <p id="modal-description"></p>
  </div>
</div>
```
At the bottom, it loads the JavaScript:
```JavaScript
<script src="app.js"></script>
```
### app.js 
app.js -> frontend logic
The frontend uses this API URL:
```JavaScript
const API_URL = "https://lotr-api-gs1y.onrender.com/characters/";
```
Then it gets the HTML container:
```JavaScript
const container = document.getElementById("characters");
```
So the JavaScript knows:
-Where to get data from -> API_URL
-Where to put data -> #characters

Page load triggers character loading, this function is called:
```JavaScript
loadCharacters();
```
That means as soon as the script loads, the frontend starts fetching character data.

Inside loadCharacters(), the browser sends a request to the API:
```JavaScript
const response = await fetch(API_URL);
const characters = await response.json();
```
This means:
-Browser -> GET https://lotr-api-gs1y.onrender.com/characters/
The backend responds with a JSON list of characters.

Before adding cards, the container is cleared:
```JavaScript
container.innerHTML = "";
```
This prevents duplicate cards if the function runs again.

The frontend loops through all characters:
```JavaScript
characters.forEach((character) => {
  const card = document.createElement("article");
  card.className = "character-card";
```
For each character, it builds card HTML:
```JavaScript
card.innerHTML = `
  <img src="${character.image}" alt="${character.name}" class="character-image" />
  <div class="character-card-content">
    <h2 class="character-name">${character.name}</h2>
    <p class="character-meta"><strong>Age:</strong> ${character.age}</p>
    <p class="character-meta"><strong>Race:</strong> ${character.race}</p>
    <p class="description-preview">${character.description}</p>
    <p class="click-more">Click to read more...</p>
  </div>
`;
```
Then it inserts the card into the page:
```JavaScript
container.appendChild(card);
```
Each card gets a click event:
```JavaScript
card.addEventListener("click", () => openModal(character));
```
So when the user clicks a card:
Card click -> openModal(character)

The modal is filled using the clicked character data:
```JavaScript
modalImage.src = character.image;
modalImage.alt = character.name;
modalName.textContent = character.name;
modalAge.textContent = character.age;
modalRace.textContent = character.race;
modalDescription.innerHTML = character.description;
```
Then the modal becomes visible:
```JavaScript
modal.classList.remove("hidden");
```
The close button runs:
```JavaScript
closeModalButton.addEventListener("click", closeModal);
```
And closeModal() hides the modal again:
```JavaScript
function closeModal() {
  modal.classList.add("hidden");
}
```
The user can also close it by clicking outside the modal content:
```JavaScript
modal.addEventListener("click", (event) => {
  if (event.target === modal) {
    closeModal();
  }
});
```
### style.css 
style.css -> frontend styling
The cards are arranged in a responsive grid:
```CSS
.characters-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}
```
On bigger screens, it changes layout:
```CSS
@media (min-width: 1100px) {
  .characters-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```
The modal is hidden by default when it has the hidden class:
```CSS
.modal.hidden {
  display: none;
}
```
## 7. Deployment flow

Deployment flow is the path from local project files to the running API online.
```text
Code
  ↓
Docker setup
  ↓
FastAPI app
  ↓
PostgreSQL database
  ↓
Render deployment
  ↓
Live API URL
  ↓
Frontend fetches live data
```
1. Docker Compose defines the local deployment setup
docker-compose.yml -> runs backend + database together
The app service runs FastAPI with Uvicorn:
```YAML
web:
  build: ./project
  command: uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
  ports:
    - "8004:8000"
```
This means:
local machine port 8004 -> container port 8000
So locally, the backend is accessed through:
http://localhost:8004

2. PostgreSQL runs as a separate service
web-db -> PostgreSQL database container
```YAML
web-db:
  environment:
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
```
The backend depends on the database:
```YAML
depends_on:
  - web-db
```
So the backend expects PostgreSQL to be available before it works correctly.

3. Environment variables connect backend to database
```YAML
environment:
  - ENVIRONMENT=dev
  - TESTING=0
  - DATABASE_URL=postgres://postgres:postgres@web-db:5432/web_dev
  - DATABASE_TEST_URL=postgres://postgres:postgres@web-db:5432/web_test
```
Important part:
DATABASE_URL -> main development database
DATABASE_TEST_URL -> separate test database
This is better than hardcoding database credentials inside Python files.

4. Databases are created at startup
create.sql -> creates PostgreSQL databases
```YAML
CREATE DATABASE web_dev;
CREATE DATABASE web_test;
```
So the project has:
web_dev  -> normal app data
web_test -> test data

5. FastAPI app starts from main.py
main.py -> deployment entry point
```python
app = create_application()

init_db(app)
```
When Uvicorn runs:
```python
uvicorn app.main:app
```
it looks for:
app/main.py -> app variable

That app variable is the FastAPI application.

6. Database is registered during startup
db.py -> connects app to PostgreSQL
```python
def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
```
This makes the deployed app able to use:
```python
Character.all()
Character.filter()
character.save()
```
7. Frontend points to the deployed API
The frontend is not calling localhost. It calls the deployed Render URL:
```JavaScript
const API_URL = "https://lotr-api-gs1y.onrender.com/characters/";
```
8. Seed script populates deployed API
seed_characters.py -> uploads character data
The seed script also uses the deployed API URL by default:
```python
API_URL = os.getenv("API_URL", "https://lotr-api-gs1y.onrender.com/characters/")
```
It checks existing characters first:
```python
existing_characters = get_existing_characters()
```
Then it either updates or creates data:
```python
if existing_character:
    response = requests.put(update_url, json=character)
else:
    response = requests.post(API_URL, json=character)
```
So this script is useful after deployment because it fills the live API with character data.

## 8. Testing
Testing in this project checks if the API works correctly without needing to manually click around or send requests yourself.
The project has two main types of tests:
unit tests -> test routes with mocked CRUD/database logic
integration tests -> test routes with a real test database

1. conftest.py sets up the test app
conftest.py -> shared pytest setup
This file creates fixtures that tests can reuse.
```python
@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client
```
This fixture creates a FastAPI test client without connecting to the real database.

2. Test settings override normal settings
During tests, the app does not use normal dev settings.
It uses test settings:
```python
def get_settings_override():
    return Settings(
        environment="test",
        testing=1,
        database_url=os.environ.get("DATABASE_TEST_URL"),
    )
```
Important line:
```python
app.dependency_overrides[get_settings] = get_settings_override
```
This means:
normal config -> replaced with test config

3. test_hello.py tests the health/config route
test_hello.py -> simple endpoint test
```python
def test_hello(test_app):
    response = test_app.get("/hello")
    assert response.status_code == 200
    assert response.json() == {
        "message": "hello!",
        "environment": "test",
        "testing": True,
    }
```
This confirms:
-/hello works
-test config is loaded
-testing=True

### Unit tests
test_characters_unit.py -> mocked tests
Unit tests do not use the real database.
Instead, they replace CRUD functions with fake versions using monkeypatch.
Example: create character unit test:
 ```python
async def mock_post(payload):
    return 1

monkeypatch.setattr(crud, "post", mock_post)
```
This means:
crud.post() -> replaced with mock_post()
So when the route calls crud.post(payload), it does not actually save anything.
It just returns:
```python
1
```
Then the test checks the API response:
```python
response = test_app.post("/characters/", data=json.dumps(test_request_payload))

assert response.status_code == 201
assert response.json() == test_response_payload
```
Why monkeypatch is used?
Monkeypatch is used to fake database behavior.
Instead of this:
route -> crud.py -> real database
the test does this:
route -> fake crud function
That makes the test faster and more isolated.
The unit test is checking:
Does the route behave correctly if CRUD returns expected data?
It is not checking if PostgreSQL works.

Unit tests also check errors
Example: if crud.get() returns None, the API should return 404:
```python
async def mock_get(id):
    return None

monkeypatch.setattr(crud, "get", mock_get)

response = test_app.get("/characters/9999")
assert response.status_code == 404
assert response.json() == {"detail": "Character not found"}
```
This tests the route error handling.

### Integration tests
test_characters.py -> real database tests
Integration tests use a test database.
The fixture is:
```python
@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
```
Example: create character integration test
```python
response = test_app_with_db.post(
    "/characters/",
    data=json.dumps(
        {
            "name": "Frodo",
            "age": 50,
            "race": "Hobbit",
            "description": "Ring bearer",
            "image": "images/frodo.jpg",
        }
    ),
)

assert response.status_code == 201
assert response.json()["name"] == "Frodo"
```
This test actually goes through the real backend flow.

Example: read character integration test
First, the test creates a character:
```python
response = test_app_with_db.post(
    "/characters/",
    data=json.dumps(
        {
            "name": "Frodo",
            "age": 50,
            "race": "Hobbit",
            "description": "Ring bearer",
            "image": "images/frodo.jpg",
        }
    ),
)
character_id = response.json()["id"]
```
Then it reads that character:
```python
response = test_app_with_db.get(f"/characters/{character_id}")
assert response.status_code == 200
```
This proves:
-POST saves data
-GET can retrieve saved data
-database flow works

### Validation tests
The tests also check bad input.
Example: empty JSON body:
```python
response = test_app.post("/characters/", data=json.dumps({}))
assert response.status_code == 422
```
Why 422?
Because Pydantic expects:
```txt
name
age
race
description
image
```
If fields are missing, FastAPI rejects the request before CRUD/database logic runs.

### Parametrized tests
The project uses pytest.mark.parametrize to test many invalid update cases without writing separate test functions.
```python
@pytest.mark.parametrize(
    "character_id, payload, status_code, detail",
    [
        (9999, VALID_CHARACTER, 404, "Character not found"),
        (0, VALID_CHARACTER, 422, [...]),
        (1, {}, 422, [...]),
    ],
)
```
This is cleaner than writing eight almost identical tests.
It checks cases like:
-nonexistent id -> 404
-id = 0 -> 422
-missing name -> 422
-missing age -> 422
-missing race -> 422
-missing description -> 422
-missing image -> 422

