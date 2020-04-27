
import requests

iq_session = requests.Session()
iq_session.auth = requests.auth.HTTPBasicAuth("admin", "admin123")
iq_url = "http://localhost:8070"
default = "Distributed"
add_tag = {}

orgs = iq_session.get(f'{iq_url}/api/v2/organizations').json()["organizations"]
for org in orgs:
	if org["id"] == "ROOT_ORGANIZATION_ID":
		for tag in org["tags"]:
			if tag["name"] == default:
				tag_id = tag['id']
				print(f"Found default tag ({default}): {tag_id}")
				add_tag = {"tagId": tag_id }
				
if not bool(add_tag):
	print(f"Did not find tag:{default}"); exit(1)

print(f"Checking for applications without tags ...")
apps = iq_session.get(f'{iq_url}/api/v2/applications').json()["applications"]
for app in apps:
	if len(app["applicationTags"]) == 0:
		print(f" -Adding tag to app: {app['publicId']}")
		app["applicationTags"].append(add_tag)
		app_id = app["id"]
		url = f"{iq_url}/api/v2/applications/{app_id}"
		result = iq_session.put(url, json=app)
		print(result.status_code == requests.codes.ok)

print("== fin")
