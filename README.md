Generates tiny websites from collections of markdown files, optionally with tags.


Synopsis
--------

`
pip install rantbase markdown mako PyYaml 
mkdir mysite
cd mysite
python -m rantbase init

echo '#one #two #three

Hello World' > docs/hello.md

./rant update
`

Then point your browser at mysite/web (via some web server).