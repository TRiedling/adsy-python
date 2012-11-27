#!/usr/bin/python2
# coding: utf-8

# Copyright (c) 2012, Adfinis SyGroup AG
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Adfinis SyGroup AG nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Adfinis SyGroup AG BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from IPython.core.display import HTML, display_html
import traceback
import subprocess
import sys
from textwrap import wrap
from pprint import pformat

def areload():
	"""Enable autoreload. Might be buggy!"""
	get_ipython().magic('load_ext autoreload')
	get_ipython().magic('autoreload 2')

def do_bisect_step(state):
	"""Calls git bisect with the information from test/test_with_regex

	state: True: test was ok -> False: test failed"""
	str_state = 'bad'
	if state == True:
		str_state = 'good'
	proc = subprocess.Popen(
		 ['git', 'bisect', str_state],
		 stdout = subprocess.PIPE,
		 stderr = subprocess.PIPE,
		 stdin  = subprocess.PIPE
	)

	stdout, stderr = proc.communicate()
	returncode     = proc.wait()
	sys.stdout.write(stdout)
	sys.stderr.write(stderr)
	ereload()
	return returncode

def html_settings():
	"""Call this once in your notebook or qtconsole."""
	return HTML("""
		<script type="text/javascript">
			var inputInverval;
			var intervalCount = 0;
			var inputUp = false;
			function toggleInput() {
				if(inputUp) {
					$('.input').slideDown();
					$('.code_cell').addClass('cell');
					$('.code_cell').addClass('vbox');
				}
				else {
					$('.input').slideUp();
					$('.code_cell').removeClass('cell');
					$('.code_cell').removeClass('vbox');
				}
				inputUp = !inputUp;
			}
			function slideInputUp() {
				if(intervalCount > 15) {
					clearInterval(inputInterval);
				}
				intervalCount += 1;
				if(inputUp == false) {
					try {
						// Only slideUp if we're not on notebook server
						// meaning Print View and nbconverted
						if($('#save_status').length == 0) {
							toggleInput();
						}
						clearInterval(inputInterval);
					} catch(e) {}
				}
			}
			if (typeof jQuery == 'undefined') {
				// if jQuery Library is not loaded
				var script = document.createElement( 'script' );
				script.type = 'text/javascript';
				script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js';
				document.body.appendChild(script);
			}
			$('head').append([
'				<style type="text/css">',
'					table.nowrap td {',
'						white-space: nowrap;',
'					}',
'					table.bound {',
'						margin-right: 80px;',
'					}',
'					table.dataframe {',
'						margin-right: 80px;',
'					}',
'				</style>'].join("\\n"));
			setTimeout(slideInputUp, 200);
			// jQuery is doing this interval trick
			// I guess its the way to do it then.
			inputInterval = setInterval(slideInputUp, 1000);
		</script>
		<a href="javascript:toggleInput()">Toggle Input</a>
		""")

def print_html(data, tight=False, projection=None):
	"""Pretty prints database-API cursor, dicts or objects, fallback to pprint.

	data       : The data to pretty print.
	tight      : If used with dictonaries, do not textwrap and do not use <pre>.
	projection : A list of fields to display (used for dicts only)"""

	if hasattr(data, 'description') and hasattr(data, 'fetchall'):
		return html_cursor(data)
	elif hasattr(data, "__dict__"):
		return html_dict(data.__dict__, tight, projection)
	elif str(data.__class__) == "<type 'dict'>":
		return html_dict(data, tight, projection)
	elif str(data.__class__) == "<class 'dict'>":
		return html_dict(data, tight, projection)
	elif (
		str(data.__class__) == "<class 'list'>"
	or
		str(data.__class__) == "<type 'list'>"
	):
		if len(data) > 0:
			if (
				str(data[0].__class__) == "<class 'dict'>"
			or
				str(data[0].__class__) == "<type 'dict'>"
			):
				return html_multi_dict(data, tight, projection)
	return html_pprint(data)

def pprint_wrap(data):
	"""Pretty print and wrap the data."""
	return enc('\n'.join(['\n$'.join(wrap(x, width=80))
			for x in pformat(data).split('\n')]))

def html_pprint(data):
	return HTML('\n'.join([
		"<pre>",
		pprint_wrap(data),
		"</pre>"]))

def enc_v2(value):
	return unicode(value).replace(
		'&',
		'&amp;'
	).replace(
		'<',
		'&lt;'
	).replace(
		'>',
		'&gt;'
	)

def enc_v3(value):
	return str(value).replace(
		'&',
		'&amp;'
	).replace(
		'<',
		'&lt;'
	).replace(
		'>',
		'&gt;'
	)

if sys.version_info[0] == 2:
	enc = enc_v2
else:
	enc = enc_v3


def html_cursor(cursor):
	"""Pretty prints a generic database API cursor."""
	if cursor.description is None:
		display_html(HTML("<i>No data returned</i>"))
		return
	headers = [x[0] for x in cursor.description]
	header_line = "<tr><th>" + ("</th><th>".join(headers)) + "</th></tr>"
	def getrow(row):
		rendered = ["<tr>"]+["<td>%s</td>" % enc(row[col]) for col in
			range(0, len(headers))]+["</tr>"]
		return "".join(rendered)
	rows = [header_line] + [getrow(row) for row in cursor]
	body = '\n'.join(rows)
	table = '<table class="nowrap">\n%s\n</table>' % body
	return HTML(table)

def _table_config(tight):
	if tight:
		output = ['<table class="bound"><tr>']
		td_start = "<td>"
		td_end   = "</td>"
		print_function = enc
	else:
		output = ['<table class="nowrap"><tr>']
		td_start = "<td><pre>"
		td_end   = "</pre></td>"
		print_function = pprint_wrap
	return (
		output,
		td_start,
		td_end,
		print_function
	)

def html_dict(dict_, tight=False, projection=None):
	"""Pretty print a dictionary.

	dict_      : The dict to pretty print.
	tight      : Do not textwrap and do not use <pre>.
	projection : A list of fields to display"""
	(
		output,
		td_start,
		td_end,
		print_function
	) = _table_config(tight)

	fields = None
	if projection == None:
		fields = dict_
	else:
		fields = projection
	for key in fields:
		output += ["<th>", key, "</th>"]
	output += ["</tr><tr>"]
	for key in fields:
		output += [td_start, print_function(dict_[key]), td_end]
	output += ["</table>"]
	return HTML('\n'.join(output))

def html_multi_dict(array_, tight=False, projection=None):
	"""Pretty print an array of dictionaries.

	array_     : The multi dict to pretty print.
	tight      : Do not textwrap and do not use <pre>.
	projection : A list of fields to display"""
	(
		output,
		td_start,
		td_end,
		print_function
	) = _table_config(tight)
	fields = None
	if projection == None:
		fields = array_[0]
	else:
		fields = projection
	if len(array_) < 1:
		return HTML("")
	for key in fields:
		output += ["<th>", key, "</th>"]
	for dict_ in array_:
		output += ['<tr>']
		for key in fields:
			output += [td_start, print_function(dict_[key]), td_end]
		output += ['</tr>']
	output += ["</table>"]
	return HTML('\n'.join(output))

def blackhole(func, *args, **kwargs):
	"""Ignores any errors from the function func"""
	try:
		return func(*args, **kwargs)
	except:
		return None

def filter_none(data):
	"""Filters all None entry of a list/iterator"""
	for x in data:
		if x is not None:
			yield x

def blackiter(func, data, *args, **kwargs):
	"""Like list comprehension but ignores execeptions"""
	for x in data:
		try:
			yield func(x, *args, **kwargs)
		except:
			pass

def whiteiter(func, data, *args, **kwargs):
	'''Like list comprehension but ignores and logs execeptions'''
	for x in data:
		try:
			yield func(x, *args, **kwargs)
		except Exception as e:
			print("Error in record:")
			print(pprint_wrap(x))
			traceback.print_exc()

def solarized():
	"""Solarized code mirror theme."""
	html = """
<style type="text/css">
.cm-s-ipython { background-color: #002b36; color: #839496; }
.cm-s-ipython span.cm-keyword {color: #859900; font-weight: bold;}
.cm-s-ipython span.cm-number {color: #b58900;}
.cm-s-ipython span.cm-operator {color: #268bd2; font-weight: bold;}
.cm-s-ipython span.cm-meta {color: #cb4b16;}
.cm-s-ipython span.cm-comment {color: #586e75; font-style: italic;}
.cm-s-ipython span.cm-string {color: #2aa198;}
.cm-s-ipython span.cm-error {color: #dc322f;}
.cm-s-ipython span.cm-builtin {color: #cb4b16;}
.cm-s-ipython span.cm-variable {color: #839496;}
</style>"""
	return HTML(html)

