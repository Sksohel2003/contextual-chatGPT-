from main import handle_query
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    """
    Handle incoming messages from the Chainlit interface and provide streaming responses.
    """
    user_message = message.content  # Get the user's message from the Chainlit interface
    msg = cl.Message(content="")

    resp = handle_query(user_message)
    print(resp)
    for chunk in resp.response_gen:
        # await cl.Message(content=chunk).send()
        await msg.stream_token(chunk)
    await msg.update()
    
    # while not resp.is_done:
    #     pass
    # # Call your handle_query method to get the streaming response
    # await cl.Message(content=resp.response).send()
