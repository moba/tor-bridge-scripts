#!/bin/bash

find . -name 'tor/*.cfg' | sort -R | head -n 50 | xargs sed -i -e "s:^PublishServerDescriptor 1:PublishServerDescriptor 0:g"
