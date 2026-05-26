from dataclasses import dataclass


@dataclass(frozen=True)
class EndpointAPI:
    new_chat: str = "/api/v2/chats/new"
    completions: str = "/api/v2/chat/completions"
    completed: str = "/api/chat/completed"
    suggestions: str = "/api/task/suggestions/completions"
    upload_file: str = "/api/v2/files/getstsToken"
