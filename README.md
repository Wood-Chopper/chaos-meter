# software-entropy
Tool used to measure various parameters of a dependency graph. Those parameters represent the software entropy.

**Steps:**
* Build the project graph
* Analyse the graph

## Build the project graph

Currently, the tool supports building the graph of javascript, typescript and java projects.

### Typescript graph

To build the graph of a frontend project, you need to install Madge. [Madge](https://www.npmjs.com/package/madge) is a tool that generates a graph of your file dependencies. It works with both CommonJS and ES6 module syntax, and it works with both JavaScript and TypeScript.

Install Madge globally:
```shell
npm install -g madge
```

Execute this command to build the graph:
```shell
madge --extensions ts --exclude '.*.spec.ts' ./src > project-name.madge
```

### Java graph

To build the graph of a backend project, we use jdeps. [jdeps](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jdeps.html) is a tool that generates a graph of your file dependencies. jdeps is able to analyse a jar but is not able to recursively analyse a fat jar.

For applications that are not modularized, you can use the following command to generate the graph:

```shell
jdeps -verbose:class -e com.example.* application-jar.jar > project-name.jdeps
```

For applications that are modularized (i.e hexagonal applications), you can use a similar command to generate the graph:

```shell
jdeps -verbose:class -e com.example.*  **/target/**SNAPSHOT.jar > project-name.jdeps
```

Note that the -e flag is used to only include the se.hms package in the graph.

Another way could be to unpack the fat jar and target the relevant jars in a single call to jdeps like in the previous example.

## Usage
```shell
usage: Software Entropy calculator [-h] -g GRAPH -m {cycle,in-degree,out-degree,centrality-degree,flow-hierarchy,density,topology} [-e EXCLUDE]

Tool used to measure various metrics of a software dependency graph.

options:
  -h, --help            show this help message and exit
  -g GRAPH, --graph GRAPH
                        The file containing the dependency graph. Example: "path/to/graph.<jdeps|madge|graph>"
  -m {cycle,in-degree,out-degree,centrality-degree,flow-hierarchy,density,topology}, --metric {cycle,in-degree,out-degree,centrality-degree,flow-hierarchy,density,topology}
                        The metric to output
  -e EXCLUDE, --exclude EXCLUDE
                        Regex to identify the components to be excluded from the analysis. This allows to differentiate models from logical components and have more relevant results. Example: ".*\.model\..*|.*\.entity\..*|.*\.dto\..*"

```


## Examples

**Compute the density of a graph**
```shell
python3 entropy.py -g path/to/graph -m density
```
**Compute the topology of a graph by excluding models from the analysis**
```shell
python entropy.py -g path/to/graph -e ".*\.model\..*|.*\.entity\..*|.*\.dto\..*" -m topology
```
