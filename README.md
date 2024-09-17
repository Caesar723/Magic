# Magic-Fan-Made

https://github.com/Caesar723/Magic/assets/76422688/1b1334d8-efcb-4a2d-b21e-675b05e6f39b




Magic-Fan-Made is a card game that combines elements of Magic: The Gathering and Hearthstone, closely resembling Magic: The Gathering but with some unique differences.

## How to Set Up the Development Environment

### Using Docker

1. **Pull the Docker Image:**
   ```bash
   docker pull registry.cn-shanghai.aliyuncs.com/magic_fan_made/develop_env_ubuntu:latest
   ```

2. **Run the Docker Container:**
   ```bash
   docker run -d --shm-size=4096m -p 1201:6901 -p 8000:8000 \
   --name cloud -e VNC_PW=cloud1234 registry.cn-shanghai.aliyuncs.com/magic_fan_made/develop_env_ubuntu
   ```
   - `-d`: Run the container in detached mode.
   - `--shm-size=4096m`: Allocate 4096 MB of shared memory.
   - `-p 1201:6901`: Map port 6901 inside the container to port 1201 on the host.
   - `-p 8000:8000`: Map port 8000 inside the container to port 8000 on the host.
   - `--name cloud`: Assign the name 'cloud' to the container.
   - `-e VNC_PW=cloud1234`: Set the VNC password to 'cloud1234'.

### Accessing the Development Environment

- Navigate to [https://0.0.0.0:1201](https://0.0.0.0:1201)
  - **Username:** `kasm_user`
  - **Password:** `cloud1234`

Once inside the Ubuntu development environment, open a terminal and execute the following commands to start the server:
```bash
bash custom_startup.sh
bash init.sh
```

## How to View the Technical Documentation

For technical documentation, visit: [https://www.xuanpei-chen.top:8000/tech_doc](https://www.xuanpei-chen.top:8000/tech_doc)
