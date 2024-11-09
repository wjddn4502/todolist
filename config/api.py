from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request, name: str):
    return {"message": f"Hello {name}"}

