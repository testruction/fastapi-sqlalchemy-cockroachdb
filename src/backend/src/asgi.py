# -*- coding: utf-8 -*-
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

from backendservice.app import create_app

app = create_app()

if __name__ == "__main__":
    asyncio.run(serve(app, Config()))
