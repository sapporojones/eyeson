

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



