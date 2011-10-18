# *      Copyright (C) 2011 Libor Zoubek
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# */

import sys,os,util,re

sys.path.append( os.path.join ( os.path.dirname(__file__),'server') )

RESOLVERS = []
util.debug('%s searching for modules' % __name__)
for module in os.listdir(os.path.join(os.path.dirname(__file__),'server')):
	if module == '__init__.py' or module[-3:] != '.py':
		continue
	module = module[:-3]
	exec 'import %s' % module
	util.debug('found %s %s' % (eval(module),dir(eval(module))))
	RESOLVERS.append(eval(module))
del module
util.debug('done')
##
# resolves given URL to list of streams 
# @param url
# @return [] iff resolver was found but failed
# @return None iff no resolver was found
# @return array of stream URL's 
def resolve(url):
	url = util.decode_html(url)
	util.info('Resolving '+url)
	resolver = _get_resolver(url)
	if resolver == None:
		return None
	value = resolver(url)
	if value == None:
		return []
	return value

def _get_resolver(url):
	util.debug('Get resolver for '+url)
	for r in RESOLVERS:
		util.debug(' querying %s' % r)
		if r.supports(url):
			return r.url

# returns true iff we are able to resolve stream by given URL
def can_resolve(url):
	return not _get_resolver(url) == None
##
# finds streams in given data according to given regexes
# @param data piece of text (HTML code) to search in
# @param regexes - array of strings - regular expressions, each MUST define named group called 'url'
#        which retrieves resolvable URL (that one is passsed to resolve operation)
# @return array of dictionaries with keys: name,url,quality
# @return None if at least 1 resoler failed to resolve and nothing else has been found
# @return [] if no resolvable URLs or no resolvers for URL has been found
def findstreams(data,regexes):
	print regexes
	print data
	resolved = []
	error = True
	for regex in regexes:
		for match in re.finditer(regex,data,re.IGNORECASE | re.DOTALL):
			streams = resolve(match.group('url'))
			print streams
			if not streams == None:
				error = False
				if len(streams) > 0:
					for stream in streams:
						item = {}
						item['name'] = stream
						item['url'] = stream
						item['quality'] = 'Unknown'
						resolved.append(item)
	if error:
		return None
	return resolved

