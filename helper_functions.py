import urllib.parse
import urllib.request
import re


async def youtube(ctx, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})',
                                htm_content.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])
