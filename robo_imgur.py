from imgurpython import ImgurClient

client_id = '739f573e90420d1'
client_secret = '4ba2601847acdfeedb6d9bf6cba81ec456c3dda3'

client = ImgurClient(client_id, client_secret)

# Example request
items = client.gallery()
for item in items:
    print(item.link)