#!/usr/bin/env python

import yaml
import re
import simplejson as json
import os
import sys
from markdown import markdown
'''
Render the file client.html via the problem data, config file and template
'''
# A textbox for storing answers to questions, parametrized by size
# answerbox_template = "<input type=\"text\" class=\"answerbox\" size=\"%d\" value=\"\">"
# Use new style
answerbox_template = "<input type=\"text\" class=\"answerbox\" size=\"{}\" value=\"\">"

# Load the yaml config file
with open('../config.yaml','r') as f:
    config = yaml.load(f)
# Combine two paths to retrieve the path for problem data
problem_data_filename = os.path.join(config['Data path'],
    config['WebWork problem json relative path'])
# Get the server html filename
server_html_path = config['Server configuration']['html file to serve']
# Load problem data from the combined path
with open(problem_data_filename,'r') as f:
    problem_data = json.load(f)

# Load client template html file, with a parameter for the html body
with open( "client_template.html" ,'r') as f:
    client_template = f.read()
#client_template = open('client_template.html','r').read()

# Add part text and answerboxes to client template body
part_str = ''
for part in sorted(problem_data.keys()):
    part_info = problem_data[part]
    #part = 'part%s'%part
    # Use new style
    part = 'part{}'.format(part)
    # Make the size of the answerbox twice the length of the answer
    #answer_box_str = answerbox_template%( len(str(part_info['answer'])) * 2)
    # Use new style
    answer_box_str = answerbox_template.format( len(str(part_info['answer'])) * 2)
    # In the part text, replace backslash followed by at least one whitespace by a single whitespace
    part_text = re.sub(r'\ +',' ',part_info['text'])
    # Convert to HTML and put the answer_box_str within
    # NOTE: New style formatting cannot be applied due to the old-formatting structure of json file
    part_text = markdown(part_text)%answer_box_str
    # Substitute left and right code tag by $ in part_text
    part_text = re.sub(r'\[\<code\>','$',part_text)
    part_text = re.sub(r'\<\/code\>\]','$',part_text)
    # Combine multiple spaces into one
    #part_str += "<div id=\"tip%s\" class=\"tip\" style=\"display:none;\"></div>"%part
    #part_str += "<div id=\"%s\" class=\"%s\">\n%s\n</div>"% \
    #    (part, 
    #     'tip' if "is_clue" in part_info and part_info["is_clue"] else "part", 
    #     part_text)
    # Use new style
    # NOTE: In json file, part_info["is_clue"]=true instead of part_info["is_clue"]=True 
    part_str += "<div id=\"{0}\" class=\"{1}\">\n{2}\n</div>".format(\
         part, 
         'tip' if "is_clue" in part_info and part_info["is_clue"] else "part", 
         part_text)
# Remove ordered list tags since already included in client_template
part_str = part_str.replace('<ol>','')
part_str = part_str.replace('</ol>','')
# Print the newly rendered html file
# NOTE: New style formatting cannot be applied due to the old-formatting structure of client_template.html
with open(server_html_path,'w') as f:
    f.write(client_template%part_str)
