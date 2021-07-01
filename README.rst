

.. image:: https://travis-ci.com/sapporojones/eyeson.svg?branch=main



******
eyeson
******

A tool to view at-a-glance info about an arbitrary solar system in EVE Online.

Description
###########

One day I was on a roam in EVE Online, my ye olde pastime of feeding aggressively ships I can't afford.
I found myself near a system that seemed like it was heavily trafficked by hostiles, and 
I wanted a fast way to get information about that solar system from several sources at once.

The next day I woke up and started on this as a personal project but decided to put it up in the hopes 
someone might find it useful.  

Installation
############

* Clone this repo via git clone.
* `cd` in to the directory you cloned the repo to and `pip install .`
* eyeson is now installed as a python module which you can run with `python -m eyeson`

**Alternatively**

* Eventually this will be on pypi in which case likely installation will be `pip install eyeson`
* eyeson is now installed as a python module which you can run with `python -m eyeson`
* It's probably best not to count on that right now though since that isn't done 
* Running that pip command will cause pip to error out or look at you funny 

Usage
#####

There are two arguments used in this application.  This count doesn't include `-h` for help.

* `-s <system name>`

  * This argument allows you to provide a system name, partial match or exact.
  * In the event you use a partial system name it will be matched against EVE ESI and the closest match will be used.
  * If you do not provide this argument, a default system will be used.
* `-n <number of rows to return>`

  * This is the number of rows to be returned for kills found.
  * In the event you don't care or fail to provide it, a default number will be used.
    
Usage Examples
##############

* `python -m eyeson -n 5`

  * returns information on the default system and five rows of losses in the system
* `python -m eyeson -s Jita -n 3`

  * returns the three most recent losses in Jita along with basic info about Jita
* `python -m eyeson -s OWXT-S`  

  * returns the default number of losses in the system 0WXT-S.


Changelog
=========


All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

[v1.1.0](https://github.com/sapporojones/eyeson/releases/tag/v1.1.0) - 2021-06-30
---------------------------------------------------------------------------------

<small>[Compare with v1.0.1](https://github.com/sapporojones/eyeson/compare/v1.0.1...v1.1.0)</small>

**Added**

* Adding github actions dependabot, release drafter, greetings, some templates ([5c22304](https://github.com/sapporojones/eyeson/commit/5c223043c7de37722f7ce9f8891dd6f8d8311ff8) by sapporojones).


[v1.0.1](https://github.com/sapporojones/eyeson/releases/tag/v1.0.1) - 2021-06-30
---------------------------------------------------------------------------------

<small>[Compare with v1.0.0](https://github.com/sapporojones/eyeson/compare/v1.0.0...v1.0.1)</small>


[v1.0.0](https://github.com/sapporojones/eyeson/releases/tag/v1.0.0) - 2021-06-30
---------------------------------------------------------------------------------

<small>[Compare with first commit](https://github.com/sapporojones/eyeson/compare/8cd6fca1a3c70fec86bdd99843b58675f74b1642...v1.0.0)</small>

**Changed**

- Changes in pip usage ([71006e3](https://github.com/sapporojones/eyeson/commit/71006e3d755059015b0ed8249e117776d7163698) by sapporojones).

**Fixed**

- Fixing yaml formatting errors for .travis.yml ([4224d4e](https://github.com/sapporojones/eyeson/commit/4224d4ea2baa50dbe5588a794f6d7becc36998a9) by sapporojones).


