# What the Name!
## For user
Enter into this [URL](https://www.whathename.com)

## For dev
### Web up
To force all the new data will be reloaded, use
```
docker-compose up --build
```
or
```
docker-compose up --build frontend
docker-compose up --build backend
```
if you will need just refresh a microservice

---

If anything has been changed, 
```
docker-compose up
```
or 
```
docker-compose up frontend
docker-compose up backend
```

### Web down
Use this
```
docker-compose down 
```
or
```
docker-compose down frontend
docker-compose down backend
```

### What is next
 - [ ] Upload the web to internet
 - [ ] Create a screen changer to prevent backend to be completely prepared
 - [ ] Add option to select continent instead of just country