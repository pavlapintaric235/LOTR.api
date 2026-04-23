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
