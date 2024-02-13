# software-entropy
Tool used to measure software entropy

## Build typescript graph

To build the graph of a frontend project, you need to install Madge. Madge is a tool that generates a graph of your file dependencies. It works with both CommonJS and ES6 module syntax, and it works with both JavaScript and TypeScript.

Install Madge globally:
```shell
npm install -g madge
```

Execute this command to build the graph:
```shell
madge --extensions ts --exclude '.*.spec.ts' ./src > <project-name>.madge
```


## Build java graph

To build the graph of a backend project, we use jdeps. jdeps is a tool that generates a graph of your file dependencies. jdeps is able to analyse a jar but is not able to recursively analyse a fat jar.

For applications that are not modularized, you can use the following command to generate the graph:

```shell
jdeps -verbose:class -e se.hms.* <application-jar>.jar > <project-name>.jdeps
```

For applications that are modularized (i.e hexagonal applications), you can use a similar command to generate the graph:

```shell
jdeps -verbose:class -e se.hms.*  **/target/**SNAPSHOT.jar > <project-name>.jdeps
```

Note that the -e flag is used to only include the se.hms package in the graph.

Another way could be to unpack the fat jar and target the relevant jars in a single call to jdeps like in the previous example.

