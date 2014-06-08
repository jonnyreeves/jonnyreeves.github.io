Title: Maven and ANT – Managing Your Flash Project’s Build Dependencies
Date: 2011-04-02 16:15
Category: ActionScript

Project build dependency management and resolution is one of the more difficult problems you’ll face as your project grows in size; however even the smallest of projects (and teams) can benefit greatly from getting automatic dependency resolution in place.

## What Are My Project’s Build Dependencies?
Most of us are aware of dependencies in object orientated programming – these are the objects that our class in question needs to operate and most of us know the design patterns which we can use to externalise these dependency. Project build dependencies aren’t radically different; instead of referring to objects and instances; we are talking about the source code files (.as) that your project needs when it compiles. Any source code that you haven’t directly written for your project is a build dependency.

Imagine a simple project which makes use of TweenLite and where the source files (.as) for the TwenLite library have been copied into the source folder (src). Now if this were a real project it would result in the greensock code also being committed to our source repository. So, what’s the problem with this? Here’s a couple of potential issues:

* The project compilation time will be increased as MXMLC will be forced to recompile all the greensock code
* Developers need to checkout all the source code for TweenLite even tho they will never be editing it – furthermore, some developers may get over excited and decide to start making modifications to this code (at which point it stops being a 3rd party library!)
* If your project consists of multiple modules (ie: Other SWFs which are loaded at runtime) you will need to make sure they all have exactly the same copy of the TweenLite source code available on the source-path due to the way Flash manages loaded [Class Definitions in LoaderContexts](https://web.archive.org/web/20120406204734/http://www.senocular.com/flash/tutorials/contentdomains/?page=2#ChildDomainsDefinitionVersioning).


## Using Linked Resource Folders To Share Dependencies Across Projects
Most IDEs allow you to create [Linked Resource Folders](http://help.eclipse.org/juno/index.jsp?topic=%2Forg.eclipse.platform.doc.user%2Fconcepts%2Fconcepts-13.htm); the concept is simple – projects can import other projects source folders to allow them to share code, similar to unix symlinks – sounds great – however in practice it can cause lots of headaches!

Image a workspace that includes three folders/libraries which are linked:

* 3rdparty – This project doesn’t compile or create anything, it simply serves as a dumping ground for all application’s shared dependencies, in this case, TweenLite.

* main – This is our application’s Main project, this makes use of TweenLite and also loads in other module SWFs at runtime.

* module – This is a module which the Main application will load in at runtime – it also makes use of TweenLite (let’s face it, what Flash app doesn’t!)

Both the ‘main’ project and the ‘module’ project make use of a Linked Resource named ‘ThirdParty’ which in turn resolves to the location of the ’3rdparty’ project in our workspace. This allows them to include the TweenLite source code without having to copy/paste it into each project. This solves one of the major problems we’ve outlined above – all our application’s projects (including the modules) will now make use of the exact same version of their dependencies thanks to the ‘ThirdParty’ Linked Resource folder – also, when we want to update to a newer version of a library we just have to update the library in a single place and recompile everything – easy.

However, apart from not solving the other two issues (slower compilation and the fact we are checking in raw source code that we don’t wish to maintain) we have also just created a new, much uglier problem with our project – it’s no longer easy to build!

When creating a large project you should always strive to make the build as simple and easy as possible; I try and keep the following things in mind:

* You should be able to check the entire application’s source out of version control with a single command; no more.

* You should be able to create a fresh build of the application (including all modules) with a single command (eg: by issuing ant package from a fresh checkout of the source code

* Developers should be able to work on the project using whichever IDE or tool they wish; don’t rely on a particular environment use, such as FlashBuilder or FDT

By using linked resources we have broken these rules – the whole Linked Resource concept is tightly coupled to a given IDE; even if you check in all your .project and .settings files it isn’t going to work if someone decides they want to give IntelliJ a spin.

## SWCs To The Rescue!
When ActionScript 3 became available, Adobe provided Flash developers with a new tool, the SWC. SWCs are just zip files in disguise (if you don’t believe me, rename the extension from .swc to .swc.zip and then open it) which contain a SWF file and an XML catalouge which allows your IDE to parse all the class definitions the SWF contains. All the major Actionscript IDEs provide tools for working with SWC files.

SWCs are preferable to just dumping the source code into your project for a number of reasons – infact they solve nearly all the points we listed above.

* Compilation becomes faster as SWCs are already pre-compiled

* Instead of checking the entire source tree of the 3rd party library into SVN we are now only checking a single, compressed file – this makes checkout faster and also means that developers won’t be able to start modifying the library.

But one thing is not checked off – what about projects which make use of multiple modules – it would appear we still have the same problem that all of our modules must use the exact same version of the library – now you could just solve this by making use of a LinkedResource which points to a bunch of SWCs but that’s still not great; and when it really comes down to it – should these SWCs really be in version control at all – after all you are in not in control of their development and you don’t decide when they get updated.

## Automatically Managing Your SWCs with Maven
So, it’s now becoming clear that you and your application have some serious dependency issues when it comes to 3rd Party SWCs; don’t worry, the first step is admission – let’s start by declaring them. This article is going to focus on using Maven to declare and resolve your project’s dependencies – other solutions are available :)

Maven’s dependency management work on the simple premise that the dependencies your application relies upon (in our case, SWCs) exist out on the Internet on a special type of file server, known to Maven as a [Maven Repository](https://web.archive.org/web/20120406204734/http://maven.apache.org/guides/introduction/introduction-to-repositories.html). Maven Repositories can either be public facing (in the case of the [Central Maven Repo](https://web.archive.org/web/20120406204734/http://repo1.maven.org/maven2/).) or internal on a company’s own Intranet. Maven Repositories sole purpose is to house and catalogue build artefacts so that they can be fetched (resolved) during a project’s build. Instead of checking your applications dependencies into version control, you instead just list the dependencies in your project and then Maven will fetch them when required.

So, let’s start with a very simple application which consists of a single project which has a single build dependency on [AS3Commons Logging](https://web.archive.org/web/20120406204734/http://www.as3commons.org/as3-commons-logging/index.html). (I would have used TweenLite as an example, but it’s not available on any public Maven repositories at the time of writing). The first thing we need to do is get a simple build script on the go – I’m going to use ANT to perform the build (Maven, which describes itself as a project management tool is more than capable of both compiling and managing your project’s dependencies, but this article is is just focuses on using Maven for managing dependencies). Maven and ANT get along just fine (although their user’s pdon't always see eye to eye](https://web.archive.org/web/20120406204734/http://java.dzone.com/news/maven-or-ant) on the Internet!); all we need to do is grab a copy of the [Maven ANT Tasks JAR](https://web.archive.org/web/20120406204734/http://maven.apache.org/ant-tasks/index.html), add it to our project and reference it in our ANT Script:

A Skeleton ANT Build Script Which Makes Use Of the Maven ANT Tasks

```xml
<project name="maven-dependencies" xmlns:artifact="antlib:org.apache.maven.artifact.ant">

	<!-- Inclde the Maven ANT Tasks -->
	<path id="maven-ant-tasks.classpath" path="maven-ant-tasks-2.1.1.jar" />
	<typedef resource="org/apache/maven/artifact/ant/antlib.xml"
		uri="antlib:org.apache.maven.artifact.ant"
		classpathref="maven-ant-tasks.classpath" />

	<!-- Include the FlexSDK ANT Tasks -->
	<taskdef resource="flexTasks.tasks" classpath="${FLEX_HOME}/ant/lib/flexTasks.jar" />
</project>
```

In the example above I have copied the maven-ant-tasks.jar file into my project; however another approach is to copy the maven-ant-tasks.jar file into your ANT_HOME folder (if you’re on Windows this will be Users{username}.antlib). For more information on getting the Maven ANT Tasks setup on your machine, please refer to the [Maven ANT Tasks Installation Documentation](https://web.archive.org/web/20120406204734/http://maven.apache.org/ant-tasks/installation.html).

Now that we have access to the Maven ANT Tasks in our application’s build, the next thing we want to do is list, and resolve our dependencies. This is accomplished by in the “resolve” target shown below:

The Resolve ANT Target which Lists and Pulls Down Dependencies

```xml
<!-- =================================
	  target: resolve
	  Uses the Maven ANT Tasks to define and resolve all the dependencies require to build
	  this application.
	 ================================= -->
<target name="resolve" description="Resolve the project's dependencies">

	<!-- The pathId value 'resolves.swcs.classpath' will be an ANT FileSet which points to all the
		SWC files we are about to define -->
	<artifact:dependencies filesetId="resolved.swcs.classpath" versionsId="resolved.swcs.versions">

		<!-- This is where we list our dependency on as3commons-logging version 2.0; by adding this
			line here, we are telling Maven that our application depends upon this SWC -->
		<dependency groupId="org.as3commons" artifactId="as3commons-logging" type="swc" version="1.2" />

		<!-- This is where we provide Maven with the URL of the remote repository where some, or all of
			our dependencies can be retrieved from - if you work with a team you will probably want to
			setup your own Maven Repository in house -->
		<remoteRepository id="adobe-opensource" url="http://opensource.adobe.com/svn/opensource/cairngorm3/maven-repository" />

	</artifact:dependencies>

	<!-- Copies all the files resolved in the task above into the "libs" folder -->
	<copy todir="libs">
		<fileset refid="resolved.swcs.classpath" />

		<!-- This Mapper will remove all the folder heirarchy and version numbers from the resolved SWCs -->
		<mapper classpathref="maven-ant-tasks.classpath" classname="org.apache.maven.artifact.ant.VersionMapper"
			from="${resolved.swcs.versions}" to="flatten" />
	</copy>
</target>
```

The above target breaks down into two major parts – the [`artifact:dependencies` task](https://web.archive.org/web/20120406204734/http://maven.apache.org/ant-tasks/reference.html#dependencies) lists and resolves the project’s dependencies and the copy task then copies these dependencies into the “libs” folder in the project. The two interesting lines int he artifact:dependenciestask are the dependency line which lists as3commons-logging as a dependency (note how we specify the type as “swc” (Maven defaults the type to “jar”) and the version at 1.2). and the remoteRepository line which tells Maven which Maven Repository the dependency should be resolved from – in this project’s case we are using [Adobe’s OpenSource Maven Repository](https://web.archive.org/web/20120406204734/http://opensource.adobe.com/svn/opensource/cairngorm3/maven-repository/); however as mentioned in the comments, you will probably want to create and maintain your own Maven Repo to house your project’s artifacts in (I’m hoping to cover how to setup your own Repo in another post).

## Next Steps
The above is really just the tip of the iceberg; if you want to really get to grips with dependency management through Maven then you are going to want to start listing your dependencies (and the Maven Repositories they can be resolved from) in a [POM file](https://web.archive.org/web/20120406204734/http://maven.apache.org/pom.html#What_is_the_POM) (Project Object Model). POM files not only serve as a place to list dependencies and the URLs of Repositories, but they can define the entire build cycle of the project when using Maven (and in the case of Flash, [FlexMojos](https://web.archive.org/web/20120406204734/http://flexmojos.sonatype.org/)) to compile. POM files include an [inheritance model](https://web.archive.org/web/20120406204734/http://maven.apache.org/pom.html#Inheritance) (so a Modules’ POM file can extend the main Project’s POM file) allowing you to keep all your dependency definitions in a central place.

Also, this tutorial hasn’t touched on one of the most powerful feature of Maven, [transitive dependency resolution](https://web.archive.org/web/20120406204734/http://www.sonatype.com/books/mvnref-book/reference/pom-relationships-sect-transitive.html). A quick example would be if your project depends on the RobotLegs Framework; from the example above you can see how you could define a dependency on RobotLegs:

Now, you would expect Maven to pull down RobotLegs.swc for you – but those of you familiar with RobotLegs will remember that RobotLegs itself has a dependency upon SwiftSuspenders.swc – Maven will automatically pull down both RobotLegs.swc AND the required version of the SwiftSuspenders.swc for you, even tho you only listed RobotLegs as a dependency! However, in order for this to work, RobotLegs needs to be uploaded to a Maven Repo along with a POM file which lists SwiftSuspenders as a dependency (and where it can be fetched from in turn) – The Java community is all over this and it works like magic – unfortunatley the Flash community is lagging quite far behind – it would be amazing if FlashDevs started pushing their SWCs up to the Central Maven Repo (it would certainly save people from having to setup and maintain their own local repos!)