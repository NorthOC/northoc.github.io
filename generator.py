""" json parses .json files, which contain data"""
import json
import re
import unicodedata
import os
from pathlib import Path

# parse json file
def parse_json_file(config_filepath):
    """returns the contents of a .json file\n
    structure of json objects:\n
    output.html{
        base: "path to base template"
        head: "path to head template",
        body: "path to body template",
        content: "path to content",
    }
    """
    with open(config_filepath, 'r', encoding="utf-8") as file:
        defaults = json.load(file) 

    params = {}

    #combining each
    for data_filepath in defaults:
        with open(data_filepath, 'r', encoding="utf-8") as file:
            data = json.load(file)
        defaults[data_filepath]["pages"] = data

    for data_filepath in defaults:
        pages = defaults[data_filepath]["pages"]
        for item in pages:
            with open(pages[item]["content"], 'r', encoding='utf-8') as f:
                    lines = f.read()
            # Sets title param from h1 if title is not specifiend in json file
            if 'title' not in pages[item]:
                title = re.search("^# (.*)", lines, re.MULTILINE)
                if title is not None:
                    pages[item]['title'] = title.group(1)
                else:
                    pages[item]['title'] = "Untitled Document"

            # Sets og-img param with first image in md document
            if 'og-img' not in pages[item]:
                og_img = re.search(r"!\[(.*?)\]\((.*?)\)", lines)
                if og_img is not None:
                    pages[item]['og-img'] = og_img.group(2)
                else:
                    pages[item]['og-img'] = ""

            # Sets the default base, body and head templates
            if 'base' not in pages[item]:
                pages[item]['base'] = defaults[data_filepath]['base']
            if 'body' not in pages[item]:
                pages[item]['body'] = defaults[data_filepath]['body']
            if 'head' not in pages[item]:
                pages[item]['head'] = defaults[data_filepath]['head']
        params.update(pages)
    #print(params)
    return params

# static site generator
def generate_html(params, cwd=os.path.abspath(os.getcwd()) + os.sep):
    """the engine that generates the page"""

    #cleanup previously indexed files
    if (Path.is_file(Path("config/" + "indexer.txt"))):
        cleanup()
    # used for generated html deletion
    indexer_blob = ""

    # json file generated key value pairs
    for page in params:

        # templates specified in json file
        head_template = params[page]["head"]
        body_template = params[page]["body"]

        # these variables will hold the output of each filled out html template
        head_blob = ''
        body_blob = ''
        # generate meta desc for seo purposes if desc or
        # description key is not specified in json file
        if "desc" in params[page] or "description" in params[page]:
            auto_description = False
        else:
            auto_description = True

        # CLI indicator verbose
        #print(f"CREATE {page} FROM [{head_template}, {body_template}] WITH", end=' ')
        print(f"CREATE {page} WITH", end=' ')

        # generate body section
        with open(body_template, 'r', encoding="utf-8") as body:
            # html template
            body = body.read()

        # string literal variables
        to_fill_out = re.findall('({{=)(.*?)(}})', body)
        for touple in to_fill_out:
            # tag_name
            key = touple[1].strip()
            body = body.replace(touple[0] + touple[1] + touple[2], params[page][key])

        # in a template, there should only be one {{ content }} variable
        to_fill_out = re.findall('({{)(.*?)(}})', body)

        for touple in to_fill_out:
            key = touple[1].strip()
            contents = params[page][key]
            print(contents, end=' ')
            # markdown party
            generated_html = md_to_web(contents, params[page])
            body = body.replace(touple[0] + touple[1] + touple[2], generated_html)
            # generate auto description
            if auto_description:
                sanitized_desc = generate_desc(generated_html)
            
        # file partial management
        file_partials = re.findall("({{)([^=].*)(}})", body)
        for partial in file_partials:
            lines_of_html = ""
            partial_values = partial[1].strip().split(" ")
            directory = os.getcwd() + os.sep + partial_values[2]
            #print(partial_values)
            
            if len(partial_values) == 1:
                continue

            with open(Path(cwd + "templates/partials/" + partial_values[0] + ".html"), "r", encoding="utf-8") as p:
                partial_html_code = p.read()
            
            with open(Path(cwd + partial_values[2]), "r", encoding="utf-8") as articles:
                payload = json.load(articles)
                #print(payload)
            sorted_data = {k: v for k, v in sorted(payload.items(),
                                    key=lambda item: item[1]["date"], reverse=True)}
                #print(sorted_data)
            
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
                                temp_var = params[item][key]
                            temp = temp.replace(touple[0] + touple[1] + touple[2], temp_var)
                        lines_of_html += temp + "\n"
                case _:
                    total = len(sorted_data)
                    #print(partial_values)
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
                                temp_var = params[item][key]
                            temp = temp.replace(touple[0] + touple[1] + touple[2], temp_var)
                        lines_of_html += temp + "\n"
                        count -= 1
            #print(partial)
            body = body.replace(partial[0] + partial[1] + partial[2], lines_of_html)

        #directory partial management
        dir_partials = re.findall("({{=)(.*)(}})", body)
        for partial in dir_partials:
            lines_of_html = ""
            partial_values = partial[1].strip().split(" ")
            directory = os.getcwd() + os.sep + partial_values[2]
            #print(partial_values)

            if len(partial_values) == 1:
                continue
            
            if not os.path.isdir(directory):
                continue

            with open(Path(cwd + "templates/partials/" + partial_values[0] + ".html"), "r", encoding="utf-8") as p:
                partial_html_code = p.read()

            files_in_dir = os.listdir(directory)
            #print(files_in_dir)

            match partial_values[1]:
                case "all":
                    for item in files_in_dir:
                        temp = partial_html_code
                        variables = re.findall("({{=)(.*?)(}})", partial_html_code)
                        for touple in variables:
                            temp_var = partial_values[2] + os.sep + item
                            temp = temp.replace(touple[0] + touple[1] + touple[2], temp_var)
                        lines_of_html += temp + "\n"
                case _:
                    total = len(sorted_data)
                    #print(partial_values)
                    count = int(partial_values[1])
                    if total < count:
                        count = total
                    for item in sorted_data:
                        if count == 0:
                            break
                        temp = partial_html_code
                        variables = re.findall("({{=)(.*?)(}})", partial_html_code)
                        for touple in variables:
                            temp_var = partial_values[2] + os.sep + item
                            temp = temp.replace(touple[0] + touple[1] + touple[2], temp_var)
                        lines_of_html += temp + "\n"
                        count -= 1
            #print(partial)
            body = body.replace(partial[0] + partial[1] + partial[2], lines_of_html) 


            # final html_body generated
        body_blob = body
            #print(body_blob)

        # generate head template
        with open(head_template, 'r', encoding="utf-8") as head:

            head = head.read()

            to_fill_out = re.findall('({{=)(.*?)(}})', head)

            # (%=)(tag_name)(%)
            for touple in to_fill_out:

                # tag_name
                key = touple[1].strip()
                head = head.replace(touple[0] + touple[1] + touple[2], params[page][key])

            #print(head)

            head_lines = head.split("\n")

            # auto generate  meta description if desc or
            # description key not specified in json (for seo)
            if auto_description:
                desc_tag = f"    <meta name=\"description\" content=\"{sanitized_desc}\">"
                head_lines.insert(-1, desc_tag)

            # final head
            head_blob = "\n".join(head_lines)
            #print(head_blob)

        # create subdirectories
        

        # read the base template blob
        with open(Path(cwd + params[page]["base"]), 'r', encoding="utf-8") as base:
            base_blob = base.read()

            to_fill_out = re.findall('({{=)(.*?)(}})', base_blob)

            for touple in to_fill_out:

                key = touple[1].strip()
                base_blob = base_blob.replace(touple[0] + touple[1] + touple[2], params[page][key])

            to_fill_out = re.findall('({{)(.*?)(}})', base_blob)

            for touple in to_fill_out:

                key = touple[1].strip()
                match key:
                    case "head":
                        base_blob = base_blob.replace(touple[0] + touple[1] + touple[2], head_blob)
                    case "body":
                        base_blob = base_blob.replace(touple[0] + touple[1] + touple[2], body_blob)

        # creates an index page if a page slug does not contain .html
        if ".html" not in page:
            page = page + os.sep + "index.html"
        
                #print(page)
        #os.makedirs(os.path.dirname(cwd + page), exist_ok=True)
        Path(cwd + page).parent.mkdir(exist_ok=True, parents=True)

        # write head and body blobs to file
        with open(Path(cwd + page), 'w+', encoding="utf-8") as result:
            result.write(base_blob)

        if not auto_description:
            print("(MANUAL DESCRIPTION!)", end=" ")
        print("...done!")

        # add created page path to indexer blob
        indexer_blob += str(Path(page)) + "\n"

        # prettify for readability
        look_good_html(page)

    write_to_indexer(indexer_blob)

def md_to_web(md_file, page_params):
    """takes a .md file and returns a compiled HTML string"""

    with open(md_file, 'r', encoding="utf-8") as file:
        data = file.read()

    #process string literal variables
    to_fill_out = re.findall('({{=)(.*?)(}})', data)

    for touple in to_fill_out:
        # tag_name
        key = touple[1].strip()
        data = data.replace(touple[0] + touple[1] + touple[2], page_params[key])

    h_tags = [["# ", "h1"], ["## ", "h2"],
    ["### ", "h3"], ["#### ", "h4"], ["##### ", "h5"], ["###### ", "h6"]]

    # process images
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", data)

    for touple in images:
        md_tag = f"![{touple[0]}]({touple[1]})"
        image_tag = f"<figure>\n<img src=\"{touple[1]}\" \
alt=\"{touple[0]}\"/>\n<figcaption>{touple[0]}</figcaption>\n</figure>"

        data = data.replace(md_tag, image_tag)

    # process links
    links = re.findall(r"\n\[(.*?)\]\((.*?)\)\n", data)
    #print(links)
    for touple in links:
        md_tag = f"[{touple[0]}]({touple[1]})"
        if touple[1].startswith('http'):
            link_tag = f"<a target='_blank' href=\"{touple[1]}\">{touple[0]}</a>"
        else:
            link_tag = f"<a href=\"{touple[1]}\">{touple[0]}</a>"
        data = data.replace(md_tag, link_tag)
    
    # process code blocks
    blocks = re.findall(r"(```)(.*)(\n)([\s\S]*?)(```)", data)
    for touple in blocks:
        # escape html
        temp = touple[3].replace("&", "&amp;").replace("<", "&lt;")\
                .replace(">", "&gt;").replace("\"", "&quot;").replace("\'", "&#39;").split("\n")
        temp.pop()
        # wrap each line in pre tags
        codeblock = ""
        for item in temp:
            if item.startswith("//") or item.startswith("#"):
                item = "<span class=\"comment\">" + item + "</span>"
            codeblock += "<pre>" + item + "</pre>\n"
        lang = touple[1].strip()
        if len(lang) > 0:
            codeblock = f"<code class=\"code-block {lang}\">\n" + codeblock + "</code>"
        else:
            codeblock = "<code class=\"code-block\">\n" + codeblock + "</code>"

        md_tag = f"{touple[0]}{touple[1]}{touple[2]}{touple[3]}{touple[4]}"
        data = data.replace(md_tag, codeblock)


    data = data.split("\n\n")
    #print (data)
    for line in data:

        # html code
        if line.startswith("<"):
            pass

        elif line.startswith("{{"):
            pass

        # ordered lists
        elif line.startswith("1. "):
            new_list = []
            new_string = ""
            current_depth = 0
            prev_depth = 0

            # single line contains full list
            listing = line.split("\n")
            new_list.append("<ol>")
            for item in listing:
                item = re.findall(r"\d\. (.*)", item)
                new_list.append(f"\n<li>{item[0]}</li>\n")
            # list end
            new_list.append("</ol>")

            # replace markdown with html
            for thing in new_list:
                new_string += thing
            data[data.index(line)] = new_string

        # Unordered list
        elif line.startswith("* "):
            temp = line.split("\n")
            new_list = []
            started = False
            new_string = ""
            current_depth = 0
            prev_depth = 0
            for item in temp:
                ul_list = re.findall(r"^(\s*?)(\* )(.*)", item)
                current_depth = len(ul_list[0][0])
                if not started and prev_depth == 0 and len(ul_list[0][0]) == 0:
                    new_list.append(f"<ul>\n<li>{ul_list[0][2]}</li>\n")
                    started = True
                elif current_depth > prev_depth:
                    new_list.append(f"<ul>\n<li>{ul_list[0][2]}</li>\n")
                elif current_depth < prev_depth:
                    last_item = str(new_list.pop())
                    last_item = last_item + "</ul>\n"
                    new_list.append(last_item)                
                    new_list.append(f"<li>{ul_list[0][2]}</li>\n")
                else:
                    new_list.append(f"<li>{ul_list[0][2]}</li>\n")
                prev_depth = current_depth
            new_list.append("</ul>")
            for thing in new_list:
                new_string += thing
            data[data.index(line)] = new_string

        # headings
        elif line.startswith("#"):
            for i, _h_tag in enumerate(h_tags):
                # remove all h1 tags for SEO and because it is in params[title]
                if line.startswith(h_tags[i][0]):
                    index = data.index(line)
                    if h_tags[i][0] == h_tags[0][0]:
                        data[index] = ''
                        break
                    else:
                        #create heading id for on-page link bookmarks
                        id_heading = line[len(h_tags[i][0]):].lower()
                        normalized = unicodedata.normalize('NFD', id_heading)
                        decoded = "".join([c for c in normalized if not unicodedata.combining(c)])
                        h_id = re.sub(r"[^a-zA-Z0-9]+", ' ', decoded).strip().replace(" ", "_")

                        html_open_tag = "<" + h_tags[i][1] + f" id=\"{h_id}\">"
                        html_close_tag = "</" + h_tags[i][1] + ">"
                        line = line.replace(h_tags[i][0], html_open_tag, 1) + html_close_tag
                        data[index] = line
                        break

        # inline and p tags
        else:
            temp = line

            # bold_italic
            bold_italic = re.findall(r"(\*\*\*)(.*?)(\*\*\*)", temp)

            if len(bold_italic) != 0:
                for touple in bold_italic:
                    temp = temp.replace(\
                        touple[0] + touple[1] + touple[2], f"<strong><em>{touple[1]}</em></strong>")

            # bold
            bold = re.findall(r"(\*\*)(.*?)(\*\*)", temp)

            if len(bold) != 0:
                for touple in bold:
                    temp = temp.replace(\
                        touple[0] + touple[1] + touple[2], f"<strong>{touple[1]}</strong>")
            # italic
            italic = re.findall(r"(\*)(.*?)(\*)", temp)

            if len(italic) != 0:
                for touple in italic:
                    temp = temp.replace(\
                        touple[0] + touple[1] + touple[2], f"<em>{touple[1]}</em>")
            # strikethrough
            strikethrough = re.findall("(~~)(.*?)(~~)", temp)

            if len(strikethrough) != 0:
                for touple in strikethrough:
                    temp = temp.replace(\
                        touple[0] + touple[1] + touple[2], f"<s>{touple[1]}</s>")
            # code
            inline_code = re.findall("(`)([^`]{1}.*?)(`)", temp)

            if len(inline_code) != 0:
                for touple in inline_code:
                    temp = temp.replace(\
                        touple[0] + touple[1] + touple[2], f"<code>{touple[1]}</code>")

            data[data.index(line)] = f"<p>{temp}</p>"

    data_string = ''

    for item in data:
        if item not in ('<p></p>', ''):
            # inline links
            links = re.findall(r"\[(.*?)\]\((.*?)\)", item)
            #print(links)
            for touple in links:
                md_tag = f"[{touple[0]}]({touple[1]})"
                if touple[1].startswith('http'):
                    link_tag = f"<a target='_blank' href=\"{touple[1]}\">{touple[0]}</a>"
                else:
                    link_tag = f"<a href=\"{touple[1]}\">{touple[0]}</a>"
                item = item.replace(md_tag, link_tag)
            
            # inline code
            inline_code = re.findall("(`)([^`]{1}.*?)(`)", item)
            for touple in inline_code:
                md_tag = touple[0] + touple[1] + touple[2]
                code_tag = f"<code>{touple[1]}</code>"
                item = item.replace(md_tag, code_tag)
            
                        # bold_italic
            bold_italic = re.findall(r"(\*\*\*)(.*?)(\*\*\*)", item)

            if len(bold_italic) != 0:
                for touple in bold_italic:
                    item = item.replace(\
                        touple[0] + touple[1] + touple[2], f"<strong><em>{touple[1]}</em></strong>")

            # bold
            bold = re.findall(r"(\*\*)(.*?)(\*\*)", item)

            if len(bold) != 0:
                for touple in bold:
                    item = item.replace(\
                        touple[0] + touple[1] + touple[2], f"<strong>{touple[1]}</strong>")
            # italic
            italic = re.findall(r"(\*)(.*?)(\*)", item)

            if len(italic) != 0:
                for touple in italic:
                    item = item.replace(\
                        touple[0] + touple[1] + touple[2], f"<em>{touple[1]}</em>")
            # strikethrough
            strikethrough = re.findall("(~~)(.*?)(~~)", item)

            if len(strikethrough) != 0:
                for touple in strikethrough:
                    item = item.replace(\
                        touple[0] + touple[1] + touple[2], f"<s>{touple[1]}</s>")

            data_string += item + "\n"
    #print(data_string)
    return data_string 

# prettifier
def look_good_html(page, cwd=os.path.abspath(os.getcwd()) + os.sep, spaces = 2):
    '''beautifies the generated html. the spaces arg intents each level by that many spaces.'''

    # specify tags that don't require indentation
    no_indent = ["meta", "link", "img"]
    depth = 0
    indent = ' ' * spaces
    data = ''
    # read page
    with open(Path(cwd + page), 'r', encoding="utf-8") as f:
        data = f.read().split("\n")

    # rewrite page
    with open(Path(cwd + page), 'w', encoding="utf-8") as f:
        for line in data:
            if line != '':
                line = line.strip()
                # find all tags
                #<[^\/].*?>|\/>
                open_tag = re.findall(r"<[^!\/ ]*?>|<[^!\/].*? ", line)
                close_tag = re.findall(r"<\/.*?>|\/>", line)
                if len(open_tag) != 0:
                    #print(depth, open_tag, close_tag)
                    f.write(f"{indent * depth}{line}\n")

                    # check if the tag should be indented and there is a closing tag for it
                    if open_tag[0][1: -1] not in no_indent and len(close_tag) == 0:
                        depth += 1
                elif len(close_tag) != 0:
                    depth -= 1
                    #print(depth, open_tag, close_tag)
                    f.write(f"{indent * depth}{line}\n")
                else:
                    f.write(f"{indent * depth}{line}\n")

# generate meta description
def generate_desc(body_blob):
    """generates automatic meta description"""
    inner_html = re.sub(r"<h[0-9].*>*<\/h[0-9]>|<figcaption>[^<]*<\/figcaption>|<[^>]*>", "", body_blob)
    inner_html = re.sub(r'\s+',' ',inner_html)
    inner_html = re.sub(r"\"|\'", "", inner_html)
    inner_html = (inner_html[:155] + '...') if len(inner_html) > 155 else inner_html
    return inner_html.strip()

def write_to_indexer(indexer_blob):
    with open(Path("config/indexer.txt"), "w", encoding="utf-8") as f:
        f.write(indexer_blob)

def cleanup ():
    with open(Path("config/indexer.txt"), "r", encoding="utf-8") as f:
        indexed_files = f.read().strip().split("\n")
    for file in indexed_files:
        os.remove(file)
        if len(file.split(os.sep)) > 1:
            os.removedirs(os.sep.join(file.split(os.sep)[:-1]))
    os.remove(Path("config/indexer.txt"))
    print("Clean up complete")

if __name__ == "__main__":

    # paths to settings files
    config_path = Path("config/defaults.json")

    #print(parse_json_file(config_path))
    generate_html(parse_json_file(config_path))