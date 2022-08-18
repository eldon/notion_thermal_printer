#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3
from notion_client import Client
from subprocess import Popen, PIPE
import yaml

LP_PRINTER = 'ZJ_58'

with open('.notion_config.yaml', 'r') as f:
    notion_config = yaml.safe_load(f)

notion = Client(auth=notion_config['auth_token'])
matching_records = notion.databases.query(
    database_id=notion_config['database_id'],
    filter={'property': notion_config['record_property'], 'select': {'equals': notion_config['record_value']}},
)['results'] 
record_titles = [d['properties']['Name']['title'][0]['plain_text'] for d in matching_records]

p = Popen(['lp', '-d', LP_PRINTER], stdin=PIPE)
p.stdin.write('\n\n'.join(record_titles).encode('utf-8'))
output = p.communicate()[0]