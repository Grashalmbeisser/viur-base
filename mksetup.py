#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, datetime, binascii

cwd = os.getcwd()
dirs = []
files = {}

for dirname, dirnames, filenames in os.walk("."):
	if dirname == ".":
		for ignore in [".idea", ".git", "server"]:
			if ignore in dirnames:
				dirnames.remove(ignore)

		for ignore in ["README.md", "mksetup.py", ".gitignore", ".gitmodules"]:
			if ignore in filenames:
				filenames.remove(ignore)

		dirname = ""
	elif dirname.startswith("./"):
		dirname = dirname[2:]

	for dir in dirnames:
		dirs.append(((dirname + "/") if dirname else "") + dir)

	for file in filenames:
		filename = ((dirname + "/") if dirname else "") + file
		if filename == "viur_server.py":
			tfilename = "{{app_id}}.py"
		else:
			tfilename = filename

		f = open(filename, "rb")
		files[tfilename] = binascii.hexlify(f.read())
		f.close()

out = ""
out += "# -*- coding: utf-8 -*-\n"
out += "# THIS FILE WAS GENERATED WITH %s ON %s\n" % (__file__, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
out += "# DO NOT EDIT THIS FILE PERMANENTLY - IT WILL GO AWAY!\n\n"

out += "import os, sys, binascii, datetime\n\n"

out += "dirs = %s\n" % dirs
out += "files = %s\n\n" % files

out += """

def confirm(quest):
	sys.stdout.write(quest)
	try:
		answ = raw_input()
	except NameError:
		answ = input()

	return answ.lower() in ["y","yes"]

cwd = os.getcwd()
prgc = sys.argv[0]

if prgc.startswith("/") or prgc[1]==":":
    path = os.path.dirname(prgc)
else:
    path = os.path.abspath(os.path.dirname(os.path.join(cwd, prgc)))

path = os.path.abspath( os.path.join( path , ".." ) )
os.chdir(path)
appid = path[ path.rfind( os.path.sep )+1: ].strip()

if not confirm("This will initialize the application %s in %s - Continue [y/N]?" % (appid, path)):
	print("Setup aborted.")
	sys.exit(0)

for folder in dirs:
	folder = os.path.join(path, *folder.split("/"))
	if not os.path.exists(folder):
		print("Creating %s..." % folder)
		os.mkdir(folder)

vars = {
	"app_id": appid,
	"path": path,
	"user_module": "user_custom",
	"user_module_class": "CustomUser",
	"timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
}

for name, content in files.items():
	content = binascii.unhexlify(content)

	for k, v in vars.items():
		name = name.replace("{{%s}}" % k, v)
		content = content.replace("{{%s}}" % k, v)

	name = os.path.join(*name.split("/"))

	if os.path.exists(name):
		if not confirm("The file %s already exists - Override [y/N]?" % name):
			print("Skipping %s!" % name)
			continue

	sys.stdout.write("Writing %s..." % name)
	open(name, "w+").write(content)
	print("Done")
"""

print(out)
