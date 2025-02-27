# browser-use Docker Container

This repository provides a Docker setup for running [browser-use](https://github.com/browser-use/browser-use) inside a container. The container provides VNC access for debugging.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Using

Create docker-compose.yml file:

```yaml
services:
  browser-use-api:
    build: .
    container_name: browser-use-api
    env_file:
      - .env
    volumes:
      - .:/app
    ports:
      - '5000:5000'
      - '5900:5900'
    extra_hosts:
      - 'host.docker.internal:host-gateway'
```

Run the container:

```sh
docker compose up
```

Access the container shell to manually run scripts inside the container:

```sh
docker compose exec browser-use bash
```

Run `browser-use` inside the container:

```sh
python gpt-demo.py
```

## Connect via VNC

Use any VNC client and connect to:

```
localhost:5900
```

Password: `secret`

## Connecting to Local Ollama

If you're running Ollama on your host machine, add the `extra_hosts` configuration as shown above. This allows the container to connect to Ollama using `host.docker.internal:11434` as the host address.

```
    ...
    extra_hosts:
      - 'host.docker.internal:host-gateway'    # Required for connecting to Ollama running on host machine
```

## Stopping the Container

To stop the running container:

```sh
docker compose down
```

## License

This project is open-source and licensed under the MIT License.
