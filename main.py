
import asyncio
import getpass
from nio import AsyncClient, MatrixRoom, RoomMessageText ,RoomMessage, RoomMessageNotice, RoomMessagesResponse

async def cb_print_messages(self, room: MatrixRoom, event: RoomMessageText):
        """Callback to print all received messages to stdout.

        Arguments:
            room {MatrixRoom} -- Provided by nio
            event {RoomMessageText} -- Provided by nio
        """
        if event.decrypted:
            encrypted_symbol = "🛡 "
        else:
            encrypted_symbol = "⚠️ "
        print(
            f"{room.display_name} |{encrypted_symbol}| {room.user_name(event.sender)}: {event.body}"
        )
        
async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    print(
        f"Message received in room {room.display_name}\n"
        f"{room.user_name(event.sender)} | {event.body}"
    )
    
    
async def login_and_sync( homeserver_url, username, password):
    # Create an AsyncClient instance
    client = AsyncClient(homeserver=homeserver_url,user="nikreed",ssl=False)
    client.add_event_callback(message_callback, RoomMessageText)

    password = "dsfai48**92"
    login_response = await client.login( password)
    
    # Check if login was successful
    if login_response:
        print(f"Logged in as {username}")
    else:
        print("Login failed.")
        return

    print("RESONSE:",login_response)
    # Sync with the server
    try :
        # await client.sync()
        await client.sync()
    except :
        print("****ERROR*****")
        await client.close()
        return
    print("done")
    # Do something with the client, such as joining a room or sending messages
    # Example: Join a room and print messages
    ROOM_ID = room_id = "!lIppryFduYlBdEdKzn:aria-net.org" #input("Enter the room ID to join: ")
    room = await client.join(room_id)
    print("room:",room)
    room = client.rooms[ROOM_ID]
    print(f"Room {room.name} is encrypted: {room.encrypted}")
    # Print messages in the room
    
    # Keep the script running until user stops it
    while True:
        await client.sync()
        msg = input("Enter a message")
        resp = await client.room_send(
    # Watch out! If you join an old room you'll see lots of old messages
            room_id=room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": msg},
    )
        await client.sync()
        pass

    # Remember to gracefully close the client when done
    await client.close()

# Get user credentials
homeserver_url = "https://aria.im" #@nikreedog:aria-net.org input("Enter the Matrix homeserver URL: ")
username = "nikreed"
#"#input("Enter your Matrix username: ")
# password = getpass.getpass("Enter your Matrix password: ")
# Get user credentials

password = "dsfai48**92" #getpass.getpass("Enter your Matrix password: ")

    # Login with the provided credentials
# Run the login and sync function

asyncio.get_event_loop().run_until_complete(login_and_sync(homeserver_url, username, password))
exit()
