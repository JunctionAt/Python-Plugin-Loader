Python Plugin Loader
====================

Warning: This fork is not compatible at ALL with the original. It includes a 
completely redone event system, doesn't include the decorator API and more.
This readme may also not contain 100% accurate information, however it should
contain some clues, and an example.

The python plugin loader is a pluginloader for bukkit to load python plugins
via jython (and hopefully via jpype eventually). 


Using the plugin loader
-----------------------

Building
********


1. Get maven.
2. Run mvn clean package
3. Your product will be in target/


Running
*******

0. Ensure you are using a bukkit build that uses
   https://github.com/Bukkit/Bukkit/pull/335 - otherwise, only some of your
   plugins will work.
1. Put PyPluginLoader-0.2.jar in your bukkit/plugins/ dir
2. Put jython.jar in your bukkit/lib/ dir
3. [Re-]Start bukkit

Using plugins
*************

1. Stick the plugin.pyp in your bukkit/plugins/ dir
2. [Re-]Start bukkit

Writing plugins
===============

Writing plugins with PythonLoader is fairly easy. There are two apis, both
of which are pretty simple; The first is the bukkit api, which this loader
lightly wraps; and the other is a decorators-and-functions api.

Basics
------

Your plugins go in either a zip or a directory (known to windows users as "folders");
that zip or directory name must match this regex: \.py\.?(dir|zip|p|pl|plug|plugin)$


Class (bukkit standard) API
---------------------------

To write a plugin with this api is almost identical to writing one in java, so
much so that you can safely use the documentation on how to write a java
plugin; simply translate it into python. the java2py tool may even work on
existing java plugins (though no promises).

See the "Sample plugin using class api" section for a more detailed example.

your plugin.yml:

    name: MyHawtPlugin
    main: MyPlugin
    version: 0.1

your plugin.py:

    class SampleClass(PythonPlugin):
        def onEnable():
            print "enabled!"
        def onDisable():
            print "disabled!"

API Details
===========

The api contains quite a few places where you can do things multiple ways. This
section documents these.

Plugin files
------------

Your plugin may go in:

- A zip whos name ends in either .py.zip or .pyp
- A directory whose name ends in .py.dir or \_py_dir (for windows users)
- A python file (obviously, named .py)

Zips with the .pyp extension are recommended if you release any plugins. When
you use a zip, your must specify your own metadata; it will not allow guessed
metadata.

When using a dir or a zip, your zip or dir must contain a main python file and
optionally a plugin.yml containing metadata (see the following section). Your
python main file normally should be named either plugin.py or main.py.
plugin.py should generally be used when you are using the class api and main.py
when using the decorator api. Under some conditions you may want to change the
name of your main file (such as, other plugins needing to be able to import
it). This is not recommended but is possible with the main field in the
metadata.

When using a single .py file in plugins, your single .py is your main python
file. You cannot have a separate plugin.yml - if you want to have any special
metadata, you will need a directory or zip plugin.

Plugin metadata
---------------

Plugins require metadata. The absolute minimum metadata is a name and a version.
The location of your main file/class is also required, if you don't like
defaults. The 'main' field of plugin metadata has special behavior:

- if the main is set in plugin.yml, it searches for the value set in main as
   the main file before searching for the default file names. see "Main files".
- the main is used to search for a main class before searching the default
   class name.

There are three places you can put this metadata. In order of quality:

- plugin.yml

plugin.yml is the best as you are able to set all metadata fields that exist
in bukkit, and should be used for all plugins that you release. plugin.yml is
used in all java plugins (as it is the only option for java plugins). as such,
opening up java plugin jars is a good way to learn what can go in it. Here is
an example of plugin.yml:

    name: SamplePlugin
    main: SampleClass
    version: 0.1-dev
    commands:
        samplecommand:
            description: send a sample message
            usage: /<command>

The plugin filename is automatically used if no plugin.yml is found. The
extension is removed from the filename and used as the "name" field.
The version field is set to "dev" (as this case should only occur when first
creating a plugin). the main field is set to a default value that has no
effect.

Summary of fields:

- "main" - name of main python file or name of main class
- "name" - name of plugin to show in /plugins list and such. used to name the
   config directory. for this reason it must not equal the full name of the
   plugin file.
- "version" - version of plugin. shown in errors, and other plugins can access it
- "website" - mainly for people reading the code

Sample plugin using class api
-----------------------------

plugin.yml
**********

    name: SamplePlugin
    main: SampleClass
    version: 0.1-dev
    commands:
        samplecommand:
            description: send a sample message
            usage: /<command>

plugin.py
*********

    from org.bukkit.event.player import PlayerListener
    from org.bukkit.event.Event import Type, Priority
    
    class SampleClass(PythonPlugin):
        def __init__(self):
            self.listener = SampleListener(self)
            print "sample plugin main class instantiated"
    
        def onEnable(self):
            pm = self.getServer().getPluginManager()
            pm.registerEvent(Type.PLAYER_PICKUP_ITEM, listener, Priority.Normal, self)
            pm.registerEvent(Type.PLAYER_RESPAWN, listener, Priority.Normal, self)
            
            print "sample plugin enabled"
        
        def onDisable(self):
            print "sample plugin disabled"
        
        def onCommand(self, sender, command, label, args):
            msg = "sample plugin command"
            print msg
            sender.sendMessage(msg)
            return True
    
    class SampleListener(PlayerListener):
        def __init__(self, plugin):
            self.plugin = plugin
        
        def onPlayerJoin(self, event):
            msg = "welcome from the sample plugin, %s" % event.getPlayer().getName()
            print msg
            event.getPlayer().sendMessage(msg)
    
    print "sample plugin main file run"
