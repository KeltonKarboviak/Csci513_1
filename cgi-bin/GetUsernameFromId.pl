#!/usr/bin/perl

use strict;
use CGI;


my $query = new CGI;
my $id = $query->param('id');

# Remove leading and trailing spacing
$id =~ s/^\s+|\s+$//g;

# For security, remove some Unix metacharacters
# $name =~ s/;|>|>>|<|\*|\?|\&|\|//g;
$id =~ s/"/\\"/g;

# Compose a Java command
my $cmd = "/usr/bin/java -Djava.security.egd=file:/dev/./urandom GetUsernameFromId \"$id\"";

system($cmd);
