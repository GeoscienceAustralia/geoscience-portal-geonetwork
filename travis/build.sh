#!/bin/bash

mvn --settings travis/settings.xml clean deploy -P external
