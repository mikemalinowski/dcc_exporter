# DCC Exporter

The DCC Exporter is a generalised export framework that is designed to work in 
any of the following applications:

* Maya
* Max
* Mobu
* Houdini

The framework has the following library requirements:
* qute
* crosswalk
* xstack
* xstack_app
* scribble
* squiggle

(all of these can be downloaded from https://github.com/mikemalinowski)

The exporter is intended as a framework allows you to plug in your own export 
definitions. An export definition might be a "Maya Animation Export Type" or a
"Max Skeletal Mesh Export Type". Out the box this does not come with any export
defintions apart from an example.

The framework then allows the user to add definitions to the session, specifying export
options and that data will then be stored within the scene. This ensures that any
other developer who opens that scene can export the same data out without prior 
knowledge of how the previous user exported their data. 


# DCC Exporter App

The app is a Qt based frontend to make the user experience of adding, removing and 
editing export entries within a scene easier. However the framework itself does not
rely on Qt or a UI and can therefore be run headless or be wrapped in a different 
UI framework.
