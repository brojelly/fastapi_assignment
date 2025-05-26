# main.py

from typing import Annotated

from fastapi import FastAPI, Path, HTTPException, Query

from app.models.movies import MovieModel
from app.models.users import UserModel
from app.schemas.movies import MovieResponse, CreateMovieRequest, MovieSearchParams, MovieUpdateRequest
from app.schemas.users import UserCreatRequest, UserUpdateRequest, UserSearchParams

app = FastAPI()

@app.post("/users")
async def create_user(data: UserCreatRequest):
    user = UserModel.create(**data.dict())
    return user.id

@app.get("/users")
async def get_all_users():
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@app.get("/users/{user_id}")
async def get_user(user_id:int = Path(gt = 0)):
    user = UserModel.get(id = user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}")
async def update_user(data: UserUpdateRequest, user_id:int = Path(gt = 0)):
    user = UserModel.get(id = user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.update(**data.model_dump())
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id:int = Path(gt = 0)):
    user = UserModel.get(id = user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"detail": f"User:{user_id}, deleted"}

@app.get('/users/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404)
    return filtered_users


@app.get('/movies', response_model=list[MovieResponse], status_code=200)
async def get_movies(query_params: Annotated[MovieSearchParams, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}

    if valid_query:
        return MovieModel.filter(**valid_query)

    return MovieModel.all()

@app.post('/movies', response_model=MovieResponse, status_code=201)
async def create_movie(data: CreateMovieRequest):
	movie = MovieModel.create(**data.model_dump())
	return movie

@app.get('/movies/{movie_id}', response_model=MovieResponse, status_code=200)
async def get_movie(movie_id: int = Path(gt=0)):
	movie = MovieModel.get(id=movie_id)
	if movie is None:
		raise HTTPException(status_code=404)
	return movie

@app.patch('/movies/{movie_id}', response_model=MovieResponse, status_code=200)
async def edit_movie(data: MovieUpdateRequest, movie_id: int = Path(gt=0)):
	movie = MovieModel.get(id=movie_id)
	if movie is None:
		raise HTTPException(status_code=404)
	movie.update(**data.model_dump())
	return movie

@app.delete('/movies/{movie_id}', status_code=204)
async def delete_movie(movie_id: int = Path(gt=0)):
	movie = MovieModel.get(id=movie_id)
	if movie is None:
		raise HTTPException(status_code=404)
	movie.delete()
	return


UserModel.create_dummy()
MovieModel.create_dummy()
# API 테스트를 위한 더미를 생성하는 메서드 입니다.

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
