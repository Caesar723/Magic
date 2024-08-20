def main():
    import uvicorn
    ip_address = get_local_ip()
    #print(ip_address)
    #ip_address="10.208.15.84"
    ip_address="0.0.0.0"
    #ip_address="localhost"
    uvicorn.run(
        "server:app",
        host=ip_address,
        port=443,
        ssl_keyfile="src/xuanpei-chen.top_ssh/xuanpei-chen.top.key",
        ssl_certfile="src/xuanpei-chen.top_ssh/xuanpei-chen.top_public.crt",
        ssl_ca_certs="src/xuanpei-chen.top_ssh/xuanpei-chen.top_chain.crt",
        reload=True
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
    #print(get_local_ip())
    main()
    
