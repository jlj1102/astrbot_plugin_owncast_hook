import httpx
import asyncio
from apimain import getapi

async def main():
    data = await getapi.ocstat("http://192.168.1.69:8080", "4a5uaBZALRKmDVqF6EdLiIMkLNOW3uL-myCuLWFO01A=")
    print(data)

if __name__ == "__main__":
    asyncio.run(main())