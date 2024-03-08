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

## Analyse the graph

**Simply run:**
```shell
python3 entropy.py <project-name>.<extention>

python entropy.py -g path/to/graph -m ".*\.model\..*|.*\.entity\..*|.*\.dto\..*"
```
