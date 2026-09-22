def main():
    import uvicorn
    from pathlib import Path
    from sqlalchemy.exc import OperationalError
    from database import ensure_database_schema

    for attempt in range(30):
        try:
            ensure_database_schema()
            print("Database schema is ready.")
            break
        except OperationalError:
            if attempt == 29:
                raise
            import time
            time.sleep(1)

    ip_address = get_local_ip()
    print(ip_address)
    ip_address="172.20.10.7"
    ip_address="0.0.0.0"
    #ip_address="localhost"
    uvicorn.run(
        "server:app",
        host=ip_address,
        port=443,
        ssl_keyfile=Path("/app/tls/magic-ip.key"),
        ssl_certfile=Path("/app/tls/magic-ip.crt"),
        reload=False,
        reload_dirs=["src", "!src/user_cache"]
    )
def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 使用Google的公共DNS服务器来确定本地IP地址
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip
if __name__=="__main__":
    
    main()
    
