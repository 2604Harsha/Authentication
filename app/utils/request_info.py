from fastapi import Request

def get_client_ip(request: Request) -> str:
    # Works behind proxies too
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.client.host


def get_user_agent(request: Request) -> str:
    return request.headers.get("user-agent")