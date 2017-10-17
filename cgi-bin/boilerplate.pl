#!/usr/bin/perl

use strict;
use CGI;

my $query = new CGI;
my $name = $query->param('dev_name');

# Remove leading and trailing spacing
$name =~ s/^\s+|\s+$//g;

# For security, remove some Unix metacharacters
# $name =~ s/;|>|>>|<|\*|\?|\&|\|//g;
$name =~ s/"/\\"/g;

# Compose a Java command
my $cmd = "/usr/bin/java -Djava.security.egd=file:/dev/./urandom boilerplate \"$name\"";

system($cmd);
