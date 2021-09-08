import zipfile
import os

def extract_zip(input_zip):
    input_zip=zipfile.ZipFile(input_zip)
    items = {}
    for name in input_zip.namelist():
        items[name] = input_zip.read(name)
    return items

items = extract_zip("test.cbz")

manifest = []
spine = []

iteration = -1
for i in items:
    iteration += 1

    #remove .jpg
    title = i[:len(i) - 4]

    #files
    xhtml = f"{title}.xhtml"
    jpg = f"{title}.jpg"


    #manifest
    manJpg = f"<item href=\"Images/{jpg}\" id=\"image-{iteration}\" media-type=\"image/jpeg\" />"
    manXhtml = f"<item href=\"Text/{xhtml}\" id=\"html-{iteration}\" media-type=\"application/xhtml+xml\" />"
    #spine
    spineXhtml = f"<itemref idref=\"html-{iteration}\" />"

    manifest.append(manJpg)
    manifest.append(manXhtml)
    spine.append(spineXhtml)


    imagePath = os.path.join(os.path.dirname(os.path.realpath(__file__)) + "/epub extracted/epub-boilerplate/book/OEBPS/Images", jpg)
    with open(imagePath, "wb") as f:
        f.write(items[i])

    textPath = os.path.join(os.path.dirname(os.path.realpath(__file__)) + "/epub extracted/epub-boilerplate/book/OEBPS/Text", xhtml)
    with open(textPath, "w") as f:
        textFile = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>{title}</title>
    <link href="../Styles/style.css" rel="stylesheet" type="text/css" />
  </head>
  <body>
    <div id="chapter-1" xml:lang="en-US">
      <img alt="" src="../Images/{jpg}"/>
    </div>
  </body>
</html>""".format(title = title, jpg = jpg, curlyBraceO="{",   curlyBraceC="}")

        f.write(textFile)

manifestStr = ""
spineStr = ""
for i in manifest:
    manifestStr += i + "\n"

for i in spine:
    spineStr += i + "\n"


contentOpf = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <!-- ISBN -->
    <dc:identifier id="bookid" opf:scheme="ISBN">urn:isbn:[ISBN]</dc:identifier>
    <dc:title>Title</dc:title>
    <dc:rights>Copyright © [YEAR] [COPYRIGHT HOLDER]. All rights reserved.</dc:rights>

    <!-- BISAC Subject Headings List: http://bisg.org/?page=BISACFaQ -->
    <dc:subject>[LIST / OF / SUBJECTS]</dc:subject>

    <dc:creator opf:file-as="[LASTNAME, NAME]" opf:role="aut">[NAME LASTNAME]</dc:creator>

    <dc:source>[SOURCE URL]</dc:source>

    <!-- List of contributors

         See: MARC Code List for Relators: http://www.loc.gov/marc/relators/relaterm.html

         Examples:

         * Editor [edt]
           Use for a person or organization who prepares for publication a work not primarily his/her own,
           such as by elucidating text, adding introductory or other critical matter, or technically directing
           an editorial staff.

         * Cover designer [cov]
           Use for a person or organization responsible for the graphic design of a book cover,
           album cover, slipcase, box, container, etc. For a person or organization responsible
           for the graphic design of an entire book, use Book designer; for book jackets, use Bookjacket designer.

         * Translator [trl]
           Use for a person or organization who renders a text from one language into another, or from an older
           form of a language into the modern form.

         -->

    <dc:contributor opf:file-as="[LASTNAME, NAME]" opf:role="edt">[NAME LASTNAME]</dc:contributor>
    <dc:contributor opf:file-as="[LASTNAME, NAME]" opf:role="cov">[NAME LASTNAME]</dc:contributor>

    <dc:publisher>[PUBLISHER NAME]</dc:publisher>
    <dc:date opf:event="publication">2012-01-01</dc:date>

    <!-- Language code: http://en.wikipedia.org/wiki/List_of_ISO_639-2_codes -->
    <dc:language>en</dc:language>

    <meta name="cover" content="[COVER_NAME].jpg" />

    <!-- UUID generator: http://www.famkruithof.net/uuid/uuidgen -->
    <dc:identifier opf:scheme="UUID">urn:uuid:[UUID]</dc:identifier>

  </metadata>

  <!-- MANIFEST (mandatory)
       List of all the resources of the book (XHTML, CSS, images,…).
       The order of item elements in the manifest is NOT significant.

       http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.3
  -->

  <manifest>
   <item href="Styles/style.css" id="css" media-type="text/css" />
    {manifestStr}
  </manifest>

  <!-- SPINE (mandatory)

       The spine element defines the default reading order of the content. It doesn't list every file in the manifest,
       just the reading order.

       The value of the idref tag in the spine has to match the ID tag for that entry in the manifest.

       For example, if you have the following reference in your manifest:

          <item id="chapter-1" href="chapter01.xhtml" media-type="application/xhtml+xml" />

       your spine entry would be:

          <itemref idref="chapter-1" />

       http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.4

       -->
  <spine toc="ncx">
    {spineStr}
  </spine>


</package>""".format(manifestStr = manifestStr, spineStr = spineStr )


contentOpfPath = textPath = os.path.join(os.path.dirname(os.path.realpath(__file__)) + "/epub extracted/epub-boilerplate/book/OEBPS", "content.opf")
with open(contentOpfPath, "wb") as f:
    f.write(contentOpf.encode("utf-8"))

"""
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))

test = zipfile.ZipFile('test.epub', 'w')
zipdir(os.path.dirname(os.path.realpath(__file__)) + "/epub extracted/epub-boilerplate/book/", test)
"""
