import pathlib

file_path = pathlib.Path(r'd:\coding\For antigravity\chat kara\templates\marketplace\caterer_list.html')
content = file_path.read_text('utf-8')

# Fix city filter
content = content.replace('request_GET.city==city', 'request_GET.city == city')
# Fix category filter
content = content.replace('request_GET.category==cat.id|stringformat:"s"', 'request_GET.category == cat.id|stringformat:"s"')
# Fix sort filters
content = content.replace("request_GET.sort=='newest'", "request_GET.sort == 'newest'")
content = content.replace("request_GET.sort=='price_asc'", "request_GET.sort == 'price_asc'")
content = content.replace("request_GET.sort=='price_desc'", "request_GET.sort == 'price_desc'")

file_path.write_text(content, 'utf-8')
print("Successfully replaced formatting in HTML.")
