all: output/lab-handout.html output/lab-material.zip output/MN.html

topo: topology.py
	mn --custom topology.py --topo LabTopology --controller none --mac --arp --switch lxbr --link tc

clean:
	mn -c

output/lab-handout.html: .resources/metadata.md README.md .resources/pandoc.css
	mkdir -p output
	docker run -ti --rm -v "`pwd`":/workspace/ scc-registry.lancs.ac.uk/teaching/pandoc_base:latest sh -c "cd /workspace; cat .resources/metadata.md README.md | pandoc -s -f markdown+task_lists -t html5 --css .resources/pandoc.css --lua-filter=.resources/enable-checkbox.lua --embed-resources -o output/lab-handout.html"

output/MN.html: .resources/metadata.md MN.md .resources/pandoc.css
	mkdir -p output
	docker run -ti --rm -v "`pwd`":/workspace/ scc-registry.lancs.ac.uk/teaching/pandoc_base:latest sh -c "cd /workspace; cat .resources/metadata.md MN.md | pandoc -s -f markdown+task_lists -t html5 --css .resources/pandoc.css --lua-filter=.resources/enable-checkbox.lua --embed-resources -o output/MN.html"	

output/lab-material.zip: topology.py server.py solution/Makefile .devcontainer.json
	mkdir -p output
	zip -j output/lab-material.zip topology.py server.py solution/Makefile .devcontainer.json

clean:
	rm -f output/*.html
	rmdir -p output 2>/dev/null || true
