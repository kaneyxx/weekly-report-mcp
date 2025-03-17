#!/usr/bin/env python3
"""
Example script demonstrating how to use the Weekly Report Checker MCP server as a client.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.main"],
    )

    print("Connecting to Weekly Report Checker MCP server...")
    
    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            print("Connected to server!")
            
            # Get missing reports
            print("\n--- Missing Reports ---")
            status, _ = await session.read_resource("weekly-report://status")
            print(status)
            
            # Get statistics
            print("\n--- Report Statistics ---")
            stats, _ = await session.read_resource("weekly-report://stats")
            print(stats)
            
            # Get all members
            print("\n--- All Members ---")
            members, _ = await session.read_resource("weekly-report://all-members")
            print(members)
            
            # Check a specific person
            name = "陳冠宇"  # Replace with an actual name
            print(f"\n--- Status for {name} ---")
            person_status, _ = await session.read_resource(f"weekly-report://person/{name}")
            print(person_status)

if __name__ == "__main__":
    asyncio.run(main())