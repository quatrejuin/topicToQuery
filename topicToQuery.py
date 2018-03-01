# To convert the TREC topics in to Indri Query parameter xml file
import glob
import re
from os.path import basename, dirname
import sys

if len(sys.argv) > 1:
    # Input File path
    path = sys.argv[1]

# Output file will be lcated in the same path as input file
# but with the output_prefix and extension .xml
output_prefix = "query_param_"
list_of_file = glob.glob(path)

for file in list_of_file:
    lists_topics = []
    with open(file) as fp:
        num_val = 0
        for line in fp:
            # Get <num>
            result = re.match(r"<num>\s*Number:\s*(\d+)\n", line)
            if bool(result):
                num_val = int( result.group(1), 10)

            # Get <title>
            title_str = ""
            result = re.match(r"<title>\s*Topic:\s*(.*)\n", line)
            if bool(result):
                title_str = result.group(1)
                lists_topics += [{"num": num_val, "title": title_str}]

    print("{} ({} request converted)".format(file, len(lists_topics)))

    # Write the Indri query format file
    with open(dirname(path) + "/" + output_prefix + basename(file)[:-4] + ".xml", "w") as fw:
        param = ("<parameters>\n")
        for topic in lists_topics:
            query = (
                    "\t<query>\n"
                     "\t\t<type>indri</type>\n"
                     "\t\t<number>" + topic["num"] + "</number>\n"
                     "\t\t<text>\n"
                     "\t\t\t#combine( " + topic["title"] + " )\n"
                     "\t\t</text>\n"
                    "\t</query>\n"
                     )
            param += query
        param += ("\t<memory>1G</memory>\n"
                     "\t<index>./test_output</index>\n"
                     "\t<trecFormat>true</trecFormat>\n"
                     "\t<count>1000</count>\n"
                     "</parameters>")
        fw.writelines(param)
