# [Gradient Unoffical Docker](https://github.com/hotrungnhan/gradient-unoffical-docker) 

## [Support me by register account with REF, thanks you !!!](https://app.gradient.network/signup?code=YTZLI2)
# Setup
1. [Download Docker Desktop](https://www.docker.com/products/docker-desktop).
2. Login to [Gradient](https://app.gradient.network/).
3. Download Extensions and start a node.
4. Replace `EMAIL` with your email, `PASSWORD` with your password.
5. Open CMD and use the Docker Run command of the built image from Docker Hub.
6. Check and Manage the app from Docker Desktop > Containers.
7. If you're container stuck at any step, please verify your credential.
# Usage Options
## A) Use built image from [Docker Hub](https://hub.docker.com/r/hotrungnhan/gradient-sentry)
#### Docker Compose
```
services:
  gradient-sentry:
    image: hotrungnhan/gradient-sentry
    restart: unless-stopped
    pull_policy: always
    environment:
      - EMAIL=your_key
      - PASSWORD=your_key
```
## B) Docker Run
```
docker run -d \
  --restart unless-stopped \
  --pull always \
  -e EMAIL="your_key" \
  -e PASSWORD="your_key" \
  hotrungnhan/gradient-sentry
```

# Credit 
* [Kellphy](https://github.com/Kellphy)
* * [MRColorR](https://github.com/MRColorR)
