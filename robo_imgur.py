from imgurpython import ImgurClient

client_id = '739f573e90420d1'
client_secret = '4ba2601847acdfeedb6d9bf6cba81ec456c3dda3'

client = ImgurClient(client_id, client_secret)

# Example request
tag = "cat"
items = client.gallery_tag(tag, sort='viral', page=0, window='week')
print type(items)
print items.data
