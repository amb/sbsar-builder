# sbsar-builder
Builds a Substance .sbsar and .sbs from a set of images. Requires Substance Automation Toolkit, and its Python module installed. 

Change "wsbs.tools_path" in combine.py to match your root folder for SAT executables. If you want to use the Windows shortcut, modify it to match your folder and Python executable.

This script is work in progress and assumes metallic workflow with only base color, normal and roughness, with metallic set to zero automatically.

What it looks like in action: https://twitter.com/th127/status/1082286537252003842

Uses https://github.com/thestr4ng3r/py-substance-wrapper for some of the baking.
