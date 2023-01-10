import re
import json

with open("index.html", "r", encoding="utf-8") as f:
    data = f.read()

partials = re.findall("({{)(.*)(}})", data)
for partial in partials:
    lines_of_html = ""
    partial_values = partial[1].strip().split(" ")
    print(partial_values)

    with open("templates/partials/" + partial_values[0] + ".html", "r", encoding="utf-8") as p:
        partial_html_code = p.read()
        
    with open("articles.json", "r", encoding="utf-8") as art:
        payload = json.load(art)
        sorted_data = {k: v for k, v in sorted(payload.items(), 
                            key=lambda item: item[1]["date"], reverse=True)}
        print(len(sorted_data))
    
    match partial_values[1]:
        case "all":
            for item in sorted_data:
                temp = partial_html_code
                variables = re.findall("({{=)(.*?)(}})", partial_html_code)
                for touple in variables:
                    # tag_name
                    key = touple[1].strip()
                    if key == "page":
                        temp_var = item
                    else:
                        temp_var = payload[item][key]
                    temp = temp.replace(touple[0] + touple[1] + touple[2], temp_var)
                lines_of_html += temp + "\n"
        case other:
            total = len(sorted_data)
            count = int(partial_values[1])
            if total < count:
                count = total
            for item in sorted_data:
                if count == 0:
                    break
                temp = partial_html_code
                variables = re.findall("({{=)(.*?)(}})", partial_html_code)
                for touple in variables:
                    # tag_name
                    key = touple[1].strip()
                    if key == "page":
                        temp_var = item
                    else:
                        temp_var = payload[item][key]
                    temp = temp.replace(touple[0] + touple[1] + touple[2], temp_var)
                lines_of_html += temp + "\n"
                count -= 1
    #print(partial)
    data = data.replace(partial[0] + partial[1] + partial[2], lines_of_html)

print(data)
#with open("index.html", "w", encoding="utf-8") as f:
    #f.write(data)